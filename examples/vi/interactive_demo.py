#!/usr/bin/env python3
"""
=============================================================================
  🚀 LOCKETLAM - GIAO DIỆN CLI TƯƠNG TÁC ĐẦY ĐỦ TÍNH NĂNG (BẢN TIẾNG VIỆT)
  Tác giả: LAMDev x DaLyMMO.com
  Bản quyền © 2026 LAMDev x DaLyMMO.com. Bảo lưu mọi quyền.
=============================================================================
Script demo tương tác trực quan 100% bằng Tiếng Việt, hỗ trợ đầy đủ các module:
Hồ sơ cá nhân, Khoảnh khắc (Ảnh/Video HEVC <6MB), Bạn bè & Nhắn tin Real-time.
"""

import os
import sys
import json
import time
from typing import Optional

# Đảm bảo đường dẫn gốc thư viện luôn được ưu tiên
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from locketlam import LocketClient, NoteType
from locketlam.exceptions import (
    LocketError,
    AuthenticationError,
    StorageUploadError,
    LocketAPIError
)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_banner(uid: Optional[str] = None):
    print("=" * 66)
    print("       🚀 LOCKETLAM CLIENT CLI - DEMO ĐẦY ĐỦ TÍNH NĂNG")
    print("         Phát triển bởi: LAMDev x DaLyMMO.com")
    print("=" * 66)
    if uid:
        masked_uid = uid[:4] + "****" + uid[-4:] if len(uid) > 8 else "****"
        print(f"  [Phiên Hoạt Động]: UID = {masked_uid} (Đã đăng nhập)")
    else:
        print("  [Phiên Hoạt Động]: Chưa đăng nhập")
    print("-" * 66)


def get_authenticated_client(session_path: str = "locketlam_session.json") -> LocketClient:
    """Khởi tạo và kiểm tra phiên đăng nhập LocketClient."""
    root_session = os.path.join(REPO_ROOT, session_path)
    if os.path.exists(root_session):
        client = LocketClient(session_path=root_session)
    else:
        client = LocketClient(session_path=session_path)

    if not client.is_authenticated():
        clear_screen()
        print_banner()
        print("Chưa tìm thấy phiên đăng nhập hợp lệ. Vui lòng đăng nhập:")
        email = input("Email Locket: ").strip()
        import getpass
        password = getpass.getpass("Mật khẩu: ").strip()
        try:
            print("Đang đăng nhập vào hệ thống máy chủ Locket...")
            client.login(email, password)
            print("Đăng nhập thành công! Đã lưu phiên hoạt động.")
            time.sleep(1)
        except Exception as e:
            print(f"Đăng nhập thất bại: {e}")
            sys.exit(1)

    return client


