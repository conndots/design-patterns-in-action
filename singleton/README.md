从Java Singleton的一个隐含错误的实现谈起
============
Singleton模式可以说是一个非常常见而简单的设计模式了。《设计模式：可复用面向对象软件的基础》中介绍，Singleton模式的用意是：保证运行环境中只有一个目标类的实例，并提供一个全局的接口获得这个实例。  
  
在我的Github repo [conndots/design-pattern-in-action](https://github.com/conndots/design-patterns-in-action)中的[singleton]()目录中记录了python、ruby、java的单例实现方法。这里主要介绍Java的单例实现方法。[《如何正确地写出单例模式》](http://wuchong.me/blog/2014/08/28/how-to-correctly-write-singleton-pattern/)这篇博客里介绍了用java多种实现单例模式的方法，本文也有参考里面的实现。  
  
#一个看似没有问题的实现
  
```java
public Class SingletonWithDoubleCheckedLockingUnsafeEdition {
        private static SingletonWithDoubleCheckedLockingUnsafeEdition INSTANCE = null;
        private static final Object LOCK = new Object();

        public static SingletonWithDoubleCheckedLockingUnsafeEdition getInstance() {
            if (INSTANCE == null) {
                synchronized(LOCK) {
                    if (INSTANCE == null) {
                        INSTANCE = new SingletonWithDoubleCheckedLockingUnsafeEdition();
                    }
                }
            }
            return INSTANCE;
        }
        
        private SingletonWithDoubleCheckedLockingUnsafeEdition() {}
}
```
   
这段实现也是我一直实现单例的方法，叫双重检验锁的方法。比起使用方法的synchronized关键字更加高效，与在静态域直接初始化对象相比，实现了懒加载（lazy initialization）。然并卵，这是一种有潜在问题的实现。  
这段程序是想要做：首先，判断INSTANCE是否为空，否的话，无需加锁直接获取对象；否则，进入同步域，这时只有一个线程在同步域内。但是，在等待或者进入同步域过程中，可能INSTANCE已经被初始化赋值了，所以再次判断INSTANCE是否为空，防止生成类的多个对象，违背单例的原则。初始化完成后，退出同步域，返回这个对象。  
  
人生若只如初见，一切都那么美好。  
  
然并卵。  
  
#Java的指令重排序优化
在计算机中，软件系统与硬件系统的一个共同目标是，在不改变程序运行结果的前提下，尽可能地提高并行度。编译器、处理器也遵循这样一个目标。  
  
不同的指令间可能存在数据依赖。比如下面计算圆的面积的语句：      
  
```java
double r = 2.3d; //(1)
double pi = 3.1415926; //(2)
double area = pi * r * r; //(3)
```    
  
area的计算依赖于r与pi两个变量的赋值指令。而r与pi无依赖关系。  
  
as-if-serial语义是指：不管如何重排序（编译器与处理器为了提高并行度），（单线程）程序的结果不能被改变。这是编译器、Runtime、处理器必须遵守的语义。  
  
虽然，（1） - happens before -> （2）,（2） - happens before -> （3），但是计算顺序(1)(2)(3)与(2)(1)(3)  对于r、pi、area变量的结果并无区别。编译器、Runtime在优化时可以根据情况重排序（1）与（2），而丝毫不影响程序的结果。  
  
当然，这里说的重排序优化是正对字节码指令的。这样造成的幻觉就是，我们写的单线程程序都是线性执行的，as-if-serial语义使得程序员无需担心重排序干扰代码的逻辑，也不需担心内存的可见性。  
  
#指令重排序优化会影响初始化对象吗
我们说的是指令重排序。看起来`INSTANCE = new SingletonWithDoubleCheckedLockingUnsafeEdition();`是一条赋值语句，事实上，它并不是一个原子操作。它大概会做三件事情：  
1. 为对象分配内存；  
2. 调用对应的构造做对象的初始化操作；  
3. 将引用INSTANCE指向新分配的空间。  

这里并没有细化到指令的级别，但我们仍然可以分析出三个操作的依赖性： 2依赖于1，3依赖于1。第二步与第三步是独立无依赖的，是可以被优化重排序的。  
  
Nani???  
  
我们看看按照1->3->2的顺序执行会发生什么。  
  
线程1：getInstance()  
线程1：判断INSTANCE是否为空？Y  
线程1：获取同步锁  
线程1：判断INSTANCE是否为空? Y  
线程1：为新对象分配内存  
线程1：将引用INSTANCE指向新分配的空间。  
线程2：getInstance()  
线程2：判断INSTANCE是否为空? N  
线程2：返回INSTANCE对象 （擦。INSTANCE表示老子还没被初始化呢）  
线程2：使用INSTANCE对象时发现这货不能用，bug found!
线程1：调用对应构造器作对象初始化操作。  
  
我们说的是多线程环境下的执行，当然不会像上面那样的线性过程，我想你懂我的意思的。这样的bug不是一定会出现，却是一个不小的隐患。  
  
#幸好，我们有volatile关键字提供内存屏障  
大家对volatile关键字可能更多的印象是内存的可见性和提供的原子性。一个变量被声明为volatile后，在不同的线程的缓存中不会有副本，保证一致性。对声明volatile的变量的任意读都可以见到任意线程对这个volatile变量的写入。对于加有volatile的变量，可以保证对它读写的原子性。  
  
而实际上，volatile的内存语义可以小结如下（详细的解释可见：[《深入理解Java内存模型（四）——volatile》](http://www.infoq.com/cn/articles/java-memory-model-4)）：  
  
* 线程A写一个volatile变量，实质上是线程A向接下来将要读这个volatile变量的某个线程发出了（其对共享变量所在修改的）消息。  
* 线程B读一个volatile变量，实质上是线程B接收了之前某个线程发出的（在写这个volatile变量之前对共享变量所做修改的）消息。  
* 线程A写一个volatile变量，随后线程B读这个volatile变量，这个过程实质上是线程A通过主内存向线程B发送消息。  
  
然而，java存在着指令重排序优化的可能。Java内存模型规定多种情况下不允许指令重排序。  
  
为了实现volatile的内存语义，编译器在生成字节码时，会在指令序列中插入内存屏障来禁止特定类型的处理器重排序。
  
大多数的处理器都支持内存屏障的指令。    
    
对于编译器来说，发现一个最优布置来最小化插入屏障的总数几乎不可能，为此，Java内存模型采取保守策略。下面是基于保守策略的JMM内存屏障插入策略：  
  
* 在每个volatile写操作的前面插入一个StoreStore屏障。  
* 在每个volatile写操作的后面插入一个StoreLoad屏障。  
* 在每个volatile读操作的后面插入一个LoadLoad屏障。  
* 在每个volatile读操作的后面插入一个LoadStore屏障。   
  
在x86处理器平台上，保守的读写策略会被优化成：  
  
![](http://cdn.infoqstatic.com/statics_s1_20150807-0037u2/resource/articles/java-memory-model-4/zh/resources/7.png)
  
可以看到，x86只对写-读操作做了内存屏障。在其上对volatile的写操作比读操作开销大。  
  
在一次volatile变量的写操作后，会添加StoreLoad屏障，保证任何对volatile变量的读操作不会被放到1->2->3或者1->3->2操作之前，这样，实现了对象初始化过程的完整的原子性。  
    
  
#正确的姿势实现单例模式
只需要在INSTANCE变量加上volatile关键字的声明。代码如下：  
  
```java
public class SingletonWithDoubleCheckedLockingFineEdition {
        private static volatile SingletonWithDoubleCheckedLockingFineEdition INSTANCE = null;
        private static final Object LOCK = new Object();

        public static SingletonWithDoubleCheckedLockingFineEdition getInstance() {
            if (INSTANCE == null) {
                synchronized(LOCK) {
                    if (INSTANCE == null) {
                        INSTANCE = new SingletonWithDoubleCheckedLockingFineEdition();
                    }
                }
            }
            return INSTANCE;
        }

        private SingletonWithDoubleCheckedLockingFineEdition() {}
}
```             
     


#References:
* [《如何正确地写出单例模式》](http://wuchong.me/blog/2014/08/28/how-to-correctly-write-singleton-pattern/)
* [《深入理解Java内存模型》](http://www.infoq.com/resource/minibooks/java_memory_model/zh/pdf/think_deep_in_java_mem_model.pdf)