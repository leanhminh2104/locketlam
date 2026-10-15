#!/usr/bin/env python3
"""
=============================================================================
  💬 VÍ DỤ 7: NHẮN TIN, THẢ TIM TIN NHẮN, CHIA SẺ KHOẢNH KHẮC & XEM ẨN DANH (CHAT MODULE)
  Thư viện: locketlam
=============================================================================

Mục tiêu file này:
  1. Lấy danh sách hộp thư đến (Inbox / Conversations) kèm số tin chưa đọc.
  2. Đọc toàn bộ lịch sử tin nhắn 2 chiều trực tiếp từ database Firestore.
  3. Gửi tin nhắn văn bản, emoji tới bạn bè.
  4. Chia sẻ trực tiếp bài đăng khoảnh khắc vào đoạn chat (`send_moment`).
     (Hỗ trợ gửi bài độc lập không cần caption hoặc kèm tin nhắn).
  5. Thả biểu cảm cảm xúc (Reaction) vào tin nhắn của bạn bè (`send_reaction`).
     Hỗ trợ bất kỳ icon hoặc combo nhiều icon (`"❤️"`, `"🔥🥰"`, `"❤️❤️❤️❤️❤️"`).
  6. Gỡ bỏ cảm xúc khỏi tin nhắn (`remove_reaction`).
  7. Thu hồi / xóa tin nhắn do mình gửi (`delete_message`).
  8. Đánh dấu đã đọc ở chế độ ẩn danh (`send_read_receipt=False` - không hiện 'Đã xem').
  9. Lắng nghe tin nhắn mới thời gian thực qua WebSocket (`listen_realtime`).
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
TARGET_FRIEND_UID = ""       # <-- Nhập UID của bạn bè muốn nhắn tin / test
MESSAGE_TO_SEND = "Chào bạn! Đây là tin nhắn tự động từ thư viện LocketLam 🚀"


def main():
    print("=" * 60)
    print("💬 DEMO: NHẮN TIN CHAT, REACTION & ĐỒNG BỘ TIN NHẮN LOCKET")
    print("=" * 60)

    if not client.is_authenticated():
        print("❌ Chưa đăng nhập! Vui lòng chạy file '01_login_and_session.py' trước.")
        return

    try:
        # =====================================================================
        # 1. LẤY HỘP THƯ ĐẾN (DANH SÁCH CUỘC TRÒ CHUYỆN)
        # =====================================================================
        print("\n📬 Đang tải danh sách cuộc trò chuyện trong Inbox...")
        conversations = client.chat.get_conversations()
        print(f"👉 Tìm thấy {len(conversations)} cuộc trò chuyện.")

        selected_friend_uid = TARGET_FRIEND_UID
        selected_conv_id = None

        for idx, conv in enumerate(conversations[:5], 1):
            c_id = conv.get("id") or conv.get("conversation_id")
            other_uid = conv.get("other_user_id") or conv.get("recipient_id")
            unread = conv.get("unread_count", 0)
            last_msg = conv.get("last_message", {}).get("text", "")
            print(f"   [{idx}] Hội thoại ID: {c_id}")
            print(f"       Bạn bè UID  : {other_uid}")
            print(f"       Chưa đọc    : {unread} tin")
            print(f"       Tin cuối    : {last_msg}")

            if not selected_friend_uid and other_uid:
                selected_friend_uid = other_uid
                selected_conv_id = c_id

        # =====================================================================
        # 2. XEM LỊCH SỬ TIN NHẮN (ĐỒNG BỘ FIRESTORE TRỰC TIẾP)
        # =====================================================================
        if selected_friend_uid:
            print(f"\n📜 Đang tải lịch sử tin nhắn với UID: {selected_friend_uid}...")
            messages = client.chat.get_messages(other_user_id=selected_friend_uid, fetch_server=True)
            print(f"👉 Tổng số tin nhắn tải về: {len(messages)}")

            for m in messages[-5:]:  # In 5 tin nhắn gần nhất
                sender = "Bạn" if m.get("sender_id") == client.session.uid else "Đối phương"
                txt = m.get("text") or "[Media/Moment]"
                m_id = m.get("id") or m.get("message_id")
                print(f"   - [{sender}] {txt} (ID: {m_id})")

        # =====================================================================
        # 3. GỬI TIN NHẮN VĂN BẢN (client.chat.send_message)
        # =====================================================================
        if selected_friend_uid and TARGET_FRIEND_UID:
            print(f"\n📤 Đang gửi tin nhắn tới {selected_friend_uid}...")
            res_msg = client.chat.send_message(
                receiver_uid=selected_friend_uid,
                text=MESSAGE_TO_SEND
            )
            print(f"🎉 Gửi tin nhắn thành công! ID tin: {res_msg.get('id')}")

        # =====================================================================
        # 4. CHIA SẺ KHOẢNH KHẮC VÀO CHAT (send_moment)
        # =====================================================================
        # Có thể chia sẻ bất kỳ khoảnh khắc nào (kèm text hoặc không cần text):
        # client.chat.send_moment(
        #     receiver_uid=selected_friend_uid,
        #     moment_uid="MOMENT_UID_CAN_CHIA_SE",
        #     text="Xem cái này hài chưa nè 😂"  # Để None nếu chỉ muốn gửi ảnh/video thuần
        # )

        # =====================================================================
        # 5. THẢ BIỂU CẢM (REACTION) VÀO TIN NHẮN BẠN BÈ
        # =====================================================================
        # Hỗ trợ bất kỳ icon hoặc combo icon: "❤️", "🔥", "❤️❤️❤️❤️❤️"
        # client.chat.send_reaction(
        #     conversation_id=selected_conv_id,
        #     message_id="MESSAGE_ID_CUA_BAN_BE",
        #     emoji="🔥"
        # )

        # =====================================================================
        # 6. ĐÁNH DẤU ĐÃ ĐỌC Ở CHẾ ĐỘ ẨN DANH (KHÔNG HIỆN 'ĐÃ XEM')
        # =====================================================================
        if selected_friend_uid:
            print(f"\n👁️ Đang đánh dấu đã đọc ở chế độ ẩn danh (send_read_receipt=False)...")
            client.chat.mark_as_read(
                other_user_id=selected_friend_uid,
                send_read_receipt=False  # Không cho đối phương biết mình đã đọc
            )
            print("✅ Đã đánh dấu đọc thành công trong im lặng!")

    except LocketError as e:
        print(f"❌ Có lỗi: {e}")


if __name__ == "__main__":
    main()
