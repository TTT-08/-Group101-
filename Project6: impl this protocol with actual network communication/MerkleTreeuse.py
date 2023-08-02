import hashlib

def calculate_hash(data):
    """计算数据的哈希值"""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

class MerkleTree:
    def __init__(self, data_list):
        """初始化Merkle Tree"""
        self.data_list = data_list
        self.tree = self.build_tree()

    def build_tree(self):
        """构建Merkle Tree"""
        tree = [calculate_hash(data) for data in self.data_list]

        while len(tree) > 1:
            new_level = []
            for i in range(0, len(tree), 2):
                if i + 1 < len(tree):
                    combined_data = tree[i] + tree[i + 1]
                    new_level.append(calculate_hash(combined_data))
                else:
                    new_level.append(tree[i])
            tree = new_level

        return tree

    def get_root(self):
        """获取Merkle Tree的根哈希值"""
        return self.tree[0]

if __name__ == '__main__':
    # 假设有一组数据块
    data_blocks = ["sdu", "txj", "202100460086"]

    # 创建Merkle Tree实例
    merkle_tree = MerkleTree(data_blocks)

    # 获取Merkle Tree的根哈希值
    root_hash = merkle_tree.get_root()
    print("Merkle Tree的根哈希值:", root_hash)

    # 假设数据块3被篡改
    tampered_data = "hhhhh"
    data_blocks[2] = tampered_data

    # 重新创建Merkle Tree
    tampered_merkle_tree = MerkleTree(data_blocks)
    tampered_root_hash = tampered_merkle_tree.get_root()

    # 验证Merkle Tree的根哈希值是否发生变化，以判断数据是否被篡改
    if tampered_root_hash == root_hash:
        print("数据完整性验证通过")
    else:
        print("数据完整性验证失败，数据可能被篡改")
