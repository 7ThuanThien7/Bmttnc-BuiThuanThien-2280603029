from flask import Flask, request, jsonify
# Assuming cipher classes are in a 'cipher' directory
from cipher.transposition import TranspositionCipher
from cipher.playfair import PlayFairCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.caesar import CaesarCipher

app = Flask(__name__)

# --- Instantiate Ciphers ---
transposition_cipher = TranspositionCipher()
playfair_cipher = PlayFairCipher()
vigenere_cipher = VigenereCipher()
railfence_cipher = RailFenceCipher()
caesar_cipher = CaesarCipher()

# --- Transposition Cipher Routes ---
@app.route('/api/transposition/encrypt', methods=['POST'])
def transposition_encrypt():
    """
    Encrypts plain text using the Transposition Cipher.
    Expects JSON: {"plain_text": "your text", "key": your_key_integer}
    Returns JSON: {"encrypted_text": "result"}
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400
        plain_text = data.get('plain_text')
        key_str = data.get('key')

        if plain_text is None or key_str is None:
            return jsonify({"error": "Missing 'plain_text' or 'key'"}), 400
        if not isinstance(plain_text, str):
            return jsonify({"error": "'plain_text' must be a string"}), 400
        
        try:
            key = int(key_str)
        except ValueError:
            return jsonify({"error": "'key' for transposition cipher must be an integer"}), 400

        encrypted_text = transposition_cipher.encrypt(plain_text, key)
        return jsonify({'encrypted_text': encrypted_text})
    except Exception as e:
        # Log the exception for debugging
        app.logger.error(f"Error in transposition_encrypt: {e}")
        return jsonify({"error": "An unexpected error occurred during encryption."}), 500

@app.route('/api/transposition/decrypt', methods=['POST'])
def transposition_decrypt():
    """
    Decrypts cipher text using the Transposition Cipher.
    Expects JSON: {"cipher_text": "your text", "key": your_key_integer}
    Returns JSON: {"decrypted_text": "result"}
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400
        cipher_text = data.get('cipher_text')
        key_str = data.get('key')

        if cipher_text is None or key_str is None:
            return jsonify({"error": "Missing 'cipher_text' or 'key'"}), 400
        if not isinstance(cipher_text, str):
            return jsonify({"error": "'cipher_text' must be a string"}), 400

        try:
            key = int(key_str)
        except ValueError:
            return jsonify({"error": "'key' for transposition cipher must be an integer"}), 400

        decrypted_text = transposition_cipher.decrypt(cipher_text, key)
        return jsonify({'decrypted_text': decrypted_text})
    except Exception as e:
        app.logger.error(f"Error in transposition_decrypt: {e}")
        return jsonify({"error": "An unexpected error occurred during decryption."}), 500

# --- Caesar Cipher Routes ---
@app.route('/api/caesar/encrypt', methods=['POST'])
def caesar_encrypt():
    """
    Encrypts plain text using the Caesar Cipher.
    Expects JSON: {"plain_text": "your text", "key": shift_integer}
    Returns JSON: {"encrypted_text": "result"}
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400
        plain_text = data.get('plain_text')
        key_str = data.get('key')

        if plain_text is None or key_str is None:
            return jsonify({"error": "Missing 'plain_text' or 'key'"}), 400
        if not isinstance(plain_text, str):
            return jsonify({"error": "'plain_text' must be a string"}), 400

        try:
            key = int(key_str)
        except ValueError:
            return jsonify({"error": "'key' for Caesar cipher must be an integer"}), 400
            
        # Assuming CaesarCipher class has encrypt method: encrypt(text, shift)
        encrypted_text = caesar_cipher.encrypt(plain_text, key)
        return jsonify({'encrypted_text': encrypted_text})
    except Exception as e:
        app.logger.error(f"Error in caesar_encrypt: {e}")
        return jsonify({"error": "An unexpected error occurred during encryption."}), 500

@app.route('/api/caesar/decrypt', methods=['POST'])
def caesar_decrypt():
    """
    Decrypts cipher text using the Caesar Cipher.
    Expects JSON: {"cipher_text": "your text", "key": shift_integer}
    Returns JSON: {"decrypted_text": "result"}
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400
        cipher_text = data.get('cipher_text')
        key_str = data.get('key')

        if cipher_text is None or key_str is None:
            return jsonify({"error": "Missing 'cipher_text' or 'key'"}), 400
        if not isinstance(cipher_text, str):
            return jsonify({"error": "'cipher_text' must be a string"}), 400
        
        try:
            key = int(key_str)
        except ValueError:
            return jsonify({"error": "'key' for Caesar cipher must be an integer"}), 400

        # Assuming CaesarCipher class has decrypt method: decrypt(text, shift)
        decrypted_text = caesar_cipher.decrypt(cipher_text, key)
        return jsonify({'decrypted_text': decrypted_text})
    except Exception as e:
        app.logger.error(f"Error in caesar_decrypt: {e}")
        return jsonify({"error": "An unexpected error occurred during decryption."}), 500

