from __future__ import annotations

import requests
from .device import DeviceProfile
from .session import SessionManager
from .exceptions import LocketAPIError
from .modules.user import UserModule
from .modules.moments import MomentsModule
from .modules.friends import FriendsModule
from .modules.chat import ChatModule

class LocketClient:
    """
    Main client for the locketlam library.
    Provides complete programmatic access to all Locket Camera services
    with authentic iOS device fingerprint and hardware emulation.
    """
    API_BASE = "https://api.locketcamera.com"

    def __init__(
        self,
        session_path: str = "locketlam_session.json",
        device: DeviceProfile = None,
        auto_emulate: bool = True,
        **device_kwargs
    ):
        if device is not None:
            self.device = device
        elif not auto_emulate or device_kwargs:
            self.device = DeviceProfile(auto_emulate=auto_emulate, **device_kwargs)
        else:
            self.device = DeviceProfile(auto_emulate=True)

        self.session = SessionManager(session_path=session_path, device=self.device)

        # Service modules
        self.user = UserModule(self)
        self.moments = MomentsModule(self)
        self.friends = FriendsModule(self)
        self.chat = ChatModule(self)

    def set_device(
        self,
        auto_emulate: bool = True,
        installation_id: str = None,
        bundle_id: str = None,
        hardware_model: str = None,
        model_name: str = None,
        ios_version: str = None,
        app_version: str = None,
        build_number: str = None,
        custom_user_agent: str = None,
        custom_analytics: dict = None,
        appcheck_token: str = None,
        instance_id_token: str = None
    ):
        """
        Configures device parameters.
        - auto_emulate=True: Uses automatic realistic iOS emulation presets.
        - auto_emulate=False: Uses the user's custom-provided device identifiers. Any omitted
          parameter automatically falls back to realistic defaults.
        """
        if auto_emulate:
            self.device.enable_auto_emulation()
        else:
            self.device.set_custom_device(
                installation_id=installation_id,
                bundle_id=bundle_id,
                hardware_model=hardware_model,
                model_name=model_name,
                ios_version=ios_version,
                app_version=app_version,
                build_number=build_number,
                custom_user_agent=custom_user_agent,
                custom_analytics=custom_analytics,
                appcheck_token=appcheck_token,
                instance_id_token=instance_id_token
            )
        self.session.save()

    def is_authenticated(self) -> bool:
        """Checks whether the client has an active authenticated session."""
        return bool(self.session.id_token and self.session.uid)

    def login(self, email: str, password: str) -> dict:
        """Authenticates with Locket using email and password."""
        return self.session.login(email, password)

    def post_api(self, endpoint: str, payload: dict = None) -> dict:
        """
        Sends an authenticated HTTP POST request to the Locket Camera backend
        complete with JWT Authorization and genuine iOS analytics/device metadata.
        Uses low-level standard urllib to bypass HTTP client fingerprint blocking (403).
        """
        import json
        import urllib.request
        import urllib.error

        token = self.session.get_valid_token()
        url = f"{self.API_BASE}/{endpoint}"

        headers = {
            **self.device.default_headers,
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8"
        }

        body = {
            "data": {
                **(payload or {}),
                "analytics": self.device.analytics_data
            }
        }
        raw_data = json.dumps(body, ensure_ascii=False).encode("utf-8")

        req = urllib.request.Request(url, data=raw_data, headers=headers)
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("result", data)
        except urllib.error.HTTPError as e:
            try:
                err_data = json.loads(e.read().decode("utf-8"))
                return err_data.get("result", err_data)
            except Exception:
                return {"status": e.code, "error": str(e)}
        except Exception as e:
            return {"error": str(e)}
