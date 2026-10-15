"""
Basic tests for locketlam package using standard unittest
"""
import unittest
from locketlam import LocketClient, DeviceProfile

class TestLocketLam(unittest.TestCase):
    def test_device_profile_creation(self):
        device = DeviceProfile()
        self.assertIn("com.locket.Locket", device.user_agent)
        self.assertIn("platform", device.analytics_data)
        self.assertEqual(device.analytics_data["platform"], "ios")

    def test_client_initialization_without_session(self):
        client = LocketClient(session_path="non_existent_session.json")
        self.assertFalse(client.is_authenticated())
        self.assertIsNotNone(client.device)

if __name__ == "__main__":
    unittest.main()
