#!/usr/bin/env python3
"""
=============================================================================
  👀 VÍ DỤ 5: TƯƠNG TÁC FEED, XEM LƯỢT XEM, THẢ TIM & BÌNH LUẬN (FEED & ENGAGEMENT)
  Thư viện: locketlam
=============================================================================

Mục tiêu file này:
  1. Lấy danh sách feed khoảnh khắc mới nhất từ bạn bè (`client.moments.get_latest`).
  2. Lấy tất cả khoảnh khắc của chính mình (`get_all_my_moments`).
  3. Lấy khoảnh khắc thực thụ của một người bạn bằng Username (`get_shared_moments_by_username`).
  4. Xem chi tiết ai đã xem bài đăng và các emoji cảm xúc đã thả (`get_views`).
  5. Thả biểu cảm cảm xúc (React emoji: ❤️, 🔥, 🥺, vv.) vào khoảnh khắc.
  6. Gửi bình luận (Comment) vào khoảnh khắc (bình luận sẽ nhảy vào tin nhắn chat).
  7. Xóa bài đăng khoảnh khắc của mình (`client.moments.delete`).
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
# CẤU HÌNH TEST
# =============================================================================
TARGET_USERNAME_TO_VIEW = ""   # <-- Nhập username bạn bè muốn xem khoảnh khắc (hoặc để trống)
REACTION_EMOJI = "❤️"          # <-- Emoji muốn thả: ❤️, 🔥, 🥰, 🥳, 🥺
COMMENT_TEXT = "Ảnh đẹp quá bạn ơi! 🔥"


def main():
    print("=" * 60)
    print("👀 DEMO: TƯƠNG TÁC FEED, THẢ TIM, COMMENT & QUẢN LÝ BÀI ĐĂNG")
    print("=" * 60)

    if not client.is_authenticated():
        print("❌ Chưa đăng nhập! Vui lòng chạy file '01_login_and_session.py' trước.")
        return

    try:
        # =====================================================================
        # 1. LẤY FEED KHOẢNH KHẮC MỚI NHẤT TỪ BẠN BÈ
        # =====================================================================
        print("\n📥 Đang tải feed bạn bè mới nhất...")
        feed = client.moments.get_latest()
        print(f"👉 Tìm thấy {len(feed)} khoảnh khắc trên feed.")

        # =====================================================================
        # 2. LẤY TẤT CẢ BÀI ĐĂNG CỦA CHÍNH MÌNH (BOT/USER HIỆN TẠI)
        # =====================================================================
        print("\n📂 Đang lấy danh sách khoảnh khắc của chính bạn...")
        my_moments = client.moments.get_all_my_moments()
        print(f"👉 Tổng số bài đăng của bạn: {len(my_moments)}")

        if my_moments:
            latest_post = my_moments[0]
            moment_id = latest_post.get("moment_uid") or latest_post.get("id")
            caption = latest_post.get("caption", "Không có caption")
            print(f"\n🔍 Chi tiết bài đăng gần nhất của bạn:")
            print(f"   - Moment ID: {moment_id}")
            print(f"   - Caption  : {caption}")

            # =================================================================
            # 3. XEM AI ĐÃ XEM VÀ THẢ TIM BÀI ĐĂNG (client.moments.get_views)
            # =================================================================
            print(f"\n👀 Đang kiểm tra lượt xem và reactions cho Moment: {moment_id}...")
            views_data = client.moments.get_views(moment_uid=moment_id)
            views_count = views_data.get("views_count", len(views_data.get("viewers", [])))
            print(f"👉 Tổng lượt xem: {views_count}")
            print(f"👉 Danh sách UID đã xem: {views_data.get('viewers', [])}")
            print(f"👉 Danh sách reactions : {views_data.get('reactions', [])}")

        # =====================================================================
        # 4. LẤY KHOẢNH KHẮC CỦA BẠN BÈ BẰNG USERNAME
        # =====================================================================
        if TARGET_USERNAME_TO_VIEW:
            print(f"\n🔍 Đang lấy bài đăng của @{TARGET_USERNAME_TO_VIEW}...")
            posts = client.moments.get_shared_moments_by_username(
                username=TARGET_USERNAME_TO_VIEW,
                limit=5  # Lấy tối đa 5 bài
            )
            print(f"👉 Tìm thấy {len(posts)} bài đăng.")
            for idx, p in enumerate(posts, 1):
                p_id = p.get("moment_uid") or p.get("id")
                print(f"   [{idx}] ID: {p_id} | Caption: {p.get('caption', '')}")

                # Ví dụ thả tim vào bài đầu tiên:
                if idx == 1:
                    print(f"   ❤️ Đang thả biểu cảm '{REACTION_EMOJI}' vào bài...")
                    client.moments.react(moment_uid=p_id, reaction=REACTION_EMOJI)
                    print("   ✅ Đã thả tim thành công!")

        # =====================================================================
        # 5. BÌNH LUẬN (COMMENT) VÀO BÀI ĐĂNG
        # =====================================================================
        # client.moments.comment(
        #     moment_uid="MOMENT_UID_CAN_COMMENT",
        #     receiver_uid="UID_NGUOI_DANG",
        #     text=COMMENT_TEXT
        # )

        # =====================================================================
        # 6. XÓA BÀI ĐĂNG KHOẢNH KHẮC
        # =====================================================================
        # client.moments.delete(moment_uid="MOMENT_UID_MUON_XOA")

    except LocketError as e:
        print(f"❌ Có lỗi: {e}")


if __name__ == "__main__":
    main()
