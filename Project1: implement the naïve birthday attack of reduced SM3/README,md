# 生日攻击
## 1 原理分析
利用生日攻击找n比特碰撞的原像​ 对于任意消息（这里只考虑数字字符串，其他字符串也可以转化到数字字符串）M，我们计算H=SM3(M)，如果我们只考虑前n比特（下文中的相等都是指前n比特），那么在前0-2^n范围内，至少存在一组碰撞的概率几乎是100%。

那么对于特定的消息M，如何利用生日攻击去找到这个碰撞像呢？

我们可以任取两个消息m1，m2，计算h=SM3(abs(M1-M2)，直到得到H= h

## 2 代码分析
代码部分主要分为SM3的实现和生日攻击的实现
### 2.1 SM3的实现
为了实现SM3，我们首先定义一些辅助函数和常量，包括左移函数leftshift、FF和GG函数、P0和P1函数、T函数以及初始向量IV等。

然后padding函数，用于对输入消息进行填充，使其长度满足SM3算法的要求。
```
def padding(message):
    m = bin(int(message, 16))[2:]
    if len(m) != len(message) * 4:
        # 将输入消息转换为二进制表示，并进行填充
        m = '0' * (len(message) * 4 - len(m)) + m
    l = len(m)
    l_bin = '0' * (64 - len(bin(l)[2:])) + bin(l)[2:]
    m = m + '1'
    m = m + '0' * (448 - len(m) % 512) + l_bin
    m = hex(int(m, 2))[2:]
    return m
```

接下来的block函数将填充后的消息按照128比特分块。message_extension函数根据分块后的消息生成消息扩展，其中使用了W和W1两个列表存储中间结果。essage_compress函数根据消息扩展对当前块进行压缩运算。

最后的SM3函数将所有分块进行压缩运算得到最终的输出。
### 2.1 生日攻击的实现

brithday_attack函数实现了生日攻击，它首先生成2^16个随机数，并利用padding、block和SM3函数获得对应的哈希值。然后统计哈希值的出现次数，找出重复的哈希值，利用哈希函数发生碰撞的可能性，进行n次尝试直到找到一对碰撞的输入。
```
def brithday_attack():
    random_value = []
    r = randomnum(pow(2, 16))
    for i in range(pow(2, 16)):
        m = padding(str(r[i]))
        M = block(m)
        Mn = SM3(M)
        tmp = ""
        for k in Mn:
            tmp += hex(k)[2:]
        random_value.append(tmp[:7])  # tmp[:n] -> SM3算法输出 n*4 比特

    collision = dict(Counter(random_value))
    for key, value in collision.items():
        if value > 1:
            print(key)
```

## 3 运行结果
由于SM3输出为256比特，而个人笔记本不具备足够的算力，因而我尝试通过减少输出比特进行测试，最终成功攻击输出值为24比特的SM3函数。

其中16bit运行成功如下（由于有较多碰撞，在这里只列举了一部分）：
![Alt text](58fd0d0d8b4415dd676679afe1d8790a.png)

20bit运行成功如下：
![dfdceeedd0f7ab7e670dd6bda6499bbf.png](../_resources/dfdceeedd0f7ab7e670dd6bda6499bbf.png)

24bit运行成功如下：
![638cefeb0b96d7fb28c1bf3a8c9bdd96.png](../_resources/638cefeb0b96d7fb28c1bf3a8c9bdd96.png)

28bit运行成功如下：
![7e877aa137b2efada6ec97c43856af18.png](../_resources/7e877aa137b2efada6ec97c43856af18.png)