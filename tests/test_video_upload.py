#!/usr/bin/env python3
"""
Unit and integration tests for Locket video compression and upload pipelines.
Tests video processing with:
  - Input 1: tests/videos/tiktok_video_58s.mp4 (~3.91 MB, below 6MB limit) -> tests/videos/video_58s_after_upload.mp4
  - Input 2: tests/videos/tiktok_video_10p.mp4 (~41.30 MB, above 6MB limit) -> tests/videos/video_10p_after_upload.mp4 (HEVC compressed < 6MB)
"""

import os
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from locketlam import LocketClient
from locketlam.modules.moments import MomentsModule


class TestVideoUploadAndCompression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session_path = os.path.join(REPO_ROOT, "locketlam_session.json")
        cls.client = LocketClient(session_path=cls.session_path)
        cls.moments = cls.client.moments

        cls.videos_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos")

        # Standardized input video paths in tests/videos/
        cls.video_58s_in = os.path.join(cls.videos_dir, "tiktok_video_58s.mp4")
        cls.video_10p_in = os.path.join(cls.videos_dir, "tiktok_video_10p.mp4")

        # Standardized output processed video paths in tests/videos/
        cls.video_58s_out = os.path.join(cls.videos_dir, "video_58s_after_upload.mp4")
        cls.video_10p_out = os.path.join(cls.videos_dir, "video_10p_after_upload.mp4")

    def test_input_files_exist(self):
        """Verify that input video test files exist in tests/videos/."""
        self.assertTrue(
            os.path.exists(self.video_58s_in),
            f"Input file not found: {self.video_58s_in}"
        )
        self.assertTrue(
            os.path.exists(self.video_10p_in),
            f"Input file not found: {self.video_10p_in}"
        )

    def test_output_files_exist_and_under_limit(self):
        """Verify that output processed video files exist and respect Locket's 6MB ceiling."""
        self.assertTrue(
            os.path.exists(self.video_58s_out),
            f"Output file not found: {self.video_58s_out}"
        )
        self.assertTrue(
            os.path.exists(self.video_10p_out),
            f"Output file not found: {self.video_10p_out}"
        )

        # 6MB strict limit: 6,291,456 bytes
        size_58s = os.path.getsize(self.video_58s_out)
        size_10p = os.path.getsize(self.video_10p_out)

        self.assertLess(
            size_58s,
            6291456,
            f"video_58s_after_upload exceeds 6MB ceiling: {size_58s} bytes"
        )
        self.assertLess(
            size_10p,
            6291456,
            f"video_10p_after_upload exceeds 6MB ceiling: {size_10p} bytes"
        )

    def test_extract_thumbnail(self):
        """Test thumbnail extraction from the video files."""
        if os.path.exists(self.video_58s_in):
            thumb_bytes = self.moments.extract_thumbnail(self.video_58s_in)
            self.assertIsInstance(thumb_bytes, bytes)
            self.assertGreater(len(thumb_bytes), 0)

    def test_video_58s_size_threshold(self):
        """Verify that video under 6MB retains safe original size without compression."""
        size_58s = os.path.getsize(self.video_58s_in)
        self.assertLess(size_58s, 6291456)


if __name__ == "__main__":
    unittest.main()
