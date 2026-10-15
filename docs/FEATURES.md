# 📋 LocketLam — Full API Catalog

> **What is this file for?**
> This is the **API reference** — a complete catalog of every class, method, parameter and return type in locketlam. Read this file when you need to **look up a specific method name, what parameters it takes, or what it returns**.

| If you want to... | Go to |
|:---|:---|
| 🚀 **Introduction, install & quick start** | ➡️ [README.md](../README.md) (EN) · [README_VI.md](../README_VI.md) (VI) |
| 🛠️ **Step-by-step integration code examples** | ➡️ [INTEGRATION.md](INTEGRATION.md) (EN) · [INTEGRATION_VI.md](INTEGRATION_VI.md) (VI) |
| 💡 **Complete runnable scripts** | ➡️ [examples/en/](../examples/en/) (EN) · [examples/vi/](../examples/vi/) (VI) |
| 🇻🇳 **Vietnamese version of this catalog** | ➡️ [FEATURES_VI.md](FEATURES_VI.md) |

> **Version**: 1.0.1 · **Package**: [locketlam](https://pypi.org/project/locketlam/) · **Author**: LAMDev x DaLyMMO.com · **License**: MIT

---


## 📑 Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Hardware & Device Fingerprint Emulation (`DeviceProfile`)](#2-hardware--device-fingerprint-emulation-deviceprofile)
3. [Authentication & Session Engine (`SessionManager`)](#3-authentication--session-engine-sessionmanager)
4. [User Profile Module (`client.user`)](#4-user-profile-module-clientuser)
5. [Moments & Media Pipeline (`client.moments`)](#5-moments--media-pipeline-clientmoments)
6. [Friends, Groups & Moderation (`client.friends`)](#6-friends-groups--moderation-clientfriends)
7. [Direct Messaging & Real-Time WebSockets (`client.chat`)](#7-direct-messaging--real-time-websockets-clientchat)
8. [Exception Hierarchy](#8-exception-hierarchy)
9. [Packaging & Publishing Guide](#9-packaging--publishing-guide)
10. [Copyright & License](#-copyright--license)

---

## 1. Architecture Overview

The `locketlam` library is organized in a modular, client-centric design:

```
locketlam/
├── LocketClient (Entry Point)
│   ├── .device   -> DeviceProfile (iOS emulation & headers)
│   ├── .session  -> SessionManager (Tokens & auto-refresh)
│   ├── .user     -> UserModule (Profile & account settings)
│   ├── .moments  -> MomentsModule (Photos, videos & notes)
│   ├── .friends  -> FriendsModule (Friends, groups, lookup)
│   └── .chat     -> ChatModule (Direct messages & WebSockets)
```

---

## 2. Hardware & Device Fingerprint Emulation (`DeviceProfile`)

Ensures all outgoing HTTP and WebSocket connections emulate an authentic iPhone device, avoiding bot detection and App Check blocks.

### Emulation Toggle: Automatic (True) vs. User-Provided (False)
You can seamlessly switch modes using `client.set_device(...)` or when instantiating `DeviceProfile(...)`:
- **`auto_emulate=True` (Default)**: The library automatically picks a realistic iPhone model and generates all required identifiers (`installation_id`, User-Agent, experiments).
- **`auto_emulate=False`**: Gives full control to the user to inject their exact physical iPhone credentials (`installation_id`, `hardware_model`, `ios_version`, `custom_user_agent`, etc.).

```python
from locketlam import LocketClient

client = LocketClient()

# Mode 1: Automatic realistic emulation (True)
client.set_device(auto_emulate=True)

# Mode 2: User custom hardware credentials (False)
client.set_device(
    auto_emulate=False,
    installation_id="YOUR_CUSTOM_UUID",       # Physical device installation ID
    hardware_model="iPhone16,2",              # e.g., iPhone 15 Pro Max
    ios_version="18.2.0",                     # iOS firmware version
    app_version="2.69.0"                      # Locket client version
)
```

### Supported Preset Models (when `auto_emulate=True`)
- `iPhone 13 Pro` (`hw/iPhone14_2`, iOS `17.4.1`)
- `iPhone 13` (`hw/iPhone14_5`, iOS `17.5.1`)
- `iPhone 14 Pro` (`hw/iPhone15_2`, iOS `17.6.1`)
- `iPhone 14 Pro Max` (`hw/iPhone15_3`, iOS `18.0.1`)
- `iPhone 15 Pro` (`hw/iPhone16_1`, iOS `18.1.0`)

### Attributes & Methods
| Property / Method | Type | Description |
| :--- | :--- | :--- |
| `auto_emulate` | `bool` | `True` for library presets; `False` for custom user input. |
| `set_device(...)` | Method | Configures or updates device emulation parameters. |
| `installation_id` | `str` | Persistent installation UUID per session. |
| `bundle_id` | `str` | Bundle identifier: `com.locket.Locket`. |
| `user_agent` | `str` | Formatted iOS user agent string (or custom user-agent). |
| `analytics_data` | `dict` | Google Protobuf experiment flags and client metadata. |
| `default_headers` | `dict` | Headers containing `x-ios-bundle-identifier` and user agent. |
| `to_dict()` | `dict` | Serializes profile for session storage. |
| `from_dict(data)` | `classmethod`| Reconstructs profile from stored dictionary. |

---

## 3. Authentication & Session Engine (`SessionManager`)

Manages Firebase JWT credentials, refresh tokens, and persistence.

### Methods
| Method | Parameters | Returns | Description |
| :--- | :--- | :--- | :--- |
| `client.login(email, password)` | `email: str`, `password: str` | `dict` | Authenticates with Firebase and saves session. |
| `client.is_authenticated()` | None | `bool` | Returns `True` if active tokens exist. |
| `client.session.get_valid_token()`| None | `str` | Returns a valid `idToken`, **auto-refreshing in background** if near expiration. |
| `client.session.refresh()` | None | None | Manually forces token renewal via Secure Token API. |
| `client.session.save()` | None | None | Persists session to JSON file. |
| `client.session.load()` | None | `bool` | Loads session from disk if present. |

---

## 4. User Profile Module (`client.user`)

Handles user profile details, name modifications, and settings synchronization.

### Methods
| Method | Parameters | Description |
| :--- | :--- | :--- |
| `get_profile(user_uid=None)` | `user_uid: str` (optional) | Retrieves profile of current user or target UID. |
| `get_profile_by_username(username)` | `username: str` | Looks up public user profile directly by Locket username. |
| `update_name(first_name, last_name)`| `first_name: str`, `last_name: str` | Changes display name on Locket. |
| `update_birthdate(birthdate)` | `birthdate: str` (`YYYY-MM-DD`) | Updates account birthdate. |
| `update_avatar(image_url)` | `image_url: str` | Sets new profile picture from Firebase Storage URL. |
| `sync_client_data(...)` | `push_notifications: bool`, `extra_data: dict` | Syncs app configuration and push notification preferences. |
| `set_notification_token(fcm_token)` | `fcm_token: str` | Registers Firebase Cloud Messaging (FCM) device token. |

---

## 5. Moments & Media Pipeline (`client.moments`)

Manages capturing, compressing, and posting photos and videos to the Locket feed.

### Supported Note Overlay Types (`NoteType`)
- **General & Functional (`NoteType`)**:
  - `NoteType.STANDARD`: Default text overlay.
  - `NoteType.REVIEW`: Rating and review badge.
  - `NoteType.MUSIC`: Song caption badge.
  - `NoteType.LOCATION`: Geolocation tag.
  - `NoteType.WEATHER`: Live weather tag.
  - `NoteType.TIME`: Timestamp overlay.
  - `NoteType.STREAK`: Streak count badge.
  - `NoteType.POLL`: Interactive question.
  - `NoteType.COLOR_PALETTE`: Artistic color palette.
- **Decorative & Lifestyle**:
  - `NoteType.OOTD`: Outfit of the day.
  - `NoteType.PARTY_TIME`: Celebration / Party 🥳.
  - `NoteType.GOOD_MORNING`: Morning greeting ☀️.
  - `NoteType.GOODNIGHT`: Goodnight 🌙.
  - `NoteType.MISS_YOU`: Miss you heart badge ❤️.
- **In Love & Couple**:
  - `NoteType.IN_LOVE_LONGING`, `NoteType.IN_LOVE_MISS`, `NoteType.IN_LOVE_HUG`, `NoteType.IN_LOVE_JEALOUS`, `NoteType.IN_LOVE_DUCK`, `NoteType.IN_LOVE_POUT`, `NoteType.IN_LOVE_REPLY`.

### Video Limits:
- **Duration**: Uncapped by API (supports **10s, 30s, 60s (1 min)** or longer).
- **Max File Size**: Firebase Storage enforces a strict hard limit of **< 6 MB (6,291,455 bytes)**. Videos must be encoded below 6 MB.

### Methods
| Method | Parameters | Description |
| :--- | :--- | :--- |
| `upload_image(file_or_bytes)` | `str` path or `bytes` | Auto-converts to `.webp` and uploads via Google Resumable protocol with authentic `downloadTokens`. |
| `upload_video(file_or_bytes)` | `str` path or `bytes` | Uploads `.mp4` video to Locket Video Storage (< 6 MB limit check). |
| `post(...)` | `image`, `caption`, `video`, `note_type`, `is_private`, `recipients` | Posts a photo or video moment with customizable note styling. Set `is_private=True` to send to yourself only. |
| `get_latest()` | None | Retrieves latest moments feed from all friends. |
| `get_shared_moments_by_username(username, limit=None)` (or `get_posts_by_username`) | `username: str`, `limit: int` | **Retrieves actual moments (photos/videos) shared by a user**, filtering out pure text chat messages, returning genuine moments with `moment_uid` and `thumbnail_url`. |
| `get_shared_moments_by_user(user_uid, limit=None)` | `user_uid: str`, `limit: int` | Retrieves genuine shared moments by User UID. |
| `get_views(moment_uid)` | `moment_uid: str` | **Fetches view count and list of users who viewed your moment (`getMomentViews`).** |
| `comment(moment_uid, receiver_uid, text)` | `moment_uid: str`, `receiver_uid: str`, `text: str` | **Comments on a moment (`sendChatMessageV2`)**, which links the moment directly inside the chat conversation. |
| `react(moment_uid, reaction="❤️", from_memory=False)` | `moment_uid: str`, `reaction: str` | **Sends emoji reaction to a photo or video moment** (`reactToMoment`). |
| `get_filters()` | None | Fetches available camera filters. |
| `mark_as_viewed(moment_uid)` | `moment_uid: str` | Sends view signal for a specific moment. |
| `get_rollcall_posts(week_of_year=None, year=None, source="banner")` | `week_of_year: int`, `year: int`, `source: str` | Retrieves weekly Rollcall event posts (auto-calculates current ISO week). |
| `delete(moment_uid)` | `moment_uid: str` | Deletes a previously posted moment. |

---

## 6. Friends, Groups & Moderation (`client.friends`)

Complete control over contacts, friend requests, groups, and user moderation.

### Methods
| Method | Parameters | Description |
| :--- | :--- | :--- |
| `get_groups_and_friends()` | None | Retrieves list of joined groups (`getGroupsState`). |
| `get_all_friends()` | None | **Retrieves complete list of friends with full profile details (UID, Names, Username, Avatar).** |
| `resolve_invite_token_from_username(username)` | `username: str` | Resolves public link `https://locket.cam/<username>` into real iOS invite token. |
| `fetch_user_by_invite_token(invite_token)` | `invite_token: str` | Looks up detailed profile information by invite token. |
| `send_request(user_uid, source="inviteCardPopup")` | `user_uid: str`, `source: str` | Sends friend request matching genuine iOS payload. |
| `send_request_by_username(username)`| `username: str` | Resolves token and sends friend request directly by username. |
| `accept_request(user_uid)` | `user_uid: str` | Accepts an incoming friend request. |
| `remove(user_uid)` | `user_uid: str` | Removes friend. |
| `block(user_uid)` | `user_uid: str` | Blocks user. |
| `unblock(user_uid)` | `user_uid: str` | Unblocks user. |
| `suggest_friends(phone_contacts)` | `phone_contacts: list` | Retrieves friend recommendations from phone numbers. |


---

## 7. Direct Messaging & Real-Time WebSockets (`client.chat`)

Real-time interactions over HTTPS and WebSocket connections.

### Methods
| Method | Parameters | Description |
| :--- | :--- | :--- |
| `send_message(receiver_uid, text=None, moment_uid=None)` | `receiver_uid: str`, `text: str`, `moment_uid: str` | Sends text message, full-sized emoji, or attaches a moment (auto-synced). |
| `send_moment(receiver_uid, moment_uid, text=None)` | `receiver_uid: str`, `moment_uid: str`, `text: str` | **Shares a moment directly into chat** (yours or any friend's). **Leave `text=None` to send purely the standalone moment without text!** |
| `get_messages(other_user_id=None, conversation_id=None, fetch_server=True)` | `other_user_id: str`, `conversation_id: str`, `fetch_server: bool` | **Queries live Firestore database**, retrieving full-fidelity messages, server IDs, reactions, sender info, and precise chronological timeline. |
| `get_conversations()` | None | **Retrieves inbox conversations list** including peer UID, unread count, read status, latest message snippet, and last seen timestamp (`other_last_read_at`). |
| `send_reaction(conversation_id, message_id, emoji, validate_receiver=True)` | `conversation_id: str`, `message_id: str`, `emoji: str` | **Sends emoji reaction to a specific friend's message** (`sendChatMessageReaction`). Supports single emojis and multi-emoji combos (`"❤️"`, `"🔥🥰"`, `"❤️❤️❤️❤️❤️"`). Prevents reacting to own messages. |
| `remove_reaction(conversation_id, message_id)` | `conversation_id: str`, `message_id: str` | **Removes / unreacts your emoji reaction** from a message (`removeChatMessageReaction`). |
| `delete_message(conversation_uid, message_uid, validate_ownership=True)` | `conversation_uid: str`, `message_uid: str` | **Recalls / unsends a message** (`deleteChatMessage`). Automatically validates ownership so you can only recall your own sent messages. |
| `mark_as_read(conversation_uid=None, other_user_id=None, send_read_receipt=True)` | `conversation_uid: str`, `other_user_id: str`, `send_read_receipt: bool` | Marks conversation as read. Setting **`send_read_receipt=False`** enables Ghost / Incognito mode (reads messages without notifying the sender). |
| `listen_realtime(other_user_id, callback)` | `other_user_id: str`, `callback: callable` | Connects directly to `wss://api.locketcamera.com/wss_v2/chat` to stream messages in real-time. |

---

## 8. Exception Hierarchy

```
LocketError (Base Exception)
├── AuthenticationError     (Login failure, invalid token, client blocked)
├── StorageUploadError       (Binary upload failures to Firebase Storage)
└── LocketAPIError           (Server response errors with HTTP status code)
```

## 9. Packaging & Publishing Guide

For developers looking to build and distribute the package:

### 9.1. Install Build Dependencies
```bash
pip install --upgrade build twine
```

### 9.2. Build & Validate
```bash
# 1. Clean previous artifacts and generate wheels/sdist
python -m build

# 2. Validate distribution integrity
python -m twine check dist/*
```

### 9.3. Release to PyPI
```bash
# Publish artifacts to the official PyPI registry
python -m twine upload dist/*
```

---

## 📜 Copyright & License

Copyright © 2026 **LAMDev x DaLyMMO.com**. All rights reserved.

Distributed under the [MIT License](../LICENSE).

