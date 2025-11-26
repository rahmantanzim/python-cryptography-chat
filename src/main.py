#This is the entry point of the application
import sys
from src.security import key_manager
from src.app import chat_app


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
        
        test_message = "This is a TEST MESSAGE From Tanzim"
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
        
def cli_server(args):
    if len(args) != 2:
        print("Usage: python -m src.main server <port> <partner_public_key_path>")
        return
    try:
        port = int(args[0])
    except ValueError:
        print(f"[ERROR] Port must be an integer.")
        return
    
    partner_pub_path = args[1]
    #########################
    #########################
    #########################
    #########################
    #########################
    #########################
    #########################
    #########################
    #########################
    #########################
    #########################
    #########################
    

def main():
    pass
    if len(sys.argv) < 2:
        print(f"CLI User Manual:")
        print("python -m src.main generate-keys")
        print("  python -m src.main test-crypto")
        
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == 'generate-keys':
        cli_generate_keys()
    elif cmd == 'test-crypto':
        cli_test_crypto()
    else:
        print(f"Unknown Command: {cmd}")
        print("Please use: generate-keys, test-crypto")
        sys.exit(1)
            
if __name__ == "__main__":
    main() #run main() when the file is executed directly,
         
            
        
