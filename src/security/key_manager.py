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
    """Create the 'keys/' directory if not exist."""
    os.makedirs(DEFAULT_KEYS_DIR, exist_ok=True)
    
def gen_and_save_keys(
    private_key_path: str = DEFAULT_PRIVATE_KEY_PATH,
    public_key_path: str = DEFAULT_PUBLIC_KEY_PATH,
    key_size: int = 2048 #2048 is secured and fast at the same time
    ) -> Tuple[str,str]: #this function will return a tuple with 2 strings which are actually the path of 2 files
    _ensure_keys_dir_exists() # important safety check
    
    private_key = rsa.generate_private_key(
        public_exponent= 65537,
        key_size=key_size
    ) # this generates a private key object and stores in the private_key variable
    public_key = private_key.public_key()
    
    #serialization: Private key
    with open(private_key_path,'wb') as f:
        f.write(private_key.private_bytes(p
            encoding=serialization.Encoding.PEM, #key will be encoded in PEM format
            format=serialization.PrivateFormat.PKCS8, #modern recommended format for private keys.
            encryption_algorithm= serialization.NoEncryption(), #private key file will be plain-text PEM without a password
        ))
    with open(public_key_path,'wb') as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )
    return private_key_path, public_key_path
    
def load_private_key(path:str = DEFAULT_PRIVATE_KEY_PATH):
    try:
        with open(path, 'rb') as f:
            private_key = serialization.load_pem_private_key( #converts PEM bytes into real private key object
                f.read(), #reads the entire file
                password=None,
            )
        return private_key
    except FileNotFoundError:
        raise FileNotFoundError(f"Private key could not be found at: {path} ")
    except Exception as exc: #exc keeps the original error attached
        raise ValueError(f"Failped to load private key: {exc}") from exc            

def load_public_key(path: str = DEFAULT_PUBLIC_KEY_PATH):
    #Load the public key from the PEM file
    try:
        with open(path,'rb') as f:
            public_key = serialization.load_pem_public_key(f.read())
        return public_key
    except FileNotFoundError:
        raise FileNotFoundError(f"public key file could not be found at {path}")
    except Exception as exc:
        raise ValueError(f"Failed to load public key from {path}: {exc}") from exc