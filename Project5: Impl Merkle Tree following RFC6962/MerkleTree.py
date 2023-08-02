from hashlib import sha256
import string
import random

CHAR_SET = string.punctuation + string.ascii_letters + string.digits

def calculate_hash(data):
    """计算给定数据的 SHA-256 哈希值"""
    return sha256(data.encode('utf-8')).hexdigest()

def concatenate_zero(data):
    """将数据与前缀 0 进行拼接，用于表示左子叶子节点"""
    return hex(0) + data

def concatenate_one(data1, data2):
    """将两个数据进行拼接，用于表示右子叶子节点"""
    return hex(1) + data1 + data2

class MerkleTree:
    def __init__(self, data):
        """构造函数，初始化 Merkle 树"""
        self.leaves = data
        self.root, self.leaf_positions = self.build_merkle_tree()
        print('根哈希值:', self.root)
        print(self.leaf_positions)

    def build_merkle_tree(self):
        """构建 Merkle 树，并返回根哈希值以及叶子节点位置信息"""
        nodes = []
        leaf_positions = {}
        depth = 0

        if len(self.leaves) == 0:
            nodes = calculate_hash('').hexdigest()
            print('深度: 0')
            return nodes, {}

        elif len(self.leaves) == 1:
            nodes.append(calculate_hash(concatenate_zero(self.leaves[0])))
            print('深度: 1')
            return nodes, {}

        else:
            for leaf in self.leaves:
                nodes.append(calculate_hash(leaf))

            while len(nodes) > 1:
                depth += 1
                temp = []

                if len(nodes) % 2 == 0:
                    while len(nodes) > 1:
                        a = nodes.pop(0)
                        leaf_positions[a] = 0
                        b = nodes.pop(0)
                        leaf_positions[b] = 1
                        temp.append(calculate_hash(concatenate_one(a, b)))
                    nodes = temp
                else:
                    last = nodes.pop(-1)
                    while len(nodes) > 1:
                        a = nodes.pop(0)
                        leaf_positions[a] = 0
                        b = nodes.pop(0)
                        leaf_positions[b] = 1
                        temp.append(calculate_hash(concatenate_one(a, b)))
                    temp.append(last)
                    leaf_positions[last] = 1
                    nodes = temp

            print('深度:', depth + 1)
            return nodes[0], leaf_positions

    def audit_path(self, m, leaves):
        """生成某个叶子节点的审核路径"""
        k = 0
        path = []

        if len(leaves) == 2:
            path.append(leaves[(m + 1) % 2])
            return path
        elif len(leaves) > 2:
            for i in range(1, len(leaves)):
                if pow(2, i) >= len(leaves):
                    k = pow(2, i - 1)
                    break

            if m < k:
                path.extend(self.audit_path(m, leaves[0:k]))
                path.append(self.compute_merkle_tree_hash(leaves[k:len(leaves)]))
                return path
            elif m >= k:
                path.extend(self.audit_path(m - k, leaves[k:len(leaves)]))
                path.append(self.compute_merkle_tree_hash(leaves[0:k]))
                return path
        return path

    def compute_merkle_tree_hash(self, leaves):
        """计算 Merkle 树的哈希值"""
        k = 0
        if len(leaves) == 1:
            return leaves[0]
        elif len(leaves) == 2:
            return calculate_hash(concatenate_one(leaves[0], leaves[1]))
        else:
            for i in range(0, len(leaves)):
                if pow(2, i) >= len(leaves):
                    k = pow(2, i - 1)
                    break
            return calculate_hash(concatenate_one(self.compute_merkle_tree_hash(leaves[0:k]),
                                                  self.compute_merkle_tree_hash(leaves[k:len(leaves)])))

    def membership_proof(self, m, leaf):
        """验证成员存在性的证明"""
        audit_path = self.audit_path(m, [calculate_hash(leaf)])
        print('路径:', audit_path)

        leaf_hash = calculate_hash(leaf)
        for i in audit_path:
            if self.leaf_positions[i] == 0:
                leaf_hash = calculate_hash(concatenate_one(i, leaf_hash))
            else:
                leaf_hash = calculate_hash(concatenate_one(leaf_hash, i))

        if leaf_hash == self.root:
            return True
        return False

def test_merkle_tree(length):
    """测试 Merkle 树的构建和验证"""
    long_random = ''.join(random.choice(CHAR_SET) for _ in range(length))
    all_strings = [long_random[i:i + 2] for i in range(0, len(long_random))]
    print("叶子节点:", all_strings)
    print("数量:", len(all_strings))
    print("根节点:", MerkleTree(all_strings).root)

if __name__ == '__main__':
    test_merkle_tree(100000)
    ex = MerkleTree(['1', '2', '3', '4', '5'])
    print(ex.membership_proof(1, '2'))
