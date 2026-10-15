from __future__ import annotations

class UserModule:
    """Manages user profile details, name, birthdate, settings synchronization, and lookups."""
    def __init__(self, client):
        self.client = client

    def get_profile(self, user_uid: str = None) -> dict:
        """
        Retrieves user profile details (fetches self if user_uid is omitted).
        Automatically synchronizes fresh photoUrl from Firebase Auth for the current user.
        """
        target = user_uid or self.client.session.uid
        res = self.client.post_api("fetchUserV2", {"user_uid": target})
        profile = res.get("data", res)

        # For self profile, enrich with authentic Firebase Auth profile (photoUrl, email)
        if not user_uid or user_uid == self.client.session.uid:
            try:
                import requests
                token = self.client.session.get_valid_token()
                lookup_url = f"{self.client.session.FIREBASE_AUTH_URL}:lookup?key={self.client.session.FIREBASE_API_KEY}"
                headers = {
                    "User-Agent": self.client.device.user_agent,
                    "X-Ios-Bundle-Identifier": self.client.device.bundle_id,
                    "Content-Type": "application/json"
                }
                fb_res = requests.post(lookup_url, json={"idToken": token}, headers=headers, timeout=5)
                if fb_res.status_code == 200:
                    fb_users = fb_res.json().get("users", [])
                    if fb_users:
                        fb_u = fb_users[0]
                        if fb_u.get("photoUrl"):
                            profile["profile_picture_url"] = fb_u["photoUrl"]
                        if fb_u.get("email"):
                            profile["email"] = fb_u["email"]
            except Exception:
                pass

        return profile

    def get_profile_by_username(self, username: str) -> dict:
        """
        Looks up a user profile directly by Locket username via genuine invite token resolution.
        """
        token = self.client.friends.resolve_invite_token_from_username(username)
        if token:
            res = self.client.friends.fetch_user_by_invite_token(token)
            return res.get("user", res)
        return {"error": "User not found or unable to resolve username link"}

    def update_profile(self, **kwargs) -> dict:
        """
        Updates any supported profile attributes (first_name, last_name, birthdate, profile_picture_url, etc.).
        """
        res = self.client.post_api("changeProfileInfo", kwargs)
        return res

    def update_name(self, first_name: str, last_name: str) -> dict:
        """Updates display first and last name."""
        return self.update_profile(first_name=first_name, last_name=last_name)

    def update_birthdate(self, birthdate: str) -> dict:
        """Updates birthdate (format: YYYY-MM-DD)."""
        return self.update_profile(birthdate=birthdate)

    def update_avatar(self, image_or_url) -> dict:
        """
        Updates profile avatar. Accepts either:
        - Image file path (e.g. 'avatar.jpg', 'avatar.png')
        - Raw image bytes
        - Direct Firebase Storage image URL
        """
        import requests
        if isinstance(image_or_url, str) and image_or_url.startswith("http"):
            image_url = image_or_url
        else:
            image_url = self.upload_avatar(image_or_url)

        # Update avatar in Firebase Auth profile (iOS authentic method)
        token = self.client.session.get_valid_token()
        url = f"{self.client.session.FIREBASE_AUTH_URL}:update?key={self.client.session.FIREBASE_API_KEY}"
        headers = {
            "User-Agent": self.client.device.user_agent,
            "X-Ios-Bundle-Identifier": self.client.device.bundle_id,
            "Content-Type": "application/json"
        }
        payload = {
            "idToken": token,
            "photoUrl": image_url,
            "returnSecureToken": True
        }
        res = requests.post(url, json=payload, headers=headers)
        if res.status_code == 200:
            data = res.json()
            self.client.session.id_token = data.get("idToken", token)
            self.client.session.refresh_token = data.get("refreshToken", self.client.session.refresh_token)
            self.client.session.save()
            return {"status": 200, "profile_picture_url": image_url, "user": data}
        return {"status": res.status_code, "profile_picture_url": image_url, "error": res.text}

    def upload_avatar(self, file_path_or_bytes) -> str:
        """
        Uploads and sets public profile avatar directly to Locket Firebase Storage.
        Converts to optimized WebP format automatically.
        """
        import io, requests
        try:
            # pyrefly: ignore [missing-import]
            from PIL import Image
        except ImportError:
            raise ImportError("Pillow is required for avatar processing. Install it using: pip install pillow")

        if isinstance(file_path_or_bytes, str):
            with open(file_path_or_bytes, "rb") as f:
                raw_bytes = f.read()
        else:
            raw_bytes = file_path_or_bytes

        img = Image.open(io.BytesIO(raw_bytes))
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGBA")
        else:
            img = img.convert("RGB")
        out = io.BytesIO()
        img.save(out, format="WEBP", quality=85)
        webp_data = out.getvalue()

        user_uid = self.client.session.uid
        token = self.client.session.get_valid_token()
        url = f"https://firebasestorage.googleapis.com/v0/b/locket-img/o/users%2F{user_uid}%2Fpublic%2Fprofile_pic.webp"

        headers = {
            "Authorization": f"Firebase {token}",
            "Content-Type": "image/webp",
            "x-firebase-storage-version": "ios/12.12.1",
            "x-firebase-gmpid": self.client.session.FIREBASE_APP_ID,
            "User-Agent": f"{self.client.device.user_agent} (GTMSUF/1)"
        }
        res = requests.post(url, data=webp_data, headers=headers)
        if res.status_code != 200:
            raise Exception(f"Avatar upload failed ({res.status_code}): {res.text}")

        meta = res.json()
        dl_token = meta.get("downloadTokens", "")
        return f"https://firebasestorage.googleapis.com:443/v0/b/locket-img/o/users%2F{user_uid}%2Fpublic%2Fprofile_pic.webp?alt=media&token={dl_token}"

    def sync_client_data(self, push_notifications: bool = True, auto_sync: bool = True, extra_data: dict = None) -> dict:
        """
        Synchronizes client app preferences with the Locket backend.
        - auto_sync=True (Default): Uses authentic emulated iOS version and push state.
        - auto_sync=False: Allows passing custom dictionary in extra_data.
        """
        if auto_sync:
            data = {
                "ios_version": f"{self.client.device.app_version}.{self.client.device.build_number}",
                "push_notifications_enabled": push_notifications
            }
        else:
            data = {"push_notifications_enabled": push_notifications}

        if extra_data:
            data.update(extra_data)
        return self.client.post_api("setClientData", {"client_data": data})

    def set_notification_token(self, fcm_token: str = None, auto_fake: bool = True) -> dict:
        """
        Registers a Firebase Cloud Messaging (FCM) device push token.
        - auto_fake=True (Default): Automatically simulates a realistic Apple FCM push token.
        - auto_fake=False: Uses the user's explicitly provided fcm_token.
        """
        import string, random
        if not auto_fake:
            token = fcm_token or ""
        else:
            if fcm_token:
                token = fcm_token
            else:
                rand_suffix = "".join(random.choices(string.ascii_letters + string.digits + "_-", k=140))
                token = f"{self.client.device.installation_id}:APA91b{rand_suffix}"

        payload = {
            "app": "locket",
            "installation_id": self.client.device.installation_id,
            "notification_token": token
        }
        return self.client.post_api("setNotificationToken", payload)
