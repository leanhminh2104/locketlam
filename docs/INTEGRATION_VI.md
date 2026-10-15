# 📘 LocketLam — Hướng Dẫn Tích Hợp (Bản Tiếng Việt)

> **File này dùng để làm gì?**
> Đây là tài liệu hướng dẫn tích hợp từng bước dành cho lập trình viên — bao gồm code mẫu thực tế cho từng tính năng. Đọc file này khi bạn muốn biết **cách viết code để sử dụng từng API cụ thể** trong dự án của mình.

| Bản tài liệu | Ngôn ngữ | Vai trò |
|:---|:---|:---|
| 🇬🇧 **[INTEGRATION.md](INTEGRATION.md)** | **English** | **Bản chính (Primary)** |
| 🇻🇳 **[INTEGRATION_VI.md](INTEGRATION_VI.md)** | **Tiếng Việt** | **Bản phụ (Secondary)** |

---

### 🗺️ Bản Đồ Điều Hướng Tài Liệu

| Bạn muốn... | Đi đến |
|:---|:---|
| 🚀 **Giới thiệu tổng quan & khởi đầu nhanh** | ➡️ [README_VI.md](../README_VI.md) (VI) · [README.md](../README.md) (EN) |
| 📚 **Tra cứu chi tiết từng method, tham số & kiểu dữ liệu** | ➡️ [FEATURES_VI.md](FEATURES_VI.md) (VI) · [FEATURES.md](FEATURES.md) (EN) |
| 💡 **Mã nguồn mẫu chạy được ngay (8 scripts hoàn chỉnh)** | ➡️ [examples/vi/](../examples/vi/) (VI) · [examples/en/](../examples/en/) (EN) |

---

## 📑 Mục Lục

