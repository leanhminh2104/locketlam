# 📘 LocketLam — Developer Integration Guide (English Primary)

> **What is this file for?**
> This is the **step-by-step developer integration guide** — providing battle-tested, production-grade code examples for every feature. Read this document when you need to know **how to write code to integrate specific features** of `locketlam` into your application or bot.

| Document Version | Language | Status |
|:---|:---|:---|
| 🇬🇧 **[INTEGRATION.md](INTEGRATION.md)** | **English** | **Primary (Main)** |
| 🇻🇳 **[INTEGRATION_VI.md](INTEGRATION_VI.md)** | **Vietnamese** | **Secondary (Bản phụ)** |

---

### 🗺️ Documentation Navigation Map

| If you want to... | Go to |
|:---|:---|
| 🚀 **High-level overview & quick start** | ➡️ [README.md](../README.md) (EN) · [README_VI.md](../README_VI.md) (VI) |
| 📚 **Complete catalog of classes, methods, and parameters** | ➡️ [FEATURES.md](FEATURES.md) (EN) · [FEATURES_VI.md](FEATURES_VI.md) (VI) |
| 💡 **Complete runnable scripts (8 full feature showcases)** | ➡️ [examples/en/](../examples/en/) (EN) · [examples/vi/](../examples/vi/) (VI) |

---

## 📑 Table of Contents

