import math

class TranspositionCipher:
    def _get_key_order(self, key_string):
        if not key_string:
            return None, "Error: Key cannot be empty."
        
        indexed_key = []
        for i, char in enumerate(key_string):
            indexed_key.append((char, i))
        
        indexed_key.sort()
        
        order_map = [0] * len(key_string)
        read_order = []
        for i, (_, original_idx) in enumerate(indexed_key):
            order_map[original_idx] = i
            read_order.append(original_idx)
            
        key_col_pairs = sorted([(char, i) for i, char in enumerate(key_string)])
        ordered_original_indices = [original_idx for char, original_idx in key_col_pairs]

        return ordered_original_indices, None

    def encrypt_text(self, plaintext, key_string):
        if not key_string:
             return "Error: Key cannot be empty."

        num_cols = len(key_string)
        if num_cols == 0: # Prevent division by zero if key_string becomes empty after some processing
            return "Error: Key length cannot be zero after processing."
            
        num_rows = math.ceil(len(plaintext) / num_cols)
        
        padded_plaintext = plaintext.ljust(num_rows * num_cols, 'X')
        
        grid = [['' for _ in range(num_cols)] for _ in range(num_rows)]
        
        ptr = 0
        for r in range(num_rows):
            for c in range(num_cols):
                grid[r][c] = padded_plaintext[ptr]
                ptr += 1
        
        ciphertext = ""
        key_col_pairs = sorted([(key_string[i], i) for i in range(num_cols)])
        
        for _, col_idx in key_col_pairs:
            for r in range(num_rows):
                ciphertext += grid[r][col_idx]
                
        return ciphertext

    def decrypt_text(self, ciphertext, key_string):
        if not key_string:
            return "Error: Key cannot be empty."

        num_cols = len(key_string)
        text_len = len(ciphertext)
        
        if num_cols == 0:
            return "Error: Key length cannot be zero."
        num_rows = math.ceil(text_len / num_cols)

        key_col_pairs = sorted([(key_string[i], i) for i in range(num_cols)])
        
        grid = [['' for _ in range(num_cols)] for _ in range(num_rows)]
        
        cipher_ptr = 0
        for _, original_col_idx in key_col_pairs:
            for r in range(num_rows):
                if cipher_ptr < text_len:
                    grid[r][original_col_idx] = ciphertext[cipher_ptr]
                    cipher_ptr += 1
                else:
                    grid[r][original_col_idx] = ''
        
        plaintext = ""
        for r in range(num_rows):
            for c in range(num_cols):
                plaintext += grid[r][c]
        
        final_plaintext = plaintext.replace('X', '') 
        return final_plaintext
