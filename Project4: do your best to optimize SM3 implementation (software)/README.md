# SM3优化加速
## 1 SM3算法实现
由project1中对于SM3的介绍，我们了解到，SM3算法主要包括数据填充、数据扩展和迭代压缩三个过程。为了更好的实现SM3的性能，我们用C++重新编写SM3(此部分借鉴了网上的实现方法)
## 2 优化思路
通过查找相关资料，对于SM3的优化，我们可以从以下几个方向考虑：
1. 循环展开和指令级并行优化：在SM3的压缩函数中有多次循环，可以考虑进行循环展开和使用SIMD指令集进行指令级并行优化，以加快计算速度。
2. 查表优化：对于一些重复计算，可以考虑使用查表的方式来加速，例如使用预计算的常量表来代替重复计算。
3. 内存访问模式优化：优化内存访问模式，使得数据在缓存中的命中率更高，可以考虑使用局部性原理，避免不必要的内存读写操作。
4. 多线程并行优化：在多核处理器上，可以将不同的消息块交给不同的线程来计算，以实现并行化，加快整体计算速度。
5.数据复用：在计算中间值时，有些值可以被多次使用，可以考虑将它们缓存起来以避免重复计算。

我们根据系统原理里面所学的知识，由于SM3本质上是求哈希值，故整体优化思路是尝试进行多线程实现，测量计算2000次所需的时间，将任务分配到多个线程并行处理。

具体代码分析如下：
* com 函数：对一个64字节的消息分块进行压缩操作，更新哈希值。

* SM3 函数：这是哈希函数的入口，对消息进行填充，划分为64字节的块并进行哈希计算。

* 多线程函数：Th4 和 Th8 函数：这些函数分别对消息进行多次SM3哈希计算。

* 多线程函数调用：th4 和 th8 函数：这些函数创建多个线程以并行执行哈希计算。
```
// 8线程的函数，每个线程计算125次SM3
void Th8(unsigned char* message, uint len, unsigned char* Hash)
{
	for (int i = 0; i < 125; i++)
		SM3(message, len, Hash);
}
// 调用8个线程并行计算SM3

void th8(unsigned char* message, uint len, unsigned char* Hash)
{
	thread* threads = new thread[thread_num * 2];
	int i = 0;
	for (i = 0; i < thread_num * 2; i++)
		threads[i] = thread(Th4, ref(message), len, Hash);
	for (i = 0; i < thread_num * 2; i++)
		threads[i].join();
}

int main()
{
	LARGE_INTEGER BegainTime;
	LARGE_INTEGER EndTime;
	LARGE_INTEGER Frequency;
	QueryPerformanceFrequency(&Frequency);
	unsigned char m[256] = "TXJ202100460086";
	unsigned char hash[256] = "";
	uint len = strlen((const char*)m);
	QueryPerformanceCounter(&BegainTime);
	for (int i = 0; i < 1000; i++)
		SM3(m, len, hash);
	QueryPerformanceCounter(&EndTime);
	printf("明文:\n%s\n\n", m);
	printf("密文:\n");
	printer(hash, 32);
	cout << "单线程运行1000次时间：" << (double)(EndTime.QuadPart - BegainTime.QuadPart) / Frequency.QuadPart << "秒" << endl;
	QueryPerformanceCounter(&BegainTime);
		th4(m, len, hash);
	QueryPerformanceCounter(&EndTime);
	cout << "四线程运行1000次时间：" << (double)(EndTime.QuadPart - BegainTime.QuadPart) / Frequency.QuadPart << "秒" << endl;
	QueryPerformanceCounter(&BegainTime);
		th8(m, len, hash);
	QueryPerformanceCounter(&EndTime);
	cout << "八线程运行1000次时间：" << (double)(EndTime.QuadPart - BegainTime.QuadPart) / Frequency.QuadPart << "秒" << endl;
	return 0;
}
```
## 3 运行结果
![](https://img1.imgtp.com/2023/08/02/aHd27QJY.png)
## 4 结果分析
从运行结果来看，四线程相较于单线程运行1000次速度提升了50%倍多，但是八线程提升不是很显著，我个人分析和查阅资料后推断产生这种结果的原因可能如下：
* 数据竞争和同步开销：在多线程情况下，需要确保线程之间的数据同步和互斥，以避免数据竞争问题。如果同步开销很大，可能会抵消掉并行带来的性能提升。在您提供的代码中，线程函数 Thread8 内的线程函数调用似乎存在错误，它使用了 Thread4 函数，这可能导致线程之间的竞争条件，影响了正确的并行计算。

* 任务划分不均匀：在进行多线程并行计算时，任务的划分需要合理，以确保各个线程的负载均衡。如果任务划分不均匀，某些线程可能会完成较多的工作，而其他线程则可能闲置，从而影响整体性能提升。

* 线程创建和销毁开销：线程的创建和销毁都会引入一定的开销，如果任务规模较小，线程的创建和销毁开销可能会占据整体运行时间的较大比例，从而减少了并行带来的性能提升。

* 资源竞争：如果计算过程中存在多线程之间的资源竞争，如共享内存的读写，可能会导致线程间的等待，降低了并行的效率。
