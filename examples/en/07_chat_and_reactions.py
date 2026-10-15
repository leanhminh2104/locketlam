#!/usr/bin/env python3
"""
=============================================================================
  💬 EXAMPLE 7: CHAT, REACTIONS, SHARE MOMENTS & INCOGNITO READ (CHAT MODULE)
  Library: locketlam
=============================================================================

Objectives:
  1. Retrieve inbox conversations with unread counter.
  2. Sync full 2-way chat history directly from Firestore database.
  3. Send text and emoji messages.
  4. Share moment posts directly into chat (`send_moment`).
  5. React to friend's messages (`send_reaction`) with single or stacked emojis ("❤️", "🔥", "❤️❤️❤️❤️❤️").
  6. Remove reaction from messages (`remove_reaction`).
  7. Delete sent messages (`delete_message`).
  8. Mark messages as read in incognito mode (`send_read_receipt=False` - without "Seen" status).
  9. Real-time message streaming via WebSocket (`listen_realtime`).
"""

import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from locketlam import LocketClient
from locketlam.exceptions import LocketError

SESSION_FILE = os.path.join(REPO_ROOT, "locketlam_session.json")
client = LocketClient(session_path=SESSION_FILE)

# =============================================================================
# TEST CONFIGURATION
# =============================================================================
TARGET_FRIEND_UID = ""       # <-- Friend's UID to test chat
MESSAGE_TO_SEND = "Hello! This is an automated message sent via Python LocketLam 🚀"


def main():
    print("=" * 60)
    print("💬 DEMO: CHAT, REACTIONS & MESSAGE SYNC")
    print("=" * 60)

    if not client.is_authenticated():
        print("❌ Not authenticated! Run '01_login_and_session.py' first.")
        return

    try:
        # =====================================================================
        # 1. FETCH INBOX (CONVERSATIONS LIST)
        # =====================================================================
        print("\n📬 Fetching inbox conversations...")
        conversations = client.chat.get_conversations()
        print(f"👉 Found {len(conversations)} conversations.")

        selected_friend_uid = TARGET_FRIEND_UID
        selected_conv_id = None

        for idx, conv in enumerate(conversations[:5], 1):
            c_id = conv.get("id") or conv.get("conversation_id")
            other_uid = conv.get("other_user_id") or conv.get("recipient_id")
            unread = conv.get("unread_count", 0)
            last_msg = conv.get("last_message", {}).get("text", "")
            print(f"   [{idx}] Conversation ID: {c_id}")
            print(f"       Friend UID      : {other_uid}")
            print(f"       Unread Messages : {unread}")
            print(f"       Last Message    : {last_msg}")

            if not selected_friend_uid and other_uid:
                selected_friend_uid = other_uid
                selected_conv_id = c_id

        # =====================================================================
        # 2. VIEW CHAT HISTORY (FIRESTORE SYNC)
        # =====================================================================
        if selected_friend_uid:
            print(f"\n📜 Fetching message history for UID: {selected_friend_uid}...")
            messages = client.chat.get_messages(other_user_id=selected_friend_uid, fetch_server=True)
            print(f"👉 Total downloaded messages: {len(messages)}")

            for m in messages[-5:]:  # Print last 5 messages
                sender = "You" if m.get("sender_id") == client.session.uid else "Friend"
                txt = m.get("text") or "[Media/Moment]"
                m_id = m.get("id") or m.get("message_id")
                print(f"   - [{sender}] {txt} (ID: {m_id})")

        # =====================================================================
        # 3. SEND TEXT MESSAGE (client.chat.send_message)
        # =====================================================================
        if selected_friend_uid and TARGET_FRIEND_UID:
            print(f"\n📤 Sending message to {selected_friend_uid}...")
            res_msg = client.chat.send_message(
                receiver_uid=selected_friend_uid,
                text=MESSAGE_TO_SEND
            )
            print(f"🎉 Message sent successfully! ID: {res_msg.get('id')}")

        # =====================================================================
        # 4. SHARE MOMENT INTO CHAT (send_moment)
        # =====================================================================
        # Share any moment with or without accompanying text:
        # client.chat.send_moment(
        #     receiver_uid=selected_friend_uid,
        #     moment_uid="TARGET_MOMENT_UID",
        #     text="Check this out! 😂"
        # )

        # =====================================================================
        # 5. REACT TO FRIEND'S MESSAGE
        # =====================================================================
        # client.chat.send_reaction(
        #     conversation_id=selected_conv_id,
        #     message_id="FRIEND_MESSAGE_ID",
        #     emoji="🔥"
        # )

        # =====================================================================
        # 6. INCOGNITO READ (NO 'SEEN' RECEIPT SENT)
        # =====================================================================
        if selected_friend_uid:
            print("\n👁️ Marking as read silently in incognito mode (send_read_receipt=False)...")
            client.chat.mark_as_read(
                other_user_id=selected_friend_uid,
                send_read_receipt=False
            )
            print("✅ Messages marked as read silently!")

    except LocketError as e:
        print(f"❌ Error occurred: {e}")


if __name__ == "__main__":
    main()
