#!/usr/bin/env python3
"""
=============================================================================
  🎬 EXAMPLE 4: POST VIDEO MOMENTS & AUTO H.265 COMPRESSION
  Library: locketlam
=============================================================================

Objectives:
  1. Post video (.mp4) files to Locket Video Storage.
  2. Smart Auto-Compression (Auto Compress & Optimize):
     - Locket enforces a strict file size ceiling of < 6 MB (6,291,455 bytes).
     - With `auto_compress=True` (default), videos are automatically compressed
       using Apple HEVC/H.265, maintaining Full HD resolution for videos up to 3-5 mins.
  3. Compression priority modes:
     - 'video'   : Allocates maximum bitrate to sharp visuals.
     - 'audio'   : Preserves pristine high-fidelity audio/music.
     - 'balanced': Optimal balance between video clarity and audio quality (recommended).
  4. Real-time encoding and upload tracking via `progress_callback`.
"""

import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from locketlam import LocketClient, NoteType
from locketlam.exceptions import LocketError

SESSION_FILE = os.path.join(REPO_ROOT, "locketlam_session.json")
client = LocketClient(session_path=SESSION_FILE)

# =============================================================================
# VIDEO PATH CONFIGURATION
# =============================================================================
# Supports local .mp4 file path or direct web video URL:
VIDEO_PATH = "sample_video.mp4"       # <-- Replace with your video file
VIDEO_CAPTION = "Video test from Python LocketLam 🎬"


def my_progress_callback(percent: int, status_text: str):
    """Callback function tracking compression and upload in real-time."""
    print(f"\r⏳ [{percent:3d}%] {status_text}", end="", flush=True)


def main():
    print("=" * 60)
    print("🎬 DEMO: POST VIDEO & AUTO H.265 HEVC COMPRESSION")
    print("=" * 60)

    if not client.is_authenticated():
        print("❌ Not authenticated! Run '01_login_and_session.py' first.")
        return

    full_video_path = os.path.join(REPO_ROOT, VIDEO_PATH) if not os.path.isabs(VIDEO_PATH) else VIDEO_PATH
    if not os.path.exists(full_video_path):
        print(f"⚠️ Video file not found: '{VIDEO_PATH}'")
        print("💡 Tip: Place an '.mp4' file in your project directory and update VIDEO_PATH in line 35.")
        return

    file_size_mb = os.path.getsize(full_video_path) / (1024 * 1024)
    print(f"📁 Video file : {VIDEO_PATH}")
    print(f"📦 Source size: {file_size_mb:.2f} MB")

    try:
        # =====================================================================
        # METHOD 1: POST DIRECTLY VIA client.moments.post(...)
        # =====================================================================
        # Passing `video=...` automatically:
        #   1. Extracts the first frame as a WebP thumbnail.
        #   2. Compresses with H.265 to safe ~5.7MB if source is >= 6MB.
        #   3. Uploads to Firebase Storage (Resumable Protocol).
        #   4. Broadcasts to Locket feed with your selected badge.
        print("\n🚀 Processing and uploading video to Locket...")

        res = client.moments.post(
            video=full_video_path,
            caption=VIDEO_CAPTION,
            note_type=NoteType.PARTY_TIME,
            auto_compress=True,
            priority="balanced",
            progress_callback=my_progress_callback
        )
        print("\n\n🎉 Video posted successfully!")
        print(f"👉 Moment ID : {res.get('id')}")
        print(f"👉 Video URL : {res.get('data', {}).get('video_url')}")
        print(f"👉 Thumb URL : {res.get('data', {}).get('thumbnail_url')}")

        # =====================================================================
        # METHOD 2: UPLOAD STANDALONE VIDEO (URL ONLY)
        # =====================================================================
        # video_url = client.moments.upload_video(
        #     video_path_or_bytes=full_video_path,
        #     auto_compress=True,
        #     priority="video",
        #     progress_callback=my_progress_callback
        # )
        # print(f"\n🔗 Video Storage URL: {video_url}")

    except LocketError as e:
        print(f"\n❌ Error posting video: {e}")


if __name__ == "__main__":
    main()
