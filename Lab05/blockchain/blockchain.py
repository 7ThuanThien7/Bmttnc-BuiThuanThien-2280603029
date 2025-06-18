from block import Block
import hashlib
import time

class Blockchain:
    def __init__(self):
        # Khởi tạo chuỗi và danh sách giao dịch hiện tại
        self.chain = []
        self.current_transactions = []
        # Tạo khối nguyên thủy (Genesis Block)
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = Block(
            index=len(self.chain) + 1,
            previous_hash=previous_hash,
            timestamp=time.time(),
            transactions=self.current_transactions,
            proof=proof
        )
        # Reset lại danh sách giao dịch hiện tại sau khi đã thêm vào khối
        self.current_transactions = []
        # Thêm khối mới vào chuỗi
        self.chain.append(block)
        return block

    def get_previous_block(self):
        """Trả về khối cuối cùng trong chuỗi."""
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while not check_proof:
            # Công thức tính toán hash để kiểm tra
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            # Nếu hash có 4 số 0 ở đầu, bằng chứng là hợp lệ
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def add_transaction(self, sender, receiver, amount):
        self.current_transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        # Trả về chỉ số của khối tiếp theo sẽ được đào
        return self.get_previous_block().index + 1
        
    def is_chain_valid(self, chain):
        """
        Kiểm tra tính hợp lệ của toàn bộ chuỗi.
        """
        previous_block = chain[0]
        block_index = 1
        
        while block_index < len(chain):
            block = chain[block_index]
            
            # 1. Kiểm tra xem 'previous_hash' của khối hiện tại có khớp với hash của khối trước đó không
            if block.previous_hash != previous_block.hash:
                return False
            
            # 2. Kiểm tra xem bằng chứng (proof) của khối hiện tại có hợp lệ không
            previous_proof = previous_block.proof
            proof = block.proof
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            
            # Di chuyển đến khối tiếp theo
            previous_block = block
            block_index += 1
            
        return True