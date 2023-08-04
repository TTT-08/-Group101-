# 实现SM2 2p签名与真实网络通信
## 1 原理分析
![](https://img1.imgtp.com/2023/08/04/2oobmdoO.png)
## 2 代码分析
计算机网络通信中各种协议相当复杂，例如三次握手，累计确定，分组缓存，但是这些应该属于操作系统内核的部分，但是对于应用程序来讲，操作系统需要抽象出一个概念，让上层应用去编程，这个概念就是socket。

socket就像插座一样，客户端的插头插进服务器插座，就建立了连接

这个socket可以理解成（客户端ip，客户端port，服务器ip，服务器端port），ip用来区分不同主机，port端口用来区分主机中不同的进程。 socket是“open—write/read—close”模式的一种实现，那么socket就提供了这些操作对应的函数接口。
### 2.1 服务器伪代码：
```
listenfd=socket（.....）；
bind（listenfd，本机的ip和知名端口，....）;
listen（listenfd，....）；
while（true）
{
    connfd=accept（listenfd，....）；
    receive（connfd，....）；//这里读取客户端send的数据
    send（connfd，....）；
}
```
## 2.2客户端伪代码
```
clienfd=socekt（.....）;
connect（clienfd，服务器的ip和port，.....）；
send（cliend，数据）； //这里的发送就相当于上面的read（）
receive（clienfd，....）；
close（clienfd）
```
## 3 结果分析
成功实现通信
![](https://img1.imgtp.com/2023/08/04/xtneXtwa.png)