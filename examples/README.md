# 📚 Danh Mục Mã Nguồn Ví Dụ Tham Khảo (LocketLam Examples)

| Hướng Dẫn Tích Hợp | Danh Mục API | Trang Chủ Repo |
|:---|:---|:---|
| 🇬🇧 [docs/INTEGRATION.md](../docs/INTEGRATION.md) | 🇬🇧 [docs/FEATURES.md](../docs/FEATURES.md) | 🇬🇧 [README.md](../README.md) |
| 🇻🇳 [docs/INTEGRATION_VI.md](../docs/INTEGRATION_VI.md) | 🇻🇳 [docs/FEATURES_VI.md](../docs/FEATURES_VI.md) | 🇻🇳 [README_VI.md](../README_VI.md) |

---

Thư viện hỗ trợ 2 bộ ví dụ song ngữ độc lập tương đương:
- 🇻🇳 **[`examples/vi/`](./vi/)**: Bộ ví dụ & Menu CLI Full Tiếng Việt.
- 🇬🇧 **[`examples/en/`](./en/)**: Bộ ví dụ & Menu CLI Full Tiếng Anh (English).

---

## 🇻🇳 Phiên Bản Tiếng Việt (`examples/vi/`)

| STT | File ví dụ | Nội dung & Tính năng |
| :---: | :--- | :--- |
| **01** | [`vi/01_login_and_session.py`](./vi/01_login_and_session.py) | **Đăng nhập & Phiên**: Giả lập máy iOS (`set_device`), tự gia hạn token ngầm, lưu `locketlam_session.json`. |
| **02** | [`vi/02_user_profile.py`](./vi/02_user_profile.py) | **Hồ sơ cá nhân**: Xem thông tin, tìm qua Username, đổi họ tên, ngày sinh, avatar (WebP) và đồng bộ Apple APNs token. |
| **03** | [`vi/03_post_image_moment.py`](./vi/03_post_image_moment.py) | **Đăng ảnh**: 158+ nhãn `NoteType`, tùy biến gradient hex + emoji, đăng công khai/chọn bạn bè/riêng tư. |
| **04** | [`vi/04_post_video_moment.py`](./vi/04_post_video_moment.py) | **Đăng video & Nén HEVC**: Đăng video MP4, tự trích thumbnail, tự nén Apple H.265 khi file $\ge$ 6 MB. |
| **05** | [`vi/05_feed_views_reactions.py`](./vi/05_feed_views_reactions.py) | **Feed & Tương tác**: Lấy feed, xem ai đã xem (`get_views`), thả biểu cảm emoji ❤️ và bình luận. |
| **06** | [`vi/06_friends_and_contacts.py`](./vi/06_friends_and_contacts.py) | **Bạn bè**: Kết bạn qua link/username (`locket.cam/<user>`), chấp nhận kết bạn, hủy và chặn/bỏ chặn. |
| **07** | [`vi/07_chat_and_reactions.py`](./vi/07_chat_and_reactions.py) | **Nhắn tin**: Đồng bộ Firestore, gửi tin nhắn, share khoảnh khắc, thả tim tin nhắn, xem ẩn danh. |
| **CLI**| [`vi/interactive_demo.py`](./vi/interactive_demo.py) | **Menu CLI Tương tác**: Ứng dụng dòng lệnh giao diện 100% Tiếng Việt chọn số trực tiếp. |

---

## 🇬🇧 English Version (`examples/en/`)

| No. | Example Script | Description & Features |
| :---: | :--- | :--- |
| **01** | [`en/01_login_and_session.py`](./en/01_login_and_session.py) | **Auth & Session**: iOS device profile, background token auto-refresh, `locketlam_session.json` persistence. |
| **02** | [`en/02_user_profile.py`](./en/02_user_profile.py) | **User Profile**: Fetch profile, lookup by username, update name/birthdate/avatar and APNs push token sync. |
| **03** | [`en/03_post_image_moment.py`](./en/03_post_image_moment.py) | **Post Photo**: 158+ `NoteType` presets, 100% custom gradient & emoji overlays, public/private moments. |
| **04** | [`en/04_post_video_moment.py`](./en/04_post_video_moment.py) | **Post Video & HEVC**: Upload MP4, auto-extract thumbnail, auto-compress H.265 if size $\ge$ 6 MB. |
| **05** | [`en/05_feed_views_reactions.py`](./en/05_feed_views_reactions.py) | **Feed & Engagement**: Latest feed, viewer inspection (`get_views`), emoji reactions, comments. |
| **06** | [`en/06_friends_and_contacts.py`](./en/06_friends_and_contacts.py) | **Friends & Contacts**: Send requests by username, accept invites, remove & block/unblock. |
| **07** | [`en/07_chat_and_reactions.py`](./en/07_chat_and_reactions.py) | **Chat & Messaging**: Firestore sync, direct messages, share moments into chat, incognito read receipts. |
| **CLI**| [`en/interactive_demo.py`](./en/interactive_demo.py) | **Interactive CLI Demo**: Terminal menu-driven showcase in 100% English. |

---

### 🚀 Cách chạy / How to run:

```bash
# Tiếng Việt
python examples/vi/01_login_and_session.py
python examples/vi/interactive_demo.py

# English
python examples/en/01_login_and_session.py
python examples/en/interactive_demo.py
```
