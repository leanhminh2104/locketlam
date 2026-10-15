from __future__ import annotations

import os
import json
import time
import requests
from .exceptions import AuthenticationError
from .device import DeviceProfile

class SessionManager:
    """
    Manages session persistence, JWT idToken, and Refresh Token,
    with automatic background renewal before expiration.
    """
    FIREBASE_API_KEY = "AIzaSyCQngaaXQIfJaH0aS2l7REgIjD7nL431So"
    FIREBASE_AUTH_URL = "https://identitytoolkit.googleapis.com/v1/accounts"
    FIREBASE_TOKEN_URL = "https://securetoken.googleapis.com/v1/token"
    FIREBASE_APP_ID = "1:641029076083:ios:cc8eb46290d69b234fa606"

    def __init__(self, session_path: str = "locketlam_session.json", device: DeviceProfile = None):
        self.session_path = session_path
        self.device = device or DeviceProfile()
        self.uid = None
        self.email = None
        self.id_token = None
        self.refresh_token = None
        self.expires_at = 0
        self.load()

    def load(self) -> bool:
        """Loads saved session from local file if available."""
        if not self.session_path or not os.path.exists(self.session_path):
            return False

        try:
            with open(self.session_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.uid = data.get("uid")
            self.email = data.get("email")
            self.id_token = data.get("idToken")
            self.refresh_token = data.get("refreshToken")
            self.expires_at = data.get("expiresAt", 0)
            if "device" in data:
                self.device = DeviceProfile.from_dict(data["device"])
            return True
        except Exception:
            return False

    def save(self):
        """Persists current session and device parameters to file."""
        if not self.session_path:
            return

        data = {
            "uid": self.uid,
            "email": self.email,
            "idToken": self.id_token,
            "refreshToken": self.refresh_token,
            "expiresAt": self.expires_at,
            "device": self.device.to_dict()
        }
        with open(self.session_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def login(self, email: str, password: str) -> dict:
        """Authenticates with Firebase via email and password."""
        url = f"{self.FIREBASE_AUTH_URL}:signInWithPassword?key={self.FIREBASE_API_KEY}"
        headers = self.device.default_headers
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        res = requests.post(url, json=payload, headers=headers)
        data = res.json()
        if res.status_code != 200:
            err = data.get("error", {}).get("message", "Authentication failed")
            raise AuthenticationError(f"Login failed: {err}")

        self.uid = data["localId"]
        self.email = data["email"]
        self.id_token = data["idToken"]
        self.refresh_token = data["refreshToken"]
        self.expires_at = int(time.time() * 1000) + int(data["expiresIn"]) * 1000
        self.save()
        return data

    def refresh(self):
        """Renews idToken using the stored refreshToken with iOS bundle headers."""
        if not self.refresh_token:
            raise AuthenticationError("No refresh token available to renew session!")

        url = f"{self.FIREBASE_TOKEN_URL}?key={self.FIREBASE_API_KEY}"
        headers = {
            "User-Agent": self.device.user_agent,
            "X-Ios-Bundle-Identifier": self.device.bundle_id,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }

        res = requests.post(url, data=data, headers=headers)
        res_data = res.json()
        if res.status_code != 200:
            err = res_data.get("error", {}).get("message", "Token renewal failed")
            raise AuthenticationError(f"Token refresh failed: {err}")

        self.id_token = res_data["id_token"]
        self.refresh_token = res_data["refresh_token"]
        self.expires_at = int(time.time() * 1000) + int(res_data["expires_in"]) * 1000
        self.save()

    def get_valid_token(self) -> str:
        """Returns a valid idToken, automatically refreshing if close to expiry."""
        if not self.id_token:
            raise AuthenticationError("Not authenticated! Please call login() first.")

        now_ms = int(time.time() * 1000)
        if now_ms >= (self.expires_at - 60000):
            self.refresh()

        return self.id_token
