from blockchain import Blockchain

# --- Testing the blockchain ---
my_blockchain = Blockchain()

# --- Adding transactions ---
# Thêm một vài giao dịch vào danh sách giao dịch chờ
print("Adding transactions...")
my_blockchain.add_transaction('Alice', 'Bob', 10)
my_blockchain.add_transaction('Bob', 'Charlie', 5)
my_blockchain.add_transaction('Charlie', 'Alice', 3)

# --- Mining a new block ---
print("Mining a new block...")
# Lấy khối và bằng chứng trước đó
previous_block = my_blockchain.get_previous_block()
previous_proof = previous_block.proof

# Tìm bằng chứng mới (đây là quá trình "đào" coin)
new_proof = my_blockchain.proof_of_work(previous_proof)

# Thêm một giao dịch thưởng cho "thợ đào" (Miner)
# Giao dịch này không có người gửi (coi như là 'Genesis' hoặc hệ thống tự thưởng)
my_blockchain.add_transaction('Genesis', 'Miner', 1)

# Tạo khối mới và thêm vào chuỗi
previous_hash = previous_block.hash
new_block = my_blockchain.create_block(new_proof, previous_hash)

# --- Displaying the blockchain ---
print("\n--- Blockchain Details ---")
for block in my_blockchain.chain:
    print(f"Block #{block.index}")
    print(f"Timestamp: {block.timestamp}")
    print(f"Transactions: {block.transactions}")
    print(f"Proof: {block.proof}")
    print(f"Previous Hash: {block.previous_hash}")
    print(f"Hash: {block.hash}")
    print("----------------------------")

# --- Check if the blockchain is valid ---
is_valid = my_blockchain.is_chain_valid(my_blockchain.chain)
print(f"Is Blockchain Valid: {is_valid}")