# --- PlayFair Cipher Routes ---
@app.route('/api/playfair/encrypt', methods=['POST'])
def playfair_encrypt():
    """
    Encrypts plain text using the PlayFair Cipher.
    Expects JSON: {"plain_text": "your text", "key": "your_key_string"}
    Returns JSON: {"encrypted_text": "result"}
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400
        plain_text = data.get('plain_text')
        key = data.get('key')

        if plain_text is None or key is None:
            return jsonify({"error": "Missing 'plain_text' or 'key'"}), 400
        if not isinstance(plain_text, str) or not isinstance(key, str):
            return jsonify({"error": "'plain_text' and 'key' must be strings"}), 400
        
        # Assuming PlayFairCipher class has encrypt method: encrypt(text, key_string)
        encrypted_text = playfair_cipher.encrypt(plain_text, key)
        return jsonify({'encrypted_text': encrypted_text})
    except Exception as e:
        app.logger.error(f"Error in playfair_encrypt: {e}")
        return jsonify({"error": "An unexpected error occurred during encryption."}), 500

@app.route('/api/playfair/decrypt', methods=['POST'])
def playfair_decrypt():
    """
    Decrypts cipher text using the PlayFair Cipher.
    Expects JSON: {"cipher_text": "your text", "key": "your_key_string"}
    Returns JSON: {"decrypted_text": "result"}
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400
        cipher_text = data.get('cipher_text')
        key = data.get('key')

        if cipher_text is None or key is None:
            return jsonify({"error": "Missing 'cipher_text' or 'key'"}), 400
        if not isinstance(cipher_text, str) or not isinstance(key, str):
            return jsonify({"error": "'cipher_text' and 'key' must be strings"}), 400

        # Assuming PlayFairCipher class has decrypt method: decrypt(text, key_string)
        decrypted_text = playfair_cipher.decrypt(cipher_text, key)
        return jsonify({'decrypted_text': decrypted_text})
    except Exception as e:
        app.logger.error(f"Error in playfair_decrypt: {e}")
        return jsonify({"error": "An unexpected error occurred during decryption."}), 500

