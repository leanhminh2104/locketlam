# 🚀 LocketLam - Thư Viện Python Toàn Diện Cho Locket Camera

<p align="center">
  <img src="https://raw.githubusercontent.com/leanhminh2104/locketlam/main/assets/banner.PNG" alt="LocketLam Banner" width="700" onerror="this.style.display='none'"/>
</p>

<p align="center">
  <b>Thư viện Python SDK mã nguồn mở điều khiển Locket Camera với giả lập phần cứng thiết bị Apple iOS chính hãng 100%.</b>
</p>

<p align="center">
  <a href="https://pypi.org/project/locketlam/"><img src="https://img.shields.io/pypi/v/locketlam.svg?style=flat-square&color=blue" alt="PyPI Version"></a>
  <a href="https://pypi.org/project/locketlam/"><img src="https://img.shields.io/pypi/pyversions/locketlam.svg?style=flat-square" alt="Python Versions"></a>
  <a href="https://github.com/leanhminh2104/locketlam/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="License MIT"></a>
  <a href="https://github.com/leanhminh2104/locketlam/blob/main/README.md"><img src="https://img.shields.io/badge/Language-English-blue.svg?style=flat-square" alt="English Docs"></a>
</p>

---

## 🗺️ Bản Đồ Tài Liệu

> **Bạn đang ở: README_VI** — trang giới thiệu chính. Đọc để hiểu thư viện làm được gì và có phù hợp với nhu cầu của bạn không.

