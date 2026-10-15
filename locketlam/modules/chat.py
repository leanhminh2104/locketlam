from __future__ import annotations

import uuid
import json
import asyncio

class ReactionEmoji:
    """Standard and official preset emojis for Locket Camera chat and moments."""
    # Official Remote Config Quick Reactions
    YELLOW_HEART = "💛"
    FIRE = "🔥"
    HEART_EYES = "😍"
    TWO_HEARTS = "💕"
    SPARKLE_HEART = "💖"
    SMILING_HEARTS = "🥰"
    LAUGHING = "😂"
    KISS = "💋"
    HEART_HANDS = "🫶"
    RED_HEART = "❤️"

    # Default quick reaction sets configured by Locket server
    DEFAULT_QUICK_REACTIONS = ["💛", "🔥", "😍", "💕"]
    OFFICIAL_PALETTE = ["💛", "💖", "🥰", "😂", "🔥", "💋", "🫶", "❤️", "😍", "💕"]

class ChatModule:
    """Manages Direct Messaging, Emoji Reactions, and WebSocket Real-Time Chat."""
    ReactionEmoji = ReactionEmoji

    def __init__(self, client):
        self.client = client

    @staticmethod
    def get_supported_reactions() -> list:
        """Returns the full list of official preset reaction emojis in Locket."""
        return list(ReactionEmoji.OFFICIAL_PALETTE)

    def _get_history_file(self) -> str:
        """Returns the local path for persistent chat history cache."""
        import os
        base_dir = os.path.dirname(os.path.abspath(self.client.session.session_path or "locketlam_session.json"))
        return os.path.join(base_dir, "chat_history.json")

    def _load_history(self) -> dict:
        """Loads cached chat history."""
        import os, json
        hfile = self._get_history_file()
        if os.path.exists(hfile):
            try:
                with open(hfile, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_history(self, history: dict):
        """Saves cached chat history."""
        import json
        hfile = self._get_history_file()
        try:
            with open(hfile, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def record_message(
        self,
        conversation_id: str,
        sender_uid: str,
        receiver_uid: str,
        text: str,
        message_id: str = None,
        client_token: str = None,
        timestamp: str = None,
        reaction: str = None
    ) -> dict:
        """Records a sent, received, or imported message in chronological history."""
        import time, datetime
        history = self._load_history()
        conv = history.setdefault(conversation_id, [])

        ts = timestamp or datetime.datetime.now(datetime.timezone.utc).isoformat()
        entry = {
            "conversation_id": conversation_id,
            "message_id": message_id,
            "client_token": client_token,
            "sender_uid": sender_uid,
            "receiver_uid": receiver_uid,
            "is_me": sender_uid == self.client.session.uid,
            "text": text,
            "has_reaction": bool(reaction),
            "reaction": reaction,
            "timestamp": ts
        }

        # Avoid duplicates by client_token or message_id
        for i, existing in enumerate(conv):
            if (client_token and existing.get("client_token") == client_token) or \
               (message_id and existing.get("message_id") == message_id):
                conv[i].update(entry)
                self._save_history(history)
                return conv[i]

        conv.append(entry)
        # Sort chronologically by timestamp
        conv.sort(key=lambda m: m.get("timestamp", ""))
        self._save_history(history)
        return entry

    def fetch_messages_from_server(self, conversation_id: str = None, other_user_id: str = None) -> list:
        """
        Directly queries Locket's live Firestore database to fetch official, full-fidelity
        messages exchanged in a conversation, including official document message IDs,
        reactions, sender details, and server timestamps.
        """
        import urllib.request
        token = self.client.session.id_token
        my_uid = self.client.session.uid
        if not token:
            return []

        cid = conversation_id
        if not cid and other_user_id:
            # Discover conversation ID with other_user_id
            try:
                u_url = f"https://firestore.googleapis.com/v1/projects/locket-4252a/databases/(default)/documents/users/{my_uid}/conversations"
                req = urllib.request.Request(u_url, headers={"Authorization": f"Bearer {token}"})
                with urllib.request.urlopen(req) as resp:
                    udata = json.loads(resp.read().decode("utf-8"))
                for doc in udata.get("documents", []):
                    c_candidate = doc["name"].split("/")[-1]
                    curl = f"https://firestore.googleapis.com/v1/projects/locket-4252a/databases/(default)/documents/conversations/{c_candidate}"
                    creq = urllib.request.Request(curl, headers={"Authorization": f"Bearer {token}"})
                    with urllib.request.urlopen(creq) as cresp:
                        cdata = json.loads(cresp.read().decode("utf-8"))
                    members = [v.get("stringValue") for v in cdata.get("fields", {}).get("members", {}).get("arrayValue", {}).get("values", [])]
                    if other_user_id in members:
                        cid = c_candidate
                        break
            except Exception:
                pass

        if not cid:
            return []

        url = f"https://firestore.googleapis.com/v1/projects/locket-4252a/databases/(default)/documents/conversations/{cid}/messages"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except Exception:
            return []

        server_messages = []
        for doc in data.get("documents", []):
            fields = doc.get("fields", {})
            doc_id = doc["name"].split("/")[-1]
            sender = fields.get("sender", {}).get("stringValue", "")
            body = fields.get("body", {}).get("stringValue", "")
            created_at = fields.get("created_at", {}).get("timestampValue", "")
            client_token = fields.get("client_token", {}).get("stringValue")
            
            # Reactions
            reactions_list = []
            if "reactions" in fields:
                for r in fields["reactions"].get("arrayValue", {}).get("values", []):
                    rf = r.get("mapValue", {}).get("fields", {})
                    reactions_list.append({
                        "sender": rf.get("sender", {}).get("stringValue"),
                        "emoji": rf.get("emoji", {}).get("stringValue"),
                        "created_at": rf.get("created_at", {}).get("timestampValue")
                    })

            is_me = (sender == my_uid)
            msg_obj = {
                "conversation_id": cid,
                "message_id": doc_id,
                "client_token": client_token,
                "sender_uid": sender,
                "receiver_uid": other_user_id if other_user_id else (None if is_me else my_uid),
                "is_me": is_me,
                "text": body,
                "has_reaction": len(reactions_list) > 0,
                "reaction": reactions_list[0]["emoji"] if reactions_list else None,
                "reactions": reactions_list,
                "timestamp": created_at
            }
            server_messages.append(msg_obj)
            self.record_message(
                conversation_id=cid,
                sender_uid=sender,
                receiver_uid=msg_obj["receiver_uid"],
                text=body,
                message_id=doc_id,
                client_token=client_token,
                reaction=msg_obj["reaction"]
            )

        server_messages.sort(key=lambda m: m.get("timestamp", ""))
        return server_messages

    def get_messages(self, other_user_id: str = None, conversation_id: str = None, fetch_server: bool = True) -> list:
        """
        Retrieves the complete chronological list of messages exchanged with a user.
        - If fetch_server is True (default), queries live official messages directly from
          Locket's database and synchronizes local history.
        - Sorts all messages in exact chronological timeline order.
        """
        if fetch_server:
            server_msgs = self.fetch_messages_from_server(
                conversation_id=conversation_id,
                other_user_id=other_user_id
            )
            if server_msgs:
                return server_msgs

        history = self._load_history()
        my_uid = self.client.session.uid

        matched_messages = []
        for cid, msgs in history.items():
            if conversation_id and cid != conversation_id:
                continue
            for m in msgs:
                if other_user_id:
                    if m.get("sender_uid") == other_user_id or m.get("receiver_uid") == other_user_id:
                        matched_messages.append(m)
                else:
                    matched_messages.append(m)

        matched_messages.sort(key=lambda m: m.get("timestamp", ""))
        return matched_messages

    def send_message(self, receiver_uid: str, text: str = None, moment_uid: str = None) -> dict:
        """
        Sends a chat message, emoji reaction, or moment to a friend.
        - receiver_uid: The friend's UID.
        - text: Message text (optional if sending a moment_uid).
        - moment_uid: Optional moment ID to attach/share in chat (can be yours or a friend's).
        """
        token = str(uuid.uuid4()).upper()
        # If sending a moment without text, use zero-width invisible character to satisfy API validation
        msg_text = text if (text is not None and text != "") else ("\u200b" if moment_uid else "")
        payload = {
            "receiver_uid": receiver_uid,
            "msg": msg_text,
            "moment_uid": moment_uid,
            "from_memory": False,
            "intensity": {
                "value": "0",
                "@type": "type.googleapis.com/google.protobuf.Int64Value"
            },
            "client_token": token
        }
        res = self.client.post_api("sendChatMessageV2", payload)
        conv_uid = res.get("data", {}).get("conversation_uid")
        if conv_uid:
            self.record_message(
                conversation_id=conv_uid,
                sender_uid=self.client.session.uid,
                receiver_uid=receiver_uid,
                text=text or "",
                client_token=token
            )
        data_res = res.get("data", res)
        if isinstance(data_res, dict) and "msg_id" not in data_res:
            data_res["msg_id"] = token
            data_res["client_token"] = token
        return data_res

    def send_moment(self, receiver_uid: str, moment_uid: str, text: str = None) -> dict:
        """
        Sends/shares a moment (photo/video) directly into chat with a friend.
        - receiver_uid: Target friend's UID.
        - moment_uid: Canonical UID or moment ID (can be your own moment or any friend's moment).
        - text: Optional message text accompanying the moment. If omitted (None or ''), sends purely the standalone moment!
        """
        return self.send_message(receiver_uid=receiver_uid, text=text, moment_uid=moment_uid)

    def delete_message(self, conversation_uid: str, message_uid: str, validate_ownership: bool = True) -> dict:
        """
        Deletes (recalls / unsends) a sent chat message from a conversation.
        - conversation_uid: The conversation identifier.
        - message_uid: The specific message UID to delete.
        - validate_ownership: If True, prevents attempting to delete other users' messages (as Locket only permits recalling your own sent messages).
        """
        if validate_ownership:
            history = self._load_history()
            conv = history.get(conversation_uid, [])
            for m in conv:
                if (m.get("message_id") == message_uid or m.get("client_token") == message_uid) and not m.get("is_me"):
                    raise ValueError(f"Cannot recall/delete message ({message_uid}) because it was sent by someone else. You can only recall your own messages.")

        payload = {
            "conversation_uid": conversation_uid,
            "message_uid": message_uid
        }
        res = self.client.post_api("deleteChatMessage", payload)
        if res.get("status") == 200:
            history = self._load_history()
            if conversation_uid in history:
                history[conversation_uid] = [
                    m for m in history[conversation_uid]
                    if m.get("message_id") != message_uid and m.get("client_token") != message_uid
                ]
                self._save_history(history)
        return res

    def send_reaction(self, conversation_id: str, message_id: str, emoji: str, validate_receiver: bool = True) -> dict:
        """
        Reacts to a specific chat message with an emoji (e.g. '❤️', '🔥', '🫶', '😂').
        - conversation_id: The conversation UID.
        - message_id: The target message UID to react to.
        - emoji: The reaction emoji string.
        - validate_receiver: If True, prevents accidentally reacting to own messages (as Locket only permits reacting to friend's messages).
        """
        if validate_receiver:
            history = self._load_history()
            conv = history.get(conversation_id, [])
            for m in conv:
                if m.get("message_id") == message_id and m.get("is_me"):
                    raise ValueError(f"Cannot react to your own message ({message_id}). Locket only allows reactions on friend's messages.")

        payload = {
            "conversation_id": conversation_id,
            "message_id": message_id,
            "emoji": emoji
        }
        res = self.client.post_api("sendChatMessageReaction", payload)
        if res.get("status") == 200:
            history = self._load_history()
            if conversation_id in history:
                for m in history[conversation_id]:
                    if m.get("message_id") == message_id:
                        m["reaction"] = emoji
                        m["has_reaction"] = True
                self._save_history(history)
        return res

    def remove_reaction(self, conversation_id: str, message_id: str) -> dict:
        """
        Removes (unreacts) your emoji reaction from a specific chat message.
        - conversation_id: The conversation UID.
        - message_id: The target message UID to remove reaction from.
        """
        payload = {
            "conversation_id": conversation_id,
            "message_id": message_id
        }
        res = self.client.post_api("removeChatMessageReaction", payload)
        if res.get("status") == 200:
            history = self._load_history()
            if conversation_id in history:
                for m in history[conversation_id]:
                    if m.get("message_id") == message_id:
                        m["reaction"] = None
                        m["has_reaction"] = False
                self._save_history(history)
        return res

    def mark_as_read(
        self,
        conversation_uid: str = None,
        other_user_id: str = None,
        send_read_receipt: bool = True
    ) -> dict:
        """
        Marks a conversation as read.
        - conversation_uid: Identifier of the conversation (V2 standard).
        - other_user_id: Peer user ID (if conversation_uid is not known).
        - send_read_receipt:
            * True (default): Sends 'Seen' read receipt notification to the sender.
            * False (Ghost / Incognito mode): Marks the conversation as read locally
              without notifying the other person that you have read their messages.
        """
        payload = {
            "send_read_receipt": bool(send_read_receipt)
        }
        if conversation_uid:
            payload["conversation_uid"] = conversation_uid
        if other_user_id:
            payload["other_user_id"] = other_user_id

        res = self.client.post_api("markAsRead", payload)
        return res

    def get_conversations(self) -> list:
        """
        Retrieves the summary list of all conversations for the authenticated user,
        including conversation ID, peer user, unread count, read status, and latest message snippet.
        """
        import urllib.request
        token = self.client.session.id_token
        my_uid = self.client.session.uid
        if not token:
            return []

        url = f"https://firestore.googleapis.com/v1/projects/locket-4252a/databases/(default)/documents/users/{my_uid}/conversations"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except Exception:
            return []

        conversations = []
        for doc in data.get("documents", []):
            fields = doc.get("fields", {})
            cid = doc["name"].split("/")[-1]
            members = [v.get("stringValue") for v in fields.get("members", {}).get("arrayValue", {}).get("values", [])]
            other_uid = [m for m in members if m != my_uid]
            peer_uid = other_uid[0] if other_uid else None

            latest_msg_field = fields.get("latest_message", {}).get("mapValue", {}).get("fields", {})
            latest_body = latest_msg_field.get("body", {}).get("stringValue")
            latest_sender = latest_msg_field.get("sender", {}).get("stringValue")
            latest_time = latest_msg_field.get("created_at", {}).get("timestampValue")

            unread_count = int(fields.get("unread_count", {}).get("integerValue", 0))
            is_read = fields.get("is_read", {}).get("booleanValue", True)
            other_read_time = fields.get("other_last_read_at", {}).get("timestampValue")

            conversations.append({
                "conversation_id": cid,
                "peer_uid": peer_uid,
                "members": members,
                "unread_count": unread_count,
                "is_read": is_read,
                "other_last_read_at": other_read_time,
                "latest_message": {
                    "text": latest_body,
                    "sender_uid": latest_sender,
                    "timestamp": latest_time
                }
            })

        return conversations

    async def listen_realtime(self, other_user_id: str, on_message):
        """
        Listens for real-time messages via Locket WebSocket.
        - other_user_id: UID of the conversation peer.
        - on_message: Callback function (sync or async) invoked on message receipt.
        """
        try:
            # pyrefly: ignore [missing-import]
            import websockets
        except ImportError:
            raise ImportError(
                "The 'websockets' package is required for real-time streaming. "
                "Install it using: pip install websockets"
            )

        token = self.client.session.get_valid_token()
        my_uid = self.client.session.uid

        # Auto-resolve target: if user entered a username instead of UID, resolve to UID
        target_uid = other_user_id
        if other_user_id and not any(c.isupper() for c in other_user_id) and len(other_user_id) < 28:
            try:
                prof = self.client.user.get_profile_by_username(other_user_id)
                if prof.get("uid"):
                    target_uid = prof["uid"]
            except Exception:
                pass

        ws_url = f"wss://api.locketcamera.com/wss_v2/chat?otherUserId={target_uid}&userId={my_uid}"

        headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": self.client.device.user_agent,
            "x-ios-bundle-identifier": self.client.device.bundle_id
        }

        async with websockets.connect(ws_url, additional_headers=headers) as ws:
            async for raw in ws:
                try:
                    data = json.loads(raw)
                except Exception:
                    data = raw

                if asyncio.iscoroutinefunction(on_message):
                    await on_message(data)
                else:
                    on_message(data)