# --- Vigenere Cipher Routes ---
@app.route('/api/vigenere/encrypt', methods=['POST'])
def vigenere_encrypt():
    """
    Encrypts plain text using the Vigenere Cipher.
    Expects JSON: {"plain_text": "your text", "key": "your_key_string"}
    Returns JSON: {"encrypted_text": "result"}
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400
        plain_text = data.get('plain_text')
        key = data.get('key')

        if plain_text is None or key is None:
            return jsonify({"error": "Missing 'plain_text' or 'key'"}), 400
        if not isinstance(plain_text, str) or not isinstance(key, str):
            return jsonify({"error": "'plain_text' and 'key' must be strings"}), 400
        if not key.isalpha(): # Vigenere key should typically be alphabetic
             return jsonify({"error": "'key' for Vigenere cipher should be alphabetic"}), 400


        # Assuming VigenereCipher class has encrypt method: encrypt(text, key_string)
        encrypted_text = vigenere_cipher.encrypt(plain_text, key)
        return jsonify({'encrypted_text': encrypted_text})
    except Exception as e:
        app.logger.error(f"Error in vigenere_encrypt: {e}")
        return jsonify({"error": "An unexpected error occurred during encryption."}), 500

@app.route('/api/vigenere/decrypt', methods=['POST'])
def vigenere_decrypt():
    """
    Decrypts cipher text using the Vigenere Cipher.
    Expects JSON: {"cipher_text": "your text", "key": "your_key_string"}
    Returns JSON: {"decrypted_text": "result"}
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400
        cipher_text = data.get('cipher_text')
        key = data.get('key')

        if cipher_text is None or key is None:
            return jsonify({"error": "Missing 'cipher_text' or 'key'"}), 400
        if not isinstance(cipher_text, str) or not isinstance(key, str):
            return jsonify({"error": "'cipher_text' and 'key' must be strings"}), 400
        if not key.isalpha(): # Vigenere key should typically be alphabetic
             return jsonify({"error": "'key' for Vigenere cipher should be alphabetic"}), 400

        # Assuming VigenereCipher class has decrypt method: decrypt(text, key_string)
        decrypted_text = vigenere_cipher.decrypt(cipher_text, key)
        return jsonify({'decrypted_text': decrypted_text})
    except Exception as e:
        app.logger.error(f"Error in vigenere_decrypt: {e}")
        return jsonify({"error": "An unexpected error occurred during decryption."}), 500

# --- RailFence Cipher Routes ---
@app.route('/api/railfence/encrypt', methods=['POST'])
def railfence_encrypt():
    """
    Encrypts plain text using the RailFence Cipher.
    Expects JSON: {"plain_text": "your text", "key": number_of_rails_integer}
    Returns JSON: {"encrypted_text": "result"}
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400
        plain_text = data.get('plain_text')
        key_str = data.get('key')

        if plain_text is None or key_str is None:
            return jsonify({"error": "Missing 'plain_text' or 'key'"}), 400
        if not isinstance(plain_text, str):
            return jsonify({"error": "'plain_text' must be a string"}), 400

        try:
            key = int(key_str)
            if key <= 1: # Number of rails must be greater than 1
                return jsonify({"error": "'key' (number of rails) for RailFence cipher must be greater than 1"}), 400
        except ValueError:
            return jsonify({"error": "'key' for RailFence cipher must be an integer"}), 400
        
        # Assuming RailFenceCipher class has encrypt method: encrypt(text, rails_integer)
        encrypted_text = railfence_cipher.encrypt(plain_text, key)
        return jsonify({'encrypted_text': encrypted_text})
    except Exception as e:
        app.logger.error(f"Error in railfence_encrypt: {e}")
        return jsonify({"error": "An unexpected error occurred during encryption."}), 500

@app.route('/api/railfence/decrypt', methods=['POST'])
def railfence_decrypt():
    """
    Decrypts cipher text using the RailFence Cipher.
    Expects JSON: {"cipher_text": "your text", "key": number_of_rails_integer}
    Returns JSON: {"decrypted_text": "result"}
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400
        cipher_text = data.get('cipher_text')
        key_str = data.get('key')

        if cipher_text is None or key_str is None:
            return jsonify({"error": "Missing 'cipher_text' or 'key'"}), 400
        if not isinstance(cipher_text, str):
            return jsonify({"error": "'cipher_text' must be a string"}), 400

        try:
            key = int(key_str)
            if key <= 1: # Number of rails must be greater than 1
                return jsonify({"error": "'key' (number of rails) for RailFence cipher must be greater than 1"}), 400
        except ValueError:
            return jsonify({"error": "'key' for RailFence cipher must be an integer"}), 400

        # Assuming RailFenceCipher class has decrypt method: decrypt(text, rails_integer)
        decrypted_text = railfence_cipher.decrypt(cipher_text, key)
        return jsonify({'decrypted_text': decrypted_text})
    except Exception as e:
        app.logger.error(f"Error in railfence_decrypt: {e}")
        return jsonify({"error": "An unexpected error occurred during decryption."}), 500

# --- Main Function ---
if __name__ == "__main__":
    # It's good practice to enable logging for debugging
    import logging
    logging.basicConfig(level=logging.DEBUG)
    app.run(host="0.0.0.0", port=5000, debug=True)
