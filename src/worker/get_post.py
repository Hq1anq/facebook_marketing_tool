import time
from selenium.webdriver.common.by import By
from PySide6.QtCore import QRunnable, Signal, Slot, QObject

from src.manager import DriverManager

class GetPost(QRunnable):
    class Signals(QObject):
        add_row = Signal(str, str, str, str, str)
        loading = Signal(str)
        success = Signal(str)
        error = Signal(str)
        unlogin = Signal()
        finished = Signal()
        
    def __init__(self, driver_manager: DriverManager):
        super().__init__()
        self.driver_manager = driver_manager
        self.signals = self.Signals()
        self.max_tabs = 3  # Number of concurrent tabs

    @Slot()
    def run(self):
        if not self.driver_manager.setup_driver():
            self.signals.error.emit("Xung đột! Vui lòng đóng tất cả các trình duyệt Chrome")
            self.signals.finished.emit()
            return

        self.driver_manager.jump_to_facebook()
        if not self.driver_manager.check_login():
            self.signals.unlogin.emit()
            self.signals.finished.emit()
            return

        self.driver = self.driver_manager.driver
        self.driver.set_window_size(1300, 800)
        self.driver.set_window_position(0, 0)
        self.get_post()
            
    def get_post(self):
        self.driver_manager.handle_chat_close()
        
        if not self.group_list:
            self.signals.success.emit("Không có group nào để quét")
            self.signals.finished.emit()
            return

        # Process groups in batches of max_tabs
        for batch_start in range(0, len(self.group_list), self.max_tabs):
            batch = self.group_list[batch_start:batch_start + self.max_tabs]
            self._process_batch(batch)
                    
        self.signals.success.emit("Đã lấy thông tin các post")
        self.signals.finished.emit()

    def _process_batch(self, batch):
        """Process a batch of groups concurrently using multiple tabs"""
        original_tab = self.driver.current_window_handle
        
        # Prepare tab state for each group in the batch
        tab_states = []
        
        for i, group in enumerate(batch):
            link_group = group.get("link group", "")
            name_group = group.get("name group", "")
            
            if not link_group:
                continue
            
            if not link_group.endswith("/"):
                link_group += "/"
            
            # First group reuses the current tab, others open new tabs
            if i == 0:
                tab_handle = original_tab
                self.driver.switch_to.window(tab_handle)
            else:
                self.driver.execute_script("window.open('about:blank');")
                tab_handle = self.driver.window_handles[-1]
                self.driver.switch_to.window(tab_handle)
            
            # Navigate to group's posted content
            self.driver.get(link_group + "my_posted_content")
            
            tab_states.append({
                "handle": tab_handle,
                "link_group": link_group,
                "name_group": name_group,
                "seen_post_ids": set(),
                "scroll_count": 0,
                "no_new_post_count": 0,
                "done": False,
            })
        
        if not tab_states:
            return
        
        # Wait for all tabs to fully load
        for ts in tab_states:
            self.driver.switch_to.window(ts["handle"])
            self.driver_manager.wait_for_url_contains("")
        
        max_scrolls = 20
        no_new_post_limit = 3
        
        # Round-robin: cycle through tabs until all are done
        while any(not ts["done"] for ts in tab_states):
            for ts in tab_states:
                if ts["done"]:
                    continue
                
                # Switch to this tab
                try:
                    self.driver.switch_to.window(ts["handle"])
                except Exception:
                    ts["done"] = True
                    continue
                
                self.driver_manager.handle_chat_close()
                self.signals.loading.emit(f"Đang quét: {ts['name_group']}")
                
                # Extract posts currently visible
                story_containers = self.driver.find_elements(
                    By.CSS_SELECTOR, 'div[data-ad-rendering-role="story_message"]'
                )
                
                found_new = False
                
                for story_div in story_containers:
                    try:
                        post_wrapper = story_div.find_element(
                            By.XPATH, "./ancestor::div[contains(@class, 'x1yztbdb')]"
                        )
                        
                        link_post = ""
                        post_id = ""
                        
                        # Extract post ID from multi_permalinks
                        all_links = post_wrapper.find_elements(By.TAG_NAME, "a")
                        for a in all_links:
                            href = a.get_attribute("href")
                            if href and "multi_permalinks=" in href:
                                post_id = href.split("multi_permalinks=")[1].split("&")[0]
                                link_post = f"{ts['link_group']}posts/{post_id}"
                                break
                        
                        # Fallback
                        if not link_post:
                            try:
                                link_element = post_wrapper.find_element(
                                    By.XPATH, ".//a[contains(@href, '/groups/') and contains(@href, '/posts/')]"
                                )
                                raw_href = link_element.get_attribute("href")
                                link_post = raw_href.split("?__cft__")[0]
                                post_id = link_post.rstrip("/").split("/")[-1]
                            except:
                                pass
                        
                        # Dedup check
                        unique_id = post_id if post_id else link_post
                        if not unique_id or unique_id in ts["seen_post_ids"]:
                            continue
                        
                        # Extract content only for new posts
                        raw_content = story_div.text.strip()
                        content = (raw_content[:20] + "...") if len(raw_content) > 20 else raw_content
                        
                        ts["seen_post_ids"].add(unique_id)
                        found_new = True
                        self.signals.add_row.emit(
                            ts["link_group"], ts["name_group"], link_post, content, ""
                        )
                        
                    except Exception:
                        continue
                
                # Update scroll tracking
                if found_new:
                    ts["no_new_post_count"] = 0
                else:
                    ts["no_new_post_count"] += 1
                
                ts["scroll_count"] += 1
                
                # Check stop conditions
                if ts["no_new_post_count"] >= no_new_post_limit or ts["scroll_count"] >= max_scrolls:
                    ts["done"] = True
                    continue
                
                # Scroll down for next round
                self.driver.execute_script("window.scrollBy(0, 1000);")
            
            # Brief pause between rounds to let pages load
            time.sleep(2)
        
        # Close extra tabs (keep original)
        for ts in tab_states:
            if ts["handle"] != original_tab:
                try:
                    self.driver.switch_to.window(ts["handle"])
                    self.driver.close()
                except Exception:
                    pass
        
        # Switch back to original tab
        try:
            self.driver.switch_to.window(original_tab)
        except Exception:
            pass
    
    def setup(self, group_list: list):
        self.group_list = group_list