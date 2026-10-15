#!/usr/bin/env python3
"""
=============================================================================
  📸 EXAMPLE 3: POST PHOTO MOMENTS & CUSTOM GRADIENT BADGES
  Library: locketlam
=============================================================================

Objectives:
  1. Post photos to Locket from local file paths or web URLs.
  2. Use 158+ built-in badge presets from `NoteType` (FEELING_CUTE, PARTY_TIME, etc.).
  3. Fully customize gradient badge overlays (hex colors, custom emoji icon, text).
  4. Broadcast to all friends or send selectively to specific friend UIDs.
  5. Post in private mode (saved exclusively to personal memories).
"""

import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from locketlam import LocketClient, NoteType
from locketlam.exceptions import LocketError

# Initialize client using stored session
SESSION_FILE = os.path.join(REPO_ROOT, "locketlam_session.json")
client = LocketClient(session_path=SESSION_FILE)

# =============================================================================
# POST CONFIGURATION
# =============================================================================
# You can supply a local image path (.jpg, .png, .webp) or a direct web URL:
IMAGE_SOURCE = "https://picsum.photos/1080/1080"  # Or "my_photo.jpg"

# Optional list of friend UIDs to send to (leave empty [] to broadcast to ALL friends):
SPECIFIC_RECIPIENTS = []  # e.g.: ["FRIEND_UID_1", "FRIEND_UID_2"]


def main():
    print("=" * 60)
    print("📸 DEMO: POST PHOTOS & CUSTOM OVERLAYS ON LOCKET")
    print("=" * 60)

    if not client.is_authenticated():
        print("❌ Not authenticated! Run '01_login_and_session.py' first.")
        return

    try:
        # =====================================================================
        # METHOD 1: POST WITH A BUILT-IN LOCKET BADGE PRESET (NoteType)
        # =====================================================================
        # Over 158 built-in badge styles from Locket Remote Config:
        # e.g.: NoteType.FEELING_CUTE, NoteType.PARTY_TIME, NoteType.IN_LOVE_LONGING, etc.
        print("\n[1] Posting photo with preset badge: 'IN_LOVE_LONGING'...")
        res1 = client.moments.post(
            image=IMAGE_SOURCE,
            caption="Thinking of someone special...",
            note_type=NoteType.IN_LOVE_LONGING,
            recipients=SPECIFIC_RECIPIENTS if SPECIFIC_RECIPIENTS else None
        )
        print("🎉 Posted successfully!")
        print(f"👉 Moment ID  : {res1.get('id')}")
        print(f"👉 Thumbnail  : {res1.get('data', {}).get('thumbnail_url')}")

        # =====================================================================
        # METHOD 2: 100% CUSTOM GRADIENT COLORS & EMOJI ICON
        # =====================================================================
        # Freely customize hex colors (colors: [Start_Hex, End_Hex]),
        # text color (text_color), and any emoji icon:
        print("\n[2] Posting photo with custom gradient badge...")
        res2 = client.moments.post(
            image=IMAGE_SOURCE,
            caption="Late night coding vibes 💻",
            icon="⚡",
            colors=["#FF416C", "#8A2387"],
            text_color="#FFFFFF"
        )
        print("🎉 Custom gradient badge posted successfully!")
        print(f"👉 Moment ID  : {res2.get('id')}")

        # =====================================================================
        # METHOD 3: POST STANDARD CAPTION (TRANSLUCENT PILL)
        # =====================================================================
        print("\n[3] Posting photo with standard caption...")
        res3 = client.moments.post(
            image=IMAGE_SOURCE,
            caption="Hello from Python LocketLam!",
            note_type=NoteType.STANDARD
        )
        print("🎉 Standard caption photo posted successfully!")
        print(f"👉 Moment ID  : {res3.get('id')}")

        # =====================================================================
        # METHOD 4: POST IN PRIVATE MODE (FOR YOUR EYES ONLY)
        # =====================================================================
        # Set is_private=True to store only in your memories without broadcasting to widgets
        # print("\n[4] Posting in private mode...")
        # res4 = client.moments.post(
        #     image=IMAGE_SOURCE,
        #     caption="Secret diary moment",
        #     is_private=True
        # )
        # print(f"🎉 Private moment posted! ID: {res4.get('id')}")

    except LocketError as e:
        print(f"❌ Error posting photo: {e}")


if __name__ == "__main__":
    main()
