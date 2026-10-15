#!/usr/bin/env python3
"""
=============================================================================
  👤 EXAMPLE 2: USER PROFILE & SETTINGS MANAGEMENT
  Library: locketlam
=============================================================================

Objectives:
  1. Retrieve your own profile or search other users via UID / Username.
  2. Update display name (First Name / Last Name).
  3. Update birthdate.
  4. Change avatar photo (auto-compressed to WebP and uploaded to Firebase Storage).
  5. Sync device push notification token with Locket servers.
"""

import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from locketlam import LocketClient
from locketlam.exceptions import LocketError

# Initialize client using stored session
SESSION_FILE = os.path.join(REPO_ROOT, "locketlam_session.json")
client = LocketClient(session_path=SESSION_FILE)

# =============================================================================
# CONFIGURATION FOR TESTING (ADJUST AS DESIRED)
# =============================================================================
NEW_FIRST_NAME = "John"              # <-- New first name
NEW_LAST_NAME = "Doe"                # <-- New last name
NEW_BIRTHDATE = "2002-10-20"         # <-- Birthdate (YYYY-MM-DD format)
TARGET_USERNAME = "locket"           # <-- Username to search
NEW_AVATAR_PATH = ""                 # <-- Avatar image path ("avatar.jpg" or leave empty)


def main():
    print("=" * 60)
    print("👤 DEMO: LOCKET USER PROFILE & ACCOUNT MANAGEMENT")
    print("=" * 60)

    if not client.is_authenticated():
        print("❌ Not authenticated! Run '01_login_and_session.py' first to log in.")
        return

    try:
        # =====================================================================
        # 1. VIEW OWN PROFILE (client.user.get_profile)
        # =====================================================================
        print("\n🔍 Fetching your profile info...")
        my_profile = client.user.get_profile()
        print(f"👉 Name      : {my_profile.get('first_name')} {my_profile.get('last_name')}")
        print(f"👉 Username  : {my_profile.get('username')}")
        print(f"👉 UID       : {my_profile.get('uid')}")
        print(f"👉 Birthdate : {my_profile.get('birthdate')}")
        print(f"👉 Avatar    : {my_profile.get('profile_picture_url')}")

        # =====================================================================
        # 2. LOOKUP ANOTHER USER BY USERNAME
        # =====================================================================
        if TARGET_USERNAME:
            print(f"\n🔎 Looking up @{TARGET_USERNAME}...")
            user_info = client.user.get_profile_by_username(TARGET_USERNAME)
            if user_info:
                print("✅ Found user:")
                print(f"👉 UID       : {user_info.get('uid')}")
                print(f"👉 Name      : {user_info.get('first_name')} {user_info.get('last_name')}")
                print(f"👉 Avatar    : {user_info.get('profile_picture_url')}")
            else:
                print(f"⚠️ User @{TARGET_USERNAME} not found")

        # =====================================================================
        # 3. UPDATE FIRST AND LAST NAME
        # =====================================================================
        # print(f"\n✏️ Updating name to '{NEW_FIRST_NAME} {NEW_LAST_NAME}'...")
        # res_name = client.user.update_name(first_name=NEW_FIRST_NAME, last_name=NEW_LAST_NAME)
        # print("✅ Name updated successfully!")

        # =====================================================================
        # 4. UPDATE BIRTHDATE
        # =====================================================================
        # print(f"\n🎂 Updating birthdate to '{NEW_BIRTHDATE}'...")
        # client.user.update_birthdate(NEW_BIRTHDATE)
        # print("✅ Birthdate updated successfully!")

        # =====================================================================
        # 5. UPDATE AVATAR PHOTO
        # =====================================================================
        # Supports local image file paths (.jpg, .png), raw bytes, or image URLs.
        # The library automatically converts to WebP and uploads to Firebase Storage.
        if NEW_AVATAR_PATH and os.path.exists(NEW_AVATAR_PATH):
            print(f"\n🖼️ Updating avatar from: {NEW_AVATAR_PATH}...")
            avatar_url = client.user.update_avatar(NEW_AVATAR_PATH)
            print(f"✅ Avatar updated successfully! New URL: {avatar_url}")

        # =====================================================================
        # 6. SYNC DEVICE & PUSH NOTIFICATIONS
        # =====================================================================
        client.user.set_notification_token(auto_fake=True)
        print("📱 Synced simulated Apple APNs push notification token.")

    except LocketError as e:
        print(f"❌ Error occurred: {e}")


if __name__ == "__main__":
    main()
