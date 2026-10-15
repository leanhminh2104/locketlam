#!/usr/bin/env python3
"""
=============================================================================
  🎬 VÍ DỤ 4: ĐĂNG VIDEO & TỰ ĐỘNG NÉN H.265 CHUẨN LOCKET (POST VIDEO MOMENT)
  Thư viện: locketlam
=============================================================================

Mục tiêu file này:
  1. Hướng dẫn đăng video (.mp4) lên Locket Storage.
  2. Cơ chế Tự Động Nén Thông Minh (Auto Compress & Optimize Video):
     - Locket có giới hạn khắt khe < 6 MB (6,291,455 bytes).
     - Với `auto_compress=True` (mặc định), thư viện tự động nén thông minh chuẩn H.265/HEVC,
       giữ nguyên 100% độ phân giải Full HD/2K/4K, hỗ trợ video dài từ 15s đến 3-5 phút mượt mà.
  3. Chọn mức ưu tiên nén (priority):
     - 'video'   : Dồn băng thông tối đa cho hình ảnh sắc nét.
     - 'audio'   : Giữ chất lượng âm thanh gốc, nhạc nền cao cấp.
     - 'balanced': Cân bằng hoàn hảo giữa âm thanh và độ nét (khuyên dùng).
  4. Theo dõi thanh tiến trình nén và upload qua `progress_callback`.
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
# CẤU HÌNH ĐƯỜNG DẪN VIDEO ĐỂ TEST
# =============================================================================
# Hỗ trợ đường dẫn file mp4 trong máy hoặc URL video trên mạng (TikTok, Reels, v.v.):
VIDEO_PATH = "tiktok_video_58s.mp4"   # <-- Đổi thành file video của bạn (ví dụ "my_video.mp4")
VIDEO_CAPTION = "Video test từ Python LocketLam 🎬"


def my_progress_callback(percent: int, status_text: str):
    """Hàm callback hiển thị tiến trình nén / upload theo thời gian thực."""
    print(f"\r⏳ [{percent:3d}%] {status_text}", end="", flush=True)


def main():
    print("=" * 60)
    print("🎬 DEMO: ĐĂNG VIDEO VÀ CƠ CHẾ TỰ ĐỘNG NÉN H.265")
    print("=" * 60)

    if not client.is_authenticated():
        print("❌ Chưa đăng nhập! Vui lòng chạy file '01_login_and_session.py' trước.")
        return

    # Kiểm tra sự tồn tại của file video
    full_video_path = os.path.join(REPO_ROOT, VIDEO_PATH) if not os.path.isabs(VIDEO_PATH) else VIDEO_PATH
    if not os.path.exists(full_video_path):
        print(f"⚠️ Không tìm thấy file video: '{VIDEO_PATH}'")
        print("💡 Gợi ý: Hãy đặt 1 file video '.mp4' vào thư mục dự án và cập nhật biến VIDEO_PATH ở dòng 35.")
        return

    file_size_mb = os.path.getsize(full_video_path) / (1024 * 1024)
    print(f"📁 Tệp video: {VIDEO_PATH}")
    print(f"📦 Dung lượng gốc: {file_size_mb:.2f} MB")

    try:
        # =====================================================================
        # CÁCH 1: ĐĂNG VIDEO TRỰC TIẾP QUA client.moments.post(...)
        # =====================================================================
        # Chỉ cần truyền tham số `video=...`. Thư viện sẽ tự động:
        #   1. Trích xuất frame đầu tiên làm thumbnail ảnh WebP.
        #   2. Kiểm tra nếu file >= 6MB thì tự nén H.265 về ~5.7MB an toàn.
        #   3. Upload lên Firebase Storage (Resumable Protocol).
        #   4. Đăng bài lên feed Locket với nhãn màu bạn chọn.
        print("\n🚀 Đang xử lý và đăng video lên Locket...")

        res = client.moments.post(
            video=full_video_path,
            caption=VIDEO_CAPTION,
            note_type=NoteType.FLEX_DEN_HOI_THO_CUOI,  # Nhãn 'Flex đến hơi thở cuối'
            auto_compress=True,                         # Tự động nén nếu vượt ngưỡng 6MB
            priority="balanced",                        # 'video', 'audio', hoặc 'balanced'
            progress_callback=my_progress_callback      # Callback xem tiến trình
        )
        print("\n\n🎉 Đăng video thành công!")
        print(f"👉 Moment ID : {res.get('id')}")
        print(f"👉 Video URL : {res.get('data', {}).get('video_url')}")
        print(f"👉 Thumb URL : {res.get('data', {}).get('thumbnail_url')}")

        # =====================================================================
        # CÁCH 2: CHỈ NÉN HOẶC UPLOAD LẤY LINK VIDEO (NẾU CẦN TÍCH HỢP RIÊNG)
        # =====================================================================
        # Nếu hệ thống của bạn chỉ cần lấy URL video sau khi upload:
        # video_url = client.moments.upload_video(
        #     video_path_or_bytes=full_video_path,
        #     auto_compress=True,
        #     priority="video",
        #     progress_callback=my_progress_callback
        # )
        # print(f"\n🔗 Video URL lưu trữ: {video_url}")

    except LocketError as e:
        print(f"\n❌ Lỗi khi đăng video: {e}")


if __name__ == "__main__":
    main()
