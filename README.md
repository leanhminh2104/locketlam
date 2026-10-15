# 🚀 LocketLam - The Ultimate Python SDK for Locket Camera

<p align="center">
  <img src="https://raw.githubusercontent.com/leanhminh2104/locketlam/main/assets/banner.PNG" alt="LocketLam Banner" width="700" onerror="this.style.display='none'"/>
</p>

<p align="center">
  <b>A production-ready, feature-complete Python client library for Locket Camera with authentic iOS hardware simulation.</b>
</p>

<p align="center">
  <a href="https://pypi.org/project/locketlam/"><img src="https://img.shields.io/pypi/v/locketlam.svg?style=flat-square&color=blue" alt="PyPI Version"></a>
  <a href="https://pypi.org/project/locketlam/"><img src="https://img.shields.io/pypi/pyversions/locketlam.svg?style=flat-square" alt="Python Versions"></a>
  <a href="https://github.com/leanhminh2104/locketlam/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="License MIT"></a>
  <a href="https://pepy.tech/project/locketlam"><img src="https://img.shields.io/pypi/dm/locketlam.svg?style=flat-square" alt="Downloads"></a>
  <a href="https://github.com/leanhminh2104/locketlam/blob/main/README_VI.md"><img src="https://img.shields.io/badge/Language-Vietnamese-red.svg?style=flat-square" alt="Vietnamese Docs"></a>
</p>

---

## 🗃️ Documentation Map

> **You are here: README** — the front page. Read this to understand what the library does and whether it suits your needs.