| Bạn muốn... | Đi đến |
|:---|:---|
| 🚀 **Cài đặt và chạy thử nhanh** | Đúng chỗ rồi — xem [Khởi Đầu Nhanh](#-khởi-đầu-nhanh) bên dưới |
| 🛠️ **Tích hợp vào dự án của mình từng bước** | ➡️ [INTEGRATION_VI.md](https://github.com/leanhminh2104/locketlam/blob/main/docs/INTEGRATION_VI.md) (VI) · [INTEGRATION.md](https://github.com/leanhminh2104/locketlam/blob/main/docs/INTEGRATION.md) (EN) |
| 📚 **Tra cứu method, tham số cụ thể** | ➡️ [FEATURES_VI.md](https://github.com/leanhminh2104/locketlam/blob/main/docs/FEATURES_VI.md) (VI) · [FEATURES.md](https://github.com/leanhminh2104/locketlam/blob/main/docs/FEATURES.md) (EN) |
| 💡 **Xem code mẫu chạy được ngay** | ➡️ [examples/vi/](https://github.com/leanhminh2104/locketlam/tree/main/examples/vi/) — 8 script hoàn chỉnh theo từng tính năng |
| 🇬🇧 **Đọc trang này bằng tiếng Anh** | ➡️ [README.md](https://github.com/leanhminh2104/locketlam/blob/main/README.md) |

---

## 📖 Mục Lục

- [Tổng Quan](#-tổng-quan)
- [Tính Năng Nổi Bật](#-tính-năng-nổi-bật)
- [Cài Đặt](#-cài-đặt)
- [Khởi Đầu Nhanh](#-khởi-đầu-nhanh)
- [Tài Liệu API Chi Tiết](#-tài-liệu-api-chi-tiết)
  - [1. Xác Thực & Quản Lý Phiên (client.session)](#1-xác-thực--quản-lý-phiên-clientsession)
  - [2. Hồ Sơ Người Dùng (client.user)](#2-hồ-sơ-người-dùng-clientuser)
  - [3. Khoảnh Khắc & Đăng Media (client.moments)](#3-khoảnh-khắc--đăng-media-clientmoments)
  - [4. Bạn Bè & Nhóm (client.friends)](#4-bạn-bè--nhóm-clientfriends)
  - [5. Tin Nhắn & WebSocket Trực Tiếp (client.chat)](#5-tin-nhắn--websocket-trực-tiếp-clientchat)
- [Xử Lý Lỗi](#-xử-lý-lỗi)
- [Ví Dụ Mẫu (Examples)](#-ví-dụ-mẫu-examples)
- [Tiếp Theo](#-tiếp-theo)
- [Đóng Góp](#-đóng-góp)
- [Ủng Hộ & Quyên Góp (Sponsor)](#-ủng-hộ--quyên-góp-sponsor)
- [Bản Quyền & Giấy Phép](#-bản-quyền--giấy-phép)
- [Tuyên Bố Miễn Trừ Trách Nhiệm](#-tuyên-bố-miễn-trừ-trách-nhiệm)

---

## 🌟 Tổng Quan

**`locketlam`** là bộ công cụ SDK Python dịch ngược chuẩn quốc tế, cho phép tương tác trực tiếp với máy chủ Locket Camera. Thư viện giúp các nhà phát triển, người làm bot và kỹ sư tự động hóa có thể đăng ảnh, upload video dài, nhắn tin trực tiếp và quản lý bạn bè bằng Python mà không cần phải chạy ứng dụng trên thiết bị iOS.

---

## ✨ Tính Năng Nổi Bật

- 📱 **Giả Lập Thiết Bị Apple iOS Chuẩn 100%**: Gửi chính xác định danh phần cứng iPhone (iPhone 13 Pro đến iPhone 15 Pro Max), bundle ID (`com.locket.Locket`), Firebase GMPID và các cờ phân tích Google Protobuf, giúp tài khoản không bao giờ bị khóa hay chặn.
- 🎬 **Tối Ưu Hóa Video Tự Động (Auto-Compression)**:
  - Tự động nén chuẩn **H.265 / HEVC (`-tag:v hvc1`)** nguyên bản của Apple.
  - **Giữ nguyên 100% độ phân giải gốc** (Full HD, 2K, 4K), nén video từ 70MB - 100MB xuống an toàn dưới **6 MB** của Locket.
  - Chuẩn hóa tốc độ khung hình **24 FPS** và chu kỳ **Keyframe GOP 2 giây** chống giật khựng khi xem stream trên feed.
  - Hỗ trợ video dài từ **15s, 1 phút đến 5 - 10 phút**.
- 🎨 **Tùy Biến Caption & Dải Màu Gradient Rực Rỡ**:
  - Hỗ trợ hơn **158+ bộ màu & biểu tượng preset có sẵn** của Locket (`NoteType`), cho phép tùy chỉnh chữ tùy ý hoặc tự phối dải màu Gradient hex riêng.
  - Hỗ trợ tự do tùy biến dải màu gradient (`colors=['#HEX1', '#HEX2']`), màu chữ (`text_color`) và biểu tượng emoji (`icon`).
- 🔄 **Tự Động Làm Mới Token (Autonomous Refresh)**: Tự động phát hiện và làm mới Firebase JWT `idToken` chạy ngầm.
- ⚡ **Hỗ Trợ WebSocket Thời Gian Thực**: Lắng nghe tin nhắn chat trực tiếp theo thời gian thực qua kênh `wss://api.locketcamera.com/wss_v2/chat`.
- 📦 **Cài Đặt 1 Bước**: Kèm sẵn công cụ xử lý FFmpeg độc lập thông qua `imageio-ffmpeg`, người dùng không cần cài đặt FFmpeg thủ công vào hệ thống.

---

## 📦 Cài Đặt

Cài đặt phiên bản mới nhất từ PyPI chỉ với 1 câu lệnh duy nhất:

```bash
pip install locketlam
```

---

## ⚡ Khởi Đầu Nhanh

### 1. Đăng Nhập & Lưu Phiên

```python
from locketlam import LocketClient

# Khởi tạo client và lưu session vào file locketlam_session.json
client = LocketClient(session_path="locketlam_session.json")
client.login("email_cua_ban@example.com", "mat_khau_cua_ban")

print(f"Đăng nhập thành công với UID: {client.session.uid}")
```

### 2. Sử Dụng Lại Phiên Đã Lưu

```python
from locketlam import LocketClient

# Tự động đọc lại phiên đã lưu mà không cần gõ lại mật khẩu
client = LocketClient(session_path="session.json")
profile = client.user.get_profile()
print(f"Xin chào, {profile.get('first_name')} {profile.get('last_name')}!")
```

---

## 📚 Tài Liệu API Chi Tiết

### 1. Khoảnh Khắc & Đăng Media (`client.moments`)

```python
from locketlam import LocketClient, NoteType

client = LocketClient(session_path="session.json")

# 1. Đăng ảnh kèm Caption văn bản tiêu chuẩn
client.moments.post(
    image="photo.jpg",
    caption="Cuối tuần dạo phố ☕"
)

# 2. Đăng video dài kèm nhãn màu Preset hoặc Tự Phối Gradient
client.moments.post(
    image="thumbnail.jpg",
    video="video_5_phut.mp4",               # Tự động nén HEVC chuẩn Apple < 6MB
    note_type=NoteType.DANG_BAN_TUONG_TU    # Nhãn "Đang bận tương tư" 💭
)

# 3. Tự do tùy biến màu sắc, biểu tượng và màu chữ
client.moments.post(
    image="thumb.jpg",
    video="clip.mp4",
    caption="Bình minh rực rỡ 🌅",
    icon="✨",
    colors=["#FF512F", "#DD2476"],          # Dải màu gradient tự chọn
    text_color="#FFFFFF"                    # Màu chữ
)

# 4. Lấy feed khoảnh khắc mới nhất
feed = client.moments.get_latest()

# 5. Thả cảm xúc emoji vào bài đăng của bạn bè
client.moments.react(moment_uid="MOMENT_ID_O_DAY", reaction="❤️")

# 6. Bình luận vào khoảnh khắc (nhảy thẳng vào tin nhắn chat)
client.moments.comment(
    moment_uid="MOMENT_ID",
    receiver_uid="FRIEND_UID",
    text="Ảnh chụp góc này đẹp quá!"
)

# 7. Xem danh sách người đã xem và biểu cảm đã thả vào bài của mình
views_info = client.moments.get_views("MOMENT_ID")
print(f"Số lượt xem: {views_info.get('count')}")
```

---

### 2. Quản Lý Hồ Sơ Cá Nhân (`client.user`)

```python
# Lấy thông tin tài khoản
me = client.user.get_profile()

# Tìm kiếm hồ sơ người dùng bằng username
user = client.user.get_profile_by_username("username_can_tim")

# Cập nhật họ và tên
client.user.update_name(first_name="Minh", last_name="Lê")

# Đổi ảnh đại diện avatar (tự động nén WebP và upload)
client.user.update_avatar("avatar_moi.png")
```

---

### 3. Bạn Bè & Nhóm (`client.friends`)

```python
# Lấy danh sách bạn bè đầy đủ kèm thông tin chi tiết
friends = client.friends.get_all_friends()

# Gửi lời mời kết bạn chỉ với Username
client.friends.send_request_by_username("nguoidung123")

# Đồng ý lời mời kết bạn
client.friends.accept_request(user_uid="TARGET_USER_UID")

# Lấy danh sách nhóm
groups = client.friends.get_groups_and_friends()
```

---

### 4. Tin Nhắn Trực Tiếp & WebSocket Real-Time (`client.chat`)

```python
# Gửi tin nhắn văn bản vào cuộc trò chuyện
client.chat.send_message(
    receiver_uid="FRIEND_UID",
    text="Chào bạn, hôm nay thế nào?"
)

# Lắng nghe tin nhắn chat theo thời gian thực (Real-Time WebSocket)
def on_new_message(msg):
    print(f"Tin nhắn mới từ {msg.get('sender')}: {msg.get('text')}")

client.chat.listen(on_message=on_new_message)
```

---

## 🛡️ Xử Lý Lỗi

Thư viện cung cấp các lớp ngoại lệ strongly-typed để xử lý sự cố an toàn:

```python
from locketlam.exceptions import (
    LocketError,
    AuthenticationError,
    StorageUploadError,
    LocketAPIError
)

try:
    client.moments.post(image="test.jpg", caption="Hello")
except AuthenticationError:
    print("Lỗi xác thực: Vui lòng kiểm tra lại tài khoản hoặc token đã hết hạn!")
except StorageUploadError as e:
    print(f"Lỗi tải lên máy chủ lưu trữ: {e}")
except LocketAPIError as e:
    print(f"Lỗi phản hồi từ Locket API: {e.status_code} - {e.message}")
except LocketError as e:
    print(f"Lỗi thư viện Locket: {e}")
```

---

## 💡 Ví Dụ Mẫu (Examples)

Thư mục [`examples/`](https://github.com/leanhminh2104/locketlam/tree/main/examples/) cung cấp các script hoàn chỉnh, chạy được ngay cho từng tính năng:

| Tính Năng | Script |
|:---|:---|
| Đăng nhập & Session | [`examples/vi/01_login_and_session.py`](https://github.com/leanhminh2104/locketlam/blob/main/examples/vi/01_login_and_session.py) |
| Hồ sơ người dùng | [`examples/vi/02_user_profile.py`](https://github.com/leanhminh2104/locketlam/blob/main/examples/vi/02_user_profile.py) |
| Đăng ảnh & NoteType | [`examples/vi/03_post_image_moment.py`](https://github.com/leanhminh2104/locketlam/blob/main/examples/vi/03_post_image_moment.py) |
| Đăng video & HEVC | [`examples/vi/04_post_video_moment.py`](https://github.com/leanhminh2104/locketlam/blob/main/examples/vi/04_post_video_moment.py) |
| Feed & Tương tác | [`examples/vi/05_feed_views_reactions.py`](https://github.com/leanhminh2104/locketlam/blob/main/examples/vi/05_feed_views_reactions.py) |
| Bạn bè & Kết bạn | [`examples/vi/06_friends_and_contacts.py`](https://github.com/leanhminh2104/locketlam/blob/main/examples/vi/06_friends_and_contacts.py) |
| Nhắn tin & Real-Time | [`examples/vi/07_chat_and_reactions.py`](https://github.com/leanhminh2104/locketlam/blob/main/examples/vi/07_chat_and_reactions.py) |
| Menu CLI tương tác | [`examples/vi/interactive_demo.py`](https://github.com/leanhminh2104/locketlam/blob/main/examples/vi/interactive_demo.py) |

```bash
python examples/vi/interactive_demo.py
```

> 📖 Xem hướng dẫn tích hợp chi tiết: [`docs/INTEGRATION_VI.md`](https://github.com/leanhminh2104/locketlam/blob/main/docs/INTEGRATION_VI.md)
> 📋 Xem toàn bộ API catalog: [`docs/FEATURES_VI.md`](https://github.com/leanhminh2104/locketlam/blob/main/docs/FEATURES_VI.md)

---

## 📚 Tiếp Theo

| Tài liệu | Nội dung |
|:---|:---|
| [📘 docs/INTEGRATION.md](https://github.com/leanhminh2104/locketlam/blob/main/docs/INTEGRATION.md) | Hướng dẫn tích hợp từng bước kèm code mẫu chi tiết (Bản chính - EN) |
| [📘 docs/INTEGRATION_VI.md](https://github.com/leanhminh2104/locketlam/blob/main/docs/INTEGRATION_VI.md) | Hướng dẫn tích hợp từng bước kèm code mẫu chi tiết (Bản phụ - VI) |
| [📋 docs/FEATURES.md](https://github.com/leanhminh2104/locketlam/blob/main/docs/FEATURES.md) | Danh mục API đầy đủ — toàn bộ lớp, phương thức và tham số (EN) |
| [📋 docs/FEATURES_VI.md](https://github.com/leanhminh2104/locketlam/blob/main/docs/FEATURES_VI.md) | Danh mục API đầy đủ — toàn bộ lớp, phương thức và tham số (VI) |
| [💡 examples/vi/](https://github.com/leanhminh2104/locketlam/tree/main/examples/vi/) | 8 script mẫu chạy được ngay theo từng tính năng (Tiếng Việt) |
| [💡 examples/en/](https://github.com/leanhminh2104/locketlam/tree/main/examples/en/) | 8 example scripts (English) |

---

## 🤝 Đóng Góp

Mọi đóng góp, báo lỗi và yêu cầu tính năng đều được chào đón!

1. Fork project.
2. Tạo Feature Branch (`git checkout -b feature/TinhNangMoi`).
3. Commit (`git commit -m 'feat: thêm tính năng mới'`).
4. Push (`git push origin feature/TinhNangMoi`).
5. Tạo Pull Request.

---

## 💖 Ủng Hộ & Quyên Góp (Sponsor)

Nếu thư viện **`locketlam`** hữu ích cho các dự án hoặc nghiên cứu của bạn, hãy ủng hộ tác giả một ly cà phê nhé!

<div align="center">

| Cổng Thanh Toán | Thông Tin Chi Tiết |
| :--- | :--- |
| 🌐 **Trang Ủng Hộ Chính Thức** | [https://leanhminh.io.vn/donate](https://leanhminh.io.vn/donate) |
| 🏦 **Ngân Hàng MB Bank** | Số tài khoản: `2104200637`<br>Chủ tài khoản: **LÊ VĂN ANH MINH** |
| 🏦 **Ngân Hàng ACB** | Số tài khoản: `22002921`<br>Chủ tài khoản: **LÊ VĂN ANH MINH** |
| 🟡 **Binance (UID / Pay ID)** | `283319011` |
| 💳 **PayPal Quốc Tế** | [paypal.me/leanhminh2104](https://paypal.me/leanhminh2104) |

</div>

> *Mọi sự ủng hộ dù nhỏ nhất cũng là nguồn động viên rất lớn để duy trì và cập nhật dự án. Cảm ơn các bạn rất nhiều! ❤️*

---

## 📜 Bản Quyền & Giấy Phép

Bản quyền © 2026 **LAMDev x DaLyMMO.com**.

Phát hành theo giấy phép **MIT License**. Xem file [`LICENSE`](https://github.com/leanhminh2104/locketlam/blob/main/LICENSE) để biết thêm chi tiết.

---

## ⚠️ Tuyên Bố Miễn Trừ Trách Nhiệm

Thư viện này là dự án mã nguồn mở dịch ngược phục vụ mục đích học tập, nghiên cứu và phát triển tích hợp. Thư viện **không** thuộc quyền sở hữu, liên kết hoặc bảo trợ bởi Locket Camera, Inc. Vui lòng sử dụng có trách nhiệm và tuân thủ các điều khoản dịch vụ của bên thứ ba.
