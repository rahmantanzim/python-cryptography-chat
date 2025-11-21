"""
SECURITY LAYER
This is a separate module from networking and UI
Scope: Only works with bytes, strings, and key objects.
Also shows error messages.
"""

import os
from typing import Tuple
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

# Default location for keys
DEFAULT_KEYS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)),"..", "keys") # Save the directory of key in this variable
DEFAULT_PRIVATE_KEY_PATH = os.path.join(DEFAULT_KEYS_DIR, "private_key.pem")
DEFAULT_PUBLIC_KEY_PATH = os.path.join(DEFAULT_KEYS_DIR, "public_key.pem")

def _ensure_keys_dir_exists() -> None:
    """Create the keys/ directory if it does not exist."""
    os.makedirs(DEFAULT_KEYS_DIR, exist_ok=True)