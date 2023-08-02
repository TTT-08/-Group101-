import hashlib
import time

class Block:
    def __init__(self, data, prev_hash):
        self.timestamp = time.time()
        self.data = data
        self.prev_hash = prev_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """计算块的哈希值"""
        sha = hashlib.sha256()
        sha.update(str(self.timestamp).encode('utf-8') +
                   str(self.data).encode('utf-8') +
                   str(self.prev_hash).encode('utf-8'))
        return sha.hexdigest()

class HashChain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        """创建创世块"""
        return Block("Genesis Block", "0")

    def add_block(self, data):
        """添加新块到链中"""
        prev_block = self.chain[-1]
        new_block = Block(data, prev_block.hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        """验证链的完整性"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            prev_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.prev_hash != prev_block.hash:
                return False

        return True

if __name__ == '__main__':
    hash_chain = HashChain()

    print("添加创世块到泛哈希链")
    print("创世块哈希:", hash_chain.chain[0].hash)

    hash_chain.add_block("第一个块")
    hash_chain.add_block("第二个块")

    print("验证链的完整性:", hash_chain.is_chain_valid())

    # 尝试篡改数据
    hash_chain.chain[1].data = "篡改后的数据"
    print("验证链的完整性（篡改后）:", hash_chain.is_chain_valid())