- [1. Cài Đặt](#1-cài-đặt)
- [2. Đăng Nhập & Quản Lý Phiên (Session)](#2-đăng-nhập--quản-lý-phiên-session)
- [3. Giả Lập Thiết Bị iOS Chuẩn Apple](#3-giả-lập-thiết-bị-ios-chuẩn-apple)
- [4. Đăng Ảnh & Nhãn Tùy Biến (Moments)](#4-đăng-ảnh--nhãn-tùy-biến-moments)
- [5. Đăng Video Dài & Tự Động Nén HEVC](#5-đăng-video-dài--tự-động-nén-hevc)
- [6. Feed, Tương Tác & Cảm Xúc](#6-feed-tương-tác--cảm-xúc)
- [7. Bạn Bè, Lời Mời & Chặn Người Dùng](#7-bạn-bè-lời-mời--chặn-người-dùng)
- [8. Tin Nhắn & WebSocket Trực Tiếp (Real-Time Chat)](#8-tin-nhắn--websocket-trực-tiếp-real-time-chat)
- [9. Xử Lý Lỗi Toàn Diện](#9-xử-lý-lỗi-toàn-diện)
- [10. Bộ Ví Dụ Hoàn Chỉnh](#10-bộ-ví-dụ-hoàn-chỉnh)
- [11. Bản Quyền & Giấy Phép](#11-bản-quyền--giấy-phép)

---

## 1. Cài Đặt

### Cài đặt qua PyPI (Khuyên dùng)

```bash
pip install locketlam
```

> **Yêu cầu hệ thống:** Python >= 3.8. Thư viện đã tích hợp sẵn binary nén video FFmpeg cho Windows, macOS và Linux — bạn không cần cài đặt FFmpeg thủ công ngoài hệ thống!

### Cài đặt từ mã nguồn GitHub

```bash
git clone https://github.com/leanhminh2104/locketlam.git
cd locketlam
pip install -e .
```

---

## 2. Đăng Nhập & Quản Lý Phiên (Session)

### Đăng nhập lần đầu bằng email & mật khẩu

```python
from locketlam import LocketClient

# Khởi tạo client kèm đường dẫn lưu session
client = LocketClient(session_path="session.json")

# Đăng nhập vào tài khoản Locket
client.login("user@example.com", "password123")

print("Đăng nhập thành công! User ID:", client.session.uid)
```

> Sau khi đăng nhập thành công, phiên làm việc sẽ tự động được ghi nhớ vào file `session.json`. Các token được mã hóa an toàn và tự động làm mới khi hết hạn (refresh token).

### Khởi tạo từ session đã lưu (Không cần đăng nhập lại)

```python
from locketlam import LocketClient

client = LocketClient(session_path="session.json")

if client.is_authenticated():
    print("Phiên hợp lệ! Đã xác thực với UID:", client.session.uid)
else:
    print("Phiên hết hạn hoặc chưa đăng nhập, tiến hành đăng nhập lại...")
    client.login("user@example.com", "password123")
```

---

## 3. Giả Lập Thiết Bị iOS Chuẩn Apple

Thư viện tự động giả lập đầy đủ chữ ký phần cứng của iPhone (Apple IDFA, Vendor ID, Bundle Identifier, Firebase GMPID, Protobuf Flags) giúp tài khoản vận hành tự nhiên, không bị hệ thống Locket gắn cờ bot.

```python
from locketlam import LocketClient

client = LocketClient(session_path="session.json")

# Chế độ 1: Tự động giả lập iPhone thực tế (Mặc định - Khuyên dùng)
client.set_device(auto_emulate=True)

# Chế độ 2: Tự chỉ định thông số thiết bị iOS của riêng bạn
client.set_device(
    auto_emulate=False,
    installation_id="A1B2C3D4-E5F6-7890-ABCD-EF1234567890",
    hardware_model="iPhone16,2",     # iPhone 15 Pro Max
    ios_version="18.2.0",
    app_version="2.69.0"
)
```

---

## 4. Đăng Ảnh & Nhãn Tùy Biến (Moments)

### Đăng ảnh với nhãn màu có sẵn (`NoteType`)

Thư viện hỗ trợ hơn 158 nhãn preset chính thức của Locket Camera:

```python
from locketlam import LocketClient, NoteType

client = LocketClient(session_path="session.json")

res = client.moments.post(
    image="photo.jpg",                      # Đường dẫn file nội bộ hoặc URL mạng
    caption="Dạo phố cuối tuần ☕",
    note_type=NoteType.DANG_BAN_TUONG_TU   # Chọn từ danh sách NoteType có sẵn
)

print("Đăng bài thành công! Moment ID:", res.get("id"))
```

### Đăng ảnh với dải màu Gradient tự thiết kế

```python
res = client.moments.post(
    image="coding.jpg",
    caption="Xuyên đêm lập trình 💻",
    icon="⚡",
    colors=["#FF416C", "#8A2387"],         # Gradient Hồng Neon -> Tím Đậm
    text_color="#FFFFFF"
)
```

### Đăng ảnh giới hạn bạn bè nhận bài (Recipients)

```python
res = client.moments.post(
    image="family.jpg",
    caption="Chỉ chia sẻ cho nhóm thân thiết ❤️",
    recipients=["UID_BAN_BE_1", "UID_BAN_BE_2"]
)
```

### Đăng ảnh ở chế độ riêng tư (Chỉ mình tôi)

```python
res = client.moments.post(
    image="diary.jpg",
    caption="Nhật ký cá nhân bí mật",
    is_private=True
)
```

---

## 5. Đăng Video Dài & Tự Động Nén HEVC

Máy chủ Locket Camera giới hạn video tải lên phải nhỏ hơn 6 MB. `locketlam` tích hợp sẵn hệ thống nén thích ứng H.265/HEVC theo chuẩn codec phần cứng Apple iOS, cho phép bạn tải lên các video dài (10 đến 15 phút) mà vẫn giữ nét tối đa và dung lượng luôn an toàn dưới 5.7 MB.

### Đăng video cơ bản (Tự động nén thông minh)

```python
from locketlam import LocketClient

client = LocketClient(session_path="session.json")

res = client.moments.post(
    video="clip_du_lich.mp4",               # File >= 6 MB sẽ tự động nén
    caption="Kỳ nghỉ tuyệt vời 🏖️"
)

print("Video Moment ID:", res.get("id"))
```

### Đăng video kèm thanh tiến trình (Progress Callback)

```python
from locketlam import LocketClient, NoteType

client = LocketClient(session_path="session.json")

def on_progress(percent: int, message: str):
    print(f"\r[{percent:3d}%] {message}", end="", flush=True)

client.moments.post(
    video="video_dai_10_phut.mp4",
    caption="Toàn cảnh chuyến đi 🎬",
    note_type=NoteType.FLEX_DEN_HOI_THO_CUOI,
    auto_compress=True,                    # Bật nén thích ứng HEVC
    priority="balanced",                   # 'video' (ưu tiên nét), 'audio' (ưu tiên nhạc), 'balanced'
    progress_callback=on_progress
)
print("\nĐăng video hoàn tất!")
```

### Chỉ upload video lấy URL Firebase (Không tạo bài đăng)

```python
video_url = client.moments.upload_video(
    video_path_or_bytes="raw_clip.mp4",
    auto_compress=True,
    priority="video"
)
print("URL video trên Firebase Storage:", video_url)
```

---

## 6. Feed, Tương Tác & Cảm Xúc

### Lấy bảng tin khoảnh khắc mới nhất

```python
feed = client.moments.get_latest()

for moment in feed:
    author = moment.get("user", {}).get("first_name", "Ẩn danh")
    print(f"[{moment.get('id')}] {author}: {moment.get('caption')}")
```

### Lấy toàn bộ bài đăng của chính mình

```python
my_moments = client.moments.get_all_my_moments()
print(f"Bạn đã đăng tổng cộng {len(my_moments)} khoảnh khắc.")
```

### Xem danh sách bạn bè đã xem bài đăng

```python
views = client.moments.get_views(moment_id="MOMENT_UID")

for view in views:
    print(f"- {view.get('first_name')} (UID: {view.get('uid')}) - Biểu cảm: {view.get('emoji', 'Xem thường')}")
```

### Thả cảm xúc và bình luận vào bài đăng

```python
# Thả biểu cảm emoji
client.moments.react(moment_id="MOMENT_UID", emoji="❤️")

# Gửi bình luận
client.moments.comment(moment_id="MOMENT_UID", text="Khoảnh khắc đỉnh quá bạn ơi! 🔥")

# Xóa bài đăng của chính mình
client.moments.delete(moment_id="MOMENT_UID")
```

---

## 7. Bạn Bè, Lời Mời & Chặn Người Dùng

### Lấy danh sách bạn bè đầy đủ hồ sơ

```python
friends = client.friends.get_all_friends()

for friend in friends:
    print(f"- {friend.get('first_name')} {friend.get('last_name', '')} (@{friend.get('username')}) - UID: {friend.get('uid')}")
```

### Kết bạn bằng Username (Tự động giải mã invite link)

```python
# Hỗ trợ cả username hoặc link locket.cam/<username>
client.friends.send_request_by_username("leanhminh")
```

### Quản lý lời mời kết bạn

```python
# Lấy danh sách lời mời đến và đi
requests = client.friends.get_friend_requests()
print(f"Lời mời đến: {len(requests['incoming'])}, Đã gửi: {len(requests['outgoing'])}")

# Chấp nhận lời mời kết bạn
client.friends.accept_request("UID_NGUOI_GUI")
```

### Hủy kết bạn, chặn và bỏ chặn

```python
# Hủy kết bạn (hỗ trợ UID hoặc Username)
client.friends.remove("UID_HOAC_USERNAME")

# Chặn người dùng (tự động xóa khỏi danh sách bạn bè trên Locket)
client.friends.block("UID_HOAC_USERNAME")

# Bỏ chặn
client.friends.unblock("UID_HOAC_USERNAME")
```

---

## 8. Tin Nhắn & WebSocket Trực Tiếp (Real-Time Chat)

### Lấy hộp thư đến (Danh sách cuộc trò chuyện)

```python
conversations = client.chat.get_conversations()

for conv in conversations:
    unread = conv.get("unread_count", 0)
    print(f"Hội thoại: {conv.get('id')} | Đối phương UID: {conv.get('peer_uid')} | Chưa đọc: {unread}")
```

### Gửi tin nhắn văn bản hoặc khoảnh khắc vào phòng chat

```python
# Gửi tin nhắn văn bản thông thường
client.chat.send_message(
    receiver_uid="UID_BAN_BE",
    text="Xin chào! Bạn đang làm gì đấy? 👋"
)

# Chia sẻ trực tiếp một khoảnh khắc vào chat (kèm ghi chú tùy chọn)
client.chat.send_moment(
    receiver_uid="UID_BAN_BE",
    moment_uid="MOMENT_UID",
    text="Xem bài này của tôi nhé 😄"
)
```

### Thả cảm xúc & Thu hồi tin nhắn

```python
# Thả cảm xúc emoji (hỗ trợ combo nhiều icon: '❤️', '🔥🥰', '❤️❤️❤️')
client.chat.send_reaction(
    conversation_id="CONVERSATION_ID",
    message_id="MESSAGE_ID",
    emoji="❤️"
)

# Gỡ bỏ cảm xúc đã thả
client.chat.remove_reaction(
    conversation_id="CONVERSATION_ID",
    message_id="MESSAGE_ID"
)

# Thu hồi / Xóa tin nhắn do chính bạn gửi
client.chat.delete_message(
    conversation_uid="CONVERSATION_ID",
    message_uid="MESSAGE_ID"
)
```

### Đọc tin nhắn ở chế độ Ẩn Danh (Ghost Mode)

```python
# Lấy lịch sử tin nhắn đồng bộ từ Firestore
messages = client.chat.get_messages(other_user_id="UID_BAN_BE", fetch_server=True)

# Đánh dấu đã đọc ở chế độ ẩn danh (không báo cho người gửi biết bạn đã xem)
client.chat.mark_as_read(
    other_user_id="UID_BAN_BE",
    send_read_receipt=False            # False = Chế độ ẩn danh, True = Báo đã xem
)
```

### Lắng nghe tin nhắn mới thời gian thực qua WebSocket

```python
def handle_incoming_message(msg):
    print("\n[Tin nhắn mới]:", msg)

# Mở kết nối thời gian thực wss://api.locketcamera.com/wss_v2/chat (chạy nền bất đồng bộ)
client.chat.listen_realtime(
    other_user_id="UID_BAN_BE",
    callback=handle_incoming_message
)
```

---

## 9. Xử Lý Lỗi Toàn Diện

Mọi ngoại lệ trong thư viện đều kế thừa từ lớp cha `LocketError`, giúp việc bắt lỗi trong ứng dụng sản phẩm cực kỳ thuận tiện:

```python
from locketlam.exceptions import (
    LocketError,
    AuthenticationError,
    StorageUploadError,
    LocketAPIError
)

try:
    client.moments.post(image="photo.jpg", caption="Test")

except AuthenticationError as e:
    print("❌ Lỗi phiên/xác thực (sai mật khẩu hoặc token hết hạn):", e)

except StorageUploadError as e:
    print("❌ Lỗi tải tệp lên Firebase Cloud Storage:", e)

except LocketAPIError as e:
    print(f"❌ Lỗi từ máy chủ Locket [HTTP {e.status_code}]:", e.message)

except LocketError as e:
    print("❌ Lỗi chung từ thư viện LocketLam:", e)
```

---

## 10. Bộ Ví Dụ Hoàn Chỉnh

Trong thư mục [`examples/`](../examples/), bạn có thể tìm thấy toàn bộ 8 script mẫu hoàn chỉnh, có thể chạy thử trực tiếp ngay:

| Tính Năng Thực Nghiệm | Mã Nguồn Tiếng Việt | Mã Nguồn Tiếng Anh |
|:---|:---|:---|
| 01. Đăng nhập & Lưu trữ Session | [`examples/vi/01_login_and_session.py`](../examples/vi/01_login_and_session.py) | [`examples/en/01_login_and_session.py`](../examples/en/01_login_and_session.py) |
| 02. Hồ sơ cá nhân & Cập nhật tên | [`examples/vi/02_user_profile.py`](../examples/vi/02_user_profile.py) | [`examples/en/02_user_profile.py`](../examples/en/02_user_profile.py) |
| 03. Đăng ảnh & 158+ nhãn NoteType | [`examples/vi/03_post_image_moment.py`](../examples/vi/03_post_image_moment.py) | [`examples/en/03_post_image_moment.py`](../examples/en/03_post_image_moment.py) |
| 04. Đăng video dài & Nén HEVC | [`examples/vi/04_post_video_moment.py`](../examples/vi/04_post_video_moment.py) | [`examples/en/04_post_video_moment.py`](../examples/en/04_post_video_moment.py) |
| 05. Bảng tin, Lượt xem & Cảm xúc | [`examples/vi/05_feed_views_reactions.py`](../examples/vi/05_feed_views_reactions.py) | [`examples/en/05_feed_views_reactions.py`](../examples/en/05_feed_views_reactions.py) |
| 06. Bạn bè, Lời mời & Chặn | [`examples/vi/06_friends_and_contacts.py`](../examples/vi/06_friends_and_contacts.py) | [`examples/en/06_friends_and_contacts.py`](../examples/en/06_friends_and_contacts.py) |
| 07. Nhắn tin & WebSocket Real-Time | [`examples/vi/07_chat_and_reactions.py`](../examples/vi/07_chat_and_reactions.py) | [`examples/en/07_chat_and_reactions.py`](../examples/en/07_chat_and_reactions.py) |
| Menu CLI tương tác tổng hợp | [`examples/vi/interactive_demo.py`](../examples/vi/interactive_demo.py) | [`examples/en/interactive_demo.py`](../examples/en/interactive_demo.py) |

```bash
# Trải nghiệm ngay giao diện dòng lệnh tương tác Tiếng Việt
python examples/vi/interactive_demo.py
```

---

## 11. Bản Quyền & Giấy Phép

Bản quyền © 2026 **LAMDev x DaLyMMO.com**. Tất cả các quyền được bảo lưu.

Dự án được phân phối chính thức theo giấy phép mã nguồn mở [MIT License](../LICENSE).
Mọi đóng góp và báo lỗi xin gửi về [GitHub Issues](https://github.com/leanhminh2104/locketlam/issues).
