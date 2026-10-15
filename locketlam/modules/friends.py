from __future__ import annotations

import urllib.request
import re

class FriendsModule:
    """Manages friends, friend requests, user suggestions, groups, and blocking."""
    def __init__(self, client):
        self.client = client

    def get_groups_and_friends(self) -> dict:
        """Retrieves list of user groups and friends."""
        res = self.client.post_api("getGroupsState", {})
        return res.get("data", res)

    def get_all_friends(self) -> list:
        """
        Retrieves the complete list of friends with their detailed profile information.
        """
        import json
        token = self.client.session.get_valid_token()
        my_uid = self.client.session.uid
        url = f"https://firestore.googleapis.com/v1/projects/locket-4252a/databases/(default)/documents/users/{my_uid}/friends"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        
        friends = []
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            for doc in data.get("documents", []):
                fuid = doc["name"].split("/")[-1]
                try:
                    profile = self.client.user.get_profile(fuid)
                    friends.append(profile)
                except Exception:
                    friends.append({"uid": fuid})
        except Exception:
            pass
        return friends

    def get_friend_requests(self) -> dict:
        """
        Retrieves pending incoming and outgoing friend requests from Firestore.
        Returns a dict: {'incoming': [...], 'outgoing': [...]} with full profile data.
        """
        import json
        token = self.client.session.get_valid_token()
        my_uid = self.client.session.uid
        base = f"https://firestore.googleapis.com/v1/projects/locket-4252a/databases/(default)/documents/users/{my_uid}"
        headers = {"Authorization": f"Bearer {token}"}

        res = {"incoming": [], "outgoing": []}
        for req_type in ("incoming_friend_requests", "outgoing_friend_requests"):
            key = "incoming" if "incoming" in req_type else "outgoing"
            try:
                url = f"{base}/{req_type}"
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                for doc in data.get("documents", []):
                    fuid = doc["name"].split("/")[-1]
                    try:
                        p = self.client.user.get_profile(fuid)
                        res[key].append(p)
                    except Exception:
                        res[key].append({"uid": fuid})
            except Exception:
                pass
        return res

    def resolve_invite_token_from_username(self, username: str) -> str:
        """
        Extracts genuine invite token from user's public share link (https://locket.cam/<username>).
        """
        url = f"https://locket.cam/{username}"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "com.locket.Locket/2.68.0 iPhone/27.0"}
        )
        try:
            with urllib.request.urlopen(req) as resp:
                html = resp.read().decode("utf-8", errors="ignore")
            m = re.search(r"locket\.camera%2Finvites%2F([a-zA-Z0-9]+)", html)
            if not m:
                m = re.search(r"locket\.camera/invites/([a-zA-Z0-9]+)", html)
            if m:
                return m.group(1)
        except Exception:
            pass
        return None

    def fetch_user_by_invite_token(self, invite_token: str) -> dict:
        """Fetches detailed profile information using an invite token."""
        res = self.client.post_api("fetchUserForInviteToken", {"invite_token": invite_token})
        return res.get("data", res)

    def send_request(self, user_uid: str, source: str = "inviteCardPopup") -> dict:
        """
        Sends a friend request to a target user UID matching genuine iOS client payload.
        """
        payload = {
            "user_uid": user_uid,
            "source": source,
            "platform": "iOS",
            "create_ofr_for_temp_users": False,
            "share_history_eligible": True,
            "get_reengagement_status": False,
            "prompted_reengagement": False,
            "rollcall": False,
            "invite_variant": {
                "value": "1002",
                "@type": "type.googleapis.com/google.protobuf.Int64Value"
            }
        }
        return self.client.post_api("sendFriendRequest", payload)

    def send_request_by_username(self, username: str) -> dict:
        """
        Sends a friend request directly using username (auto-resolves invite token).
        """
        token = self.resolve_invite_token_from_username(username)
        if token:
            user_data = self.fetch_user_by_invite_token(token)
            uid = user_data.get("user", {}).get("uid")
            if uid:
                return self.send_request(uid)
        
        profile = self.client.user.get_profile_by_username(username)
        if profile and profile.get("uid"):
            return self.send_request(profile["uid"])
            
        raise Exception(f"User not found for username: {username}")

    def accept_request(self, user_uid: str) -> dict:
        """Accepts an incoming friend request from a user UID."""
        payload = {
            "user_uid": user_uid,
            "during_signup": False,
            "ios_version": f"{self.client.device.app_version}.{self.client.device.build_number}"
        }
        res = self.client.post_api("acceptFriendRequest", payload)
        return res.get("data", res)

    def _resolve_target_uid(self, user_or_uid: str) -> str:
        """Helper to resolve username or raw UID to valid user_uid."""
        clean = user_or_uid.strip().lstrip("@")
        # If it's a 28-char Firebase UID (standard alphanumeric)
        if len(clean) == 28 and clean.isalnum() and not clean.isalpha() and not clean.isnumeric():
            return clean
        
        # Try resolving via profile or invite token
        try:
            profile = self.client.user.get_profile_by_username(clean)
            if profile and profile.get("uid"):
                return profile["uid"]
        except Exception:
            pass
        return clean

    def remove(self, user_uid: str) -> dict:
        """Removes a friend (unfriends). Supports either User UID or Username."""
        target_uid = self._resolve_target_uid(user_uid)
        return self.client.post_api("removeFriend", {"user_uid": target_uid})

    def block(self, user_uid: str) -> dict:
        """
        Blocks a user. Supports either User UID or Username.
        Note: On Locket backend, blocking a user automatically breaks and unfriends the relationship
        (friendship_status becomes 'none' and target is moved to blocked_users).
        """
        target_uid = self._resolve_target_uid(user_uid)
        return self.client.post_api("blockFriend", {"user_uid": target_uid})

    def unblock(self, user_uid: str) -> dict:
        """Unblocks a user. Supports either User UID or Username."""
        target_uid = self._resolve_target_uid(user_uid)
        return self.client.post_api("unblockUser", {"user_uid": target_uid})

    def suggest_friends(self, phone_contacts: list = None) -> list:
        """Retrieves suggested friends from phone contacts."""
        payload = {
            "contacts": phone_contacts or [],
            "smart_friend_suggestions": {
                "@type": "type.googleapis.com/google.protobuf.Int64Value",
                "value": "0"
            }
        }
        res = self.client.post_api("suggestFriends", payload)
        return res.get("data", res)
