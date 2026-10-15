#!/usr/bin/env python3
"""
=============================================================================
  🚀 EXAMPLE 1: LOGIN & SESSION MANAGEMENT
  Library: locketlam
=============================================================================

Objectives:
  1. Login with Locket account Email & Password.
  2. Configure iOS Device Profile (auto-emulated or custom hardware properties).
  3. Manage automatic session persistence to a JSON file (no re-login required).
  4. Auto-refresh expiring JWT ID tokens in background.
"""

import os
import sys

# Ensure repository root is in Python path when executed directly
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from locketlam import LocketClient
from locketlam.exceptions import AuthenticationError, LocketError

# =============================================================================
# 1. CONFIGURE iOS DEVICE PROFILE
# =============================================================================
# By default, the library randomly emulates iPhone 13 Pro -> 15 Pro, iOS 17/18,
# with genuine installation_id and Apple headers to avoid bot detection.
session_file = os.path.join(REPO_ROOT, "locketlam_session.json")
client = LocketClient(session_path=session_file)

# Option A: Automatic device emulation (Default & Recommended)
client.set_device(auto_emulate=True)

# Option B: Or specify your exact device parameters if preferred:
# client.set_device(
#     auto_emulate=False,
#     installation_id="12345678-ABCD-1234-ABCD-1234567890AB",
#     hardware_model="iPhone16,2",  # iPhone 15 Pro Max
#     ios_version="18.2.0",
#     app_version="2.69.0"
# )

# =============================================================================
# 2. FILL IN YOUR CREDENTIALS HERE
# =============================================================================
EMAIL = "your_email@example.com"      # <-- Your Locket account email
PASSWORD = "your_password_here"       # <-- Your Locket account password


def main():
    print("=" * 60)
    print("🔑 DEMO: LOCKET AUTHENTICATION & SESSION MANAGEMENT")
    print("=" * 60)

    # Step 1: Check if an active session already exists on disk
    if client.is_authenticated():
        print("✅ Found an active session from file!")
        print(f"👉 Current UID: {client.session.uid}")
        print(f"👉 Email: {client.session.email}")
    else:
        print("ℹ️ No session or token expired. Logging in...")

        if EMAIL == "your_email@example.com":
            print("\n⚠️ Please configure your real EMAIL / PASSWORD in lines 46-47 to run this demo!")
            return

        try:
            # Authenticates via Google Firebase Identity Toolkit
            # and automatically saves the session to 'locketlam_session.json'
            login_data = client.login(email=EMAIL, password=PASSWORD)

            print("🎉 Login successful!")
            print(f"👉 User UID : {login_data.get('localId')}")
            print(f"👉 Email    : {login_data.get('email')}")
            print(f"👉 ID Token : {login_data.get('idToken')[:25]}... (truncated)")
        except AuthenticationError as e:
            print(f"❌ Login error: {e}")
            return
        except LocketError as e:
            print(f"❌ System error: {e}")
            return

    # =========================================================================
    # 3. RETRIEVE VALID TOKEN & AUTO-REFRESH MECHANISM
    # =========================================================================
    # client.session.get_valid_token() checks token expiration.
    # If the token expires within 60 seconds, it automatically refreshes in background.
    token = client.session.get_valid_token()
    print(f"\n🔒 Valid ID Token (for API requests): {token[:30]}...")

    # To proactively force token refresh:
    # client.session.refresh()
    # print("🔄 Proactive token refresh completed!")

    print(f"💾 Session status preserved at '{session_file}'.")


if __name__ == "__main__":
    main()
