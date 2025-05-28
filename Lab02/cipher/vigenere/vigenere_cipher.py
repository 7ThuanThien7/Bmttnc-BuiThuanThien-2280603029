import string

class VigenereCipher:
    def _filter_text(self, text):
        """Filters text to keep only alphabetic characters and converts to uppercase."""
        return "".join(filter(str.isalpha, text)).upper()

    def _extend_key(self, text, key):
        """Extends the key to match the length of the filtered text."""
        filtered_text_len = len(self._filter_text(text))
        extended_key = (key * (filtered_text_len // len(key) + 1))[:filtered_text_len]
        return extended_key.upper()

    def encrypt_text(self, plaintext, key_string):
        """Encrypts text using Vigenere cipher."""
        if not key_string:
            return "Error: Key cannot be empty for Vigenere cipher."
        if not all(c.isalpha() for c in key_string):
            return "Error: Vigenere key must contain only alphabetic characters."

        key_string = self._filter_text(key_string) # Clean the key as well
        if not key_string: # If key becomes empty after filtering
             return "Error: Filtered key is empty. Key must contain alphabetic characters."

        ciphertext = []
        extended_key = self._extend_key(plaintext, key_string)
        key_idx = 0
        
        for char_plain in plaintext:
            if char_plain.isalpha():
                plain_val = ord(char_plain.upper()) - ord('A')
                key_val = ord(extended_key[key_idx].upper()) - ord('A')
                cipher_val = (plain_val + key_val) % 26
                
                cipher_char = chr(cipher_val + ord('A'))
                # Preserve original case if desired, for now, output uppercase for letters
                if char_plain.islower():
                    cipher_char = cipher_char.lower()
                ciphertext.append(cipher_char)
                key_idx += 1
            else:
                ciphertext.append(char_plain) # Preserve non-alphabetic characters
        
        return "".join(ciphertext)

    def decrypt_text(self, ciphertext, key_string):
        """Decrypts text using Vigenere cipher."""
        if not key_string:
            return "Error: Key cannot be empty for Vigenere cipher."
        if not all(c.isalpha() for c in key_string):
            return "Error: Vigenere key must contain only alphabetic characters."

        key_string = self._filter_text(key_string) # Clean the key
        if not key_string:
             return "Error: Filtered key is empty. Key must contain alphabetic characters."

        plaintext = []
        extended_key = self._extend_key(ciphertext, key_string) # Extend key based on ciphertext length
        key_idx = 0

        for char_cipher in ciphertext:
            if char_cipher.isalpha():
                cipher_val = ord(char_cipher.upper()) - ord('A')
                key_val = ord(extended_key[key_idx].upper()) - ord('A')
                plain_val = (cipher_val - key_val + 26) % 26 # Add 26 for negative results
                
                plain_char = chr(plain_val + ord('A'))
                # Preserve original case if desired
                if char_cipher.islower(): # This might not be right, depends on how encryption handled case
                    plain_char = plain_char.lower()
                plaintext.append(plain_char)
                key_idx += 1
            else:
                plaintext.append(char_cipher) # Preserve non-alphabetic characters
                
        return "".join(plaintext)
