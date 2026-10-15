from __future__ import annotations

import uuid
import random

class DeviceProfile:
    """
    Manages authentic iOS hardware specifications, client headers, and analytics emulation.
    Supports:
      - Default automatic emulation (auto_emulate=True): uses built-in realistic presets.
      - Partial or full manual override (auto_emulate=False): user supplies any subset of
        hardware credentials (installation_id, bundle_id, app_version, build_number,
        hardware_model, ios_version, model_name, custom_user_agent, custom_analytics).
        Any field not provided by the user will gracefully fall back to realistic defaults.
    """
    PRESET_MODELS = [
        {"model": "iPhone14,2", "name": "iPhone 13 Pro", "hw": "hw/iPhone14_2", "ios": "17.4.1"},
        {"model": "iPhone14,5", "name": "iPhone 13", "hw": "hw/iPhone14_5", "ios": "17.5.1"},
        {"model": "iPhone15,2", "name": "iPhone 14 Pro", "hw": "hw/iPhone15_2", "ios": "17.6.1"},
        {"model": "iPhone15,3", "name": "iPhone 14 Pro Max", "hw": "hw/iPhone15_3", "ios": "18.0.1"},
        {"model": "iPhone16,1", "name": "iPhone 15 Pro", "hw": "hw/iPhone16_1", "ios": "18.1.0"},
    ]

    def __init__(
        self,
        auto_emulate: bool = True,
        installation_id: str = None,
        bundle_id: str = None,
        app_version: str = None,
        build_number: str = None,
        model_name: str = None,
        ios_version: str = None,
        hardware_model: str = None,
        custom_user_agent: str = None,
        custom_analytics: dict = None,
        appcheck_token: str = None,
        instance_id_token: str = None
    ):
        self.auto_emulate = auto_emulate
        self._preset = random.choice(self.PRESET_MODELS)

        # Installation ID (device UUID)
        self.installation_id = installation_id or uuid.uuid4().hex[:22]

        # App bundle identifier
        self.bundle_id = bundle_id or "com.locket.Locket"

        # App version & build number
        self.app_version = app_version or "2.68.0"
        self.build_number = build_number or "2523"

        # Hardware & OS info
        hw = hardware_model or self._preset["model"]
        hw_tag = f"hw/{hw}" if not hw.startswith("hw/") else hw
        self.model_info = {
            "name": model_name or self._preset["name"],
            "model": hw,
            "hw": hw_tag,
            "ios": ios_version or self._preset["ios"]
        }

        # Custom overrides (if user wants to supply exact raw strings/dicts)
        self.custom_user_agent = custom_user_agent
        self.custom_analytics = custom_analytics
        self.appcheck_token = appcheck_token
        self.instance_id_token = instance_id_token

    @property
    def user_agent(self) -> str:
        """Returns the active User-Agent string."""
        if not self.auto_emulate and self.custom_user_agent:
            return self.custom_user_agent
        return f"{self.bundle_id}/{self.app_version} iPhone/{self.model_info['ios']} {self.model_info['hw']}"

    @property
    def analytics_data(self) -> dict:
        """Returns the active Analytics and Experiment payload."""
        if not self.auto_emulate and self.custom_analytics:
            return self.custom_analytics

        return {
            "ios_version": f"{self.app_version}.{self.build_number}",
            "experiments": {
                "flag_18": {"@type": "type.googleapis.com/google.protobuf.Int64Value", "value": "1203"},
                "flag_7": {"@type": "type.googleapis.com/google.protobuf.Int64Value", "value": "800"},
                "flag_10": {"@type": "type.googleapis.com/google.protobuf.Int64Value", "value": "505"}
            },
            "installation_id": self.installation_id,
            "platform": "ios"
        }

    @property
    def default_headers(self) -> dict:
        """Default HTTP headers matching genuine iOS client requests."""
        headers = {
            "User-Agent": self.user_agent,
            "Content-Type": "application/json",
            "Accept": "*/*",
            "x-ios-bundle-identifier": self.bundle_id
        }
        if self.appcheck_token:
            headers["X-Firebase-AppCheck"] = self.appcheck_token
        if self.instance_id_token:
            headers["Firebase-Instance-Id-Token"] = self.instance_id_token
        return headers

    def set_custom_device(
        self,
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
        Switches to manual mode (auto_emulate=False) and updates any supplied device parameters.
        Any omitted parameter retains its realistic default value.
        """
        self.auto_emulate = False
        if installation_id is not None:
            self.installation_id = installation_id
        if bundle_id is not None:
            self.bundle_id = bundle_id
        if app_version is not None:
            self.app_version = app_version
        if build_number is not None:
            self.build_number = build_number
        if ios_version is not None:
            self.model_info["ios"] = ios_version
        if model_name is not None:
            self.model_info["name"] = model_name
        if hardware_model is not None:
            self.model_info["model"] = hardware_model
            self.model_info["hw"] = f"hw/{hardware_model}" if not hardware_model.startswith("hw/") else hardware_model
        if custom_user_agent is not None:
            self.custom_user_agent = custom_user_agent
        if custom_analytics is not None:
            self.custom_analytics = custom_analytics
        if appcheck_token is not None:
            self.appcheck_token = appcheck_token
        if instance_id_token is not None:
            self.instance_id_token = instance_id_token

    def enable_auto_emulation(self):
        """Switches back to automatic realistic emulation mode."""
        self.auto_emulate = True
        self.custom_user_agent = None
        self.custom_analytics = None

    def to_dict(self) -> dict:
        """Serializes device profile."""
        return {
            "auto_emulate": self.auto_emulate,
            "installation_id": self.installation_id,
            "bundle_id": self.bundle_id,
            "app_version": self.app_version,
            "build_number": self.build_number,
            "model_info": self.model_info,
            "custom_user_agent": self.custom_user_agent,
            "custom_analytics": self.custom_analytics,
            "appcheck_token": self.appcheck_token,
            "instance_id_token": self.instance_id_token
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Restores device profile from dictionary."""
        if not data:
            return cls()
        inst = cls(
            auto_emulate=data.get("auto_emulate", True),
            installation_id=data.get("installation_id"),
            bundle_id=data.get("bundle_id", "com.locket.Locket"),
            app_version=data.get("app_version", "2.68.0"),
            build_number=data.get("build_number", "2523"),
            custom_user_agent=data.get("custom_user_agent"),
            custom_analytics=data.get("custom_analytics"),
            appcheck_token=data.get("appcheck_token"),
            instance_id_token=data.get("instance_id_token")
        )
        if "model_info" in data:
            inst.model_info = data["model_info"]
        return inst