- [1. Installation](#1-installation)
- [2. Login & Session Management](#2-login--session-management)
- [3. Authentic Apple iOS Device Emulation](#3-authentic-apple-ios-device-emulation)
- [4. Photo Moments & Custom Captions](#4-photo-moments--custom-captions)
- [5. Long Video Moments & Adaptive HEVC Compression](#5-long-video-moments--adaptive-hevc-compression)
- [6. Feed, Interactions & Reactions](#6-feed-interactions--reactions)
- [7. Friends, Invitations & Moderation](#7-friends-invitations--moderation)
- [8. Direct Messaging & Real-Time WebSockets](#8-direct-messaging--real-time-websockets)
- [9. Comprehensive Error Handling](#9-comprehensive-error-handling)
- [10. Complete Runnable Examples Directory](#10-complete-runnable-examples-directory)
- [11. Copyright & License](#11-copyright--license)

---

## 1. Installation

### Install via PyPI (Recommended)

```bash
pip install locketlam
```

> **Requirements:** Python >= 3.8. The package includes pre-bundled FFmpeg compression binaries for Windows, macOS, and Linux — no manual FFmpeg installation or external path configuration is required!

### Install from Source (GitHub)

```bash
git clone https://github.com/leanhminh2104/locketlam.git
cd locketlam
pip install -e .
```

---

## 2. Login & Session Management

### Initial Login with Email & Password

```python
from locketlam import LocketClient

# Initialize client with persistent session file path
client = LocketClient(session_path="session.json")

# Authenticate against Locket Camera servers
client.login("user@example.com", "password123")

print("Logged in successfully! User ID:", client.session.uid)
```

> Upon successful authentication, the session tokens are encrypted and cached in `session.json`. The SDK automatically handles token refresh lifecycles in the background.

### Re-initializing from Saved Session (Zero Re-login)

```python
from locketlam import LocketClient

client = LocketClient(session_path="session.json")

if client.is_authenticated():
    print("Session active and valid! UID:", client.session.uid)
else:
    print("Session expired or missing, re-authenticating...")
    client.login("user@example.com", "password123")
```

---

## 3. Authentic Apple iOS Device Emulation

All outgoing HTTP and WebSocket requests carry authentic iOS device signatures (Apple IDFA, Vendor ID, Bundle Identifier, Firebase GMPID, Protobuf Flags) to prevent accounts from being flagged or challenged by bot detection systems.

```python
from locketlam import LocketClient

client = LocketClient(session_path="session.json")

# Mode 1: Automatic realistic iPhone emulation (Default - Recommended)
client.set_device(auto_emulate=True)

# Mode 2: Specify your own physical iPhone hardware parameters
client.set_device(
    auto_emulate=False,
    installation_id="A1B2C3D4-E5F6-7890-ABCD-EF1234567890",
    hardware_model="iPhone16,2",     # iPhone 15 Pro Max
    ios_version="18.2.0",
    app_version="2.69.0"
)
```

---

## 4. Photo Moments & Custom Captions

### Posting Photos with Preset Badges (`NoteType`)

The library includes 158+ official Locket Camera badge presets:

```python
from locketlam import LocketClient, NoteType

client = LocketClient(session_path="session.json")

res = client.moments.post(
    image="photo.jpg",                      # Local file path or web URL
    caption="Weekend coffee run ☕",
    note_type=NoteType.DANG_BAN_TUONG_TU   # Select from official preset badges
)

print("Posted moment successfully! ID:", res.get("id"))
```

### Posting Photos with Custom Gradient Colors

```python
res = client.moments.post(
    image="coding.jpg",
    caption="Late night coding session 💻",
    icon="⚡",
    colors=["#FF416C", "#8A2387"],         # Neon Pink -> Deep Purple gradient
    text_color="#FFFFFF"
)
```

### Posting Moments to Selected Friends Only (Audience Filtering)

```python
res = client.moments.post(
    image="friends.jpg",
    caption="Close friends only ❤️",
    recipients=["FRIEND_UID_1", "FRIEND_UID_2"]
)
```

### Posting Private Moments (Only visible to you)

```python
res = client.moments.post(
    image="private_note.jpg",
    caption="Personal diary entry",
    is_private=True
)
```

---

## 5. Long Video Moments & Adaptive HEVC Compression

Locket Camera servers reject any video payload that exceeds 6.0 MB. `locketlam` integrates an intelligent H.265/HEVC video pipeline matching iOS hardware encoders, allowing you to upload videos up to 10–15 minutes while maintaining crisp resolution and keeping files under the safe 5.7 MB threshold.

### Basic Video Upload (Automatic Adaptive Compression)

```python
from locketlam import LocketClient

client = LocketClient(session_path="session.json")

res = client.moments.post(
    video="travel_clip.mp4",               # Files >= 6 MB automatically compressed
    caption="Scenic summer getaway 🏖️"
)

print("Video Moment ID:", res.get("id"))
```

### Video Upload with Real-Time Progress Callback

```python
from locketlam import LocketClient, NoteType

client = LocketClient(session_path="session.json")

def on_progress(percent: int, message: str):
    print(f"\r[{percent:3d}%] {message}", end="", flush=True)

client.moments.post(
    video="long_video_10min.mp4",
    caption="Complete vlog trip 🎬",
    note_type=NoteType.FLEX_DEN_HOI_THO_CUOI,
    auto_compress=True,                    # Enable adaptive HEVC compression
    priority="balanced",                   # 'video' (sharpness), 'audio' (music), 'balanced'
    progress_callback=on_progress
)
print("\nVideo moment published successfully!")
```

### Uploading Video to Firebase Storage Only (Without Posting)

```python
video_url = client.moments.upload_video(
    video_path_or_bytes="raw_clip.mp4",
    auto_compress=True,
    priority="video"
)
print("Uploaded Firebase Storage URL:", video_url)
```

---

## 6. Feed, Interactions & Reactions

### Fetching Latest Moments Feed

```python
feed = client.moments.get_latest()

for moment in feed:
    author = moment.get("user", {}).get("first_name", "Anonymous")
    print(f"[{moment.get('id')}] {author}: {moment.get('caption')}")
```

### Fetching All Your Own Published Moments

```python
my_moments = client.moments.get_all_my_moments()
print(f"You have published {len(my_moments)} moments in total.")
```

### Checking Who Viewed Your Moment

```python
views = client.moments.get_views(moment_id="MOMENT_UID")

for view in views:
    print(f"- {view.get('first_name')} (UID: {view.get('uid')}) - Emoji: {view.get('emoji', 'Regular view')}")
```

### Reacting & Commenting on Moments

```python
# Send emoji reaction
client.moments.react(moment_id="MOMENT_UID", emoji="❤️")

# Post a text comment
client.moments.comment(moment_id="MOMENT_UID", text="Awesome moment! 🔥")

# Delete your own published moment
client.moments.delete(moment_id="MOMENT_UID")
```

---

## 7. Friends, Invitations & Moderation

### Fetching Friends List with Full Profiles

```python
friends = client.friends.get_all_friends()

for friend in friends:
    print(f"- {friend.get('first_name')} {friend.get('last_name', '')} (@{friend.get('username')}) - UID: {friend.get('uid')}")
```

### Adding Friends by Username (Auto Invite Link Resolution)

```python
# Supports raw username or locket.cam/<username> link
client.friends.send_request_by_username("leanhminh")
```

### Managing Friend Requests

```python
# Check incoming and outgoing friend requests
requests = client.friends.get_friend_requests()
print(f"Incoming: {len(requests['incoming'])}, Outgoing: {len(requests['outgoing'])}")

# Accept an incoming friend request
client.friends.accept_request("SENDER_UID")
```

### Unfriending, Blocking & Unblocking

```python
# Remove a friend (supports UID or Username)
client.friends.remove("UID_OR_USERNAME")

# Block a user (automatically severs friendship on Locket servers)
client.friends.block("UID_OR_USERNAME")

# Unblock a user
client.friends.unblock("UID_OR_USERNAME")
```

---

## 8. Direct Messaging & Real-Time WebSockets

### Fetching Inbox Conversations

```python
conversations = client.chat.get_conversations()

for conv in conversations:
    unread = conv.get("unread_count", 0)
    print(f"Conversation: {conv.get('id')} | Peer UID: {conv.get('peer_uid')} | Unread: {unread}")
```

### Sending Messages & Sharing Moments into Chat

```python
# Send a standard text message
client.chat.send_message(
    receiver_uid="FRIEND_UID",
    text="Hey there! How are you doing? 👋"
)

# Share a moment directly into the conversation (with optional caption)
client.chat.send_moment(
    receiver_uid="FRIEND_UID",
    moment_uid="MOMENT_UID",
    text="Check out this moment 😄"
)
```

### Emoji Reactions & Unsending Messages

```python
# Send emoji reaction (supports combos: '❤️', '🔥🥰', '❤️❤️❤️')
client.chat.send_reaction(
    conversation_id="CONVERSATION_ID",
    message_id="MESSAGE_ID",
    emoji="❤️"
)

# Remove / unreact your reaction
client.chat.remove_reaction(
    conversation_id="CONVERSATION_ID",
    message_id="MESSAGE_ID"
)

# Recall / unsend your own sent message
client.chat.delete_message(
    conversation_uid="CONVERSATION_ID",
    message_uid="MESSAGE_ID"
)
```

### Ghost Mode (Read Messages Without Read Receipts)

```python
# Synchronize chronological chat messages from Firestore
messages = client.chat.get_messages(other_user_id="FRIEND_UID", fetch_server=True)

# Mark conversation as read in Ghost Mode (without sending read receipt to sender)
client.chat.mark_as_read(
    other_user_id="FRIEND_UID",
    send_read_receipt=False            # False = Ghost Mode, True = Send read receipt
)
```

### Real-Time WebSocket Streaming

```python
def handle_incoming_message(msg):
    print("\n[New Incoming Message]:", msg)

# Connects to wss://api.locketcamera.com/wss_v2/chat in non-blocking background task
client.chat.listen_realtime(
    other_user_id="FRIEND_UID",
    callback=handle_incoming_message
)
```

---

## 9. Comprehensive Error Handling

All SDK exceptions inherit from the base class `LocketError`, allowing clean error isolation in production systems:

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
    print("❌ Authentication failed (bad password or expired session):", e)

except StorageUploadError as e:
    print("❌ Firebase Cloud Storage upload error:", e)

except LocketAPIError as e:
    print(f"❌ Server rejected request [HTTP {e.status_code}]:", e.message)

except LocketError as e:
    print("❌ General LocketLam SDK error:", e)
```

---

## 10. Complete Runnable Examples Directory

The [`examples/`](../examples/) directory contains 8 fully working, standalone scripts ready for immediate execution:

| Feature Area | English Script | Vietnamese Script |
|:---|:---|:---|
| 01. Authentication & Session Persistence | [`examples/en/01_login_and_session.py`](../examples/en/01_login_and_session.py) | [`examples/vi/01_login_and_session.py`](../examples/vi/01_login_and_session.py) |
| 02. Profile Inspection & Username Lookup | [`examples/en/02_user_profile.py`](../examples/en/02_user_profile.py) | [`examples/vi/02_user_profile.py`](../examples/vi/02_user_profile.py) |
| 03. Posting Photos & 158+ Note Badges | [`examples/en/03_post_image_moment.py`](../examples/en/03_post_image_moment.py) | [`examples/vi/03_post_image_moment.py`](../examples/vi/03_post_image_moment.py) |
| 04. Posting Long Videos & Adaptive HEVC | [`examples/en/04_post_video_moment.py`](../examples/en/04_post_video_moment.py) | [`examples/vi/04_post_video_moment.py`](../examples/vi/04_post_video_moment.py) |
| 05. Moments Feed, Views & Reactions | [`examples/en/05_feed_views_reactions.py`](../examples/en/05_feed_views_reactions.py) | [`examples/vi/05_feed_views_reactions.py`](../examples/vi/05_feed_views_reactions.py) |
| 06. Friends List, Invites & Blocking | [`examples/en/06_friends_and_contacts.py`](../examples/en/06_friends_and_contacts.py) | [`examples/vi/06_friends_and_contacts.py`](../examples/vi/06_friends_and_contacts.py) |
| 07. Direct Chat & Real-Time WebSockets | [`examples/en/07_chat_and_reactions.py`](../examples/en/07_chat_and_reactions.py) | [`examples/vi/07_chat_and_reactions.py`](../examples/vi/07_chat_and_reactions.py) |
| Interactive All-in-One CLI Suite | [`examples/en/interactive_demo.py`](../examples/en/interactive_demo.py) | [`examples/vi/interactive_demo.py`](../examples/vi/interactive_demo.py) |

```bash
# Run the all-in-one English interactive CLI suite
python examples/en/interactive_demo.py
```

---

## 11. Copyright & License

Copyright © 2026 **LAMDev x DaLyMMO.com**. All rights reserved.

Released under the official open-source [MIT License](../LICENSE).
Contributions, feedback, and issue reports are welcome on [GitHub Issues](https://github.com/leanhminh2104/locketlam/issues).
