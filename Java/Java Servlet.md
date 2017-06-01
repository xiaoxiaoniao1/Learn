# 简介

Java Servlet 是运行在 Web 服务器上的程序，它是作为来自 Web 浏览器或其他 HTTP 客户端的请求和 HTTP 服务器上的数据库或应用程序之间的中间层。

Servlet 架构如下所示：

![Servlet架构](http://www.runoob.com/wp-content/uploads/2014/07/servlet-arch.jpg)

Servlet 执行以下主要任务：

- 读取客户端（浏览器）发送的数据
- 处理数据并生成响应结果（该过程可能需要访问数据库等操作）
- 发送响应数据到客户端（浏览器）

# 生命周期
Servlet 生命周期可被定义为从创建直到毁灭的整个过程：

- Servlet 通过调用 init () 方法进行初始化。
- Servlet 调用 service() 方法来处理客户端的请求。
- Servlet 通过调用 destroy() 方法终止。
- Servlet 最后由 JVM 的垃圾回收器进行垃圾回收。

### init() 方法
init 方法只能调用一次。它在第一次创建 Servlet 时被调用，在后续每次用户请求时不再调用。当用户调用一个 Servlet 时，就会创建一个 Servlet 实例，每一个用户请求都会产生一个新的线程，适当的时候移交给 doGet 或 doPost 方法。

> init() 方法简单地创建或加载一些数据，这些数据将被用于 Servlet 的整个生命周期。

### service() 方法
service() 方法是执行实际任务的主要方法。Servlet 容器（即 Web 服务器）调用 service() 方法来处理来自客户端（浏览器）的请求，并把格式化的响应写回给客户端。

每次服务器接收到一个 Servlet 请求时，服务器会产生一个新的线程并调用服务。service() 方法检查 HTTP 请求类型（GET、POST、PUT、DELETE 等），并在适当的时候调用 doGet、doPost、doPut，doDelete 等方法。

> service() 方法由容器调用，service 方法在适当的时候调用 doGet、doPost、doPut、doDelete 等方法。所以，开发者一般不用对 service() 方法做任何动作，只需要根据来自客户端的请求类型来重写 doGet() 或 doPost() 即可。

### destroy() 方法

destroy() 方法只会被调用一次，在 Servlet 生命周期结束时被调用。destroy() 方法可以让 Servlet 关闭数据库连接、停止后台线程等清理活动。

### 一个典型的 Servlet 生命周期图

![生命周期图](http://www.runoob.com/wp-content/uploads/2014/07/Servlet-LifeCycle.jpg)

- 第一个到达服务器的 HTTP 请求被委派到 Servlet 容器。
- Servlet 容器在调用 service() 方法之前加载 Servlet。
- 然后 Servlet 容器处理由多个线程产生的多个请求，每个线程执行一个单一的 Servlet 实例的 service() 方法。

# 面试题
### Servlet 和 GCI 的区别
Servlet 是基于 Java 编写的，处于服务器进程中，它能够通过多线程方式运行 service() 方法，一个实例可以服务于多个请求，而且一般不会销毁；而 CGI 对每个请求都生产新的进程，服务完成后销毁，所以从效率上低于 Servlet。

### Servlet 生命周期
Servlet生命周期包括三部分：

- 初始化：Web 容器加载 servlet，调用 init() 方法
- 处理请求：当请求到达时，运行其 service() 方法。service() 自动派遣运行与请求相对应的 doXXX（doGet 或者 doPost）方法。
- 销毁：服务结束，Web 容器会调用 servlet 的 distroy() 方法销毁 servlet。

### Servle 和 JSP 的区别
服务器端有一个 JSP 容器，主要处理 JSP 页面请求，容器首先把 JSP 转成一个 Servlet，所有的 JSP 元素都会被转换为 Java 代码，然后编译这个 Servlet 类。

Servlet 和 JSP 最主要的不同点在于，Servlet 的应用逻辑是在 Java 文件中，并且完全从表示层中的 HTML 里分离开来。而 JSP 的情况是 Java 和 HTML 可以组合成一个扩展名为 .jsp 的文件。JSP 侧重于视图，Servlet 主要用于控制逻辑。

### JSP有哪些内置对象？作用是什么？

JSP 共有以下 9 种基本内置组件：

|名称                  | 作用                        |
 ----------------- | ---------------------------- | 
| request | 包含用户端请求的信息          |
| response | 包含服务器传回客户端的响应信息          |
| page | 网页本身          |
| pageContext | 管理网页属性          |
| session | 与请求有关的会话          |
| application | 伴随服务器的生命周期，为多个应用程序保存信息          |
| out | 向客户端输出数据          |
| config | servlet的架构部件          |
| exception | 针对错误页面才可使用          |

### JSP有哪些基本动作？作用是什么？
- jsp:include：在页面被请求的时候引入一个文件。 
- jsp:useBean：寻找或者实例化一个JavaBean。 
- jsp:setProperty：设置 JavaBean 的属性。
- jsp:getProperty：输出某个 JavaBean 的属性。 
- jsp:forward：把请求转到一个新的页面。
- jsp:plugin：根据浏览器类型为 Java 插件生成 OBJECT 或 EMBED 标记

### JSP 中动态 INCLUDE 与静态 INCLUDE 的区别？
动态 INCLUDE 用 jsp:include 动作实现，它总是会检查所含文件中的变化，适合用于包含动态页面，并且可以带参数；静态 INCLUDE 用 include 伪码实现，不会检查所含文件的变化，适用于包含静态页面。

### 四种会话跟踪技术作用域
- page：一个页面
- request：：一次请求，一个请求可能跨越多个 page
- session：一次会话，一个会话可能跨越多个 request
- application：代表与整个 Web 应用程序相关的对象和属性，跨越了整个 Web 应用程序。

# 参考文档

[Servlet 教程](http://www.runoob.com/servlet/servlet-tutorial.html)