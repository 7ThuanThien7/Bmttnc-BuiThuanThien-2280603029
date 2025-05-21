class RailFenceCipher:
    def __init__(self):
        pass

    def rail_fence_encrypt(self, plain_text, num_rails):
        if num_rails <= 1:
            return plain_text

        rails = [[] for _ in range(num_rails)]
        rail_index = 0
        direction = 1  # 1: down, -1: up

        for char in plain_text:
            rails[rail_index].append(char)
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction
        
        cipher_text = ''.join(''.join(rail) for rail in rails)
        return cipher_text

    def rail_fence_decrypt(self, cipher_text, num_rails):
        if num_rails <= 1:
            return cipher_text

        # Calculate lengths of each rail
        rail_lengths = [0] * num_rails
        rail_index = 0
        direction = 1
        for _ in range(len(cipher_text)):
            rail_lengths[rail_index] += 1
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction

        # Reconstruct rails with actual characters from cipher_text
        # rails will be a list of strings, where each string is a rail's content
        rails_content = []
        start = 0
        for length in rail_lengths:
            rails_content.append(cipher_text[start:start + length])
            start += length
        
        # Convert these strings back into lists of characters to easily pop
        # Or, keep them as strings and use slicing as in the image
        # The image uses slicing: rails[rail_index][0] and rails[rail_index][1:]

        plain_text = ""
        rail_index = 0
        direction = 1

        # Create mutable lists from rail strings for easy char removal
        # This step is inferred to make rails[rail_index][0] and rails[rail_index][1:] work as if popping
        mutable_rails = [list(s) for s in rails_content]

        for _ in range(len(cipher_text)):
            plain_text += mutable_rails[rail_index].pop(0) # Use pop(0) for list behavior
            # If directly using strings and slicing as in image:
            # plain_text += rails_content[rail_index][0]
            # rails_content[rail_index] = rails_content[rail_index][1:]
            
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction
            
        return plain_text