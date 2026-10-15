#!/usr/bin/env python3
"""
=============================================================================
  👤 VÍ DỤ 2: QUẢN LÝ HỒ SƠ CÁ NHÂN & NGƯỜI DÙNG (USER MODULE)
  Thư viện: locketlam
=============================================================================

Mục tiêu file này:
  1. Lấy thông tin hồ sơ của chính mình hoặc của người dùng khác qua UID / Username.
  2. Đổi họ và tên hiển thị (First Name / Last Name).
  3. Cập nhật ngày sinh (Birthdate).
  4. Đổi ảnh đại diện Avatar (tự động nén WebP và upload lên Firebase Storage).
  5. Cài đặt thông báo & đồng bộ cài đặt client với server Locket.
"""

import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from locketlam import LocketClient
from locketlam.exceptions import LocketError

# Khởi tạo client từ session đã lưu
SESSION_FILE = os.path.join(REPO_ROOT, "locketlam_session.json")
client = LocketClient(session_path=SESSION_FILE)

# =============================================================================
# THÔNG TIN CẤU HÌNH ĐỂ TEST (BẠN CÓ THỂ ĐỔI THEO Ý MUỐN)
# =============================================================================
NEW_FIRST_NAME = "Minh"              # <-- Tên mới
NEW_LAST_NAME = "Anh"                # <-- Họ mới
NEW_BIRTHDATE = "2002-10-20"         # <-- Ngày sinh (định dạng YYYY-MM-DD)
TARGET_USERNAME = "locket"           # <-- Username muốn tra cứu thử
NEW_AVATAR_PATH = ""                 # <-- Đường dẫn file ảnh avatar mới (ví dụ "avatar.jpg" hoặc để trống)


def main():
    print("=" * 60)
    print("👤 DEMO: QUẢN LÝ HỒ SƠ & THÔNG TIN NGƯỜI DÙNG LOCKET")
    print("=" * 60)

    if not client.is_authenticated():
        print("❌ Chưa đăng nhập! Vui lòng chạy file '01_login_and_session.py' trước để đăng nhập.")
        return

    try:
        # =====================================================================
        # 1. XEM HỒ SƠ CỦA CHÍNH MÌNH (client.user.get_profile)
        # =====================================================================
        print("\n🔍 Đang lấy thông tin cá nhân của bạn...")
        my_profile = client.user.get_profile()
        print(f"👉 Họ tên   : {my_profile.get('first_name')} {my_profile.get('last_name')}")
        print(f"👉 Username : {my_profile.get('username')}")
        print(f"👉 UID      : {my_profile.get('uid')}")
        print(f"👉 Ngày sinh: {my_profile.get('birthdate')}")
        print(f"👉 Avatar   : {my_profile.get('profile_picture_url')}")

        # =====================================================================
        # 2. TRA CỨU HỒ SƠ NGƯỜI DÙNG KHÁC BẰNG USERNAME
        # =====================================================================
        if TARGET_USERNAME:
            print(f"\n🔎 Đang tra cứu thông tin của @{TARGET_USERNAME}...")
            user_info = client.user.get_profile_by_username(TARGET_USERNAME)
            if user_info:
                print(f"✅ Tìm thấy:")
                print(f"👉 UID      : {user_info.get('uid')}")
                print(f"👉 Tên      : {user_info.get('first_name')} {user_info.get('last_name')}")
                print(f"👉 Avatar   : {user_info.get('profile_picture_url')}")
            else:
                print(f"⚠️ Không tìm thấy người dùng có username @{TARGET_USERNAME}")

        # =====================================================================
        # 3. ĐỔI HỌ VÀ TÊN HIỂN THỊ
        # =====================================================================
        # print(f"\n✏️ Đang đổi tên thành '{NEW_FIRST_NAME} {NEW_LAST_NAME}'...")
        # res_name = client.user.update_name(first_name=NEW_FIRST_NAME, last_name=NEW_LAST_NAME)
        # print("✅ Đổi tên thành công!")

        # =====================================================================
        # 4. ĐỔI NGÀY SINH
        # =====================================================================
        # print(f"\n🎂 Đang đổi ngày sinh thành '{NEW_BIRTHDATE}'...")
        # client.user.update_birthdate(NEW_BIRTHDATE)
        # print("✅ Đổi ngày sinh thành công!")

        # =====================================================================
        # 5. ĐỔI ẢNH ĐẠI DIỆN AVATAR
        # =====================================================================
        # Hỗ trợ truyền đường dẫn file ảnh (.jpg, .png) hoặc bytes hoặc URL ảnh.
        # Thư viện tự động nén chuẩn WebP và upload lên Firebase Storage.
        if NEW_AVATAR_PATH and os.path.exists(NEW_AVATAR_PATH):
            print(f"\n🖼️ Đang đổi ảnh đại diện từ: {NEW_AVATAR_PATH}...")
            avatar_url = client.user.update_avatar(NEW_AVATAR_PATH)
            print(f"✅ Đổi avatar thành công! URL mới: {avatar_url}")

        # =====================================================================
        # 6. ĐỒNG BỘ THIẾT BỊ VÀ THÔNG BÁO PUSH
        # =====================================================================
        # Đăng ký Push Token giả lập Apple chuẩn iOS để nhận diện thiết bị
        client.user.set_notification_token(auto_fake=True)
        print("📱 Đã đồng bộ push notification token giả lập iOS.")

    except LocketError as e:
        print(f"❌ Có lỗi xảy ra: {e}")


if __name__ == "__main__":
    main()
