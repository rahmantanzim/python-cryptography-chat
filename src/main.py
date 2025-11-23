#This is the entry point of the application
import sys
from security import key_manager

def cli_generate_keys():
    try:
        private_key_path, public_key_path = key_manager.gen_and_save_keys()
        print("RSA Public, Private key pair generated successfully.")
        print(f"Private key: {private_key_path}")
        print(f"Public key:  {public_key_path}")
    except Exception as exc:
        print(f"[ERROR] Failed to generate keys: {exc}")

def cli_test_crypto():
    try:
        pass
        private_key = key_manager.load_private_key()
        public_key = key_manager.load_public_key()
        
        test_message = "This is a TEST MESSAGE"
        print(f"Original Message is: {test_message}")
        
        encrypted_message = key_manager.encrypt_message(test_message, public_key)
        print(f"Encrypted bytes length: {len(encrypted_message)}")

        decrypted_message = key_manager.decrypt_message(encrypted_message,private_key)
        print(f"Decrypted message: {decrypted_message}")
        
        #TEST RESULT
        if decrypted_message == test_message:
            print("Crypto test successful: decrypted message matches original.")
        else:
            print("Crypto test FAILED: messages do not match.")
    except FileNotFoundError as exc:
        print(f"[ERROR] {exc}")
        print("Did you run `python -m src.main generate-keys` first?")
    except Exception as exc:
        print(f"[ERROR] Crypto test failed: {exc}")      
