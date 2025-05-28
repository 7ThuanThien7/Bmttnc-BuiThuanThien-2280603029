from flask import Flask, render_template, request
# Assuming your cipher classes are in the 'cipher' directory
from cipher.caesar import CaesarCipher # Existing
from cipher.playfair import PlayFairCipher
from cipher.railfence import RailFenceCipher
from cipher.transposition import TranspositionCipher
from cipher.vigenere import VigenereCipher

app = Flask(__name__)

# --- Home Page ---
@app.route("/")
def home():
    return render_template('index.html')

# --- Caesar Cipher Routes (Existing) ---
@app.route("/caesar")
def caesar_page():
    # Assuming you have a caesar.html similar to the new ones.
    # If not, you might need to create or adjust it.
    # For consistency, I'll assume it uses the same dynamic JS form submission.
    # If caesar.html is simpler, these routes might need to return full pages.
    return render_template('caesar.html', title="Caesar Cipher", key_label="Key (shift value)")

@app.route("/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    text = request.form.get('inputPlainText', '')
    key_str = request.form.get('inputKeyPlain', '0')
    try:
        key = int(key_str)
        caesar_cipher = CaesarCipher()
        encrypted_text = caesar_cipher.encrypt_text(text, key)
        return f"Original Text: {text}<br/>Key: {key}<br/>Encrypted Text: {encrypted_text}"
    except ValueError:
        return "Error: Key must be an integer for Caesar cipher."
    except Exception as e:
        return f"An error occurred: {str(e)}"


@app.route("/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    text = request.form.get('inputCipherText', '')
    key_str = request.form.get('inputKeyCipher', '0')
    try:
        key = int(key_str)
        caesar_cipher = CaesarCipher()
        decrypted_text = caesar_cipher.decrypt_text(text, key)
        return f"Cipher Text: {text}<br/>Key: {key}<br/>Decrypted Text: {decrypted_text}"
    except ValueError:
        return "Error: Key must be an integer for Caesar cipher."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# --- Playfair Cipher Routes ---
@app.route("/playfair")
def playfair_page():
    return render_template('playfair.html', title="Playfair Cipher", key_label="Key (keyword)")

@app.route("/playfair/encrypt", methods=["POST"])
def playfair_encrypt():
    text = request.form.get('inputPlainText', '')
    key = request.form.get('inputKeyPlain', '')
    cipher = PlayFairCipher()
    encrypted_text = cipher.encrypt_text(text, key)
    return f"Original Text: {text}<br/>Key: {key}<br/>Encrypted Text: {encrypted_text}"

@app.route("/playfair/decrypt", methods=["POST"])
def playfair_decrypt():
    text = request.form.get('inputCipherText', '')
    key = request.form.get('inputKeyCipher', '')
    cipher = PlayFairCipher()
    decrypted_text = cipher.decrypt_text(text, key)
    return f"Cipher Text: {text}<br/>Key: {key}<br/>Decrypted Text: {decrypted_text}"

# --- Railfence Cipher Routes ---
@app.route("/railfence")
def railfence_page():
    return render_template('railfence.html', title="Railfence Cipher", key_label="Key (number of rails)")

@app.route("/railfence/encrypt", methods=["POST"])
def railfence_encrypt():
    text = request.form.get('inputPlainText', '')
    key_str = request.form.get('inputKeyPlain', '')
    cipher = RailFenceCipher()
    # Key validation is handled within the cipher method for Railfence
    encrypted_text = cipher.encrypt_text(text, key_str) 
    return f"Original Text: {text}<br/>Key: {key_str}<br/>Encrypted Text: {encrypted_text}"

@app.route("/railfence/decrypt", methods=["POST"])
def railfence_decrypt():
    text = request.form.get('inputCipherText', '')
    key_str = request.form.get('inputKeyCipher', '')
    cipher = RailFenceCipher()
    decrypted_text = cipher.decrypt_text(text, key_str)
    return f"Cipher Text: {text}<br/>Key: {key_str}<br/>Decrypted Text: {decrypted_text}"

# --- Transposition Cipher Routes ---
@app.route("/transposition")
def transposition_page():
    return render_template('transposition.html', title="Columnar Transposition Cipher", key_label="Key (keyword)")

@app.route("/transposition/encrypt", methods=["POST"])
def transposition_encrypt():
    text = request.form.get('inputPlainText', '')
    key = request.form.get('inputKeyPlain', '')
    cipher = TranspositionCipher()
    encrypted_text = cipher.encrypt_text(text, key)
    return f"Original Text: {text}<br/>Key: {key}<br/>Encrypted Text: {encrypted_text}"

@app.route("/transposition/decrypt", methods=["POST"])
def transposition_decrypt():
    text = request.form.get('inputCipherText', '')
    key = request.form.get('inputKeyCipher', '')
    cipher = TranspositionCipher()
    decrypted_text = cipher.decrypt_text(text, key)
    return f"Cipher Text: {text}<br/>Key: {key}<br/>Decrypted Text: {decrypted_text}"

# --- Vigenere Cipher Routes ---
@app.route("/vigenere")
def vigenere_page():
    return render_template('vigenere.html', title="Vigenere Cipher", key_label="Key (keyword)")

@app.route("/vigenere/encrypt", methods=["POST"])
def vigenere_encrypt():
    text = request.form.get('inputPlainText', '')
    key = request.form.get('inputKeyPlain', '')
    cipher = VigenereCipher()
    encrypted_text = cipher.encrypt_text(text, key)
    return f"Original Text: {text}<br/>Key: {key}<br/>Encrypted Text: {encrypted_text}"

@app.route("/vigenere/decrypt", methods=["POST"])
def vigenere_decrypt():
    text = request.form.get('inputCipherText', '')
    key = request.form.get('inputKeyCipher', '')
    cipher = VigenereCipher()
    decrypted_text = cipher.decrypt_text(text, key)
    return f"Cipher Text: {text}<br/>Key: {key}<br/>Decrypted Text: {decrypted_text}"

# --- RSA Route (from original index.html, assuming it exists) ---
@app.route("/rsa")
def rsa_page():
    # Placeholder: You'll need an rsa.html and corresponding backend logic
    # For now, just rendering a simple message or an existing rsa.html if you have one.
    # return "RSA Page - To be implemented or link to existing rsa.html"
    # If you have rsa.html:
    # return render_template('rsa.html', title="RSA Cipher", ...) 
    # For now, let's assume it's similar to Caesar and just needs a template.
    # If 'rsa.html' does not exist, this will cause an error.
    # You might want to create a basic rsa.html or comment this out if not ready.
    try:
        return render_template('rsa.html', title="RSA Cipher") # Add relevant key_labels if needed
    except Exception: # TemplateNotFound
        return "RSA page not yet fully implemented. Missing rsa.html or backend."


# --- Main Function ---
if __name__ == "__main__":
    # Ensure the cipher directory and its __init__.py exist
    # Ensure all HTML templates are in a 'templates' directory
    app.run(host="0.0.0.0", port=5050, debug=True)
