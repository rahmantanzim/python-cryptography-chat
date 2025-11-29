# This is the entry point of the application
import sys
import base64
from src.security import key_manager
from src.app import chat_app


def cli_generate_keys():
    """CLI command: generate a new RSA key pair and save to keys/."""
    try:
        private_key_path, public_key_path = key_manager.gen_and_save_keys()
        print("RSA Public, Private key pair generated successfully.")
        print(f"Private key: {private_key_path}")
        print(f"Public key:  {public_key_path}")
    except Exception as exc:
        print(f"[ERROR] Failed to generate keys: {exc}")


def cli_test_crypto():
    """CLI command: test encryption/decryption using the saved keys."""
    try:
        private_key = key_manager.load_private_key()
        public_key = key_manager.load_public_key()
        
        test_message = "Hello world"
        print(f"Original Message is: {test_message}")
        
        encrypted_message = key_manager.encrypt_message(test_message, public_key)
        encrypted_b64 = base64.b64encode(encrypted_message).decode("utf-8")
        print(f"Encrypted bytes length: {len(encrypted_message)}")
        print(f"Encrypted message (RAW BYTES): {encrypted_message}")
        print(f"Encrypted message (Base64): {encrypted_b64}")

        decrypted_message = key_manager.decrypt_message(encrypted_message, private_key)
        print(f"Decrypted message: {decrypted_message}")
        
        # TEST RESULT
        if decrypted_message == test_message:
            print("Crypto test successful: decrypted message matches original.")
        else:
            print("Crypto test FAILED: messages do not match.")
    except FileNotFoundError as exc:
        print(f"[ERROR] {exc}")
        print("Did you run `python -m src.main generate-keys` first?")
    except Exception as exc:
        print(f"[ERROR] Crypto test failed: {exc}")      


def cli_server(args):
    """
    Expected:
      args[0] = port
      args[1] = partner_public_key_path
    """
    if len(args) != 2:
        print("Usage: python -m src.main server <port> <partner_public_key_path>")
        return

    try:
        port = int(args[0])
    except ValueError:
        print(f"[ERROR] Port must be an integer.")
        return
    
    partner_pub_path = args[1]

    chat_app.start_server(port, partner_pub_path)


def cli_client(args):
    """
    Expected:
      args[0] = server_host
      args[1] = port
      args[2] = partner_public_key_path
    """
    if len(args) != 3:
        print("Usage: python -m src.main client <server_host> <port> <partner_public_key_path>")
        return

    server_host = args[0]

    try:
        port = int(args[1])
    except ValueError:
        print(f"[ERROR] Port must be an integer.")
        return

    partner_pub_path = args[2]
    chat_app.start_client(server_host, port, partner_pub_path)


def main():
    if len(sys.argv) < 2:
        print("CLI User Manual:")
        print("  python -m src.main generate-keys")
        print("  python -m src.main test-crypto")
        print("  python -m src.main server <port> <partner_public_key_path>")
        print("  python -m src.main client <server_host> <port> <partner_public_key_path>")
        sys.exit(1)
    
    cmd = sys.argv[1]
    args = sys.argv[2:]
    
    if cmd == 'generate-keys':
        cli_generate_keys()
    elif cmd == 'test-crypto':
        cli_test_crypto()
    elif cmd == 'server':
        cli_server(args)
    elif cmd == 'client':
        cli_client(args)
    else:
        print(f"Unknown Command: {cmd}")
        print("Please use: generate-keys, test-crypto, server, client")
        sys.exit(1)
            

if __name__ == "__main__":
    main()  # run main() when the file is executed directly