| If you want to... | Go to |
|:---|:---|
| 🚀 **Install & run your first snippet** | You're in the right place — see [Quick Start](#-quick-start) below |
| 🛠️ **Integrate into your project step by step** | ➡️ [INTEGRATION.md](https://github.com/leanhminh2104/locketlam/blob/main/docs/INTEGRATION.md) (EN) · [INTEGRATION_VI.md](https://github.com/leanhminh2104/locketlam/blob/main/docs/INTEGRATION_VI.md) (VI) |
| 📚 **Look up a specific method / parameter** | ➡️ [FEATURES.md](https://github.com/leanhminh2104/locketlam/blob/main/docs/FEATURES.md) (EN) · [FEATURES_VI.md](https://github.com/leanhminh2104/locketlam/blob/main/docs/FEATURES_VI.md) (VI) |
| 💡 **Copy-paste complete working scripts** | ➡️ [examples/en/](https://github.com/leanhminh2104/locketlam/tree/main/examples/en/) (EN) · [examples/vi/](https://github.com/leanhminh2104/locketlam/tree/main/examples/vi/) (VI) |
| 🇬🇧 **Read this page in Vietnamese** | ➡️ [README_VI.md](https://github.com/leanhminh2104/locketlam/blob/main/README_VI.md) |

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Comprehensive API Reference](#-comprehensive-api-reference)
  - [1. Authentication & Session Management](#1-authentication--session-management)
  - [2. User Profile Management](#2-user-profile-management)
  - [3. Moments (Feed & Uploads)](#3-moments-feed--uploads)
  - [4. Friends, Groups & Blocking](#4-friends-groups--blocking)
  - [5. Chat & Real-Time WebSockets](#5-chat--real-time-websockets)
  - [6. Device Profile Customization](#6-device-profile-customization)
  - [7. Error Handling](#7-error-handling)
- [Examples](#-examples)
- [Contributing](#-contributing)
- [Support & Donations (Sponsor)](#-support--donations-sponsor)
- [Copyright & License](#-copyright--license)
- [Disclaimer](#-disclaimer)

---

## 🌟 Overview

**`locketlam`** is a reverse-engineered Python SDK designed to provide direct programmatic access to the Locket Camera backend. It allows developers, bot creators, and automation engineers to interact seamlessly with Locket accounts using pure Python, without needing an iOS device running.

---

## ✨ Key Features

- 📱 **100% Authentic iOS Hardware Emulation**: Sends real iPhone hardware identifiers (iPhone 13 Pro through iPhone 15 Pro Max), bundle IDs (`com.locket.Locket`), Firebase GMPIDs, and Google Protobuf analytics flags to ensure requests are never blocked or flagged.
- 🔄 **Autonomous Token Renewal**: Automatic background Firebase JWT `idToken` refreshing whenever a token is near expiry.
- 🖼️ **Smart Media Pipeline**: Built-in Pillow conversion automatically transforms `.jpg`, `.png`, and other standard formats into Locket-optimized `.webp` format, uploaded via Google Cloud Storage Resumable protocol.
- ⚡ **Real-Time WebSocket Support**: Asynchronous live event listener for direct chat messages via `wss://api.locketcamera.com/wss_v2/chat`.
- 🛡️ **Defensive Architecture**: Strongly-typed exceptions (`AuthenticationError`, `StorageUploadError`, `LocketAPIError`) for robust error handling.

---

## 📦 Installation

Install the library directly from PyPI:

```bash
pip install locketlam
```

Or install with development dependencies:

```bash
pip install locketlam[dev]
```

To install from source in editable mode:

```bash
git clone https://github.com/leanhminh2104/locketlam.git
cd locketlam
pip install -e .
```

---

## ⚡ Quick Start

```python
from locketlam import LocketClient

# 1. Initialize client (auto-loads locketlam_session.json if available)
client = LocketClient(session_path="locketlam_session.json")

# 2. Authenticate if first time
if not client.is_authenticated():
    client.login("your_email@gmail.com", "your_password")
    print("Logged in successfully! User UID:", client.session.uid)

# 3. Fetch profile
profile = client.user.get_profile()
print(f"Welcome, {profile.get('first_name')} {profile.get('last_name')} (@{profile.get('username')})")

# 4. Post a moment photo
moment = client.moments.post(
    image="daily_snapshot.jpg",
    caption="Captured with locketlam! ✨",
    is_private=False
)
print("Moment posted successfully! ID:", moment.get("canonical_uid"))
```

---

## 📚 Comprehensive API Reference

### 1. Authentication & Session Management

The `SessionManager` handles credentials, refresh tokens, and JWT tokens securely.

```python
from locketlam import LocketClient

client = LocketClient(session_path="session.json")

# Login with email and password
session_data = client.login("email@example.com", "password")

# Check authentication state
if client.is_authenticated():
    print("User UID:", client.session.uid)
    print("Access Token:", client.session.id_token[:20] + "...")

# Force manual token refresh
client.session.refresh()
```

---

### 2. User Profile Management

Access via `client.user`:

```python
# 1. Get profile (self or another user by UID)
my_profile = client.user.get_profile()
other_profile = client.user.get_profile(user_uid="TARGET_USER_UID")

# 2. Update display name
client.user.update_name(first_name="Lam", last_name="Dev")

# 3. Update birthdate (format: YYYY-MM-DD)
client.user.update_birthdate("2006-04-21")

# 4. Update avatar picture
client.user.update_avatar("https://firebasestorage.googleapis.com/...")

# 5. Sync client data (push notifications, app version)
client.user.sync_client_data(push_notifications=True)
```

---

### 3. Moments (Feed & Uploads)

Access via `client.moments`:

```python
from locketlam import NoteType

# 1. Post a photo moment with rich gradient badge pill (Supports 158+ presets!)
photo_moment = client.moments.post(
    image="photo.jpg",                          # File path, bytes, or Storage URL
    note_type=NoteType.FLEX_DEN_HOI_THO_CUOI,  # Preset pill badge (custom gradient)
    is_private=False,                          # True = sent only to self (sent_to_self_only)
    recipients=None                            # Specific friends (or None for all)
)

# 2. Post with custom caption, custom gradient colors and custom emoji
custom_moment = client.moments.post(
    image="photo.jpg",
    caption="Coding with AI",
    icon="⚡",
    colors=["#FF416C", "#8A2387"],
    is_private=False
)

# 3. Post a video moment (Supports auto-compression HEVC < 6 MB, 15s to 5-10 mins)
video_moment = client.moments.post(
    image="thumb.jpg",                          # Video thumbnail image
    video="clip_10s.mp4",                       # Video file path, bytes, or Storage URL
    note_type=NoteType.MUSIC                    # Dynamic music overlay
)

# 4. Retrieve actual shared moments by Username (e.g. latest moments of a friend)
friend_moments = client.moments.get_posts_by_username("friend_username", limit=10)
for m in friend_moments:
    print(m["moment_uid"], m["thumbnail_url"], m["caption"])

# 5. React to a friend's moment with emoji
client.moments.react(moment_uid="MOMENT_ID", reaction="❤️")

# 6. Fetch moment view count and viewer list
views = client.moments.get_views(moment_uid="MOMENT_ID")
print("Views count:", views.get("count"))
print("Viewers:", views.get("moment_views"))

# 7. Comment on a moment (attaches to moment and appears in direct chat)
client.moments.comment(
    moment_uid="MOMENT_ID",
    receiver_uid="FRIEND_UID",
    text="Great shot!"
)

# 7. Mark moment as viewed
client.moments.mark_as_viewed(moment_uid="MOMENT_ID")

# 8. Fetch weekly Rollcall event posts
rollcall = client.moments.get_rollcall_posts()
print("Rollcall posts:", rollcall.get("posts", []))

# 9. Fetch latest feed from friends
feed = client.moments.get_latest()
for post in feed:
    print(post.get("user"), post.get("caption"), post.get("thumbnail_url"))

# 10. Delete a moment
client.moments.delete(moment_uid="MOMENT_CANONICAL_UID")
```

---

### 4. Friends, Groups & Blocking

Access via `client.friends`:

```python
# 1. Retrieve all friends with full profile details (UID, Names, Username, Avatar)
friends = client.friends.get_all_friends()
for f in friends:
    print(f"Friend: {f.get('first_name')} (@{f.get('username')}) - UID: {f.get('uid')}")

# 2. Retrieve groups state
groups_state = client.friends.get_groups_and_friends()

# 3. Resolve invite token from public profile link (https://locket.cam/<username>)
token = client.friends.resolve_invite_token_from_username("friend_username")
print("Invite Token:", token)

# 4. Fetch user details from invite token
user_info = client.friends.fetch_user_by_invite_token(token)
print("User info:", user_info)

# 5. Send friend request by username or UID
client.friends.send_request_by_username("friend_username")
# Or: client.friends.send_request(user_uid="TARGET_USER_UID")

# 6. Accept incoming friend request
client.friends.accept_request(user_uid="TARGET_USER_UID")

# 7. Remove (unfriend), Block & Unblock
client.friends.remove(user_uid="TARGET_USER_UID")
client.friends.block(user_uid="TARGET_USER_UID")   # Blocks user & automatically unfriends them on Locket
client.friends.unblock(user_uid="TARGET_USER_UID") # Unblocks user (removes from blocked_users)
```

---

### 5. Chat & Real-Time WebSockets

Access via `client.chat`:

```python
# 1. Send direct message or emoji
client.chat.send_message(
    receiver_uid="FRIEND_UID",
    text="Hey, check out this moment! ❤️"
)

# 2. Share a moment into chat (standalone or with text)
# a) Send standalone moment:
client.chat.send_moment(
    receiver_uid="FRIEND_UID",
    moment_uid="MOMENT_UID"  # Your moment UID or a friend's moment UID
)

# b) Send moment with accompanying text message:
client.chat.send_moment(
    receiver_uid="FRIEND_UID",
    moment_uid="MOMENT_UID",
    text="Check out this awesome moment!"
)

# 3. Get inbox conversations list
conversations = client.chat.get_conversations()

# 4. Retrieve live chronological messages from server
messages = client.chat.get_messages(other_user_id="FRIEND_UID")

# 4. React with single or multi-emoji combo to a message
client.chat.send_reaction(conversation_id="CONV_ID", message_id="MSG_ID", emoji="❤️")
client.chat.send_reaction(conversation_id="CONV_ID", message_id="MSG_ID", emoji="🔥🥰")

# 5. Remove / unreact an emoji reaction
client.chat.remove_reaction(conversation_id="CONV_ID", message_id="MSG_ID")

# 6. Recall / unsend your own message
client.chat.delete_message(conversation_uid="CONV_ID", message_uid="MSG_ID")

# 7. Mark conversation as read (send_read_receipt=False for Ghost / Incognito mode)
client.chat.mark_as_read(conversation_uid="CONV_ID", send_read_receipt=True)
client.chat.mark_as_read(conversation_uid="CONV_ID", send_read_receipt=False)

# 8. Listen to live incoming messages over WebSocket
import asyncio

async def on_new_message(msg):
    print("New incoming message:", msg)

# Start event loop
asyncio.run(client.chat.listen_realtime("FRIEND_UID", on_new_message))
```

---

### 6. Device Profile Customization

By default, `locketlam` picks a realistic iPhone profile. You can also specify custom hardware attributes:

```python
from locketlam import LocketClient, DeviceProfile

custom_device = DeviceProfile(
    model_info={
        "model": "iPhone16,1",
        "name": "iPhone 15 Pro",
        "hw": "hw/iPhone16_1",
        "ios": "18.1.0"
    },
    app_version="2.68.0",
    build_number="2523"
)

client = LocketClient(session_path="session.json", device=custom_device)
print("Emulating:", client.device.user_agent)
```

---

### 7. Error Handling

All custom exceptions inherit from `LocketError`:

```python
from locketlam.exceptions import (
    LocketError,
    AuthenticationError,
    LocketAPIError,
    StorageUploadError
)

try:
    client.login("user@email.com", "wrong_password")
except AuthenticationError as e:
    print("Auth Failed:", e)
except StorageUploadError as e:
    print("Media Upload Failed:", e)
except LocketAPIError as e:
    print(f"API Error (Status {e.status_code}):", e)
except LocketError as e:
    print("General Locket Error:", e)
```

---

## 💡 Examples

The [`examples/`](https://github.com/leanhminh2104/locketlam/tree/main/examples/) directory contains complete, runnable scripts for every feature:

| Feature | Script |
|:---|:---|
| Login & Session | [`examples/en/01_login_and_session.py`](https://github.com/leanhminh2104/locketlam/blob/main/examples/en/01_login_and_session.py) |
| User Profile | [`examples/en/02_user_profile.py`](https://github.com/leanhminh2104/locketlam/blob/main/examples/en/02_user_profile.py) |
| Post Photo & NoteType | [`examples/en/03_post_image_moment.py`](https://github.com/leanhminh2104/locketlam/blob/main/examples/en/03_post_image_moment.py) |
| Post Video & HEVC | [`examples/en/04_post_video_moment.py`](https://github.com/leanhminh2104/locketlam/blob/main/examples/en/04_post_video_moment.py) |
| Feed & Reactions | [`examples/en/05_feed_views_reactions.py`](https://github.com/leanhminh2104/locketlam/blob/main/examples/en/05_feed_views_reactions.py) |
| Friends & Contacts | [`examples/en/06_friends_and_contacts.py`](https://github.com/leanhminh2104/locketlam/blob/main/examples/en/06_friends_and_contacts.py) |
| Chat & Real-Time | [`examples/en/07_chat_and_reactions.py`](https://github.com/leanhminh2104/locketlam/blob/main/examples/en/07_chat_and_reactions.py) |
| Interactive CLI | [`examples/en/interactive_demo.py`](https://github.com/leanhminh2104/locketlam/blob/main/examples/en/interactive_demo.py) |

```bash
python examples/en/interactive_demo.py
```

> 📖 For a full step-by-step integration guide, see [`docs/INTEGRATION.md`](https://github.com/leanhminh2104/locketlam/blob/main/docs/INTEGRATION.md).
> 📋 For the complete API catalog, see [`docs/FEATURES.md`](https://github.com/leanhminh2104/locketlam/blob/main/docs/FEATURES.md).

---

## 📚 Next Steps

| Document | Description |
|:---|:---|
| [📘 docs/INTEGRATION.md](https://github.com/leanhminh2104/locketlam/blob/main/docs/INTEGRATION.md) | Step-by-step integration guide with real code snippets for every feature (EN - Primary) |
| [📘 docs/INTEGRATION_VI.md](https://github.com/leanhminh2104/locketlam/blob/main/docs/INTEGRATION_VI.md) | Step-by-step integration guide in Vietnamese (VI - Secondary) |
| [📋 docs/FEATURES.md](https://github.com/leanhminh2104/locketlam/blob/main/docs/FEATURES.md) | Full API catalog — all classes, methods and parameters (EN) |
| [📋 docs/FEATURES_VI.md](https://github.com/leanhminh2104/locketlam/blob/main/docs/FEATURES_VI.md) | Full API catalog in Vietnamese (VI) |
| [💡 examples/en/](https://github.com/leanhminh2104/locketlam/tree/main/examples/en/) | 8 complete runnable example scripts (English) |
| [💡 examples/vi/](https://github.com/leanhminh2104/locketlam/tree/main/examples/vi/) | 8 complete runnable example scripts (Vietnamese) |

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome!

1. Fork the Project.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the Branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 💖 Support & Donations (Sponsor)

If you find **`locketlam`** helpful in your projects, automations, or research, please consider supporting the development. Your contribution helps maintain the library, reverse-engineer future Locket updates, and keep the project active!

<div align="center">

| Gateway / Method | Payment Details |
| :--- | :--- |
| 🌐 **Official Donation Portal** | [https://leanhminh.io.vn/donate](https://leanhminh.io.vn/donate) |
| 🏦 **MB Bank (Vietnam Banking)** | Account Number: `2104200637`<br>Account Holder: **LE VAN ANH MINH** |
| 🏦 **ACB Bank (Asia Commercial Bank)** | Account Number: `22002921`<br>Account Holder: **LE VAN ANH MINH** |
| 🟡 **Binance (UID / Pay ID)** | `283319011` |
| 💳 **PayPal (Global)** | [paypal.me/leanhminh2104](https://paypal.me/leanhminh2104) |

</div>

> *Every contribution, no matter how small, is deeply appreciated. Thank you very much! ❤️*

---

## 📜 Copyright & License

Copyright © 2026 **LAMDev x DaLyMMO.com**.

Distributed under the **MIT License**. See [`LICENSE`](https://github.com/leanhminh2104/locketlam/blob/main/LICENSE) for more information.

---

## ⚠️ Disclaimer

This library is an unofficial, reverse-engineered project created for educational and developer interoperability purposes. It is **not** endorsed by, associated with, or affiliated with Locket Camera, Inc. Please use this tool responsibly and respect Locket Camera's terms of service and community guidelines.
