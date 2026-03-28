import json
import os

class DataManager:
    
    DEFAULT_DATA = {
        "ACCOUNT": {
            "LOGIN": {
                "cookie": "",
                "username": "xxxxxxxxxx@gmail.com", 
                "password": "**********",
                "2fa": "ABXDEFGH6572PJUS9I01JKK567GHJOPO",
                "profile name": ""
            },
            "PROXY": {
                "ip": "",
                "port": "",
                "username": "",
                "password": ""
            }
        },
        "CONFIG": {
            "POST": {
                "image": [
                    "https://i.imgur.com/1mcloud.png",
                    "https://i.imgur.com/1mcloud2.png"
                ],
                "content": [
'''🔥 𝐇𝐎𝐓 𝐇𝐎𝐓 1mcloud cập nhật! Bổ sung thêm hai dòng CPU mạnh mẽ 🔥
𝐀𝐌𝐃 𝐄𝐏𝐘𝐂 𝟕𝟓𝟒𝟑𝐏 𝟑𝟐-𝐂𝐨𝐫𝐞 𝐏𝐫𝐨𝐜𝐞𝐬𝐬𝐨𝐫
𝐀𝐌𝐃 𝐑𝐲𝐳𝐞𝐧 𝟕 𝟓𝟖𝟎𝟎𝐗 𝟖-𝐂𝐨𝐫𝐞 𝐏𝐫𝐨𝐜𝐞𝐬𝐬𝐨𝐫
Bạn đang tìm kiếm một giải pháp VPS mạnh mẽ và ổn định? Tin vui cho bạn! 1mcloud vừa cập nhật thêm hai CPU tiên tiến, giúp trải nghiệm server của bạn mượt mà và nhanh hơn bao giờ hết:
Cả hai CPU đều mang lại hiệu suất cực nhanh, tăng cường bảo mật, và đảm bảo thời gian hoạt động tối đa cho các dự án cá nhân và doanh nghiệp của bạn.
————————————————————————
📞 𝐂𝐀𝐋𝐋: 0969 593 769  
📞 𝐓𝐄𝐋𝐄: @vnvps 
📞 Chấp nhận thanh toán: Vnđ | Usdt | Paypal  
🍀🎉🎊 UY TÍN LÂU NĂM TẠI MMO4ME 🍀🎉🎊 
#vpslagi #vpschinhhang #vpsgiare #vpshosting #vpswindows #ip #freevps #vpsvn #proxy #sock #server #vps #vpsvietnamgiare #vpsgpu #vpsus #trial #sale #gpu #vpsgpu #1mcloud''',

'''🔥 Tin siêu HOT: Đã Có VPS và Proxy NHẬT BẢN!
1MCLOUD vui mừng thông báo đã bổ sung thêm 𝐉𝐚𝐩𝐚𝐧 𝐯𝐩𝐬/𝐩𝐫𝐨𝐱𝐲 vào danh mục dịch vụ. Đây là lựa chọn tuyệt vời dành cho những khách hàng cần kết nối tại khu vực này.
🎯Vì sao chọn dịch vụ của chúng tôi?
ㅤ• Đa dạng quốc gia: Không chỉ Nhật Bản, chúng tôi còn cung cấp VPS và Proxy ở nhiều khu vực khác nhau.
ㅤ• Tốc độ cao, bảo mật tối ưu: Phù hợp cho mọi nhu cầu từ cá nhân đến doanh nghiệp.
ㅤ• Hỗ trợ chuyên nghiệp: Luôn đồng hành cùng bạn 24/7.
📢 Đặt hàng ngay hôm nay để trải nghiệm dịch vụ chất lượng hàng đầu!
—————————————————————
🌐 𝐖𝐄𝐁𝐒𝐈𝐓𝐄: 1mcloud.vn
📞 𝐂𝐀𝐋𝐋: 0969 593 769  
📱  𝐓𝐄𝐋𝐄: @vnvps 
🍀🎉🎊 UY TÍN LÂU NĂM TẠI MMO4ME 🍀🎉🎊 
#vpslagi #vpschinhhang #vpsgiare #vpshosting #vpswindows #ip #freevps #vpsvn #proxy #sock #server #vps #vpsvietnamgiare #vpsgpu #vpsus #trial #sale #gpu #vpsgpu #1mcloud''',

'''🔥 Vừa Cập Bến: VPS/Proxy Nhật Bản Mới!
Lô hàng mới VPS và Proxy Nhật Bản vừa cập nhật! Tốc độ nhanh, bảo mật cao, sẵn sàng phục vụ ngay hôm nay.

Hạ tầng hiện đại, nguồn cung mới, hiệu suất tối ưu.
Đáp ứng tốt mọi nhu cầu từ làm việc đến giải trí.
📌 Nhanh tay đặt ngay, số lượng giới hạn!
—————————————————————
🌐 𝐖𝐄𝐁𝐒𝐈𝐓𝐄: 1mcloud.vn
📞 𝐂𝐀𝐋𝐋: 0969 593 769  
📱  𝐓𝐄𝐋𝐄: @vnvps 
🍀🎉🎊 UY TÍN LÂU NĂM TẠI MMO4ME 🍀🎉🎊 
#vpslagi #vpschinhhang #vpsgiare #vpshosting #vpswindows #ip #freevps #vpsvn #proxy #sock #server #vps #vpsvietnamgiare #vpsgpu #vpsus #trial #sale #gpu #vpsgpu #1mcloud'''
                ],
                "delay": [8, 10]
            },
            "COMMENT": {
                "image": [
                    "",
                    ""
                ],
                "content": [
                    "UP!",
                    "Up!",
                    "up!",
                    "UP",
                    "Up",
                    "up",
                    "🆙",
                    "🆙🆙"
                ],
                "delay": [3, 6]
            },
            "SPAM": {
                "image": [
                    "",
                    ""
                ],
                "content": [
'''🎉🎉🎉 1mcloud.vn sẵn hàng vps - proxy chính hãng VN, US, Singapore, Anh, Pháp, Đức, Hà Lan, Úc, Canada…
• 922 proxy • PIA proxy
• Uy tín nhiều năm trên MMO4ME''',

'''🌟🌟🌟 1mcloud.vn vps - proxy chính hãng giá rẻ VN US SING và các nước Châu Âu
• dùng treo acc, log via, cắm tool, cày view, livestream…
• Cấu hình cao, ổn định, uptime 99%
• Dùng thử miễn phí
• tele @vnvps
• zalo 0969593769 hỗ trợ 24/24''',

'''🚀🚀 1mcloud.vn - VPS Proxy xịn, tốc độ cao, hỗ trợ các quốc gia như VN, US, Singapore, .... Dùng tốt cho treo acc, log via, cày view và nhiều mục đích khác!
• Uptime 99%, độ ổn định cao
• Dùng thử miễn phí!
• Hỗ trợ 24/7 qua Zalo 0969593769 hoặc Telegram @vnvps.''',

'''🌐🌐 VPS Proxy chính hãng tại 1mcloud.vn - đa dạng quốc gia: VN, Mỹ, Anh, Đức, Úc và nhiều quốc gia khác
• Sẵn proxy 922 và PIA
• Phù hợp cho livestream, chạy tool, và MMO
• Uptime 99%, bảo mật và đáng tin cậy
• Liên hệ ngay qua Zalo 0969593769 hoặc Telegram @vnvps'''
                ],
                "scroll number": 3,
                "post number": 5,
                "spam delay": [3, 6],
                "scan delay": [10, 20],
                "key filter": [
                    "mua vps",
                    "mua proxy",
                    "cần vps",
                    "cần proxy",
                    "cần tìm",
                    "kiểm vps",
                    "kiểm proxy",
                    "bác nào có",
                    "tư vấn về vps",
                    "tư vấn về proxy",
                    "ai bán vps",
                    "ai bán proxy",
                    "cần tư vấn",
                    "ib mình",
                    "ib em",
                    "inbox mình",
                    "inbox em",
                    "need vps",
                    "need proxy"
                ]
            }
        },
        "TABLE": [
            {
                "link group": "https://www.facebook.com/groups/345983411894599/",
                "name group": "Cộng Đồng VPS Việt Nam",
                "posts": [
                    {
                        "link post": "",
                        "content": "",
                        "status_post": "",
                        "status_comment": ""
                    }
                ]
            },
            {
                "link group": "https://www.facebook.com/groups/vpsgiatot/",
                "name group": "VPS Giá Tốt - VPS/RDP Cheap",
                "posts": [
                    {
                        "link post": "",
                        "content": "",
                        "status_post": "",
                        "status_comment": ""
                    }
                ]
            }
        ],
    }
    
    def __init__(self, data_folder: str, data_path: str):
        self.folder_path = data_folder
        self.data_path = data_path
        self.history_path = os.path.join(data_folder, "history.json")
        self._ensure_data_directory()
        
        if not os.path.exists(self.data_path): # Nếu chưa có file data -> Tạo (kèm luôn sheet Login)
            self.save_data()
        
        self.load_data()
        self.load_history()
    
    def load_data(self) -> None:
        """Load data from JSON file or create with defaults if not exists"""
        if os.path.exists(self.data_path):
            try:
                with open(self.data_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except json.JSONDecodeError:
                self.data = self.DEFAULT_DATA
        else: self.data = self.DEFAULT_DATA
    
    def save_data(self) -> bool:
        """Save configuration to JSON file"""
        try:
            with open(self.data_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
        except:
            return False
        return True

    def load_history(self) -> None:
        """Load history from JSON file or create empty if not exists"""
        if os.path.exists(self.history_path):
            try:
                with open(self.history_path, 'r', encoding='utf-8') as f:
                    self.history = set(json.load(f))
            except json.JSONDecodeError:
                self.history = set()
        else: self.history = set()

    def save_history(self) -> bool:
        """Save history to JSON file"""
        try:
            with open(self.history_path, 'w', encoding='utf-8') as f:
                json.dump(list(self.history), f, indent=4, ensure_ascii=False)
        except:
            return False
        return True

    def add_to_history(self, item_id: str) -> None:
        """Add an item to the history and save"""
        if item_id not in self.history:
            self.history.add(item_id)
            self.save_history()

    def is_in_history(self, item_id: str) -> bool:
        """Check if an item is in the history"""
        return item_id in self.history

    def _ensure_data_directory(self) -> None:
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
            
    def clear_data(self) -> None:
        """Clear all stored data"""
        if os.path.exists(self.data_path):
            os.remove(self.data_path)
        if os.path.exists(self.history_path):
            os.remove(self.history_path)