# =============================================================================
# CHỨC NĂNG 1: HỒ SƠ NGƯỜI DÙNG & CÀI ĐẶT
# =============================================================================
def menu_user_profile(client: LocketClient):
    while True:
        clear_screen()
        print_banner(client.session.uid)
        print("  [1] HỒ SƠ CÁ NHÂN & CÀI ĐẶT TÀI KHOẢN")
        print("  1. Xem thông tin hồ sơ của tôi (Self Profile)")
        print("  2. Tra cứu hồ sơ người dùng bằng Username")
        print("  3. Đổi Họ và Tên hiển thị")
        print("  4. Cập nhật Ngày sinh")
        print("  5. Đổi ảnh đại diện Avatar (tự nén WebP và tải lên)")
        print("  6. Đồng bộ cài đặt ứng dụng & Thông báo đẩy (Sync Client)")
        print("  0. Quay lại Menu Chính")
        print("-" * 66)
        choice = input("Nhập lựa chọn của bạn [0-6]: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            try:
                prof = client.user.get_profile()
                print("\n--- Chi Tiết Hồ Sơ Cá Nhân ---")
                print(f"Mã UID: {prof.get('uid')}")
                print(f"Tên người dùng: @{prof.get('username')}")
                print(f"Họ và Tên: {prof.get('first_name')} {prof.get('last_name')}")
                print(f"Email: {prof.get('email')}")
                print(f"Ảnh đại diện: {prof.get('profile_picture_url')}")
                print(f"Huy hiệu (Badge): {prof.get('badge')}")
            except Exception as e:
                print(f"Lỗi: {e}")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "2":
            uname = input("\nNhập Username cần tìm kiếm: ").strip()
            if uname:
                try:
                    res = client.user.get_profile_by_username(uname)
                    print("\n--- Thông Tin Người Dùng Tìm Thấy ---")
                    print(f"Mã UID: {res.get('uid')}")
                    print(f"Username: @{res.get('username')}")
                    print(f"Họ và Tên: {res.get('first_name')} {res.get('last_name')}")
                    print(f"Ảnh đại diện: {res.get('profile_picture_url')}")
                except Exception as e:
                    print(f"Tìm kiếm thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "3":
            try:
                prof = client.user.get_profile()
                curr_fn = prof.get('first_name') or ''
                curr_ln = prof.get('last_name') or ''
                print(f"\nHọ và Tên hiện tại: {curr_fn} {curr_ln}".strip())
                print(f"- First Name hiện tại: '{curr_fn}'")
                print(f"- Last Name hiện tại:  '{curr_ln}'")
            except Exception:
                curr_fn, curr_ln = '', ''

            fn = input("\nNhập Tên mới (First Name) [Enter để giữ nguyên]: ").strip()
            ln = input("Nhập Họ mới (Last Name) [Enter để giữ nguyên]: ").strip()
            
            new_fn = fn if fn else curr_fn
            new_ln = ln if ln else curr_ln

            if new_fn or new_ln:
                try:
                    client.user.update_name(first_name=new_fn, last_name=new_ln)
                    print(f"Đổi tên hiển thị thành công thành: {new_fn} {new_ln}".strip())
                except Exception as e:
                    print(f"Cập nhật thất bại: {e}")
            else:
                print("Không có thông tin tên mới để cập nhật.")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "4":
            try:
                prof = client.user.get_profile()
                curr_bday = prof.get('birthdate') or 'Chưa thiết lập'
                print(f"\nNgày sinh hiện tại: {curr_bday}")
            except Exception:
                pass
            bday = input("Nhập ngày sinh mới (định dạng YYYY-MM-DD) [Enter để bỏ qua]: ").strip()
            if bday:
                try:
                    client.user.update_birthdate(bday)
                    print("Cập nhật ngày sinh thành công!")
                except Exception as e:
                    print(f"Cập nhật thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "5":
            try:
                prof = client.user.get_profile()
                curr_avatar = prof.get('profile_picture_url') or 'Chưa có ảnh'
                print(f"\nẢnh đại diện hiện tại:\n{curr_avatar}")
            except Exception:
                pass
            av_path = input("\nNhập đường dẫn file ảnh mới trong máy hoặc URL [Enter để bỏ qua]: ").strip().strip('"')
            if av_path:
                try:
                    print("Đang tải ảnh và cập nhật trên hệ thống Locket...")
                    res = client.user.update_avatar(av_path)
                    new_pic = res.get("profile_picture_url") if isinstance(res, dict) else res
                    print(f"\nĐổi avatar thành công! Link ảnh mới:\n{new_pic}")
                except Exception as e:
                    print(f"Đổi avatar thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "6":
            try:
                client.user.sync_client_data(push_notifications=True)
                print("Đồng bộ cài đặt ứng dụng thành công!")
            except Exception as e:
                print(f"Đồng bộ thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")


# =============================================================================
# CHỨC NĂNG 2: KHOẢNH KHẮC & MEDIA (ẢNH, VIDEO HEVC, BADGES)
# =============================================================================
def menu_moments(client: LocketClient):
    while True:
        clear_screen()
        print_banner(client.session.uid)
        print("  [2] KHOẢNH KHẮC & XỬ LÝ MEDIA")
        print("  1. Xem Bảng Tin Bạn Bè (get_latest)")
        print("  2. Xem Lịch Sử Các Bài Đăng Của Tôi")
        print("  3. Xem Khoảnh Khắc Của Một Người (bằng Username)")
        print("  4. Đăng Ảnh với Chữ Tiêu Chuẩn (Standard Caption)")
        print("  5. Đăng Ảnh với Preset Màu & Biểu Tượng có sẵn (158+ mẫu, tùy chỉnh chữ)")
        print("  6. Đăng Ảnh với Màu Gradient & Biểu Tượng Emoji Tự Chọn")
        print("  7. Đăng Video Dài (Hỗ trợ File / Link trực tiếp, Tùy chọn Preset & Gradient)")
        print("  8. Xem Lượt Xem & Cảm Xúc của Khoảnh Khắc (get_views)")
        print("  9. Thả Cảm Xúc Emoji vào Khoảnh Khắc của Bạn Bè")
        print("  10. Bình Luận vào Khoảnh Khắc (nhảy thẳng vào đoạn chat)")
        print("  11. Xóa Vĩnh Viễn Một Khoảnh Khắc")
        print("  0. Quay lại Menu Chính")
        print("-" * 66)
        choice = input("Nhập lựa chọn của bạn [0-11]: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            try:
                print("Đang tải bảng tin bạn bè...")
                feed = client.moments.get_latest()
                print(f"\nTổng số khoảnh khắc trong feed: {len(feed)}")
                for i, m in enumerate(feed[:10]):
                    uid = m.get("id") or m.get("canonical_uid")
                    caption = m.get("caption") or "(Không có caption)"
                    media_type = "Video" if m.get("video_url") else "Ảnh"
                    print(f" [{i+1}] [{media_type}] ID: {uid} | Người đăng: {m.get('user')}")
                    print(f"     Nội dung: {caption}")
                    if m.get("video_url"):
                        print(f"     Link Video: {m.get('video_url')[:60]}...")
            except Exception as e:
                print(f"Tải bảng tin thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "2":
            try:
                print("Đang tải toàn bộ bài đăng của bạn kèm thông tin lượt xem & thả tim...")
                my_moments = client.moments.get_all_my_moments()
                print(f"\n==================================================================")
                print(f"       📸 TOÀN BỘ BÀI ĐĂNG CỦA TÔI ({len(my_moments)} bài)")
                print(f"==================================================================")
                if not my_moments:
                    print("Bạn chưa có bài đăng nào trong lịch sử.")
                for i, m in enumerate(my_moments):
                    uid = m.get("moment_uid") or m.get("id")
                    views = m.get("views_count", 0)
                    viewers = m.get("viewers", [])
                    reactions = m.get("reactions", [])
                    thumb = m.get("thumbnail_url")
                    created_at = m.get("created_at")

                    video_url = m.get("video_url")
                    print(f"\n  [{i+1}] UID BÀI ĐĂNG: {uid} [📸 Bài đăng (Feed)]")
                    print(f"      📅 Ngày đăng: {created_at}")
                    if m.get("caption"):
                        print(f"      📝 Ghi chú / Caption: {m.get('caption')}")
                    if thumb:
                        clean_thumb = thumb.strip()
                        print(f"      🖼️ Ảnh / Thumbnail:\n{clean_thumb}")
                    if video_url:
                        clean_video = video_url.strip()
                        print(f"      🎬 Link Video:\n{clean_video}")
                    print(f"      👀 Lượt xem: {views} lượt")
                    if viewers:
                        viewer_str = ", ".join([v.get("user", "") for v in viewers])
                        print(f"         └─ Người đã xem: {viewer_str}")
                    print(f"      ❤️ Cảm xúc / Tim ({len(reactions)} tương tác):")
                    if reactions:
                        for r in reactions:
                            emo = r.get("emoji") or "❤️"
                            sender = r.get("sender", "")
                            t = r.get("created_at", "")
                            print(f"         └─ {emo} bởi {sender} ({t})")
                    else:
                        print(f"         └─ Chưa có ai thả tim/cảm xúc.")
                    print("-" * 66)

                # Option to open link in browser directly
                import webbrowser
                open_choice = input("\n[?] Bạn có muốn mở xem bài đăng nào trên Trình duyệt không? (Nhập số 1-" + str(len(my_moments)) + " hoặc ấn Enter để bỏ qua): ").strip()
                if open_choice.isdigit():
                    idx = int(open_choice) - 1
                    if 0 <= idx < len(my_moments):
                        target_m = my_moments[idx]
                        target_url = target_m.get("video_url") or target_m.get("thumbnail_url")
                        if target_url:
                            print(f"Đang mở bài đăng #{open_choice} trên trình duyệt...")
                            webbrowser.open(target_url.strip())
            except Exception as e:
                print(f"Lấy danh sách thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "3":
            uname = input("\nNhập Username cần xem bài đăng: ").strip()
            if uname:
                try:
                    user_moments = client.moments.get_shared_moments_by_username(uname, limit=5)
                    print(f"\nTìm thấy {len(user_moments)} bài đăng của @{uname}:")
                    for i, m in enumerate(user_moments):
                        uid = m.get("id") or m.get("canonical_uid")
                        print(f" [{i+1}] UID: {uid} | Caption: {m.get('caption')}")
                        if m.get("video_url"):
                            print(f"     Video: {m.get('video_url')}")
                        else:
                            print(f"     Thumbnail: {m.get('thumbnail_url')}")
                except Exception as e:
                    print(f"Tra cứu thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "4":
            img = input("\nNhập đường dẫn file ảnh (.jpg, .png) hoặc Link URL: ").strip().strip('"')
            cap = input("Nhập nội dung ghi chú (Caption): ").strip()
            priv = input("Đăng riêng tư (chỉ mình tôi xem)? [y/N]: ").strip().lower() == "y"
            if img:
                try:
                    print("Đang tải ảnh lên Locket...")
                    res = client.moments.post(image=img, caption=cap, is_private=priv)
                    print("Đăng khoảnh khắc thành công!")
                    print(f"ID bài đăng: {res.get('canonical_uid') or res.get('id')}")
                except Exception as e:
                    print(f"Đăng bài thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "5":
            img = input("\nNhập đường dẫn file ảnh (.jpg, .png) hoặc Link URL: ").strip().strip('"')
            if not img:
                input("\nChưa nhập file hoặc link ảnh. Nhấn Enter để quay lại...")
                continue

            import json
            preset_file = os.path.join(REPO_ROOT, "locketlam", "caption_presets.json")
            all_presets = []
            if os.path.exists(preset_file):
                with open(preset_file, "r", encoding="utf-8") as pf:
                    p_dict = json.load(pf)
                    for k, v in p_dict.items():
                        all_presets.append((k, v))
            else:
                all_presets = [
                    ("dang_ban_tuong_tu", {"text": "Đang bận tương tư", "icon": "💭"}),
                    ("doi_roi", {"text": "Dỗi rồi", "icon": "😤"}),
                    ("flex_den_hoi_tho_cuoi", {"text": "Flex đến hơi thở cuối", "icon": "💎"}),
                    ("party_time", {"text": "Party Time!", "icon": "🪩"}),
                    ("oach_xa_lach", {"text": "oách xà lách", "icon": "🥬"})
                ]

            page = 0
            page_size = 10
            total_pages = (len(all_presets) + page_size - 1) // page_size
            sel_badge = None

            while True:
                clear_screen()
                print("=" * 66)
                print(f"       🎨 DANH SÁCH 158+ PRESET MÀU & BIỂU TƯỢNG (TRANG {page + 1}/{total_pages})")
                print("=" * 66)
                start_idx = page * page_size
                current_items = all_presets[start_idx:start_idx + page_size]

                for idx, (p_id, p_val) in enumerate(current_items):
                    num = start_idx + idx + 1
                    t = p_val.get("text") or p_id
                    ic = p_val.get("icon") or ""
                    sec = p_val.get("section") or ""
                    sec_str = f" [{sec}]" if sec else ""
                    print(f"  [{num:3d}] {ic} {t} (Mã: {p_id}){sec_str}")

                print("-" * 66)
                print("  [N] Trang sau  |  [P] Trang trước  |  [S] Tìm kiếm  |  [0] Hủy bỏ")
                print("  👉 Nhập SỐ THỨ TỰ nhãn [1-{}] hoặc MÃ PRESET để chọn:".format(len(all_presets)))
                p_in = input("Lựa chọn của bạn: ").strip()

                if p_in == "0":
                    break
                elif p_in.lower() == "n":
                    if page + 1 < total_pages:
                        page += 1
                elif p_in.lower() == "p":
                    if page > 0:
                        page -= 1
                elif p_in.lower() == "s":
                    q = input("Nhập từ khóa tìm kiếm: ").strip().lower()
                    matches = [(i + 1, k, v) for i, (k, v) in enumerate(all_presets) if q in k.lower() or q in (v.get("text") or "").lower()]
                    print(f"\nTìm thấy {len(matches)} nhãn phù hợp:")
                    for m_num, m_id, m_val in matches[:15]:
                        print(f"  [{m_num}] {m_val.get('icon', '')} {m_val.get('text', m_id)} (Mã: {m_id})")
                    chosen = input("\nNhập số thứ tự nhãn muốn chọn (Enter để quay lại): ").strip()
                    if chosen.isdigit() and 1 <= int(chosen) <= len(all_presets):
                        sel_badge = all_presets[int(chosen) - 1][0]
                        break
                elif p_in.isdigit():
                    val = int(p_in)
                    if 1 <= val <= len(all_presets):
                        sel_badge = all_presets[val - 1][0]
                        break
                    else:
                        print("Số thứ tự không hợp lệ.")
                        time.sleep(1)
                elif any(p_in.lower() == k.lower() for k, _ in all_presets):
                    sel_badge = p_in.lower()
                    break

            if sel_badge:
                try:
                    custom_cap = input("Nhập ghi chú tùy chỉnh (Enter để giữ chữ mặc định của nhãn): ").strip()
                    print(f"\nĐang đăng bài với nhãn '{sel_badge}'...")
                    res = client.moments.post(image=img, note_type=sel_badge, caption=custom_cap)
                    print("Đăng bài thành công!")
                    print(f"ID bài đăng: {res.get('canonical_uid') or res.get('id')}")
                except Exception as e:
                    print(f"Đăng bài thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "6":
            img = input("\nNhập đường dẫn file ảnh (.jpg, .png) hoặc Link URL: ").strip().strip('"')
            cap = input("Nhập tiêu đề chữ trên nhãn: ").strip()
            icon = input("Nhập biểu tượng Emoji (ví dụ: 🔥, 🚀, ✨): ").strip() or "✨"
            c1 = input("Mã màu HEX bắt đầu (ví dụ: #FF416C): ").strip() or "#FF416C"
            c2 = input("Mã màu HEX kết thúc (ví dụ: #8A2387): ").strip() or "#8A2387"
            if img:
                try:
                    print("Đang tạo nhãn màu gradient tùy chọn và tải lên...")
                    res = client.moments.post(
                        image=img,
                        caption=cap,
                        icon=icon,
                        colors=[c1, c2],
                        text_color="#FFFFFF"
                    )
                    print("Đăng bài thành công!")
                    print(f"ID bài đăng: {res.get('canonical_uid') or res.get('id')}")
                except Exception as e:
                    print(f"Đăng bài thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "7":
            print("\n==================================================================")
            print("       🎬 ĐĂNG VIDEO KHOẢNH KHẮC (HỖ TRỢ TÙY CHỌN NOTE & NHÃN)")
            print("==================================================================")
            vid_path = input("Nhập đường dẫn file video (.mp4) hoặc Link URL video: ").strip().strip('"')
            if not vid_path:
                input("\nChưa nhập video. Nhấn Enter để quay lại...")
                continue

            thumb_path = input("Nhập ảnh đại diện thumbnail (file/URL hoặc Enter để tự trích xuất): ").strip().strip('"') or None

            # 1. Chọn kiểu Note / Nhãn đi kèm
            print("\nChọn kiểu hiển thị ghi chú (Note Style):")
            print("  1. Chữ tiêu chuẩn (Standard Caption)")
            print("  2. Nhãn màu Preset có sẵn (Chọn từ danh sách 158+ mẫu Locket)")
            print("  3. Nhãn Gradient & Emoji tự chọn màu sắc")
            print("  4. Không kèm chữ (Đăng video gốc)")
            n_choice = input("Lựa chọn của bạn [1-4, Mặc định: 1]: ").strip() or "1"

            v_note_type = NoteType.STANDARD
            v_caption = ""
            v_icon = None
            v_colors = None

            if n_choice == "1":
                v_caption = input("Nhập nội dung ghi chú (Caption): ").strip()
            elif n_choice == "2":
                import json
                preset_file = os.path.join(REPO_ROOT, "locketlam", "caption_presets.json")
                all_presets = []
                if os.path.exists(preset_file):
                    with open(preset_file, "r", encoding="utf-8") as pf:
                        p_dict = json.load(pf)
                        for k, v in p_dict.items():
                            all_presets.append((k, v))

                sel_badge = None
                page = 0
                page_size = 20
                total_pages = (len(all_presets) + page_size - 1) // page_size if all_presets else 1

                while True:
                    clear_screen()
                    print("=" * 66)
                    print(f"       🎨 CHỌN PRESET CHO VIDEO (TRANG {page + 1}/{total_pages})")
                    print("=" * 66)
                    start_idx = page * page_size
                    current_items = all_presets[start_idx:start_idx + page_size]

                    for idx, (p_id, p_val) in enumerate(current_items):
                        num = start_idx + idx + 1
                        t = p_val.get("text") or p_id
                        ic = p_val.get("icon") or ""
                        sec = p_val.get("section") or ""
                        sec_str = f" [{sec}]" if sec else ""
                        print(f"  [{num:3d}] {ic} {t} (Mã: {p_id}){sec_str}")

                    print("-" * 66)
                    print("  [N] Trang sau  |  [P] Trang trước  |  [S] Tìm kiếm  |  [0] Hủy bỏ")
                    print("  👉 Nhập SỐ THỨ TỰ nhãn [1-{}] hoặc MÃ PRESET:".format(len(all_presets)))
                    p_in = input("Lựa chọn của bạn: ").strip()

                    if p_in == "0":
                        break
                    elif p_in.lower() == "n":
                        if page + 1 < total_pages:
                            page += 1
                    elif p_in.lower() == "p":
                        if page > 0:
                            page -= 1
                    elif p_in.lower() == "s":
                        q = input("Nhập từ khóa tìm kiếm: ").strip().lower()
                        matches = [(i + 1, k, v) for i, (k, v) in enumerate(all_presets) if q in k.lower() or q in (v.get("text") or "").lower()]
                        print(f"\nTìm thấy {len(matches)} nhãn phù hợp:")
                        for m_num, m_id, m_val in matches[:15]:
                            print(f"  [{m_num}] {m_val.get('icon', '')} {m_val.get('text', m_id)} (Mã: {m_id})")
                        chosen = input("\nNhập số thứ tự nhãn muốn chọn (Enter để quay lại): ").strip()
                        if chosen.isdigit() and 1 <= int(chosen) <= len(all_presets):
                            sel_badge = all_presets[int(chosen) - 1][0]
                            break
                    elif p_in.isdigit():
                        val = int(p_in)
                        if 1 <= val <= len(all_presets):
                            sel_badge = all_presets[val - 1][0]
                            break
                        else:
                            print("Số thứ tự không hợp lệ.")
                            time.sleep(1)
                    elif any(p_in.lower() == k.lower() for k, _ in all_presets):
                        sel_badge = p_in.lower()
                        break

                v_note_type = sel_badge if sel_badge else NoteType.STANDARD
                v_caption = input("\nNhập ghi chú tùy chỉnh trên nhãn (Enter để giữ chữ mặc định): ").strip()
            elif n_choice == "3":
                v_caption = input("Nhập tiêu đề chữ trên nhãn: ").strip()
                v_icon = input("Nhập biểu tượng Emoji (ví dụ: 🔥, 🎵, ✨) [Mặc định: 🎵]: ").strip() or "🎵"
                c1 = input("Mã màu HEX bắt đầu [Mặc định: #FF416C]: ").strip() or "#FF416C"
                c2 = input("Mã màu HEX kết thúc [Mặc định: #8A2387]: ").strip() or "#8A2387"
                v_colors = [c1, c2]

            is_video_url = vid_path.startswith("http://") or vid_path.startswith("https://")
            v_priority = "balanced"
            is_locket_storage = is_video_url and "firebasestorage.googleapis.com" in vid_path
            v_priority = "balanced"
            show_progress = None

            # 2. Tùy chọn thứ tự ưu tiên khi nén (áp dụng cho cả file cục bộ và link video bên ngoài nếu cần nén)
            if not is_locket_storage:
                print("\nTùy chọn chế độ nén video:")
                print("  1. Dùng mặc định (Tự cân đối tối ưu cả hình ảnh & âm thanh)")
                print("  2. Tự chọn thứ tự ưu tiên (Ưu tiên tiếng/nghe nhạc cao cấp)")
                prio_mode = input("Lựa chọn chế độ nén [1-2, Mặc định: 1]: ").strip() or "1"
                if prio_mode == "2":
                    print("  -> Các mức ưu tiên:")
                    print("     [A] Ưu tiên âm thanh / Nghe nhạc (Giữ trọn chất lượng nhạc cực nét 160kbps)")
                    print("     [V] Ưu tiên hình ảnh / Độ phân giải cao nhất")
                    sub_p = input("  Chọn mức ưu tiên [A/V, Mặc định: A]: ").strip().lower()
                    v_priority = "audio" if sub_p != "v" else "video"

                # Hàm thanh tiến trình hiển thị %
                def show_progress(pct, msg):
                    bar_len = 30
                    filled = int(bar_len * pct / 100)
                    bar = "█" * filled + "░" * (bar_len - filled)
                    sys.stdout.write(f"\r  [{bar}] {pct:3d}% | {msg}")
                    sys.stdout.flush()

            try:
                if is_locket_storage:
                    print("\nĐang đăng video trực tiếp từ Link Locket Storage (bỏ qua bước upload/nén)...")
                elif is_video_url:
                    print(f"\nĐang tải video từ URL, nén thông minh ({v_priority.upper()}) và tải lên Locket...")
                else:
                    print(f"\nĐang xử lý nén và đăng video (Chế độ: {v_priority.upper()})...")
                res = client.moments.post(
                    image=thumb_path,
                    video=vid_path,
                    caption=v_caption,
                    note_type=v_note_type,
                    icon=v_icon,
                    colors=v_colors,
                    priority=v_priority,
                    progress_callback=show_progress
                )
                print("\n\nĐăng video khoảnh khắc thành công!")
                print(f"ID bài đăng: {res.get('canonical_uid') or res.get('id')}")
                print(f"Link Video Storage: {res.get('video_url')}")
            except Exception as e:
                print(f"\nĐăng video thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "8":
            m_id = input("\nNhập UID bài đăng cần kiểm tra: ").strip()
            if m_id:
                try:
                    views = client.moments.get_views(m_id)
                    print(f"\n==================================================================")
                    print(f"       👀 CHI TIẾT BÀI ĐĂNG: {m_id}")
                    print(f"==================================================================")
                    print(f"  Tổng số lượt xem: {views.get('count', 0)} lượt")
                    v_list = views.get("moment_views", [])
                    if v_list:
                        print("  Danh sách người đã xem:")
                        for v in v_list:
                            v_u = v.get("user")
                            v_t = v.get("viewed_at", {})
                            sec = v_t.get("_seconds") if isinstance(v_t, dict) else v_t
                            print(f"    └─ User: {v_u} (Thời gian: {sec})")
                    else:
                        print("  Chưa có lượt xem nào.")

                    r_list = views.get("reactions", [])
                    print(f"\n  Danh sách cảm xúc / Tim ({len(r_list)} tương tác):")
                    if r_list:
                        for r in r_list:
                            emo = r.get("emoji") or "❤️"
                            sender = r.get("sender", "")
                            t = r.get("created_at", "")
                            print(f"    └─ {emo} bởi {sender} ({t})")
                    else:
                        print("    └─ Chưa có ai thả tim/cảm xúc.")
                    print("-" * 66)
                except Exception as e:
                    print(f"Truy vấn thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "9":
            m_id = input("\nNhập UID bài đăng bạn bè để thả icon: ").strip()
            emoji = input("Nhập emoji reaction [Mặc định: ❤️]: ").strip() or "❤️"
            if m_id:
                try:
                    client.moments.react(moment_uid=m_id, reaction=emoji)
                    print(f"Đã thả biểu cảm {emoji} vào bài đăng {m_id} thành công!")
                except Exception as e:
                    print(f"Thả cảm xúc thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "10":
            m_id = input("\nNhập UID bài đăng để bình luận: ").strip()
            r_uid = input("Nhập UID bạn bè (chủ bài đăng): ").strip()
            text = input("Nhập nội dung bình luận: ").strip()
            if m_id and r_uid and text:
                try:
                    res = client.moments.comment(moment_uid=m_id, receiver_uid=r_uid, text=text)
                    print("Bình luận thành công! Đã nhảy vào đoạn chat.")
                    print(f"Mã tin nhắn: {res.get('msg_id') or res.get('id')}")
                except Exception as e:
                    print(f"Bình luận thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "11":
            m_id = input("\nNhập UID bài đăng cần XÓA VĨNH VIỄN: ").strip()
            confirm = input(f"Bạn có chắc chắn muốn xóa bài {m_id} không? [y/N]: ").strip().lower()
            if confirm == "y":
                try:
                    client.moments.delete(moment_uid=m_id)
                    print(f"Đã xóa bài đăng {m_id} thành công.")
                except Exception as e:
                    print(f"Xóa thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")


# =============================================================================
# CHỨC NĂNG 3: BẠN BÈ & QUẢN LÝ QUAN HỆ
# =============================================================================
def menu_friends(client: LocketClient):
    while True:
        clear_screen()
        print_banner(client.session.uid)
        print("  [3] QUẢN LÝ BẠN BÈ & NHÓM")
        print("  1. Xem danh sách tất cả bạn bè (Họ tên, Username, Avatar, UID)")
        print("  2. Xem trạng thái nhóm và bạn bè")
        print("  3. Phân giải link mời từ Username (locket.cam/<user>)")
        print("  4. Gửi lời mời kết bạn bằng Username")
        print("  5. Gửi lời mời kết bạn bằng User UID")
        print("  6. Đồng ý lời mời kết bạn từ người khác")
        print("  7. Hủy kết bạn (Unfriend)")
        print("  8. Chặn người dùng (Block User)")
        print("  9. Bỏ chặn người dùng (Unblock User)")
        print("  0. Quay lại Menu Chính")
        print("-" * 66)
        choice = input("Nhập lựa chọn của bạn [0-9]: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            try:
                friends = client.friends.get_all_friends()
                print(f"\nTổng số bạn bè: {len(friends)}")
                for i, f in enumerate(friends):
                    name = f"{f.get('first_name', '')} {f.get('last_name', '')}".strip()
                    uname = f.get('username') or '(Chưa đặt username)'
                    uid = f.get('uid')
                    print(f" [{i+1}] {name} (@{uname}) | UID: {uid}")
            except Exception as e:
                print(f"Lấy danh sách bạn bè thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "2":
            try:
                groups = client.friends.get_groups_and_friends()
                print("\nDanh Sách Nhóm:")
                print(json.dumps(groups, indent=2, ensure_ascii=False))
            except Exception as e:
                print(f"Lỗi: {e}")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "3":
            uname = input("\nNhập Username để lấy mã mời token: ").strip()
            if uname:
                try:
                    token = client.friends.resolve_invite_token_from_username(uname)
                    print(f"\nMã mời (Invite Token) của @{uname}: {token}")
                    user_info = client.friends.fetch_user_by_invite_token(token)
                    print(f"Hồ sơ: {user_info.get('first_name')} {user_info.get('last_name')}")
                    print(f"Trạng thái kết bạn: {user_info.get('friendship_status')}")
                except Exception as e:
                    print(f"Phân giải thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "4":
            uname = input("\nNhập Username để gửi kết bạn: ").strip()
            if uname:
                try:
                    res = client.friends.send_request_by_username(uname)
                    print(f"Đã gửi lời mời kết bạn tới @{uname} thành công!")
                except Exception as e:
                    print(f"Gửi kết bạn thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "5":
            target_uid = input("\nNhập UID người dùng để kết bạn: ").strip()
            if target_uid:
                try:
                    client.friends.send_request(user_uid=target_uid)
                    print(f"Đã gửi lời mời kết bạn tới UID {target_uid} thành công!")
                except Exception as e:
                    print(f"Gửi kết bạn thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "6":
            try:
                print("\nĐang tải danh sách lời mời kết bạn đang chờ...")
                requests_data = client.friends.get_friend_requests()
                incoming = requests_data.get("incoming", [])
                if not incoming:
                    print("Không có lời mời kết bạn nào đang chờ duyệt.")
                    target_uid = input("\nHoặc nhập trực tiếp UID người gửi (Enter để quay lại): ").strip()
                else:
                    print(f"\nTìm thấy {len(incoming)} lời mời kết bạn:")
                    for idx, user in enumerate(incoming, 1):
                        name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip() or "Ẩn danh"
                        uname = user.get('username') or 'N/A'
                        uid = user.get('uid') or 'N/A'
                        print(f"  [{idx}] {name} (@{uname}) | UID: {uid}")
                    
                    sel = input(f"\nNhập số thứ tự để đồng ý [1-{len(incoming)}] hoặc nhập UID trực tiếp (Enter để hủy): ").strip()
                    if sel.isdigit() and 1 <= int(sel) <= len(incoming):
                        target_uid = incoming[int(sel) - 1].get("uid")
                    else:
                        target_uid = sel

                if target_uid:
                    client.friends.accept_request(user_uid=target_uid)
                    print(f"Đã đồng ý kết bạn với {target_uid} thành công!")
            except Exception as e:
                print(f"Đồng ý kết bạn thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "7":
            try:
                print("\nĐang tải danh sách bạn bè hiện tại...")
                friends = client.friends.get_all_friends()
                if not friends:
                    print("Bạn chưa có bạn bè nào trong danh sách.")
                    target = input("\nHoặc nhập trực tiếp UID/Username để hủy kết bạn (Enter để quay lại): ").strip()
                else:
                    print(f"\nDanh sách {len(friends)} bạn bè hiện tại:")
                    for idx, f in enumerate(friends, 1):
                        name = f"{f.get('first_name', '')} {f.get('last_name', '')}".strip() or "Ẩn danh"
                        uname = f.get('username') or 'N/A'
                        uid = f.get('uid') or 'N/A'
                        print(f"  [{idx}] {name} (@{uname}) | UID: {uid}")

                    sel = input(f"\nNhập số thứ tự bạn bè muốn HỦY KẾT BẠN [1-{len(friends)}] (hoặc nhập UID/Username, Enter để hủy): ").strip()
                    if sel.isdigit() and 1 <= int(sel) <= len(friends):
                        target = friends[int(sel) - 1].get("uid")
                    else:
                        target = sel

                if target:
                    confirm = input(f"Bạn có chắc chắn muốn hủy kết bạn với '{target}'? (y/n): ").strip().lower()
                    if confirm in ("y", "yes"):
                        client.friends.remove(user_uid=target)
                        print(f"Đã hủy kết bạn với '{target}' thành công.")
                    else:
                        print("Đã hủy thao tác.")
            except Exception as e:
                print(f"Hủy kết bạn thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "8":
            try:
                print("\nĐang tải danh sách bạn bè...")
                friends = client.friends.get_all_friends()
                if friends:
                    print(f"\nDanh sách bạn bè hiện tại ({len(friends)} người):")
                    for idx, f in enumerate(friends, 1):
                        name = f"{f.get('first_name', '')} {f.get('last_name', '')}".strip() or "Ẩn danh"
                        uname = f.get('username') or 'N/A'
                        uid = f.get('uid') or 'N/A'
                        print(f"  [{idx}] {name} (@{uname}) | UID: {uid}")

                    sel = input(f"\nNhập số thứ tự để CHẶN [1-{len(friends)}] hoặc nhập UID/Username bất kỳ (Enter để hủy): ").strip()
                    if sel.isdigit() and 1 <= int(sel) <= len(friends):
                        target = friends[int(sel) - 1].get("uid")
                    else:
                        target = sel
                else:
                    target = input("\nNhập UID hoặc Username của người dùng để CHẶN (BLOCK): ").strip()

                if target:
                    confirm = input(f"Bạn có chắc muốn CHẶN '{target}' không? (y/n): ").strip().lower()
                    if confirm in ("y", "yes"):
                        client.friends.block(user_uid=target)
                        print(f"Đã CHẶN người dùng '{target}' thành công.")
                    else:
                        print("Đã hủy thao tác.")
            except Exception as e:
                print(f"Chặn thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "9":
            try:
                import urllib.request, json
                print("\nĐang tải danh sách người dùng đã bị chặn...")
                token = client.session.get_valid_token()
                my_uid = client.session.uid
                b_url = f"https://firestore.googleapis.com/v1/projects/locket-4252a/databases/(default)/documents/users/{my_uid}/blocked_users"
                b_req = urllib.request.Request(b_url, headers={"Authorization": f"Bearer {token}"})
                blocked_list = []
                try:
                    with urllib.request.urlopen(b_req, timeout=5) as b_resp:
                        b_data = json.loads(b_resp.read().decode("utf-8"))
                        for doc in b_data.get("documents", []):
                            b_uid = doc["name"].split("/")[-1]
                            try:
                                p = client.user.get_profile(b_uid)
                                blocked_list.append(p)
                            except Exception:
                                blocked_list.append({"uid": b_uid})
                except Exception:
                    pass

                if blocked_list:
                    print(f"\nDanh sách {len(blocked_list)} người dùng đang bị chặn:")
                    for idx, b in enumerate(blocked_list, 1):
                        name = f"{b.get('first_name', '')} {b.get('last_name', '')}".strip() or "Ẩn danh"
                        uname = b.get('username') or 'N/A'
                        uid = b.get('uid') or 'N/A'
                        print(f"  [{idx}] {name} (@{uname}) | UID: {uid}")

                    sel = input(f"\nNhập số thứ tự để BỎ CHẶN [1-{len(blocked_list)}] hoặc nhập UID/Username trực tiếp (Enter để hủy): ").strip()
                    if sel.isdigit() and 1 <= int(sel) <= len(blocked_list):
                        target = blocked_list[int(sel) - 1].get("uid")
                    else:
                        target = sel
                else:
                    print("Hiện tại danh sách chặn của bạn đang trống.")
                    target = input("\nNhập UID hoặc Username của người dùng để BỎ CHẶN (UNBLOCK): ").strip()

                if target:
                    client.friends.unblock(user_uid=target)
                    print(f"Đã BỎ CHẶN người dùng '{target}' thành công.")
            except Exception as e:
                print(f"Bỏ chặn thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")


# =============================================================================
# CHỨC NĂNG 4: NHẮN TIN & WEBSOCKET THỜI GIAN THỰC
# =============================================================================
def menu_chat(client: LocketClient):
    while True:
        clear_screen()
        print_banner(client.session.uid)
        print("  [4] NHẮN TIN TRỰC TIẾP & WEBSOCKET REAL-TIME")
        print("  1. Xem danh sách hộp thư các cuộc trò chuyện")
        print("  2. Xem lịch sử tin nhắn trong cuộc trò chuyện")
        print("  3. Gửi tin nhắn văn bản")
        print("  4. Chia sẻ khoảnh khắc vào cuộc trò chuyện")
        print("  5. Thả cảm xúc Emoji vào tin nhắn chat")
        print("  6. Thu hồi / Xóa tin nhắn đã gửi")
        print("  7. Đánh dấu cuộc trò chuyện đã đọc")
        print("  8. Bật lắng nghe tin nhắn trực tiếp qua WebSocket (Real-Time)")
        print("  0. Quay lại Menu Chính")
        print("-" * 66)
        choice = input("Nhập lựa chọn của bạn [0-8]: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            try:
                convs = client.chat.get_conversations()
                print(f"\nTổng số cuộc trò chuyện: {len(convs)}")
                for i, c in enumerate(convs[:10]):
                    cid = c.get("id") or c.get("conversation_id")
                    parts = c.get("participants", [])
                    last_msg = c.get("last_message", {}).get("text", "(Tin nhắn đa phương tiện)")
                    print(f" [{i+1}] ID Đoạn Chat: {cid} | Thành viên: {parts}")
                    print(f"     Tin nhắn cuối: {last_msg}")
            except Exception as e:
                print(f"Lấy danh sách trò chuyện thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "2":
            other_uid = input("\nNhập UID bạn bè để xem tin nhắn: ").strip()
            if other_uid:
                try:
                    msgs = client.chat.get_messages(other_user_id=other_uid)
                    print(f"\nLịch sử tin nhắn ({len(msgs)} tin nhắn):")
                    for m in msgs[-15:]:
                        sender = "Tôi" if m.get("sender") == client.session.uid else "Bạn bè"
                        mid = m.get("id") or m.get("msg_id")
                        print(f" [{sender}] ({mid}): {m.get('text', '')}")
                except Exception as e:
                    print(f"Lấy tin nhắn thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "3":
            r_uid = input("\nNhập UID bạn bè cần gửi tin nhắn: ").strip()
            text = input("Nhập nội dung tin nhắn: ").strip()
            if r_uid and text:
                try:
                    res = client.chat.send_message(receiver_uid=r_uid, text=text)
                    print("Gửi tin nhắn thành công!")
                    print(f"Mã tin nhắn: {res.get('msg_id') or res.get('id')}")
                except Exception as e:
                    print(f"Gửi thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "4":
            r_uid = input("\nNhập UID bạn bè cần gửi: ").strip()
            m_uid = input("Nhập UID bài đăng khoảnh khắc cần chia sẻ: ").strip()
            text = input("Lời nhắn đi kèm (Enter để gửi bài độc lập): ").strip()
            if r_uid and m_uid:
                try:
                    res = client.chat.send_moment(receiver_uid=r_uid, moment_uid=m_uid, text=text or None)
                    print("Chia sẻ bài đăng vào đoạn chat thành công!")
                    print(f"Mã tin nhắn: {res.get('msg_id') or res.get('id')}")
                except Exception as e:
                    print(f"Chia sẻ thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "5":
            c_id = input("\nNhập ID cuộc trò chuyện: ").strip()
            m_id = input("Nhập ID tin nhắn cần thả icon: ").strip()
            emoji = input("Nhập emoji (ví dụ: ❤️, 🔥, 👍): ").strip() or "❤️"
            if c_id and m_id:
                try:
                    client.chat.send_reaction(conversation_id=c_id, message_id=m_id, emoji=emoji)
                    print(f"Đã thả cảm xúc {emoji} vào tin nhắn {m_id} thành công!")
                except Exception as e:
                    print(f"Thả cảm xúc thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "6":
            c_id = input("\nNhập ID cuộc trò chuyện: ").strip()
            m_id = input("Nhập ID tin nhắn cần thu hồi: ").strip()
            if c_id and m_id:
                try:
                    client.chat.delete_message(conversation_uid=c_id, message_uid=m_id)
                    print(f"Đã thu hồi tin nhắn {m_id} thành công.")
                except Exception as e:
                    print(f"Thu hồi thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "7":
            c_id = input("\nNhập ID cuộc trò chuyện: ").strip()
            ghost = input("Chế độ ẩn danh Ghost mode (đọc không hiện thông báo đã xem)? [y/N]: ").strip().lower() == "y"
            if c_id:
                try:
                    client.chat.mark_as_read(conversation_uid=c_id, send_read_receipt=not ghost)
                    print(f"Đã đánh dấu cuộc trò chuyện {c_id} là đã đọc.")
                except Exception as e:
                    print(f"Thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")

        elif choice == "8":
            target_input = input("\nNhập UID hoặc Username bạn bè cần nghe tin nhắn (Enter để tự chọn bạn bè): ").strip()
            target_friend = target_input
            if not target_friend:
                try:
                    friends = client.friends.get_all_friends()
                    if friends:
                        target_friend = friends[0].get("uid")
                except Exception:
                    pass
            print(f"\nĐang kết nối tới máy chủ WebSocket: wss://api.locketcamera.com/wss_v2/chat...")
            print(f"Đang lắng nghe tin nhắn trực tiếp với bạn bè: {target_friend or 'Toàn bộ'}. Bấm Ctrl+C để thoát.\n")
            import asyncio

            async def handle_msg(msg):
                print(f"\n[SỰ KIỆN WEBSOCKET MỚI] Từ {msg.get('sender')}: {msg.get('text')}")

            try:
                asyncio.run(client.chat.listen_realtime(target_friend or client.session.uid, handle_msg))
            except KeyboardInterrupt:
                print("\nĐã dừng lắng nghe WebSocket.")
            except Exception as e:
                print(f"Lỗi WebSocket: {e}")
            input("\nNhấn Enter để tiếp tục...")


# =============================================================================
# ĐIỂM BẮT ĐẦU CHÍNH (MAIN MENU)
# =============================================================================
def main():
    client = get_authenticated_client()

    while True:
        clear_screen()
        print_banner(client.session.uid)
        print("  MENU CHÍNH - HÃY CHỌN MỘT MODULE ĐỂ TRẢI NGHIỆM:")
        print("  [1] Hồ Sơ Cá Nhân & Cài Đặt Tài Khoản")
        print("  [2] Khoảnh Khắc (Đăng Ảnh, Video Dài HEVC, Nhãn Màu, Thả Icon)")
        print("  [3] Quản Lý Bạn Bè & Nhóm")
        print("  [4] Nhắn Tin Trực Tiếp & WebSocket Thời Gian Thực")
        print("  [5] Làm Mới Thủ Công Token Phiên (Firebase JWT Refresh)")
        print("  [6] Đổi Tài Khoản Khác / Đăng Nhập Bằng Email & Mật Khẩu")
        print("  [0] Thoát Chương Trình")
        print("-" * 66)
        choice = input("Nhập lựa chọn của bạn [0-6]: ").strip()

        if choice == "0":
            print("\nCảm ơn bạn đã sử dụng thư viện locketlam! Chúc bạn một ngày tốt lành. 👋\n")
            break
        elif choice == "1":
            menu_user_profile(client)
        elif choice == "2":
            menu_moments(client)
        elif choice == "3":
            menu_friends(client)
        elif choice == "4":
            menu_chat(client)
        elif choice == "5":
            try:
                client.session.refresh()
                print("\nĐã làm mới token phiên đăng nhập thành công với Locket!")
            except Exception as e:
                print(f"\nLàm mới token thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")
        elif choice == "6":
            print("\n--- Đăng Nhập Vào Tài Khoản Khác ---")
            email = input("Email: ").strip()
            import getpass
            password = getpass.getpass("Mật khẩu: ").strip()
            if email and password:
                try:
                    print("Đang đăng nhập vào máy chủ Locket...")
                    client.login(email, password)
                    print(f"Đăng nhập thành công! UID đang hoạt động: {client.session.uid}")
                except Exception as e:
                    print(f"Đăng nhập thất bại: {e}")
            input("\nNhấn Enter để tiếp tục...")


if __name__ == "__main__":
    main()
