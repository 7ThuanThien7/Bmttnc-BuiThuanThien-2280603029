from flask import Flask, request, jsonify, send_from_directory
import os
import base64
from cipher.rsa import RSACipher #

app = Flask(__name__)
rsa_cipher = RSACipher()

# Đường dẫn tới thư mục keys nơi lưu trữ khóa
KEYS_DIR = os.path.join(os.path.dirname(__file__), 'cipher', 'rsa', 'keys')

@app.route('/api/rsa/generate_keys', methods=['POST'])
def generate_keys_api():
    try:
        result = rsa_cipher.generate_keys()
        return jsonify({'message': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rsa/encrypt', methods=['POST'])
def encrypt_api():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'Missing message in request body'}), 400
    
    message = data['message']
    
    try:
        public_key = rsa_cipher.load_public_key()
        encrypted_message = rsa_cipher.encrypt(message, public_key)
        # Trả về dữ liệu đã mã hóa dưới dạng base64 string để dễ truyền tải qua JSON
        return jsonify({'encrypted_message': base64.b64encode(encrypted_message).decode('utf-8')}), 200
    except FileNotFoundError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Encryption failed: {str(e)}'}), 500

@app.route('/api/rsa/decrypt', methods=['POST'])
def decrypt_api():
    data = request.get_json()
    if not data or 'encrypted_message' not in data:
        return jsonify({'error': 'Missing encrypted_message in request body'}), 400
    
    # Dữ liệu nhận được là base64 string, cần decode lại thành bytes
    encrypted_message_b64 = data['encrypted_message']
    try:
        encrypted_message_bytes = base64.b64decode(encrypted_message_b64)
    except Exception as e:
        return jsonify({'error': f'Invalid base64 data: {str(e)}'}), 400

    try:
        private_key = rsa_cipher.load_private_key()
        decrypted_message = rsa_cipher.decrypt(encrypted_message_bytes, private_key)
        if "Decryption failed" in decrypted_message or "An error occurred" in decrypted_message:
             return jsonify({'error': decrypted_message}), 400
        return jsonify({'decrypted_message': decrypted_message}), 200
    except FileNotFoundError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Decryption failed: {str(e)}'}), 500

@app.route('/api/rsa/sign', methods=['POST'])
def sign_api():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'Missing message in request body'}), 400
        
    message = data['message']
    
    try:
        private_key = rsa_cipher.load_private_key()
        signature = rsa_cipher.sign(message, private_key)
        # Trả về chữ ký dưới dạng base64 string
        return jsonify({'signature': base64.b64encode(signature).decode('utf-8')}), 200
    except FileNotFoundError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Signing failed: {str(e)}'}), 500

@app.route('/api/rsa/verify', methods=['POST'])
def verify_api():
    data = request.get_json()
    if not data or 'message' not in data or 'signature' not in data:
        return jsonify({'error': 'Missing message or signature in request body'}), 400

    message = data['message']
    signature_b64 = data['signature']
    try:
        signature_bytes = base64.b64decode(signature_b64)
    except Exception as e:
        return jsonify({'error': f'Invalid base64 signature: {str(e)}'}), 400
        
    try:
        public_key = rsa_cipher.load_public_key()
        is_valid = rsa_cipher.verify(message, signature_bytes, public_key)
        return jsonify({'is_valid': is_valid, 'message': 'Signature is valid.' if is_valid else 'Signature is invalid.'}), 200
    except FileNotFoundError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Verification failed: {str(e)}'}), 500

# Endpoint để tải public key (tùy chọn, hữu ích cho client)
@app.route('/api/rsa/public_key', methods=['GET'])
def get_public_key():
    try:
        if not os.path.exists(rsa_cipher.PUBLIC_KEY_PATH):
             return jsonify({'error': 'Public key not found. Generate keys first.'}), 404
        return send_from_directory(KEYS_DIR, 'publicKey.pem', as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Đảm bảo thư mục keys tồn tại khi khởi động app
    if not os.path.exists(KEYS_DIR):
        os.makedirs(KEYS_DIR)
    app.run(host='0.0.0.0', port=5000, debug=True)