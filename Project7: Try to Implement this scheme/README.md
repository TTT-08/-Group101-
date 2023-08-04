# 泛哈希链的实现
## 1 原理介绍
泛哈希链是一种基于哈希函数的数据结构，它通过将数据块链接在一起来创建一个链式结构，每个数据块都包含前一个数据块的哈希和当前数据块的哈希。这种结构使得链中的每个数据块都与前一个数据块以及后续数据块相关联，从而形成一个链式的数据记录。泛哈希链的每个数据块都通过哈希函数与前一个数据块的哈希以及自身的数据相结合，生成一个唯一的哈希值，确保数据块的不可篡改性。
## 2 代码实现
代码总共分为以下两类：
1. Block 类： 这个类表示链中的一个数据块：
- timestamp：表示块的创建时间戳。
- data：包含块的数据。
- prev_hash：前一个块的哈希值，用于链接块。
- hash：块自身的哈希值，由 calculate_hash 方法计算。
2. HashChain 类： 这个类用于创建和管理泛哈希链：
- chain：存储链中的所有块的列表。
- create_genesis_block ：创建创世块，作为链的起始。
- add_block ：添加新块到链中，需要指定块的数据。
- is_chain_valid ：验证链的完整性，即验证每个块的哈希和链接。

主程序创建了一个泛哈希链实例 hash_chain。添加了两个块，分别命名为 "第一个块" 和 "第二个块"。验证链的完整性，输出验证结果。然后尝试篡改第二个块的数据，再次验证链的完整性，输出验证结果。
```
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
```
## 3 结果分析
最终成功实现
![](https://img1.imgtp.com/2023/08/02/qq3FYAit.png)