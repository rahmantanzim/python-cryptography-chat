from security.key_manager import (
    generate_and_save_keys,
    load_private_key,
    load_public_key,
    encrypt_message,
    decrypt_message,
)

# 1. Generate keys
generate_and_save_keys()

# 2. Load keys
priv = load_private_key()
pub = load_public_key()

# 3. Encrypt + decrypt
cipher = encrypt_message("Hello Tanzim!", pub)
plain = decrypt_message(cipher, priv)
print(plain)  # -> "Hello Tanzim!"
