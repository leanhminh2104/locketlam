#!/usr/bin/env python3
"""
=============================================================================
  📸 VÍ DỤ 3: ĐĂNG ẢNH & TÙY BIẾN NHÃN MÀU GRADIENT (POST IMAGE MOMENT)
  Thư viện: locketlam
=============================================================================

Mục tiêu file này:
  1. Đăng ảnh lên Locket từ đường dẫn file trên máy tính hoặc URL ảnh.
  2. Sử dụng 158+ nhãn màu chuẩn có sẵn trong `NoteType` (Đang bận tương tư, Dỗi rồi, OOTD, vv.).
  3. Tùy biến nhãn màu gradient 100% (Custom Gradient Colors, Icon emoji, Chữ tùy ý).
  4. Đăng ảnh chế độ công khai (cho tất cả bạn bè) hoặc chỉ gửi riêng cho một số người bạn.
  5. Đăng ảnh chế độ riêng tư (chỉ mình bạn xem).
"""

import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from locketlam import LocketClient, NoteType
from locketlam.exceptions import LocketError

# Khởi tạo client từ session
SESSION_FILE = os.path.join(REPO_ROOT, "locketlam_session.json")
client = LocketClient(session_path=SESSION_FILE)

# =============================================================================
# CẤU HÌNH THÔNG TIN ĐĂNG BÀI
# =============================================================================
# Bạn có thể dùng đường dẫn file ảnh cục bộ (.jpg, .png, .webp)
# hoặc dùng trực tiếp link URL ảnh trên mạng:
IMAGE_SOURCE = "https://picsum.photos/1080/1080"  # Hoặc "my_photo.jpg"

# Tùy chọn gửi cho danh sách bạn bè cụ thể (để trống [] để gửi cho TẤT CẢ bạn bè):
SPECIFIC_RECIPIENTS = []  # ví dụ: ["UID_BAN_BE_1", "UID_BAN_BE_2"]


def main():
    print("=" * 60)
    print("📸 DEMO: ĐĂNG ẢNH & TÙY BIẾN NHÃN MÀU LOCKET")
    print("=" * 60)

    if not client.is_authenticated():
        print("❌ Chưa đăng nhập! Vui lòng chạy file '01_login_and_session.py' trước.")
        return

    try:
        # =====================================================================
        # CÁCH 1: ĐĂNG ẢNH VỚI NHÃN CÓ SẴN CỦA LOCKET (NoteType)
        # =====================================================================
        # Thư viện tích hợp hơn 158 nhãn có sẵn từ Remote Config của Locket:
        # Ví dụ: NoteType.DANG_BAN_TUONG_TU, NoteType.DOI_ROI, NoteType.OACH_XA_LACH,
        #        NoteType.MUON_DUOC_OM, NoteType.OVERTHINKING_VAI_CHUONG, NoteType.FEELING_CUTE, ...
        print("\n[1] Đang đăng ảnh với nhãn màu Preset: 'Đang bận tương tư'...")
        res1 = client.moments.post(
            image=IMAGE_SOURCE,
            caption="Đang bận tương tư người lạ...",   # Bạn vẫn có thể sửa chữ theo ý mình
            note_type=NoteType.DANG_BAN_TUONG_TU,      # Tự động nạp icon và màu gradient chuẩn của Locket
            recipients=SPECIFIC_RECIPIENTS if SPECIFIC_RECIPIENTS else None
        )
        print("🎉 Đăng thành công!")
        print(f"👉 Moment UID: {res1.get('id')}")
        print(f"👉 Thumbnail : {res1.get('data', {}).get('thumbnail_url')}")

        # =====================================================================
        # CÁCH 2: TỰ DO CUSTOM MÀU GRADIENT VÀ ICON THEO Ý THÍCH 100%
        # =====================================================================
        # Bạn có thể tự chọn dải màu Hex (colors: [Màu_Đầu, Màu_Cuối])
        # Màu chữ (text_color) và icon emoji bất kỳ!
        print("\n[2] Đang đăng ảnh với nhãn màu Gradient tự chế...")
        res2 = client.moments.post(
            image=IMAGE_SOURCE,
            caption="Coding ban đêm cực chill 💻",
            icon="⚡",                                    # Icon hiển thị đầu nhãn
            colors=["#FF416C", "#8A2387"],              # Dải màu gradient từ Hồng -> Tím
            text_color="#FFFFFF"                        # Màu chữ trắng
        )
        print("🎉 Đăng thành công nhãn Gradient tự chế!")
        print(f"👉 Moment UID: {res2.get('id')}")

        # =====================================================================
        # CÁCH 3: ĐĂNG ẢNH GHI CHÚ CHỮ ĐƠN GIẢN (NỀN TRONG SUỐT TIÊU CHUẨN)
        # =====================================================================
        print("\n[3] Đang đăng ảnh với caption tiêu chuẩn...")
        res3 = client.moments.post(
            image=IMAGE_SOURCE,
            caption="Hello từ Python LocketLam!",
            note_type=NoteType.STANDARD
        )
        print("🎉 Đăng ảnh caption thường thành công!")
        print(f"👉 Moment UID: {res3.get('id')}")

        # =====================================================================
        # CÁCH 4: ĐĂNG ẢNH CHẾ ĐỘ RIÊNG TƯ (CHỈ MÌNH BẠN XEM)
        # =====================================================================
        # Đặt is_private=True, ảnh sẽ chỉ lưu vào kỷ niệm của bạn mà không gửi lên widget bạn bè
        # print("\n[4] Đang đăng ảnh chế độ riêng tư...")
        # res4 = client.moments.post(
        #     image=IMAGE_SOURCE,
        #     caption="Nhật ký bí mật",
        #     is_private=True
        # )
        # print(f"🎉 Đăng riêng tư thành công! ID: {res4.get('id')}")

    except LocketError as e:
        print(f"❌ Có lỗi khi đăng ảnh: {e}")


if __name__ == "__main__":
    main()
