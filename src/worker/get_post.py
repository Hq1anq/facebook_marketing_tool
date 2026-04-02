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
        
        for group in self.group_list:
            link_group = group.get("link group", "")
            name_group = group.get("name group", "")
            
            if not link_group:
                continue
                
            self.signals.loading.emit(f"Đang quét posts: {name_group}")
            
            if not link_group.endswith("/"):
                link_group += "/"
            
            self.driver.get(link_group + "my_posted_content")
            self.driver_manager.wait_for_url_contains("")  # Wait for full load
            time.sleep(2)  # Extra wait for dynamic content
            
            seen_post_ids = set()
            scroll_count = 0
            max_scrolls = 20  # Giới hạn số lần cuộn
            no_new_post_limit = 3
            no_new_post_count = 0

            while scroll_count < max_scrolls:
                self.driver_manager.handle_chat_close()
                
                # Quét các post đang hiển thị trên màn hình
                story_containers = self.driver.find_elements(
                    By.CSS_SELECTOR, 'div[data-ad-rendering-role="story_message"]'
                )
                
                found_new_in_this_scroll = False
                
                for story_div in story_containers:
                    try:
                        # 1. OPTIMIZE: Find the post wrapper and ID first before doing anything else
                        post_wrapper = story_div.find_element(By.XPATH, "./ancestor::div[contains(@class, 'x1yztbdb')]")
                        
                        link_post = ""
                        post_id = ""
                        
                        # Use multi_permalinks to get exact ID
                        all_links = post_wrapper.find_elements(By.TAG_NAME, "a")
                        for a in all_links:
                            href = a.get_attribute("href")
                            if href and "multi_permalinks=" in href:
                                post_id = href.split("multi_permalinks=")[1].split("&")[0]
                                link_post = f"{link_group}posts/{post_id}"
                                break
                        
                        # Fallback pattern for ID extraction
                        if not link_post:
                            try:
                                # Try to find a direct post/permalink link
                                link_element = post_wrapper.find_element(
                                    By.XPATH, ".//a[contains(@href, '/groups/') and contains(@href, '/posts/')]"
                                )
                                raw_href = link_element.get_attribute("href")
                                link_post = raw_href.split("?__cft__")[0]
                                post_id = link_post.rstrip("/").split("/")[-1]
                            except: pass

                        # 2. IMMEDIATE CHECK: If we already have this post, don't extract content/labels
                        unique_id = post_id if post_id else link_post
                        if not unique_id or unique_id in seen_post_ids:
                            continue

                        # 3. EXTRACT REMAINDER: Only now perform text extraction (heavy operation)
                        raw_content = story_div.text.strip()
                        content = (raw_content[:20] + "...") if len(raw_content) > 20 else raw_content
                        
                        # Add to session and Emit
                        seen_post_ids.add(unique_id)
                        found_new_in_this_scroll = True
                        self.signals.add_row.emit(link_group, name_group, link_post, content, "")
                            
                    except Exception:
                        continue

                if found_new_in_this_scroll:
                    no_new_post_count = 0
                else:
                    no_new_post_count += 1
                
                # Nếu 3 lần cuộn liên tiếp không thấy post mới thì dừng
                if no_new_post_count >= no_new_post_limit:
                    break

                # Cuộn xuống một đoạn để load post tiếp theo
                self.driver.execute_script("window.scrollBy(0, 1000);")
                time.sleep(2)
                scroll_count += 1
                    
        self.signals.success.emit("Đã lấy thông tin các post")
        self.signals.finished.emit()
    
    def setup(self, group_list: list):
        self.group_list = group_list