import rsa
import os

KEYS_DIR = os.path.join(os.path.dirname(__file__), 'keys')
PUBLIC_KEY_PATH = os.path.join(KEYS_DIR, 'publicKey.pem')
PRIVATE_KEY_PATH = os.path.join(KEYS_DIR, 'privateKey.pem')

class RSACipher:
    def __init__(self, key_size=2048):
        self.key_size = key_size
        if not os.path.exists(KEYS_DIR):
            os.makedirs(KEYS_DIR)

    def generate_keys(self):
        """Tạo cặp khóa RSA (public và private) và lưu vào file."""
        (public_key, private_key) = rsa.newkeys(self.key_size)
        
        with open(PUBLIC_KEY_PATH, 'wb') as f:
            f.write(public_key.save_pkcs1('PEM'))
            
        with open(PRIVATE_KEY_PATH, 'wb') as f:
            f.write(private_key.save_pkcs1('PEM'))
            
        return "Keys generated and saved successfully."

    def load_public_key(self):
        """Tải public key từ file."""
        if not os.path.exists(PUBLIC_KEY_PATH):
            raise FileNotFoundError("Public key not found. Generate keys first.")
        with open(PUBLIC_KEY_PATH, 'rb') as f:
            return rsa.PublicKey.load_pkcs1(f.read())

    def load_private_key(self):
        """Tải private key từ file."""
        if not os.path.exists(PRIVATE_KEY_PATH):
            raise FileNotFoundError("Private key not found. Generate keys first.")
        with open(PRIVATE_KEY_PATH, 'rb') as f:
            return rsa.PrivateKey.load_pkcs1(f.read())

    def encrypt(self, message, public_key):
        """Mã hóa tin nhắn sử dụng public key."""
        # Dữ liệu cần là bytes
        if isinstance(message, str):
            message = message.encode('utf-8')
        return rsa.encrypt(message, public_key)

    def decrypt(self, crypto_text, private_key):
        """Giải mã tin nhắn sử dụng private key."""
        # crypto_text phải là bytes
        try:
            decrypted_message = rsa.decrypt(crypto_text, private_key)
            # Kết quả giải mã là bytes, chuyển về string
            return decrypted_message.decode('utf-8')
        except rsa.pkcs1.DecryptionError:
            return "Decryption failed. Key incorrect or data corrupted."
        except Exception as e:
            return f"An error occurred during decryption: {str(e)}"


    def sign(self, message, private_key):
        """Tạo chữ ký cho tin nhắn sử dụng private key."""
        if isinstance(message, str):
            message = message.encode('utf-8')
        # Thuật toán hash có thể thay đổi, ví dụ: 'SHA-256'
        return rsa.sign(message, private_key, 'SHA-256')

    def verify(self, message, signature, public_key):
        """Xác thực chữ ký của tin nhắn sử dụng public key."""
        if isinstance(message, str):
            message = message.encode('utf-8')
        try:
            rsa.verify(message, signature, public_key)
            return True
        except rsa.pkcs1.VerificationError:
            return False
        except Exception:
            return False