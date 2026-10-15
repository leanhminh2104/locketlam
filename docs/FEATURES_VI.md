# 📋 LocketLam — Danh Mục API Đầy Đủ (Tiếng Việt)

> **File này dùng để làm gì?**
> Đây là tài liệu **tra cứu API** — liệt kê toàn bộ các lớp, phương thức, tham số và kiểu dữ liệu trong locketlam. Đọc file này khi bạn cần **tra cứu tên một phương thức, tham số truyền vào là gì, kiểu trả về** ra sao.

| Bạn muốn... | Đi đến |
|:---|:---|
| 🚀 **Giới thiệu, cài đặt, quick start** | ➡️ [README_VI.md](../README_VI.md) (VI) · [README.md](../README.md) (EN) |
| 🛠️ **Code mẫu tích hợp từng tính năng** | ➡️ [INTEGRATION_VI.md](INTEGRATION_VI.md) (VI) · [INTEGRATION.md](INTEGRATION.md) (EN) |
| 💡 **Script mẫu chạy được ngay** | ➡️ [examples/vi/](../examples/vi/) (VI) · [examples/en/](../examples/en/) (EN) |
| 🇬🇧 **Bản tiếng Anh (Bản chính)** | ➡️ [FEATURES.md](FEATURES.md) |

> **Phiên bản**: 1.0.1 · **Gói PyPI**: [locketlam](https://pypi.org/project/locketlam/) · **Tác giả**: LAMDev x DaLyMMO.com · **Giấy phép**: MIT

---


## 📑 Mục Lục

1. [Tổng Quan Kiến Trúc](#1-tổng-quan-kiến-trúc)
2. [Giả Lập Thiết Bị & Phần Cứng iOS (`DeviceProfile`)](#2-giả-lập-thiết-bị--phần-cứng-ios-deviceprofile)
3. [Xác Thực & Quản Lý Phiên (`SessionManager`)](#3-xác-thực--quản-lý-phiên-sessionmanager)
4. [Hồ Sơ Cá Nhân & Người Dùng (`client.user`)](#4-hồ-sơ-cá-nhân--người-dùng-clientuser)
5. [Khoảnh Khắc & Xử Lý Media (`client.moments`)](#5-khoảnh-khắc--xử-lý-media-clientmoments)
6. [Bạn Bè, Nhóm & Quản Lý Chặn (`client.friends`)](#6-bạn-bè-nhóm--quản-lý-chặn-clientfriends)
7. [Nhắn Tin Trực Tiếp & Real-Time WebSocket (`client.chat`)](#7-nhắn-tin-trực-tiếp--real-time-websocket-clientchat)
8. [Hệ Thống Lỗi & Ngoại Lệ (Exceptions)](#8-hệ-thống-lỗi--ngoại-lệ-exceptions)
9. [Hướng Dẫn Đóng Gói & Phát Hành (Publishing Guide)](#9-hướng-dẫn-đóng-gói--phát-hành-publishing-guide)
10. [Bản Quyền & Giấy Phép](#-bản-quyền--giấy-phép)

---

## 1. Tổng Quan Kiến Trúc

Thư viện `locketlam` được thiết kế theo hướng đối tượng (OOP) trực quan, lấy `LocketClient` làm trung tâm điều phối các phân hệ:

```text
locketlam/
├── LocketClient (Điểm vào chính)
│   ├── .device   -> DeviceProfile (Giả lập iPhone & headers Apple)
│   ├── .session  -> SessionManager (Quản lý token & tự động gia hạn)
│   ├── .user     -> UserModule (Hồ sơ, họ tên, ngày sinh, cài đặt)
│   ├── .moments  -> MomentsModule (Đăng ảnh/video, nén WebP, các kiểu note)
│   ├── .friends  -> FriendsModule (Kết bạn bằng username/UID, nhóm, chặn)
│   └── .chat     -> ChatModule (Nhắn tin & lắng nghe WebSocket realtime)
```

---

## 2. Giả Lập Thiết Bị & Phần Cứng iOS (`DeviceProfile`)

Mọi yêu cầu gửi tới máy chủ Locket và Firebase đều mang đầy đủ thông số định danh phần cứng của iPhone thật, ngăn chặn hoàn toàn việc bị server quét bot hoặc chặn App Check.

### Cơ Chế Chuyển Đổi: Tự Động (True) hoặc Tự Nhập Mã (False)
Bạn có thể dễ dàng chuyển đổi qua hàm `client.set_device(...)` hoặc khi khởi tạo `DeviceProfile(...)`:
- **`auto_emulate=True` (Mặc định)**: Thư viện tự động lựa chọn ngẫu nhiên các dòng iPhone thật và tự sinh mã `installation_id`, headers, User-Agent chuẩn chỉ.
- **`auto_emulate=False`**: Chuyển quyền kiểm soát cho người dùng tự nhập toàn bộ mã máy thật của mình (`installation_id`, `hardware_model`, `ios_version`, `custom_user_agent`,...).

```python
from locketlam import LocketClient

client = LocketClient()

# Cách 1: Dùng chế độ tự động của thư viện (True)
client.set_device(auto_emulate=True)

# Cách 2: Tự nhập mã thiết bị và phần cứng thật của bạn (False)
client.set_device(
    auto_emulate=False,
    installation_id="MA_THIET_BI_CUA_BAN_UUID",  # Mã cài đặt thiết bị
    hardware_model="iPhone16,2",                 # Model phần cứng (ví dụ: iPhone 15 Pro Max)
    ios_version="18.2.0",                       # Phiên bản iOS máy bạn
    app_version="2.69.0"                        # Phiên bản app Locket
)
```

### Các Dòng iPhone Được Giả Lập Sẵn (Khi bật `auto_emulate=True`)
- `iPhone 13 Pro` (`hw/iPhone14_2`, iOS `17.4.1`)
- `iPhone 13` (`hw/iPhone14_5`, iOS `17.5.1`)
- `iPhone 14 Pro` (`hw/iPhone15_2`, iOS `17.6.1`)
- `iPhone 14 Pro Max` (`hw/iPhone15_3`, iOS `18.0.1`)
- `iPhone 15 Pro` (`hw/iPhone16_1`, iOS `18.1.0`)

### Các Thuộc Tính & Phương Thức
| Thuộc tính / Phương thức | Kiểu dữ liệu | Mô tả chi tiết |
| :--- | :--- | :--- |
| `auto_emulate` | `bool` | `True` = Dùng mẫu có sẵn của thư viện; `False` = Dùng thông số bạn tự nhập. |
| `set_device(...)` | Phương thức | Chuyển đổi linh hoạt giữa chế độ tự động và tự nhập mã thiết bị. |
| `installation_id` | `str` | Mã định danh thiết bị cài đặt (UUID máy). |
| `bundle_id` | `str` | Mã định danh ứng dụng iOS: `com.locket.Locket`. |
| `user_agent` | `str` | Chuỗi User-Agent chuẩn iOS Apple (hoặc User-Agent bạn tự nhập). |
| `analytics_data` | `dict` | Khối dữ liệu Protobuf experiment flags và analytics gửi kèm mỗi request. |
| `default_headers` | `dict` | Header mặc định chứa `x-ios-bundle-identifier` và user-agent. |
| `to_dict()` | `dict` | Chuyển đổi thông tin thiết bị thành từ điển để lưu file JSON. |
| `from_dict(data)` | `classmethod`| Khôi phục cấu hình thiết bị từ dữ liệu đã lưu. |

---

## 3. Xác Thực & Quản Lý Phiên (`SessionManager`)

Chịu trách nhiệm bảo mật thông tin đăng nhập, lưu trữ token và tự động làm mới JWT token ngầm.

### Các Phương Thức
| Phương thức | Tham số | Giá trị trả về | Mô tả chi tiết |
| :--- | :--- | :--- | :--- |
| `client.login(email, password)` | `email: str`, `password: str` | `dict` | Đăng nhập tài khoản qua Google Firebase Identity Toolkit. |
| `client.is_authenticated()` | Không có | `bool` | Trả về `True` nếu client đã có phiên đăng nhập hợp lệ. |
| `client.session.get_valid_token()`| Không có | `str` | Trả về `idToken` còn hạn, **tự động refresh ngầm nếu token sắp hết hạn trước 60 giây**. |
| `client.session.refresh()` | Không có | Không có | Buộc cấp lại `idToken` mới ngay lập tức qua Secure Token API. |
| `client.session.save()` | Không có | Không có | Lưu phiên đăng nhập và thiết bị ra file `session.json`. |
| `client.session.load()` | Không có | `bool` | Đọc lại phiên đăng nhập từ file nếu tồn tại. |

---

## 4. Hồ Sơ Cá Nhân & Người Dùng (`client.user`)

Quản lý thông tin tài khoản của bạn và tra cứu người dùng khác trên hệ thống.

### Các Phương Thức
| Phương thức | Tham số | Mô tả chi tiết |
| :--- | :--- | :--- |
| `get_profile(user_uid=None)` | `user_uid: str` (tùy chọn) | Lấy thông tin cá nhân của chính mình (hoặc của user khác nếu truyền UID). |
| `get_profile_by_username(username)` | `username: str` | Tra cứu hồ sơ người dùng trực tiếp bằng Username trên Locket. |
| `update_name(first_name, last_name)`| `first_name: str`, `last_name: str` | Đổi họ và tên hiển thị trên Locket. |
| `update_birthdate(birthdate)` | `birthdate: str` (`YYYY-MM-DD`) | Đổi ngày sinh của tài khoản. |
| `update_avatar(image_or_url)` | Đường dẫn file ảnh, `bytes` hoặc `url` | **Đổi ảnh đại diện Avatar**. Hỗ trợ truyền thẳng file ảnh `.jpg`, `.png`, thư viện tự nén WebP và upload lên Firebase Storage. |
| `sync_client_data(...)` | `push_notifications: bool`, `auto_sync: bool`, `extra_data: dict` | Đồng bộ cài đặt ứng dụng. Hỗ trợ `auto_sync=True` (mặc định) hoặc `False` để tự nhập thông số tùy chỉnh. |
| `set_notification_token(fcm_token=None, auto_fake=True)` | `fcm_token: str`, `auto_fake: bool` | Đăng ký Push Token thông báo. **Mặc định `auto_fake=True`**: tự động fake token chuẩn Apple. Đặt `auto_fake=False`: cho phép người dùng tự nhập mã token thật của mình. |

---

## 5. Khoảnh Khắc & Xử Lý Media (`client.moments`)

Quản lý toàn diện quy trình tải lên ảnh/video và đăng khoảnh khắc lên feed bạn bè.

### Các Kiểu Note/Caption Hỗ Trợ (`NoteType`)
Locket phân tách rõ ràng giữa **2 dạng Note**:
1. **Dynamic Text Note**: Người dùng tự gõ chữ tùy ý trên nền mờ mặc định (`STANDARD`, `POLL`, `REVIEW`, `TIME`, `WEATHER`, `LOCATION`,...).
2. **Preset Pill / Badge Note (Nhãn màu cố định có sẵn của Locket & Remote Config)**: Chữ cố định, có biểu tượng icon riêng và **dải màu nền gradient đặc trưng (colors)**. Thư viện tích hợp đầy đủ **158+ nhãn màu chuẩn xác** từ cấu hình máy chủ Locket.

#### Danh Mục Các Nhãn Màu Cố Định Phổ Biến (`NoteType`):
- **Nhóm Đôi Lứa / Tình Cảm (`In Love 💘`)**:
  - `NoteType.DANG_BAN_TUONG_TU`: 💭 **Đang bận tương tư** (Màu: `#1A2980` -> `#26D0CE`)
  - `NoteType.DOI_ROI`: 😤 **Dỗi rồi** (Màu: `#FF5F6D` -> `#FFC371`)
  - `NoteType.REP_TIN_NHAN_DI`: 📩 **Rep tin nhắn đi** (Màu: `#F00000` -> `#DC281E`)
  - `NoteType.MO_HON_NHUNG_TAM_HIEN`: 🐤 **Mỏ hỗn nhưng tâm hiền** (Màu: `#FFB75E` -> `#ED8F03`)
  - `NoteType.MUON_DUOC_OM`: 🫂 **Muốn được ôm** (Màu: `#FF9A9E` -> `#FECFEF`)
  - `NoteType.HOI_BI_NHO`: 🤏 **Hơi bị nhớ** (Màu: `#A18CD1` -> `#FBC2EB`)
  - `NoteType.DANG_GHEN`: 🔥 **Đang ghen** (Màu: `#F00000` -> `#DC281E`)
  - `NoteType.NGU_NGON_GIAC_MO_CO_EM`: 🌌 **Ngủ ngon giấc mơ có em** (Màu: `#30CFD0` -> `#330867`)
- **Nhóm Gen Z & Trend TikTok**:
  - `NoteType.FLEX_DEN_HOI_THO_CUOI`: 💎 **Flex đến hơi thở cuối** (Màu: `#F7971E` -> `#FFD200`)
  - `NoteType.OVERTHINKING_VAI_CHUONG`: 🤯 **Overthinking vai chưởng** (Màu: `#2C3E50` -> `#4CA1AF`)
  - `NoteType.OACH_XA_LACH`: 🥬 **oách xà lách** (Màu: `#11998E` -> `#38EF7D`)
  - `NoteType.TRAM_CAM_NHE`: 🫠 **Trầm cảm nhẹ** (Màu: `#1F1C2C` -> `#928DAB`)
  - `NoteType.XIN_VINH_BIET_CU`: 🕯️ **Xin vĩnh biệt cụ** (Màu: `#232526` -> `#414345`)
  - `NoteType.CHAY_NGAY_DI`: 🏃💨 **Chạy ngay đi** (Màu: `#D31027` -> `#EA384D`)
  - `NoteType.CU_TU_TU_KHOAI_SE_NHU`: 🥔 **Cứ từ từ khoai sẽ nhừ** (Màu: `#56AB2F` -> `#A8E063`)
  - `NoteType.DOC_SO_TAI_KHOAN`: 💳 **đọc số tài khoản** (Màu: `#1E90FF` -> `#00D4FF`)
  - `NoteType.CON_CAI_NIT`: 🧶 **còn cái nịt** (Màu: `#D7CCC8` -> `#8D6E63`)
  - `NoteType.DEP_TRAI_CO_GI_SAI`: 😎 **Đẹp trai có gì sai** (Màu: `#F12711` -> `#F5AF19`)
  - `NoteType.DEADLINE_RUOT`: 🔥 **Deadline dí tụt quần** (Màu: `#ED213A` -> `#93291E`)
- **Nhóm Trang Trí Đời Sống (`Decorative`)**:
  - `NoteType.FEELING_CUTE`: 🌷 **Feeling Cute** (Màu: `#F8BBD0` -> `#E91E63`)
  - `NoteType.PARTY_TIME`: 🪩 **Party Time!** (Màu: `#5EFFF5` -> `#FCFF57`)
  - `NoteType.GOOD_MORNING`: ☀️ **Good morning** (Màu: `#EF7402` -> `#EABF0F`)
  - `NoteType.GOODNIGHT`: 🌙 **Goodnight** (Màu: `#370C6F` -> `#575CD4`)
  - `NoteType.OOTD`: 🕶 **OOTD** (Màu: `#FFFFFF` -> `#DBDBDB`)
  - `NoteType.MISS_YOU`: 🥰 **Miss you** (Màu: `#EC0C00` -> `#FF493F`)
  - `NoteType.COFFEE_TIME`: ☕ **Coffee Time!** (Màu: `#4E342E` -> `#8D6E63`)
  - `NoteType.MIXUE_TIME`: 🍦 **Mixue Time!** (Màu: `#FFF9C4` -> `#F8BBD0`)
- **Nhóm Sự Kiện Lễ Hội (`Holiday`)**:
  - `NoteType.HALLOWEEN_2026`: 🎃 **Halloween** (Màu: `#150804` -> `#C8540D`)
  - `NoteType.CHRISTMAS_EVE_2026`: 🕯️ **Giáng sinh an lành** (Màu: `#2FA85F` -> `#176B3A`)
  - `NoteType.CHRISTMAS_DAY_2026`: 🎄 **Giáng sinh an lành** (Màu: `#E53935` -> `#A81818`)
  - `NoteType.NEW_YEARS_EVE_2026`: 🥂 **Xin chào 2027!** (Màu: `#FFC64B` -> `#FFEDBF`)
  - `NoteType.NEW_YEARS_DAY_2027`: 💫 **Xin chào 2027!** (Màu: `#3B00EC` -> `#823FFF`)
- **Nhóm Chữ Tiêu Chuẩn (`Dynamic`)**:
  - `NoteType.STANDARD`: Ghi chú chữ người dùng tự gõ.
  - `NoteType.REVIEW`: Đánh giá sao.
  - `NoteType.MUSIC`: Ghi chú bài hát/âm nhạc.
  - `NoteType.LOCATION`: Ghi chú vị trí địa lý.
  - `NoteType.WEATHER`: Ghi chú thời tiết.
  - `NoteType.TIME`: Ghi chú mốc thời gian.
  - `NoteType.STREAK`: Biểu tượng đếm chuỗi ngày streak.
  - `NoteType.POLL`: Bình chọn/câu hỏi tương tác.
  - `NoteType.COLOR_PALETTE`: Bảng màu nghệ thuật.

> 💡 **Cơ chế hoạt động:**  
> Khi gọi `client.moments.post(...)`, thư viện hỗ trợ người dùng **tự do custom 100%**:
> 1. **Dùng nhãn mẫu có sẵn**: Truyền `note_type=NoteType.TEN_KIEU`, thư viện tự nạp bộ màu gradient và icon mẫu của Locket (vẫn cho phép tùy chỉnh chữ caption).
> 2. **Tự do custom màu & icon**: Truyền `colors=['#FF416C', '#8A2387']`, `text_color='#FFFFFF'`, `icon='🔥'`, `caption='Chữ tuỳ ý'`. Hệ thống sẽ tạo nhãn bo góc với dải màu gradient tự chọn hiển thị rực rỡ trên app bạn bè.
> 3. **Tự động tối ưu Video (Auto Optimize)**: Tự động phát hiện video vượt quá hoặc cận kề 6 MB, áp dụng chuẩn Apple H.265/HEVC giữ nguyên 100% độ phân giải Full HD/2K/4K, tự cân đối bitrate hình ảnh và âm thanh để đưa file về ngưỡng an toàn ~5.7 MB. Hỗ trợ video dài từ **15s đến 3-5 phút** mượt mà.

### Các Phương Thức
| Phương thức | Tham số | Mô tả chi tiết |
| :--- | :--- | :--- |
| `upload_image(file_or_bytes)` | Đường dẫn file hoặc `bytes` | Tự động chuyển đổi sang chuẩn `.webp`, trích xuất `downloadTokens` chuẩn từ Google Storage và upload qua Resumable Protocol. |
| `upload_video(file_or_bytes, auto_compress=True)` | Đường dẫn file hoặc `bytes` | Upload video `.mp4` lên Video Storage của Locket. Mặc định `auto_compress=True` tự động nén thông minh chuẩn H.265 nếu quá 6 MB. |
| `optimize_video(video_input, ...)` | Đường dẫn file hoặc `bytes` | Động cơ nén video thông minh: Giữ nguyên 100% độ phân giải (`preserve_resolution=True`), dồn băng thông cho hình ảnh và tự tối ưu âm thanh AAC. |
| `post(...)` | `image`, `caption`, `video`, `note_type`, `icon`, `colors`, `text_color`, `is_private`, `recipients` | **Đăng khoảnh khắc mới lên Locket**: Hỗ trợ đầy đủ ảnh, video dài kèm nhãn màu tùy biến 100% (`colors`, `text_color`, `icon`). Đặt `is_private=True` để đăng riêng tư chỉ mình xem. |
| `get_latest()` | Không có | Lấy danh sách feed khoảnh khắc mới nhất từ bạn bè. |
| `get_shared_moments_by_username(username, limit=None)` (hoặc `get_posts_by_username`) | `username: str`, `limit: int` | **Lấy toàn bộ hoặc N bài đăng khoảnh khắc (Moments) thực thụ từ một người dùng bằng Username trực tiếp từ Live Feed Locket. Trả về đúng đối tượng bài đăng gốc với đầy đủ metadata: `moment_uid`, `thumbnail_url`, `image_url`, `video_url`, `caption`, `overlays` (nhãn màu/icon/text), `date` và `md5`. Hoàn toàn loại bỏ tin nhắn chat.** |
| `get_shared_moments_by_user(user_uid, limit=None)` | `user_uid: str`, `limit: int` | Lấy danh sách bài đăng khoảnh khắc thực thụ theo User UID từ feed máy chủ Locket. |
| `get_all_my_moments()` | Không có | **Lấy toàn bộ bài đăng của chính tài khoản hiện tại (bot)**: trả về đầy đủ `moment_uid`, ảnh `thumbnail_url`, số lượt xem `views_count`, danh sách người xem `viewers` và danh sách cảm xúc icon đã thả `reactions`. |
| `get_views(moment_uid)` | `moment_uid: str` | **Xem số lượt xem, danh sách những ai đã xem và toàn bộ biểu cảm cảm xúc (icon emoji ❤️, 🔥,...) đã thả vào bài đăng (`getMomentViews`).** |
| `comment(moment_uid, receiver_uid, text)` | `moment_uid: str`, `receiver_uid: str`, `text: str` | **Bình luận vào bài đăng khoảnh khắc** (`sendChatMessageV2`). Bình luận sẽ tự động gắn liên kết vào bài đăng và nhảy thẳng vào đoạn chat giữa 2 người. |
| `react(moment_uid, reaction="❤️", from_memory=False)` | `moment_uid: str`, `reaction: str` | **Thả biểu cảm (emoji reaction) vào ảnh hoặc video khoảnh khắc của bạn bè** (`reactToMoment`). Thả bằng icon trực tiếp. |
| `get_filters()` | Không có | Lấy danh sách các bộ lọc máy ảnh khả dụng. |
| `mark_as_viewed(moment_uid)` | `moment_uid: str` | Đánh dấu một bài đăng khoảnh khắc là đã xem. |
| `get_rollcall_posts(week_of_year=None, year=None, source="banner")` | `week_of_year: int`, `year: int`, `source: str` | Lấy danh sách bài đăng sự kiện Rollcall hàng tuần (tự động tính tuần ISO hiện tại, tránh lỗi 502). |
| `delete(moment_uid)` | `moment_uid: str` | Xóa khoảnh khắc đã đăng trước đó. |

---

## 6. Bạn Bè, Nhóm & Quản Lý Chặn (`client.friends`)

Kiểm soát danh sách bạn bè, tương tác kết bạn, danh bạ và kiểm duyệt người dùng.

### Các Phương Thức
| Phương thức | Tham số | Mô tả chi tiết |
| :--- | :--- | :--- |
| `get_groups_and_friends()` | Không có | Lấy danh sách nhóm đang tham gia (`getGroupsState`). |
| `get_all_friends()` | Không có | **Lấy toàn bộ danh sách bạn bè kèm chi tiết hồ sơ cá nhân đầy đủ (UID, Tên, Username, Avatar).** |
| `resolve_invite_token_from_username(username)` | `username: str` | Phân giải link công khai `https://locket.cam/<username>` để lấy invite token thật của app iOS. |
| `fetch_user_by_invite_token(invite_token)` | `invite_token: str` | Tra cứu thông tin hồ sơ chi tiết từ mã invite token (kèm trạng thái kết bạn `friendship_status`). |
| `send_request(user_uid, source="inviteCardPopup")` | `user_uid: str`, `source: str` | Gửi lời mời kết bạn chuẩn cấu trúc gói tin iOS. |
| `send_request_by_username(username)`| `username: str` | **Tự động tìm kiếm, phân giải token và gửi kết bạn ngay lập tức chỉ với Username.** |
| `accept_request(user_uid)` | `user_uid: str` | Đồng ý lời mời kết bạn từ người khác. |
| `remove(user_uid)` | `user_uid: str` | Hủy kết bạn (xóa khỏi danh sách bạn bè). |
| `block(user_uid)` | `user_uid: str` | **Chặn người dùng (Hệ thống Locket sẽ tự động hủy kết bạn và đưa vào danh sách đen `blocked_users`).** |
| `unblock(user_uid)` | `user_uid: str` | Bỏ chặn người dùng đã chặn trước đó (xóa khỏi `blocked_users`). |
| `suggest_friends(phone_contacts)` | `phone_contacts: list` | Tìm kiếm và gợi ý bạn bè Locket dựa trên danh bạ số điện thoại (chuẩn E.164). |

---

## 7. Nhắn Tin Trực Tiếp & Real-Time WebSocket (`client.chat`)

Tương tác nhắn tin hai chiều qua HTTP POST và luồng stream sự kiện thời gian thực.

### Các Phương Thức
| Phương thức | Tham số | Mô tả chi tiết |
| :--- | :--- | :--- |
| `send_message(receiver_uid, text=None, moment_uid=None)` | `receiver_uid: str`, `text: str`, `moment_uid: str` | Gửi tin nhắn văn bản, emoji đơn, hoặc kèm bài đăng (khoảnh khắc) tới bạn bè (tự động đồng bộ lịch sử). |
| `send_moment(receiver_uid, moment_uid, text=None)` | `receiver_uid: str`, `moment_uid: str`, `text: str` | **Gửi / chia sẻ trực tiếp bài đăng khoảnh khắc vào phòng chat** (hỗ trợ cả bài của mình hoặc bài của bất kỳ bạn bè nào). **Nếu để trống `text=None`, thư viện sẽ tự động gửi bài đăng độc lập mà KHÔNG cần kèm chữ!** |
| `get_messages(other_user_id=None, conversation_id=None, fetch_server=True)` | `other_user_id: str`, `conversation_id: str`, `fetch_server: bool` | **Đồng bộ trực tiếp từ database Firestore máy chủ Locket**, lấy toàn bộ tin nhắn 2 chiều theo dòng thời gian chuẩn, kèm Document `message_id`, thông tin người gửi và các cảm xúc đã thả. |
| `get_conversations()` | Không có | **Lấy danh sách tất cả các cuộc hội thoại trong hộp thư đến (Inbox)**: bao gồm UID bạn bè, số tin chưa đọc (`unread_count`), trạng thái đã đọc (`is_read`), thời gian đối phương xem tin (`other_last_read_at`) và tin nhắn mới nhất. |
| `send_reaction(conversation_id, message_id, emoji, validate_receiver=True)` | `conversation_id: str`, `message_id: str`, `emoji: str` | **Thả biểu cảm (emoji reaction) vào tin nhắn của bạn bè** (`sendChatMessageReaction`). Hỗ trợ bất kỳ icon đơn hoặc combo nhiều icon (`"❤️"`, `"🔥🥰"`, `"❤️❤️❤️❤️❤️"`). Tự động ngăn chặn việc thả nhầm vào tin của chính mình. |
| `remove_reaction(conversation_id, message_id)` | `conversation_id: str`, `message_id: str` | **Gỡ bỏ / hủy thả cảm xúc** khỏi tin nhắn (`removeChatMessageReaction`). |
| `delete_message(conversation_uid, message_uid, validate_ownership=True)` | `conversation_uid: str`, `message_uid: str` | **Thu hồi / xóa tin nhắn đã gửi** (`deleteChatMessage`). Tự động kiểm tra quyền sở hữu để đảm bảo chỉ thu hồi tin nhắn do chính bạn gửi. |
| `mark_as_read(conversation_uid=None, other_user_id=None, send_read_receipt=True)` | `conversation_uid: str`, `other_user_id: str`, `send_read_receipt: bool` | Đánh dấu cuộc trò chuyện là đã đọc. Hỗ trợ **`send_read_receipt=False` (chế độ ẩn danh / không gửi đã xem)** giúp xem tin nhắn mà không báo cho đối phương biết mình đã đọc. |
| `listen_realtime(other_user_id, callback)` | `other_user_id: str`, `callback: callable` | Kết nối trực tiếp vào `wss://api.locketcamera.com/wss_v2/chat` để nhận tin nhắn và sự kiện thời gian thực. |

---

## 8. Hệ Thống Lỗi & Ngoại Lệ (Exceptions)

```text
LocketError (Lớp lỗi gốc của toàn thư viện)
├── AuthenticationError     (Lỗi đăng nhập, mật khẩu sai, token hết hạn, bị chặn)
├── StorageUploadError       (Lỗi khi tải dữ liệu ảnh/video lên Firebase Cloud Storage)
└── LocketAPIError           (Lỗi trả về từ máy chủ Locket kèm mã HTTP Status)
```

## 9. Hướng Dẫn Đóng Gói & Phát Hành (Publishing Guide)

Dành cho các nhà phát triển muốn đóng gói hoặc tự triển khai bản phân phối riêng:

### 9.1. Cài đặt công cụ đóng gói
```bash
pip install --upgrade build twine
```

### 9.2. Quy trình Build & Kiểm tra
```bash
# 1. Dọn dẹp bản build cũ và tạo gói phân phối
python -m build

# 2. Kiểm tra tính hợp lệ của gói
python -m twine check dist/*
```

### 9.3. Xuất bản lên PyPI
```bash
# Đẩy gói phân phối trong thư mục dist/ lên kho lưu trữ PyPI chính thức
python -m twine upload dist/*
```

---

## 📜 Bản Quyền & Giấy Phép

Bản quyền © 2026 **LAMDev x DaLyMMO.com**. Tất cả các quyền được bảo lưu.

Phát hành theo giấy phép mã nguồn mở [MIT License](../LICENSE).

