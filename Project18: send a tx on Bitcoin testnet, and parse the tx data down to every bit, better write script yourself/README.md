# 在比特币测试网络上发送一个tx，并将tx数据解析到每个比特
这个项目总共包括两个部分，在比特币测试网络上发送一个tx和编写脚本将tx数据解析到每个比特，下面我将分成两个部分进行解析
## 1 tx数据解析到每个比特
首先我们了解到bitcoin的原理如图。
![](https://camo.githubusercontent.com/457133a6775bea73f43479ffa7d18ab58481626481b32e51cb4bb99cd802d9d5/68747470733a2f2f73322e6c6f6c692e6e65742f323032322f30372f32372f767761695471536f6772424e7839642e706e67)
为了测试交易，我们需要先到官网测试款的软件：
![](https://img1.imgtp.com/2023/08/04/MLyeokYQ.png)
安装成功后，打开测试软件：
![](https://img1.imgtp.com/2023/08/04/Hf69g9LR.png)
创建钱包和相应的收款地址txj_text
![](https://img1.imgtp.com/2023/08/04/Njo8Ww2q.png)
但是我们现在还没有bitcoin，我们可以去测试网络领取：
![](https://img1.imgtp.com/2023/08/04/U6so2V6K.png)
产看账户信息：
![](https://img1.imgtp.com/2023/08/04/J6gRo1gr.png)
我们可以验证，这都是0.00001个bitcoin
## 2 用python编写脚本进行解析
在上图中Advanced Details下找到API Call，
找到网址https://api.blockcypher.com/v1/btc/test3/addrs/tb1qq7chjccfcmpal29rv3ans74wa6ewa9kenqzmef/full?limit=50
我们编写python脚本查看对交易数据进行解析：
```
from requests_html import HTMLSession
session = HTMLSession()
url = 'https://api.blockcypher.com/v1/btc/test3/addrs/tb1qq7chjccfcmpal29rv3ans74wa6ewa9kenqzmef/full?limit=50'
response = session.get(url)
with open("parse result.txt","w") as f:

    f.write(response.html.full_text)
```
得到输出如下：
![](https://img1.imgtp.com/2023/08/04/ZIdvtjc7.png)