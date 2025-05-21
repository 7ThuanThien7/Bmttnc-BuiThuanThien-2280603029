from cipher.transposition import TranspositionCipher
from cipher.playfair import PlayFairCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from flask import Flask, request, jsonify
from cipher.caesar import CaesarCipher # Assuming CaesarCipher is in this path
app = Flask(__name__)

transposition_cipher = TranspositionCipher()

@app.route('/api/transposition/encrypt', methods=['POST'])
def transposition_encrypt():
    data = request.get_json()
    plain_text = data.get('plain_text')
    key = int(data.get('key'))
    encrypted_text = transposition_cipher.encrypt(plain_text, key)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/transposition/decrypt', methods=['POST'])
def transposition_decrypt():
    data = request.get_json()
    cipher_text = data.get('cipher_text')
    key = int(data.get('key'))
    decrypted_text = transposition_cipher.decrypt(cipher_text, key)
    return jsonify({'decrypted_text': decrypted_text})

#main function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)