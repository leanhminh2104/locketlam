#!/usr/bin/env python3
"""
=============================================================================
  🚀 VÍ DỤ 1: ĐĂNG NHẬP & QUẢN LÝ PHIÊN (SESSION & AUTHENTICATION)
  Thư viện: locketlam
=============================================================================

Mục tiêu file này:
  1. Hướng dẫn cách đăng nhập với Email & Mật khẩu tài khoản Locket.
  2. Hướng dẫn cấu hình thiết bị iOS (DeviceProfile) - tự động fake máy hoặc tự nhập mã máy thật.
  3. Quản lý lưu phiên (session) tự động vào file JSON để chạy các lần sau không cần login lại.
  4. Cơ chế tự động làm mới token ngầm (auto-refresh JWT token) của session.
"""

import os
import sys

# Đảm bảo import được thư viện khi chạy từ thư mục mã nguồn
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from locketlam import LocketClient
from locketlam.exceptions import AuthenticationError, LocketError

# =============================================================================
# 1. CẤU HÌNH THIẾT BỊ iOS (DEVICE PROFILE)
# =============================================================================
# Mặc định thư viện tự động chọn ngẫu nhiên iPhone 13 Pro -> 15 Pro, iOS 17/18,
# kèm installation_id và headers Apple chống chặn bot.
# Bạn cũng có thể tùy chỉnh nếu muốn giả lập một thiết bị cụ thể:

client = LocketClient(session_path="locketlam_session.json")

# Cách A: Dùng chế độ giả lập tự động (Mặc định - Khuyên dùng)
client.set_device(auto_emulate=True)

# Cách B: Hoặc tự nhập thông số máy thật của bạn nếu muốn:
# client.set_device(
#     auto_emulate=False,
#     installation_id="12345678-ABCD-1234-ABCD-1234567890AB",
#     hardware_model="iPhone16,2",  # iPhone 15 Pro Max
#     ios_version="18.2.0",
#     app_version="2.69.0"
# )

# =============================================================================
# 2. ĐIỀN THÔNG TIN ĐĂNG NHẬP CỦA BẠN TẠI ĐÂY
# =============================================================================
EMAIL = "your_email@example.com"      # <-- Nhập email Locket của bạn
PASSWORD = "your_password_here"       # <-- Nhập mật khẩu Locket của bạn


def main():
    print("=" * 60)
    print("🔑 DEMO: ĐĂNG NHẬP VÀ QUẢN LÝ PHIÊN LOCKET")
    print("=" * 60)

    # Bước 1: Kiểm tra xem đã có phiên đăng nhập cũ lưu trong file chưa
    if client.is_authenticated():
        print("✅ Đã phát hiện phiên đăng nhập hợp lệ từ file session!")
        print(f"👉 UID hiện tại: {client.session.uid}")
        print(f"👉 Email: {client.session.email}")
    else:
        print("ℹ️ Chưa có phiên hoặc phiên hết hạn. Đang tiến hành đăng nhập...")
        
        # Bỏ qua nếu người dùng chưa nhập tài khoản thật
        if EMAIL == "your_email@example.com":
            print("\n⚠️ Vui lòng mở file này và điền EMAIL / PASSWORD thật của bạn ở dòng 46-47 để chạy thử!")
            return

        try:
            # client.login() sẽ xác thực qua Google Firebase Identity Toolkit
            # và tự động lưu phiên ra file 'locketlam_session.json'
            login_data = client.login(email=EMAIL, password=PASSWORD)
            
            print("🎉 Đăng nhập thành công!")
            print(f"👉 User UID : {login_data.get('localId')}")
            print(f"👉 Email    : {login_data.get('email')}")
            print(f"👉 ID Token : {login_data.get('idToken')[:25]}... (đã ẩn bớt)")
        except AuthenticationError as e:
            print(f"❌ Lỗi đăng nhập: {e}")
            return
        except LocketError as e:
            print(f"❌ Lỗi hệ thống: {e}")
            return

    # =========================================================================
    # 3. LẤY TOKEN HỢP LỆ VÀ CƠ CHẾ AUTO-REFRESH TOKEN
    # =========================================================================
    # client.session.get_valid_token() sẽ tự động kiểm tra thời hạn token.
    # Nếu token sắp hết hạn trước 60 giây, nó sẽ tự động gọi refresh ngầm.
    token = client.session.get_valid_token()
    print(f"\n🔒 Valid ID Token (dùng gửi API): {token[:30]}...")

    # Nếu muốn chủ động ép buộc làm mới token ngay lập tức:
    # client.session.refresh()
    # print("🔄 Đã chủ động làm mới token thành công!")

    # Lưu lại trạng thái phiên thủ công bất kỳ lúc nào:
    # client.session.save()
    print("💾 Phiên đăng nhập đã được lưu tự động tại 'locketlam_session.json'.")


if __name__ == "__main__":
    main()
