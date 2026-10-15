#!/usr/bin/env python3
"""
=============================================================================
  🚀 LOCKETLAM - INTERACTIVE DEMO CLI (ALL FEATURES SHOWCASE)
  Author: LAMDev x DaLyMMO.com
  Copyright (c) 2026 LAMDev x DaLyMMO.com. All rights reserved.
=============================================================================
This interactive script demonstrates 100% of the features provided by the
locketlam library, including authentication, moments, videos, friends, and chat.
"""

import os
import sys
import json
import time
from typing import Optional

# Ensure package root is in path when running directly from repo
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from locketlam import LocketClient, NoteType
from locketlam.exceptions import (
    LocketError,
    AuthenticationError,
    StorageUploadError,
    LocketAPIError
)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_banner(uid: Optional[str] = None):
    print("=" * 66)
    print("       🚀 LOCKETLAM CLIENT CLI - DEMO ALL FEATURES")
    print("         Developed by: LAMDev x DaLyMMO.com")
    print("=" * 66)
    if uid:
        masked_uid = uid[:4] + "****" + uid[-4:] if len(uid) > 8 else "****"
        print(f"  [Active Session]: UID = {masked_uid} (Authenticated)")
    else:
        print("  [Active Session]: Not authenticated")
    print("-" * 66)


def get_authenticated_client(session_path: str = "locketlam_session.json") -> LocketClient:
    """Initializes and verifies the LocketClient session."""
    # Find locketlam_session.json in repo root or current dir
    root_session = os.path.join(REPO_ROOT, session_path)
    if os.path.exists(root_session):
        client = LocketClient(session_path=root_session)
    else:
        client = LocketClient(session_path=session_path)

    if not client.is_authenticated():
        clear_screen()
        print_banner()
        print("No valid session found. Please authenticate:")
        email = input("Email: ").strip()
        import getpass
        password = getpass.getpass("Password: ").strip()
        try:
            print("Logging in to Locket backend...")
            client.login(email, password)
            print("Login successful! Session saved.")
            time.sleep(1)
        except Exception as e:
            print(f"Login failed: {e}")
            sys.exit(1)

    return client


