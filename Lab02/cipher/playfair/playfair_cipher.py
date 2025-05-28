import string

class PlayFairCipher:
    def _generate_key_square(self, key):
        """Generates the 5x5 key square for Playfair cipher."""
        key = key.upper().replace("J", "I")
        key_square_chars = []
        for char in key:
            if char not in key_square_chars and char.isalpha():
                key_square_chars.append(char)
        
        alphabet = string.ascii_uppercase.replace("J", "")
        for char in alphabet:
            if char not in key_square_chars:
                key_square_chars.append(char)
        
        key_square = [key_square_chars[i:i+5] for i in range(0, 25, 5)]
        return key_square

    def _find_char_coords(self, char, key_square):
        """Finds the coordinates (row, col) of a character in the key square."""
        for r, row in enumerate(key_square):
            for c, square_char in enumerate(row):
                if square_char == char:
                    return r, c
        return None, None # Should not happen if char is in square

    def _prepare_text(self, text):
        """Prepares plaintext for Playfair encryption."""
        text = text.upper().replace("J", "I")
        processed_text = ""
        for char in text:
            if char.isalpha():
                processed_text += char
        
        # Split into digraphs, handle double letters and odd length
        digraphs = []
        i = 0
        while i < len(processed_text):
            char1 = processed_text[i]
            if i + 1 < len(processed_text):
                char2 = processed_text[i+1]
                if char1 == char2:
                    digraphs.append(char1 + "X") # Use X as filler
                    i += 1
                else:
                    digraphs.append(char1 + char2)
                    i += 2
            else: # Odd number of characters
                digraphs.append(char1 + "X") # Use X as filler
                i += 1
        return digraphs

    def encrypt_text(self, plaintext, key):
        """Encrypts text using Playfair cipher."""
        if not key:
            return "Error: Key cannot be empty."
        key_square = self._generate_key_square(key)
        digraphs = self._prepare_text(plaintext)
        ciphertext = ""

        for d1, d2 in digraphs:
            r1, c1 = self._find_char_coords(d1, key_square)
            r2, c2 = self._find_char_coords(d2, key_square)

            if r1 is None or r2 is None: # Should not happen with proper preparation
                ciphertext += d1 + d2 # Append as is if char not found (e.g. if X was not in alphabet)
                continue

            if r1 == r2: # Same row
                ciphertext += key_square[r1][(c1 + 1) % 5]
                ciphertext += key_square[r2][(c2 + 1) % 5]
            elif c1 == c2: # Same column
                ciphertext += key_square[(r1 + 1) % 5][c1]
                ciphertext += key_square[(r2 + 1) % 5][c2]
            else: # Rectangle
                ciphertext += key_square[r1][c2]
                ciphertext += key_square[r2][c1]
        
        return ciphertext

    def decrypt_text(self, ciphertext, key):
        """Decrypts text using Playfair cipher."""
        if not key:
            return "Error: Key cannot be empty."
        key_square = self._generate_key_square(key)
        # Ciphertext should already be in valid digraphs if encrypted correctly
        # For robustness, we can assume it's a stream of characters
        ciphertext_processed = ""
        for char in ciphertext.upper().replace("J", "I"):
            if char.isalpha():
                ciphertext_processed += char
        
        if len(ciphertext_processed) % 2 != 0:
             # This indicates a malformed ciphertext for Playfair
             return "Error: Ciphertext length must be even."

        digraphs = [ciphertext_processed[i:i+2] for i in range(0, len(ciphertext_processed), 2)]
        plaintext = ""

        for d1, d2 in digraphs:
            r1, c1 = self._find_char_coords(d1, key_square)
            r2, c2 = self._find_char_coords(d2, key_square)

            if r1 is None or r2 is None:
                plaintext += d1 + d2 
                continue

            if r1 == r2: # Same row
                plaintext += key_square[r1][(c1 - 1 + 5) % 5]
                plaintext += key_square[r2][(c2 - 1 + 5) % 5]
            elif c1 == c2: # Same column
                plaintext += key_square[(r1 - 1 + 5) % 5][c1]
                plaintext += key_square[(r2 - 1 + 5) % 5][c2]
            else: # Rectangle
                plaintext += key_square[r1][c2]
                plaintext += key_square[r2][c1]
        
        # Remove 'X' characters from the decrypted text.
        # This is a simple approach; 'X's that were part of the original message will also be removed.
        final_plaintext = plaintext.replace('X', '')
        return final_plaintext
