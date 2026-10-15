#!/usr/bin/env python3
"""
=============================================================================
  👥 EXAMPLE 6: FRIENDS, INVITES & BLOCK MANAGEMENT
  Library: locketlam
=============================================================================

Objectives:
  1. Fetch complete friends list with full user profiles (UID, Name, Username, Avatar).
  2. Send friend requests automatically by Username (`send_request_by_username`).
     (Automatically resolves public invite tokens from locket.cam/<username>).
  3. Accept incoming friend requests (`accept_request`).
  4. Remove friends (`remove`).
  5. Block and unblock users (`block`, `unblock`).
  6. Inspect joined groups and relationship status (`get_groups_and_friends`).
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
TARGET_USERNAME_TO_ADD = ""      # <-- Target username to send friend request (e.g. "test_user")
TARGET_UID_TO_MANAGE = ""        # <-- Target UID to remove / block / unblock


def main():
    print("=" * 60)
    print("👥 DEMO: FRIENDS LIST, REQUESTS & BLOCKING")
    print("=" * 60)

    if not client.is_authenticated():
        print("❌ Not authenticated! Run '01_login_and_session.py' first.")
        return

    try:
        # =====================================================================
        # 1. FETCH FULL FRIENDS LIST WITH PROFILES
        # =====================================================================
        print("\n📋 Fetching complete friends list...")
        friends = client.friends.get_all_friends()
        print(f"👉 Total friends: {len(friends)}")

        for idx, f in enumerate(friends[:10], 1):  # Print first 10 friends
            name = f"{f.get('first_name', '')} {f.get('last_name', '')}".strip()
            username = f.get("username", "None")
            uid = f.get("uid")
            print(f"   [{idx:2d}] {name} (@{username}) - UID: {uid}")

        # =====================================================================
        # 2. SEND FRIEND REQUEST BY USERNAME
        # =====================================================================
        if TARGET_USERNAME_TO_ADD:
            print(f"\n➕ Sending friend request to @{TARGET_USERNAME_TO_ADD}...")
            # Automatically parses https://locket.cam/<username> and sends native iOS request
            res_add = client.friends.send_request_by_username(TARGET_USERNAME_TO_ADD)
            print(f"🎉 Friend request sent successfully! Result: {res_add}")

        # =====================================================================
        # 3. ACCEPT FRIEND REQUEST
        # =====================================================================
        # client.friends.accept_request(user_uid="REQUESTER_USER_UID")

        # =====================================================================
        # 4. REMOVE FRIEND
        # =====================================================================
        # if TARGET_UID_TO_MANAGE:
        #     print(f"\n🗑️ Removing friend: {TARGET_UID_TO_MANAGE}...")
        #     client.friends.remove(user_uid=TARGET_UID_TO_MANAGE)
        #     print("✅ Friend removed successfully.")

        # =====================================================================
        # 5. BLOCK & UNBLOCK USER
        # =====================================================================
        # Blocking un-friends the user and adds them to blacklist.
        # client.friends.block(user_uid="UID_TO_BLOCK")
        # print("🚫 User blocked.")
        #
        # client.friends.unblock(user_uid="UID_TO_UNBLOCK")
        # print("🔓 User unblocked.")

        # =====================================================================
        # 6. RETRIEVE GROUPS & RELATIONSHIPS
        # =====================================================================
        print("\n👥 Fetching groups...")
        groups_state = client.friends.get_groups_and_friends()
        print(f"👉 Group state keys: {list(groups_state.keys())}")

    except LocketError as e:
        print(f"❌ Error occurred: {e}")


if __name__ == "__main__":
    main()
