#!/usr/bin/env python3
"""
=============================================================================
  👥 VÍ DỤ 6: BẠN BÈ, LỜI MỜI KẾT BẠN & QUẢN LÝ CHẶN (FRIENDS MODULE)
  Thư viện: locketlam
=============================================================================

Mục tiêu file này:
  1. Lấy toàn bộ danh sách bạn bè kèm hồ sơ đầy đủ (UID, Tên, Username, Avatar).
  2. Gửi lời mời kết bạn tự động chỉ bằng Username (`send_request_by_username`).
     (Thư viện tự động phân giải invite token công khai từ locket.cam/<username> chuẩn iOS).
  3. Đồng ý (Accept) lời mời kết bạn từ người khác (`accept_request`).
  4. Hủy kết bạn (Remove friend) (`remove`).
  5. Chặn (Block) người dùng và bỏ chặn (Unblock) (`block`, `unblock`).
  6. Lấy danh sách nhóm Locket đang tham gia (`get_groups_and_friends`).
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
TARGET_USERNAME_TO_ADD = ""      # <-- Username bạn bè muốn gửi kết bạn (ví dụ "username_test")
TARGET_UID_TO_MANAGE = ""        # <-- User UID để thử hủy kết bạn / chặn / bỏ chặn


def main():
    print("=" * 60)
    print("👥 DEMO: QUẢN LÝ BẠN BÈ, KẾT BẠN & CHẶN NGƯỜI DÙNG")
    print("=" * 60)

    if not client.is_authenticated():
        print("❌ Chưa đăng nhập! Vui lòng chạy file '01_login_and_session.py' trước.")
        return

    try:
        # =====================================================================
        # 1. LẤY TOÀN BỘ DANH SÁCH BẠN BÈ KÈM HỒ SƠ CHI TIẾT
        # =====================================================================
        print("\n📋 Đang tải toàn bộ danh sách bạn bè...")
        friends = client.friends.get_all_friends()
        print(f"👉 Tổng số bạn bè: {len(friends)}")

        for idx, f in enumerate(friends[:10], 1):  # In 10 bạn bè đầu tiên
            name = f"{f.get('first_name', '')} {f.get('last_name', '')}".strip()
            username = f.get("username", "Chưa đặt")
            uid = f.get("uid")
            print(f"   [{idx:2d}] {name} (@{username}) - UID: {uid}")

        # =====================================================================
        # 2. GỬI LỜI MỜI KẾT BẠN BẰNG USERNAME
        # =====================================================================
        if TARGET_USERNAME_TO_ADD:
            print(f"\n➕ Đang gửi lời mời kết bạn tới @{TARGET_USERNAME_TO_ADD}...")
            # Thư viện tự động giải mã link https://locket.cam/<username>
            # và gửi request chuẩn iOS
            res_add = client.friends.send_request_by_username(TARGET_USERNAME_TO_ADD)
            print(f"🎉 Gửi lời mời kết bạn thành công! Kết quả: {res_add}")

        # =====================================================================
        # 3. ĐỒNG Ý LỜI MỜI KẾT BẠN (ACCEPT REQUEST)
        # =====================================================================
        # client.friends.accept_request(user_uid="UID_NGUOI_GUI_LOI_MOI")

        # =====================================================================
        # 4. HỦY KẾT BẠN (REMOVE FRIEND)
        # =====================================================================
        # if TARGET_UID_TO_MANAGE:
        #     print(f"\n🗑️ Đang hủy kết bạn với UID: {TARGET_UID_TO_MANAGE}...")
        #     client.friends.remove(user_uid=TARGET_UID_TO_MANAGE)
        #     print("✅ Đã hủy kết bạn thành công.")

        # =====================================================================
        # 5. CHẶN (BLOCK) & BỎ CHẶN (UNBLOCK)
        # =====================================================================
        # Khi chặn, Locket sẽ tự động hủy kết bạn và đưa vào danh sách đen.
        # client.friends.block(user_uid="UID_CAN_CHAN")
        # print("🚫 Đã chặn người dùng.")
        #
        # client.friends.unblock(user_uid="UID_CAN_BO_CHAN")
        # print("🔓 Đã bỏ chặn người dùng.")

        # =====================================================================
        # 6. LẤY DANH SÁCH NHÓM ĐANG THAM GIA
        # =====================================================================
        print("\n👥 Đang lấy danh sách nhóm...")
        groups_state = client.friends.get_groups_and_friends()
        print(f"👉 Thông tin nhóm: {list(groups_state.keys())}")

    except LocketError as e:
        print(f"❌ Có lỗi: {e}")


if __name__ == "__main__":
    main()