# =============================================================================
# FEATURE 1: USER PROFILE MANAGEMENT
# =============================================================================
def menu_user_profile(client: LocketClient):
    while True:
        clear_screen()
        print_banner(client.session.uid)
        print("  [1] USER PROFILE & SETTINGS")
        print("  1. View Current Profile (Self)")
        print("  2. Lookup User by Username")
        print("  3. Update Display Name")
        print("  4. Update Birthdate")
        print("  5. Update Avatar (from local file or URL)")
        print("  6. Sync Client Data & App Settings")
        print("  0. Back to Main Menu")
        print("-" * 66)
        choice = input("Select an option [0-6]: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            try:
                prof = client.user.get_profile()
                print("\n--- Profile Details ---")
                print(f"UID: {prof.get('uid')}")
                print(f"Username: @{prof.get('username')}")
                print(f"Name: {prof.get('first_name')} {prof.get('last_name')}")
                print(f"Email: {prof.get('email')}")
                print(f"Avatar URL: {prof.get('profile_picture_url')}")
                print(f"Badge: {prof.get('badge')}")
            except Exception as e:
                print(f"Error: {e}")
            input("\nPress Enter to continue...")

        elif choice == "2":
            uname = input("\nEnter username to search: ").strip()
            if uname:
                try:
                    res = client.user.get_profile_by_username(uname)
                    print("\n--- User Profile Found ---")
                    print(f"UID: {res.get('uid')}")
                    print(f"Username: @{res.get('username')}")
                    print(f"Name: {res.get('first_name')} {res.get('last_name')}")
                    print(f"Avatar: {res.get('profile_picture_url')}")
                except Exception as e:
                    print(f"Search failed: {e}")
            input("\nPress Enter to continue...")

        elif choice == "3":
            try:
                prof = client.user.get_profile()
                curr_fn = prof.get('first_name') or ''
                curr_ln = prof.get('last_name') or ''
                print(f"\nCurrent Name: {curr_fn} {curr_ln}".strip())
                print(f"- Current First Name: '{curr_fn}'")
                print(f"- Current Last Name:  '{curr_ln}'")
            except Exception:
                curr_fn, curr_ln = '', ''

            fn = input("\nEnter New First Name [Enter to keep current]: ").strip()
            ln = input("Enter New Last Name [Enter to keep current]: ").strip()

            new_fn = fn if fn else curr_fn
            new_ln = ln if ln else curr_ln

            if new_fn or new_ln:
                try:
                    client.user.update_name(first_name=new_fn, last_name=new_ln)
                    print(f"Display name updated successfully to: {new_fn} {new_ln}".strip())
                except Exception as e:
                    print(f"Update failed: {e}")
            else:
                print("No changes provided.")
            input("\nPress Enter to continue...")

        elif choice == "4":
            try:
                prof = client.user.get_profile()
                curr_bday = prof.get('birthdate') or 'Not set'
                print(f"\nCurrent Birthdate: {curr_bday}")
            except Exception:
                pass
            bday = input("Enter New Birthdate (YYYY-MM-DD) [Enter to skip]: ").strip()
            if bday:
                try:
                    client.user.update_birthdate(bday)
                    print("Birthdate updated successfully!")
                except Exception as e:
                    print(f"Update failed: {e}")
            input("\nPress Enter to continue...")

        elif choice == "5":
            try:
                prof = client.user.get_profile()
                curr_avatar = prof.get('profile_picture_url') or 'None'
                print(f"\nCurrent Avatar URL:\n{curr_avatar}")
            except Exception:
                pass
            av_path = input("\nEnter local image path or public URL [Enter to skip]: ").strip().strip('"')
            if av_path:
                try:
                    print("Uploading image and updating on Locket backend...")
                    res = client.user.update_avatar(av_path)
                    new_pic = res.get("profile_picture_url") if isinstance(res, dict) else res
                    print(f"\nAvatar updated successfully! New URL:\n{new_pic}")
                except Exception as e:
                    print(f"Avatar update failed: {e}")
            input("\nPress Enter to continue...")

        elif choice == "6":
            try:
                client.user.sync_client_data(push_notifications=True)
                print("Client settings synchronized with Locket server.")
            except Exception as e:
                print(f"Sync failed: {e}")
            input("\nPress Enter to continue...")


# =============================================================================
# FEATURE 2: MOMENTS FEED & POSTING (PHOTOS, HEVC VIDEOS, BADGES)
# =============================================================================
def menu_moments(client: LocketClient):
    while True:
        clear_screen()
        print_banner(client.session.uid)
        print("  [2] MOMENTS & MEDIA PIPELINE")
        print("  1. View Friends Feed (get_latest)")
        print("  2. View My Own Moments History")
        print("  3. View Moments of a Specific User (by Username)")
        print("  4. Post Standard Photo Moment (Custom text caption)")
        print("  5. Post Photo with Preset Badge (158+ Locket styles)")
        print("  6. Post Photo with Custom Gradient & Emoji")
        print("  7. Post Video Moment (Auto-compressed Apple HEVC H.265 < 6MB)")
        print("  8. View Moment Details & Reactions (get_views)")
        print("  9. React to a Moment with Emoji")
        print("  10. Comment on a Moment (direct chat integration)")
        print("  11. Delete a Moment")
        print("  0. Back to Main Menu")
        print("-" * 66)
        choice = input("Select an option [0-11]: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            try:
                print("Fetching friends feed...")
                feed = client.moments.get_latest()
                print(f"\nFeed items count: {len(feed)}")
                for i, m in enumerate(feed[:10]):
                    uid = m.get("id") or m.get("canonical_uid")
                    caption = m.get("caption") or "(No caption)"
                    media_type = "Video" if m.get("video_url") else "Photo"
                    print(f" [{i+1}] [{media_type}] ID: {uid} | By: {m.get('user')}")
                    print(f"     Caption: {caption}")
                    if m.get("video_url"):
                        print(f"     Video: {m.get('video_url')[:60]}...")
            except Exception as e:
                print(f"Failed to fetch feed: {e}")
            input("\nPress Enter to continue...")

        elif choice == "2":
            try:
                my_moments = client.moments.get_all_my_moments()
                print(f"\nTotal posted moments: {len(my_moments)}")
                for i, m in enumerate(my_moments[:10]):
                    uid = m.get("moment_uid") or m.get("id")
                    views = m.get("views_count", 0)
                    print(f" [{i+1}] UID: {uid} | Views: {views} | Created: {m.get('created_at')}")
            except Exception as e:
                print(f"Failed to fetch moments: {e}")
            input("\nPress Enter to continue...")

        elif choice == "3":
            uname = input("\nEnter Username to inspect: ").strip()
            if uname:
                try:
                    user_moments = client.moments.get_shared_moments_by_username(uname, limit=5)
                    print(f"\nFound {len(user_moments)} moments from @{uname}:")
                    for i, m in enumerate(user_moments):
                        uid = m.get("id") or m.get("canonical_uid")
                        print(f" [{i+1}] UID: {uid} | Caption: {m.get('caption')}")
                        if m.get("video_url"):
                            print(f"     Video: {m.get('video_url')}")
                        else:
                            print(f"     Thumbnail: {m.get('thumbnail_url')}")
                except Exception as e:
                    print(f"Failed to query moments: {e}")
            input("\nPress Enter to continue...")

        elif choice == "4":
            img = input("\nEnter Image File Path: ").strip().strip('"')
            cap = input("Enter Caption: ").strip()
            priv = input("Private (only visible to self)? [y/N]: ").strip().lower() == "y"
            if img:
                try:
                    print("Uploading image moment...")
                    res = client.moments.post(image=img, caption=cap, is_private=priv)
                    print("Moment posted successfully!")
                    print(f"Moment UID: {res.get('canonical_uid') or res.get('id')}")
                except Exception as e:
                    print(f"Post failed: {e}")
            input("\nPress Enter to continue...")

        elif choice == "5":
            img = input("\nEnter Image File Path or URL: ").strip().strip('"')
            if not img:
                input("\nNo image provided. Press Enter to return...")
                continue

            import json
            preset_file = os.path.join(REPO_ROOT, "locketlam", "caption_presets.json")
            all_presets = []
            if os.path.exists(preset_file):
                with open(preset_file, "r", encoding="utf-8") as pf:
                    p_dict = json.load(pf)
                    for k, v in p_dict.items():
                        all_presets.append((k, v))
            else:
                all_presets = [
                    ("dang_ban_tuong_tu", {"text": "Dang ban tuong tu", "icon": "💭"}),
                    ("doi_roi", {"text": "Doi roi", "icon": "😤"}),
                    ("flex_den_hoi_tho_cuoi", {"text": "Flex", "icon": "💎"}),
                    ("party_time", {"text": "Party Time!", "icon": "🪩"}),
                    ("oach_xa_lach", {"text": "Oach xa lach", "icon": "🥬"})
                ]

            page = 0
            page_size = 10
            total_pages = (len(all_presets) + page_size - 1) // page_size
            sel_badge = None

            while True:
                clear_screen()
                print("=" * 66)
                print(f"       🎨 ALL 158+ LOCKET PRESET BADGES (PAGE {page + 1}/{total_pages})")
                print("=" * 66)
                start_idx = page * page_size
                current_items = all_presets[start_idx:start_idx + page_size]

                for idx, (p_id, p_val) in enumerate(current_items):
                    num = start_idx + idx + 1
                    t = p_val.get("text") or p_id
                    ic = p_val.get("icon") or ""
                    sec = p_val.get("section") or ""
                    sec_str = f" [{sec}]" if sec else ""
                    print(f"  [{num:3d}] {ic} {t} (Code: {p_id}){sec_str}")

                print("-" * 66)
                print("  [N] Next page  |  [P] Prev page  |  [S] Search  |  [0] Cancel")
                print("  👉 Enter NUMBER [1-{}] or CODE to select:".format(len(all_presets)))
                p_in = input("Your selection: ").strip()

                if p_in == "0":
                    break
                elif p_in.lower() == "n":
                    if page + 1 < total_pages:
                        page += 1
                elif p_in.lower() == "p":
                    if page > 0:
                        page -= 1
                elif p_in.lower() == "s":
                    q = input("Search query: ").strip().lower()
                    matches = [(i + 1, k, v) for i, (k, v) in enumerate(all_presets) if q in k.lower() or q in (v.get("text") or "").lower()]
                    print(f"\nFound {len(matches)} matching badges:")
                    for m_num, m_id, m_val in matches[:15]:
                        print(f"  [{m_num}] {m_val.get('icon', '')} {m_val.get('text', m_id)} (Code: {m_id})")
                    chosen = input("\nEnter badge number to select (Enter to return): ").strip()
                    if chosen.isdigit() and 1 <= int(chosen) <= len(all_presets):
                        sel_badge = all_presets[int(chosen) - 1][0]
                        break
                elif p_in.isdigit():
                    val = int(p_in)
                    if 1 <= val <= len(all_presets):
                        sel_badge = all_presets[val - 1][0]
                        break
                    else:
                        print("Invalid number.")
                        time.sleep(1)
                elif any(p_in.lower() == k.lower() for k, _ in all_presets):
                    sel_badge = p_in.lower()
                    break

            if sel_badge:
                try:
                    custom_cap = input("Enter custom caption (Enter to keep badge default text): ").strip()
                    print(f"\nPosting moment with badge '{sel_badge}'...")
                    res = client.moments.post(image=img, note_type=sel_badge, caption=custom_cap)
                    print("Moment posted successfully!")
                    print(f"Moment UID: {res.get('canonical_uid') or res.get('id')}")
                except Exception as e:
                    print(f"Post failed: {e}")
            input("\nPress Enter to continue...")

        elif choice == "6":
            img = input("\nEnter Image File Path or URL: ").strip().strip('"')
            cap = input("Enter Title: ").strip()
            icon = input("Enter Emoji Icon (e.g. 🔥, 🚀, ✨): ").strip() or "✨"
            c1 = input("Gradient Start Hex (e.g. #FF416C): ").strip() or "#FF416C"
            c2 = input("Gradient End Hex (e.g. #8A2387): ").strip() or "#8A2387"
            if img:
                try:
                    print("Uploading custom gradient moment...")
                    res = client.moments.post(
                        image=img,
                        caption=cap,
                        icon=icon,
                        colors=[c1, c2],
                        text_color="#FFFFFF"
                    )
                    print("Moment posted successfully!")
                    print(f"Moment UID: {res.get('canonical_uid') or res.get('id')}")
                except Exception as e:
                    print(f"Post failed: {e}")
            input("\nPress Enter to continue...")

        elif choice == "7":
            print("\n[NOTE] Locket video pipeline automatically detects video size.")
            print("Videos exceeding 6 MB will be compressed using Apple HEVC H.265 (24fps cinema, GOP 2s).")
            vid_path = input("Enter Video File Path (.mp4): ").strip().strip('"')
            thumb_path = input("Enter Thumbnail Image (Leave empty to auto-extract): ").strip().strip('"')
            cap = input("Enter Video Caption: ").strip()

            if not os.path.exists(vid_path):
                print("Error: Video file not found.")
                input("\nPress Enter to continue...")
                continue

            temp_thumb = None
            if not thumb_path or not os.path.exists(thumb_path):
                import tempfile
                import imageio_ffmpeg
                import subprocess
                fd, temp_thumb = tempfile.mkstemp(suffix=".jpg")
                os.close(fd)
                print("Extracting thumbnail from video via FFmpeg...")
                ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
                cmd = [ffmpeg_bin, "-y", "-ss", "00:00:01", "-i", vid_path, "-vframes", "1", "-q:v", "2", temp_thumb]
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                thumb_path = temp_thumb

            try:
                print("Compressing & Uploading video moment to Locket...")
                res = client.moments.post(
                    image=thumb_path,
                    video=vid_path,
                    caption=cap,
                    icon="🎬",
                    colors=["#00c6ff", "#0072ff"],
                    text_color="#FFFFFF"
                )
                print("Video Moment Posted Successfully!")
                print(f"Moment UID: {res.get('canonical_uid') or res.get('id')}")
                print(f"Video URL: {res.get('video_url')}")
            except Exception as e:
                print(f"Video upload failed: {e}")
            finally:
                if temp_thumb and os.path.exists(temp_thumb):
                    os.remove(temp_thumb)
            input("\nPress Enter to continue...")

        elif choice == "8":
            m_id = input("\nEnter Moment UID to inspect: ").strip()
            if m_id:
                try:
                    views = client.moments.get_views(m_id)
                    print("\n--- Moment Views & Reactions ---")
                    print(f"View count: {views.get('count')}")
                    print(f"Viewers: {json.dumps(views.get('moment_views', []), indent=2)}")
                    print(f"Reactions: {json.dumps(views.get('reactions', []), indent=2)}")
                except Exception as e:
                    print(f"Query failed: {e}")
            input("\nPress Enter to continue...")

        elif choice == "9":
            m_id = input("\nEnter Moment UID to react: ").strip()
            emoji = input("Enter emoji reaction [default: ❤️]: ").strip() or "❤️"
            if m_id:
                try:
                    client.moments.react(moment_uid=m_id, reaction=emoji)
                    print(f"Successfully reacted {emoji} to moment {m_id}!")
                except Exception as e:
                    print(f"Reaction failed: {e}")
            input("\nPress Enter to continue...")

        elif choice == "10":
            m_id = input("\nEnter Moment UID to comment on: ").strip()
            r_uid = input("Enter Friend Receiver UID: ").strip()
            text = input("Enter Comment Text: ").strip()
            if m_id and r_uid and text:
                try:
                    res = client.moments.comment(moment_uid=m_id, receiver_uid=r_uid, text=text)
                    print("Comment sent successfully!")
                    print(f"Message ID: {res.get('msg_id') or res.get('id')}")
                except Exception as e:
                    print(f"Comment failed: {e}")
            input("\nPress Enter to continue...")

        elif choice == "11":
            m_id = input("\nEnter Moment UID to permanently DELETE: ").strip()
            confirm = input(f"Are you sure you want to delete {m_id}? [y/N]: ").strip().lower()
            if confirm == "y":
                try:
                    client.moments.delete(moment_uid=m_id)
                    print(f"Moment {m_id} deleted successfully.")
                except Exception as e:
                    print(f"Delete failed: {e}")
            input("\nPress Enter to continue...")


# =============================================================================
# FEATURE 3: FRIENDS & RELATIONSHIP MANAGEMENT
# =============================================================================
def menu_friends(client: LocketClient):
    while True:
        clear_screen()
        print_banner(client.session.uid)
        print("  [3] FRIENDS & GROUP MANAGEMENT")
        print("  1. List All Friends (with names, usernames, avatars)")
        print("  2. View Groups & Friend State")
        print("  3. Resolve Invite Token from Username (locket.cam/<user>)")
        print("  4. Send Friend Request by Username")
        print("  5. Send Friend Request by UID")
        print("  6. Accept Incoming Friend Request")
        print("  7. Remove / Unfriend User")
        print("  8. Block User")
        print("  9. Unblock User")
        print("  0. Back to Main Menu")
        print("-" * 66)
        choice = input("Select an option [0-9]: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            try:
                friends = client.friends.get_all_friends()
                print(f"\nTotal Friends: {len(friends)}")
                for i, f in enumerate(friends):
                    name = f"{f.get('first_name', '')} {f.get('last_name', '')}".strip()
                    uname = f.get('username') or '(no username)'
                    uid = f.get('uid')
                    print(f" [{i+1}] {name} (@{uname}) | UID: {uid}")
            except Exception as e:
                print(f"Failed to list friends: {e}")
            input("\nPress Enter to continue...")

        elif choice == "2":
            try:
                groups = client.friends.get_groups_and_friends()
                print("\nGroups State:")
                print(json.dumps(groups, indent=2, ensure_ascii=False))
            except Exception as e:
                print(f"Failed: {e}")
            input("\nPress Enter to continue...")

        elif choice == "3":
            uname = input("\nEnter Username to resolve invite token: ").strip()
            if uname:
                try:
                    token = client.friends.resolve_invite_token_from_username(uname)
                    print(f"\nResolved Invite Token for @{uname}: {token}")
                    user_info = client.friends.fetch_user_by_invite_token(token)
                    print(f"Profile: {user_info.get('first_name')} {user_info.get('last_name')}")
                    print(f"Friendship Status: {user_info.get('friendship_status')}")
                except Exception as e:
                    print(f"Resolution failed: {e}")
            input("\nPress Enter to continue...")

        elif choice == "4":
            uname = input("\nEnter Username to add friend: ").strip()
            if uname:
                try:
                    res = client.friends.send_request_by_username(uname)
                    print(f"Friend request sent to @{uname} successfully!")
                except Exception as e:
                    print(f"Request failed: {e}")
            input("\nPress Enter to continue...")

        elif choice == "5":
            target_uid = input("\nEnter Target User UID: ").strip()
            if target_uid:
                try:
                    client.friends.send_request(user_uid=target_uid)
                    print(f"Friend request sent to UID {target_uid} successfully!")
                except Exception as e:
                    print(f"Request failed: {e}")
            input("\nPress Enter to continue...")

        elif choice == "6":
            target_uid = input("\nEnter Target User UID to Accept: ").strip()
            if target_uid:
                try:
                    client.friends.accept_request(user_uid=target_uid)
                    print(f"Accepted friend request from {target_uid}!")
                except Exception as e:
                    print(f"Accept failed: {e}")
            input("\nPress Enter to continue...")

        elif choice == "7":
            target = input("\nEnter User UID or Username to Remove / Unfriend: ").strip()
            if target:
                try:
                    client.friends.remove(user_uid=target)
                    print(f"Unfriended user '{target}' successfully.")
                except Exception as e:
                    print(f"Unfriend failed: {e}")
            input("\nPress Enter to continue...")

        elif choice == "8":
            target = input("\nEnter User UID or Username to BLOCK: ").strip()
            if target:
                try:
                    client.friends.block(user_uid=target)
                    print(f"User '{target}' has been BLOCKED.")
                except Exception as e:
                    print(f"Block failed: {e}")
            input("\nPress Enter to continue...")

        elif choice == "9":
            target = input("\nEnter User UID or Username to UNBLOCK: ").strip()
            if target:
                try:
                    client.friends.unblock(user_uid=target)
                    print(f"User '{target}' has been UNBLOCKED.")
                except Exception as e:
                    print(f"Unblock failed: {e}")
            input("\nPress Enter to continue...")


# =============================================================================
# FEATURE 4: DIRECT CHAT & WEBSOCKET REAL-TIME
# =============================================================================
def menu_chat(client: LocketClient):
    while True:
        clear_screen()
        print_banner(client.session.uid)
        print("  [4] DIRECT CHAT & REAL-TIME WEBSOCKET")
        print("  1. List Inbox Conversations")
        print("  2. View Messages in a Conversation")
        print("  3. Send Direct Text Message")
        print("  4. Share a Moment into Chat")
        print("  5. React to a Chat Message with Emoji")
        print("  6. Unsend / Delete Your Chat Message")
        print("  7. Mark Conversation as Read")
        print("  8. Start Live WebSocket Listener (Real-Time)")
        print("  0. Back to Main Menu")
        print("-" * 66)
        choice = input("Select an option [0-8]: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            try:
                convs = client.chat.get_conversations()
                print(f"\nTotal Conversations: {len(convs)}")
                for i, c in enumerate(convs[:10]):
                    cid = c.get("id") or c.get("conversation_id")
                    parts = c.get("participants", [])
                    last_msg = c.get("last_message", {}).get("text", "(Media/Empty)")
                    print(f" [{i+1}] Conv ID: {cid} | Participants: {parts}")
                    print(f"     Last Message: {last_msg}")
            except Exception as e:
                print(f"Failed to fetch conversations: {e}")
            input("\nPress Enter to continue...")

        elif choice == "2":
            other_uid = input("\nEnter Friend User UID: ").strip()
            if other_uid:
                try:
                    msgs = client.chat.get_messages(other_user_id=other_uid)
                    print(f"\nMessages history ({len(msgs)} messages):")
                    for m in msgs[-15:]:
                        sender = "Me" if m.get("sender") == client.session.uid else "Friend"
                        mid = m.get("id") or m.get("msg_id")
                        print(f" [{sender}] ({mid}): {m.get('text', '')}")
                except Exception as e:
                    print(f"Failed to fetch messages: {e}")
            input("\nPress Enter to continue...")

        elif choice == "3":
            r_uid = input("\nEnter Receiver Friend UID: ").strip()
            text = input("Enter Message: ").strip()
            if r_uid and text:
                try:
                    res = client.chat.send_message(receiver_uid=r_uid, text=text)
                    print("Message sent successfully!")
                    print(f"Message ID: {res.get('msg_id') or res.get('id')}")
                except Exception as e:
                    print(f"Send failed: {e}")
            input("\nPress Enter to continue...")

        elif choice == "4":
            r_uid = input("\nEnter Receiver Friend UID: ").strip()
            m_uid = input("Enter Moment UID to share: ").strip()
            text = input("Optional Message (Leave empty for standalone moment): ").strip()
            if r_uid and m_uid:
                try:
                    res = client.chat.send_moment(receiver_uid=r_uid, moment_uid=m_uid, text=text or None)
                    print("Moment shared into chat successfully!")
                    print(f"Message ID: {res.get('msg_id') or res.get('id')}")
                except Exception as e:
                    print(f"Share failed: {e}")
            input("\nPress Enter to continue...")

        elif choice == "5":
            c_id = input("\nEnter Conversation ID: ").strip()
            m_id = input("Enter Message ID to react to: ").strip()
            emoji = input("Enter emoji (e.g. ❤️, 🔥, 👍): ").strip() or "❤️"
            if c_id and m_id:
                try:
                    client.chat.send_reaction(conversation_id=c_id, message_id=m_id, emoji=emoji)
                    print(f"Reacted {emoji} to message {m_id}!")
                except Exception as e:
                    print(f"Reaction failed: {e}")
            input("\nPress Enter to continue...")

        elif choice == "6":
            c_id = input("\nEnter Conversation ID: ").strip()
            m_id = input("Enter Message ID to unsend/delete: ").strip()
            if c_id and m_id:
                try:
                    client.chat.delete_message(conversation_uid=c_id, message_uid=m_id)
                    print(f"Message {m_id} deleted successfully.")
                except Exception as e:
                    print(f"Delete failed: {e}")
            input("\nPress Enter to continue...")

        elif choice == "7":
            c_id = input("\nEnter Conversation ID: ").strip()
            ghost = input("Ghost mode (don't send read receipt)? [y/N]: ").strip().lower() == "y"
            if c_id:
                try:
                    client.chat.mark_as_read(conversation_uid=c_id, send_read_receipt=not ghost)
                    print(f"Marked conversation {c_id} as read.")
                except Exception as e:
                    print(f"Failed: {e}")
            input("\nPress Enter to continue...")

        elif choice == "8":
            target_friend = input("\nEnter Friend UID to listen to in real-time (or press Enter for all): ").strip()
            print("\nConnecting to Locket WebSocket: wss://api.locketcamera.com/wss_v2/chat...")
            print("Listening for incoming messages. Press Ctrl+C to exit.\n")
            import asyncio

            async def handle_msg(msg):
                print(f"\n[LIVE WEBSOCKET EVENT] From {msg.get('sender')}: {msg.get('text')}")

            try:
                asyncio.run(client.chat.listen_realtime(target_friend or client.session.uid, handle_msg))
            except KeyboardInterrupt:
                print("\nStopped WebSocket listener.")
            except Exception as e:
                print(f"WebSocket Error: {e}")
            input("\nPress Enter to continue...")


# =============================================================================
# MAIN INTERACTIVE ENTRY POINT
# =============================================================================
def main():
    client = get_authenticated_client()

    while True:
        clear_screen()
        print_banner(client.session.uid)
        print("  MAIN MENU - SELECT A MODULE TO EXPLORE:")
        print("  [1] User Profile & Account Settings")
        print("  [2] Moments (Photos, Auto-Compressed Videos, Badges, Reactions)")
        print("  [3] Friends & Group Relationships")
        print("  [4] Direct Chat & Real-Time WebSockets")
        print("  [5] Force Session Refresh (Firebase JWT)")
        print("  [6] Switch Account / Login with Email & Password")
        print("  [0] Exit")
        print("-" * 66)
        choice = input("Select an option [0-6]: ").strip()

        if choice == "0":
            print("\nThank you for using locketlam! Goodbye. 👋\n")
            break
        elif choice == "1":
            menu_user_profile(client)
        elif choice == "2":
            menu_moments(client)
        elif choice == "3":
            menu_friends(client)
        elif choice == "4":
            menu_chat(client)
        elif choice == "5":
            try:
                client.session.refresh()
                print("\nSession token successfully renewed with Locket backend!")
            except Exception as e:
                print(f"\nRefresh failed: {e}")
            input("\nPress Enter to continue...")
        elif choice == "6":
            print("\n--- Login to Another Account ---")
            email = input("Email: ").strip()
            import getpass
            password = getpass.getpass("Password: ").strip()
            if email and password:
                try:
                    print("Logging in to Locket backend...")
                    client.login(email, password)
                    print(f"Login successful! Active UID is now: {client.session.uid}")
                except Exception as e:
                    print(f"Login failed: {e}")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
