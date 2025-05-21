class PlayFairCipher:
    def __init__(self): # -> None:  (This type hint is in the image as a comment)
        pass

    def __init__(self):
        pass

    def create_playfair_matrix(self, key):
        key = key.replace("J", "I") # Chuyển "J" thành "I" trong khóa
        key = key.upper()
        key_set = set(key)
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        remaining_letters = [
            letter for letter in alphabet if letter not in key_set]
        matrix = list(key)

        for letter in remaining_letters:
            matrix.append(letter)
            if len(matrix) == 25:
                break
        
        playfair_matrix = [matrix[i:i+5] for i in range(0, len(matrix), 5)]
        return playfair_matrix

    def find_letter_coords(self, matrix, letter):
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == letter:
                    return row, col

    def playfair_encrypt(self, plain_text, matrix):
        # Chuyển "J" thành "I" trong văn bản đầu vào
        plain_text = plain_text.replace("J", "I")
        plain_text = plain_text.upper()
        encrypted_text = ""

        processed_text = ""
        i = 0
    
        temp_plain_text = ""
        k = 0
        while k < len(plain_text):
            char1 = plain_text[k]
            if k + 1 < len(plain_text):
                char2 = plain_text[k+1]
                if char1 == char2:
                    temp_plain_text += char1 + "X"
                    k += 1
                else:
                    temp_plain_text += char1 + char2
                    k += 2
            else:
                temp_plain_text += char1
                k += 1
        
        if len(temp_plain_text) % 2 == 1:
            temp_plain_text += "X"
        
        # Now use temp_plain_text for encryption loop as per image structure
        for i in range(0, len(temp_plain_text), 2):
            pair = temp_plain_text[i:i+2]
       

            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])
            if row1 == row2:
                encrypted_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                encrypted_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else:
                encrypted_text += matrix[row1][col2] + matrix[row2][col1]
        return encrypted_text

    def playfair_decrypt(self, cipher_text, matrix):
        cipher_text = cipher_text.upper()
        decrypted_text = ""
        # decrypted_text1 = "" # This line is in the image, commented out or unused

        for i in range(0, len(cipher_text), 2):
            pair = cipher_text[i:i+2]
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                decrypted_text += matrix[row1][(col1 - 1 + 5) % 5] + matrix[row2][(col2 - 1 + 5) % 5]
            elif col1 == col2:
                decrypted_text += matrix[(row1 - 1 + 5) % 5][col1] + matrix[(row2 - 1 + 5) % 5][col2]
            else:
                decrypted_text += matrix[row1][col2] + matrix[row2][col1]
        
        banro = ""
        # Loại bỏ ký tự 'X' nếu nó là ký tự cuối cùng và là ký tự được thêm vào
        for i in range(0, len(decrypted_text)-2, 2):
            if decrypted_text[i] == decrypted_text[i+2]:
                banro += decrypted_text[i]
            else:
                banro += decrypted_text[i] + "" + decrypted_text[i+1] # The + "" + is in the image
        
        if decrypted_text[-1] == "X":
            banro += decrypted_text[-2]
        else:
            banro += decrypted_text[-2]
            banro += decrypted_text[-1]
        return banro