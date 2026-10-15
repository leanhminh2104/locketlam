#!/usr/bin/env python3
"""
=============================================================================
  👀 EXAMPLE 5: FEED INTERACTION, VIEWS, REACTIONS & COMMENTS
  Library: locketlam
=============================================================================

Objectives:
  1. Fetch latest moments feed from friends (`client.moments.get_latest`).
  2. Fetch all personal moments (`get_all_my_moments`).
  3. Fetch shared moments of a friend by Username (`get_shared_moments_by_username`).
  4. Inspect who viewed your post and emoji reactions (`get_views`).
  5. React with emojis (❤️, 🔥, 🥺, etc.) to moments.
  6. Comment on a moment (routes directly into private direct chat).
  7. Delete your own moments (`client.moments.delete`).
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
TARGET_USERNAME_TO_VIEW = ""   # <-- Target friend's username (or leave empty)
REACTION_EMOJI = "❤️"          # <-- Emoji to react: ❤️, 🔥, 🥰, 🥳, 🥺
COMMENT_TEXT = "Amazing photo! 🔥"


def main():
    print("=" * 60)
    print("👀 DEMO: FEED INTERACTION, LIKES, COMMENTS & POST MANAGEMENT")
    print("=" * 60)

    if not client.is_authenticated():
        print("❌ Not authenticated! Run '01_login_and_session.py' first.")
        return

    try:
        # =====================================================================
        # 1. FETCH LATEST MOMENTS FEED FROM FRIENDS
        # =====================================================================
        print("\n📥 Fetching latest friends feed...")
        feed = client.moments.get_latest()
        print(f"👉 Found {len(feed)} moments on feed.")

        # =====================================================================
        # 2. FETCH ALL PERSONAL POSTS
        # =====================================================================
        print("\n📂 Fetching your own moments...")
        my_moments = client.moments.get_all_my_moments()
        print(f"👉 Total personal moments: {len(my_moments)}")

        if my_moments:
            latest_post = my_moments[0]
            moment_id = latest_post.get("moment_uid") or latest_post.get("id")
            caption = latest_post.get("caption", "No caption")
            print(f"\n🔍 Your latest post details:")
            print(f"   - Moment ID: {moment_id}")
            print(f"   - Caption  : {caption}")

            # =================================================================
            # 3. INSPECT VIEWERS & REACTIONS (client.moments.get_views)
            # =================================================================
            print(f"\n👀 Checking views and reactions for Moment: {moment_id}...")
            views_data = client.moments.get_views(moment_uid=moment_id)
            views_count = views_data.get("views_count", len(views_data.get("viewers", [])))
            print(f"👉 Total views : {views_count}")
            print(f"👉 Viewers UID : {views_data.get('viewers', [])}")
            print(f"👉 Reactions   : {views_data.get('reactions', [])}")

        # =====================================================================
        # 4. FETCH FRIEND'S MOMENTS BY USERNAME
        # =====================================================================
        if TARGET_USERNAME_TO_VIEW:
            print(f"\n🔍 Fetching moments for @{TARGET_USERNAME_TO_VIEW}...")
            posts = client.moments.get_shared_moments_by_username(
                username=TARGET_USERNAME_TO_VIEW,
                limit=5
            )
            print(f"👉 Found {len(posts)} moments.")
            for idx, p in enumerate(posts, 1):
                p_id = p.get("moment_uid") or p.get("id")
                print(f"   [{idx}] ID: {p_id} | Caption: {p.get('caption', '')}")

                # React to first post:
                if idx == 1:
                    print(f"   ❤️ Reacting with '{REACTION_EMOJI}'...")
                    client.moments.react(moment_uid=p_id, reaction=REACTION_EMOJI)
                    print("   ✅ Reacted successfully!")

        # =====================================================================
        # 5. COMMENT ON A MOMENT
        # =====================================================================
        # client.moments.comment(
        #     moment_uid="TARGET_MOMENT_UID",
        #     receiver_uid="AUTHOR_UID",
        #     text=COMMENT_TEXT
        # )

        # =====================================================================
        # 6. DELETE A MOMENT
        # =====================================================================
        # client.moments.delete(moment_uid="MOMENT_UID_TO_DELETE")

    except LocketError as e:
        print(f"❌ Error occurred: {e}")


if __name__ == "__main__":
    main()
