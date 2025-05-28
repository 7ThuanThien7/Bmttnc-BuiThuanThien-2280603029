import string # Vẫn giữ lại nếu cần thiết cho các phần khác của class

class VigenereCipher:
    def _filter_text(self, text):
        """Filters text to keep only alphabetic characters and converts to uppercase."""
        return "".join(filter(str.isalpha, text)).upper()

    def _extend_key(self, text, key):
        """Extends the key to match the length of the filtered text."""
        # text ở đây là plaintext hoặc ciphertext tùy theo ngữ cảnh gọi
        # key ở đây là key_string đã được filter và uppercase
        filtered_text_len = len("".join(filter(str.isalpha, text))) # Chỉ tính ký tự alphabet trong text
        if not key: # Đề phòng trường hợp key rỗng (mặc dù đã được kiểm tra trước)
            return ""
        extended_key = (key * (filtered_text_len // len(key) + 1))[:filtered_text_len]
        return extended_key # key đã được upper() ở encrypt/decrypt

    # Đổi tên từ encrypt_text thành encrypt
    def encrypt(self, plaintext, key_string):
        """Encrypts text using Vigenere cipher."""
        if not key_string:
            return "Error: Key cannot be empty for Vigenere cipher."
        if not all(c.isalpha() for c in key_string):
            return "Error: Vigenere key must contain only alphabetic characters."

        key_string_filtered = self._filter_text(key_string) # Clean the key
        if not key_string_filtered: # If key becomes empty after filtering
            return "Error: Filtered key is empty. Key must contain alphabetic characters."

        ciphertext = []
        # Sử dụng plaintext gốc để tính độ dài key mở rộng, nhưng chỉ quan tâm ký tự alphabet
        extended_key = self._extend_key(plaintext, key_string_filtered)
        key_idx = 0
        
        for char_plain in plaintext:
            if char_plain.isalpha():
                plain_val = ord(char_plain.upper()) - ord('A')
                key_val = ord(extended_key[key_idx].upper()) - ord('A') # extended_key đã upper
                cipher_val = (plain_val + key_val) % 26
                
                cipher_char = chr(cipher_val + ord('A'))
                if char_plain.islower():
                    cipher_char = cipher_char.lower()
                ciphertext.append(cipher_char)
                key_idx += 1
            else:
                ciphertext.append(char_plain) 
        
        return "".join(ciphertext)

    # Đổi tên từ decrypt_text thành decrypt
    def decrypt(self, ciphertext, key_string):
        """Decrypts text using Vigenere cipher."""
        if not key_string:
            return "Error: Key cannot be empty for Vigenere cipher."
        if not all(c.isalpha() for c in key_string):
            return "Error: Vigenere key must contain only alphabetic characters."

        key_string_filtered = self._filter_text(key_string) # Clean the key
        if not key_string_filtered:
            return "Error: Filtered key is empty. Key must contain alphabetic characters."

        plaintext = []
        # Sử dụng ciphertext gốc để tính độ dài key mở rộng, nhưng chỉ quan tâm ký tự alphabet
        extended_key = self._extend_key(ciphertext, key_string_filtered)
        key_idx = 0

        for char_cipher in ciphertext:
            if char_cipher.isalpha():
                cipher_val = ord(char_cipher.upper()) - ord('A')
                key_val = ord(extended_key[key_idx].upper()) - ord('A') # extended_key đã upper
                plain_val = (cipher_val - key_val + 26) % 26
                
                plain_char = chr(plain_val + ord('A'))
                if char_cipher.islower(): 
                    plain_char = plain_char.lower()
                plaintext.append(plain_char)
                key_idx += 1
            else:
                plaintext.append(char_cipher)
                
        return "".join(plaintext)
