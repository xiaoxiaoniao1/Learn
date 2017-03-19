# Java 多线程

一个程序可能包含多个并发运行的任务，线程是指一个任务从头至尾的执行流。Java 可以在一个程序中并发地启动多个线程，这些线程可以在多处理器系统上同时运行。

## 创建任务和线程

任务就是对象。为了创建任务，必须为任务定义一个实现了 Runnable 接口的类。Runnable 接口只包含了一个 run 方法，该方法告诉系统线程如何运行。

```Java
public class TaskClass implements Runnable{
	public TaskClass(){}
	
	public void run(){
	    // Tell system how to run custom thread
	}
}
```

运行线程：
```
TaskClass task = new TaskClass(); //根据任务类，创建任务
Thread thread = new Thread(task); //创建任务的线程
thread.start(); //启动线程
```

# Thread类

Thread 类包含为任务而创建的线程的构造方法，以及控制线程的方法。

- 方法 yield()：可为其他线程临时让出 CPU 时间。
- 方法 sleep(long mills)：可以将线程设置为休眠以确保其他线程的执行，休眠时间为指定的毫秒数。也可能抛出必检异常，因此需要放到 try-catch 块中。
- 方法 join()：使一个线程等待另一个线程的结束。
- Java 为每个线程都指定了一个优先级（1~10），可用 setPriority 方法设置优先级，用 getPriority 方法获取优先级。JVM 总是选择当前优先级最高的可运行线程，较低优先级的线程只有在没有比它更高优先级的线程运行时才能运行。

> 注：由于 Thread 类也实现了 Runnable 接口，所以可以定义一个 Thread 的扩展类，在里面实现 run 方法来实现线程。但**不推荐**使用这种方式，因为把任务和运行任务的机制混在了一起。把任务从线程中分离出来是比较好的选择。

# 线程池

对于大量的任务而言，为每一个任务开始一个新线程是不够高效的。线程池是管理并发执行任务个数的理想办法。Java 提供 Executor 接口来执行线程池里的任务，提供 ExecutorService 接口来管理和控制任务。

```
import java.util.concurrent.*;

public class ExecutorDemo{
	public static void main(String[] args){
		// 创建一个固定线程数的线程池
		ExecutorService executor = Executors.newFixedThreadPool(3);
		// 执行任务
		executor.execute(new PrintChar('a',100));
		executor.execute(new PrintChar('b',100));
		executor.execute(new PrintChar('c',100));
		// 关闭执行器，之后便不能接受新的任务
		executor.shutdown();
	}
}
```

详情见《29.8 线程池》。

# 线程同步

如果一个共享资源被多个线程同时访问，可能会遭到破坏。当任务1和任务2以一种会引起冲突的方式访问一个公共资源时，该问题称为“**竞争状态**”。如果一个类的对象在多线程程序中没有导致竞争状态，则称这样的类是“**线程安全的**”。

为了避免竞争状态，应该防止多个线程同时进入程序的某一特定部分，这部分称为“**临界区**”。通过使用关键字 **synchronized** 来同步方法，以便一次只有一个线程可以访问该方法。如：`public synchronized void deposit(double amount)`。

一个同步方法在执行之前需要加锁；调用一个对象的同步实例方法要求给该对象加锁；调用一个类的同步静态方法要求对该类加锁。如果一个线程调用一个对象上的同步实例方法（静态方法），首先给该对象（类）加锁，然后执行该方法，最后解锁。在解锁之前，另一个调用该对象（类）中方法的线程将会被阻塞。


## 同步语句
当执行方法中某一个代码块时，同步语句不仅可用于对 this 对象加锁，而且可用于对任何对象加锁。这个代码块称为“同步块”。
```
synchronized(expr){
	statements;
}
```
表达式 expr 必须求出对象的引用。若对象已经被另一个线程锁定，则在解锁之前，该线程将被阻塞。当获准对一个对象加锁时，该线程执行同步块中语句，然后解除给对象加的锁。