class RailFenceCipher:
    def encrypt_text(self, text, key):
        """Encrypts text using Railfence cipher."""
        try:
            rails_count = int(key)
            if rails_count < 2:
                return "Error: Key (number of rails) must be at least 2."
        except ValueError:
            return "Error: Key (number of rails) must be an integer."

        if rails_count >= len(text): # Or rails_count == 1
             return text # Encryption doesn't change the text or is trivial

        # Create a list of strings for each rail
        rails = [''] * rails_count
        direction = 1  # 1 for down, -1 for up
        current_rail = 0

        for char in text:
            rails[current_rail] += char
            if current_rail == 0:
                direction = 1
            elif current_rail == rails_count - 1:
                direction = -1
            current_rail += direction
        
        return ''.join(rails)

    def decrypt_text(self, ciphertext, key):
        """Decrypts text using Railfence cipher."""
        try:
            rails_count = int(key)
            if rails_count < 2:
                return "Error: Key (number of rails) must be at least 2."
        except ValueError:
            return "Error: Key (number of rails) must be an integer."

        text_len = len(ciphertext)
        if rails_count >= text_len or rails_count == 1:
             return ciphertext # Decryption doesn't change the text or is trivial

        # Create a matrix to simulate rails
        # Mark positions with '?'
        rail_matrix = [['\n' for _ in range(text_len)] for _ in range(rails_count)]
        
        direction = 1
        current_rail = 0
        for j in range(text_len):
            rail_matrix[current_rail][j] = '?' # Mark the spot
            if current_rail == 0:
                direction = 1
            elif current_rail == rails_count - 1:
                direction = -1
            current_rail += direction

        # Fill the matrix with ciphertext characters
        cipher_idx = 0
        for r in range(rails_count):
            for c in range(text_len):
                if rail_matrix[r][c] == '?':
                    rail_matrix[r][c] = ciphertext[cipher_idx]
                    cipher_idx += 1
        
        # Read off the plaintext
        plaintext = []
        direction = 1
        current_rail = 0
        for j in range(text_len):
            plaintext.append(rail_matrix[current_rail][j])
            if current_rail == 0:
                direction = 1
            elif current_rail == rails_count - 1:
                direction = -1
            current_rail += direction
            
        return "".join(plaintext)
