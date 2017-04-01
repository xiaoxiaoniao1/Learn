
HTTP 是一个应用层 Web 协议，通常由 HTTP 客户端发起一个请求，创建一个到服务器指定端口（默认是80端口）的 TCP 连接。HTTP 服务器则在那个端口监听客户端的请求。一旦收到请求，服务器会向客户端返回一个状态，比如"HTTP/1.1 200 OK"，以及返回的内容，如请求的文件、错误消息、或者其它信息。

![][1]

HTTP 的主要特点如下：

- 简单快速：客户向服务器请求服务时，只需传送请求方法和路径。请求方法常用的有 GET、POST 。每种方法规定了客户与服务器联系的类型不同。由于 HTTP 协议简单，使得 HTTP 服务器的程序规模小，因而通信速度很快。
- 灵活： HTTP 允许传输任意类型的数据对象。正在传输的类型由 Content-Type 加以标记。
- 无连接（限于HTTP/1.0）：无连接的含义是限制每次连接只处理一个请求。服务器处理完客户的请求，并收到客户的应答后，即断开连接。采用这种方式可以节省传输时间。
- 无状态： HTTP 是一个**无状态**的协议，即服务器不会去维护与客户交互的相关信息，因此它对于事务处理没有记忆能力。举个例子来讲，你通过服务器认证后成功请求了一个资源，紧接着再次请求这一资源时，服务器仍旧会要求你表明身份。 

无状态不代表 HTTP 不能保持 TCP 连接，更不能代表 HTTP 使用的是 UDP 协议（无连接）。HTTP 协议中，并没有规定它所依赖的层。HTTP 假定其下层协议提供可靠的传输，因此任何能够提供这种保证的协议都可以被其使用。HTTP 在 TCP/IP 协议族使用 TCP 作为其传输层，其在 TCP/IP 四层网络模型中的位置如下图所示： 

![][2]

# HTTP 协议基础

## HTTP Request

客户端发送一个 HTTP 请求到服务器的请求消息包括四个部分：**请求行**（request line）、**消息报头**（header）、空行、**请求正文**。

![enter image description here](http://upload-images.jianshu.io/upload_images/2964446-fdfb1a8fce8de946.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

以下是一个 HTTP GET 请求的实例。
```
GET /562f25980001b1b106000338.jpg HTTP/1.1
Host    img.mukewang.com
User-Agent    Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36
Accept    image/webp,image/*,*/*;q=0.8
Referer    http://www.imooc.com/
Accept-Encoding    gzip, deflate, sdch
Accept-Language    zh-CN,zh;q=0.8
```

### 请求行

请求行以一个方法符号开头，后面跟着请求的 URI 和协议版本，彼此由空格分隔。

常用的请求方法如下： 

|方法名称          |含义             |
|-----------------|----------------| 
|GET              |获取由 Request-URI 标识的任何信息(以实体的形式)，如果 Request-URI 引用某个数据处理过程，则应该以它产生的数据作为在响应中的实体，而不是该过程的源代码文本，除非该过程碰巧输出该文本。 |
|POST             |用来请求原始服务器接受请求中封装的实体作为请求行中的Request-URI标识的副属。POST主要用于向数据处理过程提供数据块，如递交表单或者是通过追加操作来扩展数据库。 |
|PUT              |以提供的Request-URI存储封装的实体。 |
|DELETE           |请求原始服务器删除Request-URI标识的资源。 |
|HEAD             |除了服务器不能在响应中返回消息体，HEAD方法与GET相同。用来获取暗示实体的元信息，而不需要传输实体本身。常用于测试超文本链接的有效性、可用性和最近的修改。| 

简单例子如下：

    GET /index.html HTTP/1.1
    POST http://192.168.2.217:8080/index.jsp HTTP/1.1

### 消息报头

消息报头是紧接着请求行（即第一行）之后的部分，用来说明服务器要使用的附加信息。

报头域由键值对组成。请求头部包含了**普通报头**、**请求报头**、**实体报头**。

**普通报头**用于所有的请求和响应消息，但并不用于被传输的实体，只用于传输的消息。比如： 

* Cache-Control：用于指定缓存指令，缓存指令是单向的(响应中出现的缓存指令在请求中未必会出现)，且是独立的(一个消息的缓存指令不会影响另一个消息处理的缓存机制)；
* Date：表示消息产生的日期和时间；
* Connection：允许发送指定连接的选项，例如指定连接是连续的，或者指定 “close” 选项，通知服务器在响应完成后关闭连接。

**请求报头**允许客户端向服务器端传递请求的附加信息以及客户端自身的信息。常用的请求报头如下： 

* Host：指定被请求资源的 Internet 主机和端口号，它通常是从 HTTP URL 中提取出来的；
* User-Agent：允许客户端将它的操作系统、浏览器和其它属性告诉服务器；
* Accept：指定客户端接受哪些类型的信息，eg:Accept:image/gif，表明客户端希望接受GIF图象格式的资源；
* Accept-Charset：指定客户端接受的字符集，缺省是任何字符集都可以接受；
* Accept-Encoding：指定可接受的内容编码，缺省是各种内容编码都可以接受；
* Authorization：证明客户端有权查看某个资源，当浏览器访问一个页面，如果收到服务器的响应代码为401(未授权)，可以发送一个包含 Authorization 请求报头域的请求，要求服务器对其进行验证。

**实体报头**定义了关于实体正文（eg：有无实体正文）和请求所标识的资源的元信息。常用的实体报头如下：

* Allow：GET，POST
* Content-Encoding：文档的编码（Encode）方法，eg：gzip；
* Content-Language：内容的语言类型，eg：zh-cn；
* Content-Length：表示内容长度，eg：80

### 空行

请求头部后面的空行是必须的。

即使第四部分的请求数据为空，也必须有空行。

### 请求正文

通常是 HTML 代码或者 JSON 格式的文本。

## HTTP 响应

在接收和解释请求消息后，服务器返回一个 HTTP 响应消息。HTTP 响应也是由四个部分组成，分别是：**状态行**、**消息报头**、空行、**响应正文**。

一个 HTTP Response 实例：
```
HTTP/1.1 200 OK
Date: Fri, 22 May 2009 06:07:21 GMT
Content-Type: text/html; charset=UTF-8

<html>
      <head></head>
      <body>
            <!--body goes here-->
      </body>
</html>
```

### 状态行

所有 HTTP 响应的第一行都是状态行，依次是当前 HTTP 版本号，3 位数字组成的状态码，以及描述状态的短语，彼此由空格分隔。

HTTP 状态码由三位数字组成，共分五种类别。状态代码的第一个数字代表当前响应的类型：

* 1xx：指示信息——请求已被服务器接收，继续处理
* 2xx：成功——请求已成功被服务器接收、理解、接受
* 3xx：重定向——需要后续操作才能完成这一请求
* 4xx：客户端错误——请求含有词法错误或者无法被执行
* 5xx：服务器错误——服务器在处理某个正确请求时发生错误

常见的状态码有如下：

```
200 OK                        //客户端请求成功
400 Bad Request               //客户端请求有语法错误，不能被服务器所理解
401 Unauthorized              //请求未经授权，这个状态代码必须和WWW-Authenticate报头域一起使用 
403 Forbidden                 //服务器收到请求，但是拒绝提供服务
404 Not Found                 //请求资源不存在，eg：输入了错误的URL
500 Internal Server Error     //服务器发生不可预期的错误
503 Server Unavailable        //服务器当前不能处理客户端的请求，一段时间后可能恢复正常
```

### 消息报头

响应消息报头包含了**普通报头**、**响应报头**、**实体报头**，普通报头和实体报头与 HTTP Request 报头中的普通报头、实体报头相同。

响应报头允许服务器传递不能放在状态行中的附加响应信息，以及关于服务器的信息和 对 Request-URI 所标识的资源进行下一步访问的信息。常用的响应报头如下： 

* Location：用于重定向接受者到一个新的位置，Location 响应报头域常用在更换域名的时候；
* Server：包含了服务器用来处理请求的软件信息，与 User-Agent 请求报头域是相对应的；
* WWW-Authenticate：必须被包含在 401(未授权的)响应消息中。

### 响应正文

消息正文类似 HTTP 请求的消息正文。

## GET 与 POST

HTTP 协议定义了很多与服务器交互的方法，最基本的有 4 种，分别是 GET, POST, PUT, DELETE 。一个 URL 用于描述一个网络上的资源，而 HTTP 中的 GET, POST, PUT, DELETE 就对应着对这个资源的查，改，增，删 4 个操作。

GET 一般用于**获取/查询**资源信息，而POST一般用于**更新**资源信息，主要区别如下：

1. GET 通过地址栏来传值（但由于敏感信息附在 URL 上，可能有安全问题）；POST 方法通过提交表单来传值，提交的数据放在 HTTP 包的 Body 中。
2. GET 提交的数据大小有限制（因为**浏览器对URL的长度有限制**，实际上 HTTP 协议规范没有对 URL 长度进行限制），而 POST 方法提交的数据没有限制。
3. 对于 GET 方式的请求，浏览器会把 http header 和 data 一并发送出去，服务器响应 200（返回数据）；而对于 POST，浏览器先发送 header ，服务器响应 100 continue，浏览器再发送 data ，服务器响应 200 ok（返回数据）。
4. GET 在浏览器回退时是无害的，而 POST 会再次提交请求。GET 请求参数会被完整保留在浏览器历史记录里，而 POST 中的参数不会被保留。
5. 对参数的数据类型，GET 只接受 ASCII 字符，而 POST 没有限制。

## HTTP不同版本区别

HTTP/1.0 与 HTTP/1.1 主要区别如下：

* 带宽优化
    
    HTTP/1.0 中，存在一些浪费带宽的现象，例如客户端只是需要某个对象的一部分，而服务器却将整个对象送过来了。HTTP/1.1 中在请求消息中引入了 range 头域，它允许只请求资源的某个部分。

    另外一种情况是请求消息中如果包含比较大的实体内容，但不确定服务器是否能够接收该请求（如是否有权限），此时若贸然发出带实体的请求，如果被拒绝也会浪费带宽。HTTP/1.1 加入了一个新的状态码100（Continue），客户端事先发送一个只带头域的请求，如果服务器因为权限拒绝了请求，就回送响应码 401（Unauthorized）；如果服务器接收此请求就回送响应码 100，客户端就可以继续发送带实体的完整请求了。

* 长连接

    HTTP 1.0 规定浏览器与服务器只保持短暂的连接，浏览器的每次请求都需要与服务器建立一个 TCP 连接，服务器完成请求处理后立即断开 TCP 连接，服务器不跟踪每个客户也不记录过去的请求。由于大多数网页的流量都比较小，一次 TCP 连接很少能通过 slow-start 区，不利于提高带宽利用率。
    
    HTTP 1.1 支持长连接（PersistentConnection）和请求的流水线（Pipelining）处理，在一个 TCP 连接上可以传送多个 HTTP 请求和响应，减少了建立和关闭连接的消耗和延迟。
    
    HTTP 1.1 还允许客户端不用等待上一次请求结果返回，就可以发出下一次请求，但服务器端必须按照接收到客户端请求的先后顺序依次回送响应结果，以保证客户端能够区分出每次请求的响应内容，这样也显著地减少了整个下载过程所需要的时间。

* 缓存

    在HTTP/1.0 中，使用`Expire头域`来判断资源的 fresh 或 stale ，并使用条件请求来判断资源是否仍有效。例如，cache 通过 If-Modified-Since 头域向服务器验证资源的 Last-Modefied 头域是否有更新，源服务器可能返回 304（Not Modified），则表明该对象仍有效；也可能返回 200（OK）替换请求的 Cache 对象。
    
    HTTP/1.1 在 1.0 的基础上加入了一些 cache 的新特性，当缓存对象的 Age 超过 Expire 时变为 stale 对象， cache 不需要直接抛弃 stale 对象，而是与源服务器进行重新激活（revalidation）。
    
* Host 头域

    在 HTTP1.0 中认为每台服务器都绑定一个唯一的IP地址，因此请求消息中的 URL 并没有传递主机名（hostname）。但随着虚拟主机技术的发展，在一台物理服务器上可以存在多个虚拟主机（Multi-homed Web Servers），并且它们共享一个 IP 地址。HTTP1.1 的请求消息和响应消息都支持 Host 头域，请求消息中如果没有 Host 头域会报告一个错误（400 Bad Request）。

* 错误提示

    HTTP/1.0 中只定义了16个状态响应码，对错误或警告的提示不够具体。HTTP/1.1 引入了一个 Warning 头域，增加对错误或警告信息的描述。
    
    此外，在HTTP/1.1中新增了24个状态响应码，如409（Conflict）表示请求的资源与资源的当前状态发生冲突；410（Gone）表示服务器上的某个资源被永久性的删除。

# HTTP 高级内容

## Cookie 与 Session

Cookie 和 Session 都为了用来保存状态信息，都是保存客户端状态的机制，它们都是为了解决 HTTP 无状态的问题。

### Cookie 机制

简单地说，cookie 就是浏览器储存在用户电脑上的一小段文本文件。cookie 是纯文本格式，不包含任何可执行的代码。一个 Web 页面或服务器告知浏览器按照一定规范来储存这些信息，并在随后的请求中将这些信息发送至服务器，Web 服务器就可以使用这些信息来识别不同的用户。大多数需要登录的网站在用户验证成功之后都会设置一个 cookie，只要这个 cookie 存在并可以，用户就可以自由浏览这个网站的任意页面。

cookie 会被浏览器自动删除，通常存在以下几种原因：

1. 会话 cookie (Session cookie) 在会话结束时（浏览器关闭）会被删除
2. 持久化 cookie（Persistent cookie）在到达失效日期时会被删除
3. 如果浏览器中的 cookie 数量达到限制，那么 cookie 会被删除以为新建的 cookie 创建空间。

大多数浏览器支持最大为 4096 字节的 Cookie。由于这限制了 Cookie 的大小，最好用 Cookie 来存储少量数据，或者存储用户 ID 之类的标识符。用户 ID 随后便可用于标识用户，以及从数据库或其他数据源中读取用户信息。 浏览器还限制站点可以在用户计算机上存储的 Cookie 的数量。大多数浏览器只允许每个站点存储 20 个 Cookie；如果试图存储更多 Cookie，则最旧的 Cookie 便会被丢弃。有些浏览器还会对它们将接受的来自所有站点的 Cookie 总数作出绝对限制，通常为 300 个。
	
使用 Cookie 的缺点：

* 不良站点用 Cookie 收集用户隐私信息
* Cookie 窃取：黑客以可以通过窃取用户的 Cookie 来模拟用户的请求行为。（跨站请求伪造 CSRF）

### Session 机制

Session机制是一种服务器端的机制，服务器使用一种类似于散列表的结构（也可能就是使用散列表）来保存信息。当程序需要为某个客户端的请求创建一个 session 的时候，服务器首先检查这个客户端的请求里是否已包含了一个 session 标识（session id）：

* 如果已包含一个session id 则说明以前已经为此客户端创建过 session，服务器就按照 session id 把这个 session 检索出来使用（如果检索不到，可能会新建一个）。
* 如果客户端请求不包含 session id，则为此客户端创建一个 session 并且生成一个与此session相关联的 session id ， session id 的值应该是一个既不会重复，又不容易被找到规律以仿造的字符串，这个 session id 将被在本次响应中返回给客户端保存。

具体实现方式：

* **Cookie方式**：服务器给每个Session分配一个唯一的JSESSIONID，并通过Cookie发送给客户端。当客户端发起新的请求的时候，将在Cookie头中携带这个JSESSIONID，这样服务器能够找到这个客户端对应的Session。
* **URL回写**：服务器在发送给浏览器页面的所有链接中都携带JSESSIONID的参数，这样客户端点击任何一个链接都会把JSESSIONID带回服务器。如果直接在浏览器输入服务端资源的url来请求该资源，那么Session是匹配不到的。

## 跨站攻击

### CSRF（跨站请求伪造）

CSRF 是通过伪造请求从而冒充用户在站内的正常操作。

![enter image description here](https://github.com/astaxie/build-web-application-with-golang/raw/master/zh/images/9.1.csrf.png?raw=true)

从上图可以看出，要完成一次 CSRF 攻击，受害者必须依次完成两个步骤 ：

1. 登录受信任网站 A，并在本地生成 Cookie 。
2. 在不退出 A 的情况下，访问危险网站 B。

防范 CSRF 攻击的三种策略：

- 验证码
	CSRF 攻击的过程，往往是在用户不知情的情况下构造网络请求。所以如果使用验证码，那么每次操作都需要用户进行互动，从而简单有效的防御了 CSRF 攻击。但会严重影响用户体验。

- 验证 HTTP Referer 字段
	HTTP 报文头中的字段 Referer 记录了该 HTTP 请求的来源地址。服务端通过验证 Referer 字段来验证请求是来自同一个站点的请求后才提供服务。但由于该字段可以人为篡改，因此也并不安全。

- 在请求地址中添加 token 并验证
	在 HTTP 请求中以参数的形式加入一个随机产生的 token，并在服务器端建立一个拦截器来验证这个 token。token 可以在用户登陆后产生并放于 session 之中，然后在每次请求时把 token 从 session 中拿出，与请求中的 token 进行比对。如果请求中没有 token 或者 token 内容不正确，则认为可能是 CSRF 攻击而拒绝该请求。

- 在 HTTP 头中自定义属性并验证
	这种方法也是使用 token 并进行验证，和上一种方法不同的是，这里并不是把 token 以参数的形式置于 HTTP 请求之中，而是把它放到 HTTP 头中自定义的属性里。通过 XMLHttpRequest 这个类，可以一次性给所有该类请求加上 csrftoken 这个 HTTP 头属性，并把 token 值放入其中。（然而这种方法的局限性非常大。XMLHttpRequest 请求通常用于 Ajax 方法中对于页面局部的异步刷新，并非所有的请求都适合用这个类来发起，而且通过该类请求得到的页面不能被浏览器所记录下，从而进行前进，后退，刷新，收藏等操作，给用户带来不便。另外，对于没有进行 CSRF 防护的遗留系统来说，要采用这种方法来进行防护，要把所有请求都改为 XMLHttpRequest 请求，这样几乎是要重写整个网站，这代价无疑是不能接受的。）

### XSS（跨站脚本攻击）

XSS 全称“跨站脚本”，是注入攻击的一种。其特点是不对服务器端造成任何伤害，而是通过一些正常的站内交互途径，例如发布评论，提交含有 JavaScript 的内容文本。这时服务器端如果没有过滤或转义掉这些脚本，作为内容发布到了页面上，其他用户访问这个页面的时候就会运行这些脚本。

理论上，所有可输入的地方没有对输入数据进行处理的话，都会存在XSS漏洞，漏洞的危害取决于攻击代码的威力，攻击代码也不局限于script。防御 XSS 攻击最简单直接的方法，就是过滤用户的输入。

如果不需要用户输入 HTML，可以直接对用户的输入进行 HTML escape 。一小段脚本：`<script>window.location.href=”http://www.baidu.com”;</script>`，经过 escape 之后就成了： `&lt;script&gt;window.location.href=&quot;http://www.baidu.com&quot;&lt;/script&gt;`。它现在会像普通文本一样显示出来，变得无毒无害，不能执行了。

## Web 缓存
		
WEB缓存(cache)位于Web服务器和客户端之间，缓存机制会根据请求保存输出内容的副本，例如 html 页面、图片、文件。当下一个请求来到的时候：如果是相同的 URL，缓存直接使用副本响应访问请求，而不是向源服务器再次发送请求。

有缓存的 Get 请求过程如下：

![][3]

主要分三种情况:

1. 未找到缓存(黑色线)：当没有找到缓存时，说明本地并没有这些数据，这种情况一般发生在我们首次访问网站，或者以前访问过，但是清除过缓存后。浏览器就会先访问服务器，然后把服务器上的内容取回来，内容取回来以后，就要根据情况来决定是否要保留到缓存中了。

2. 缓存未过期(蓝色线)：缓存未过期，指的是本地缓存没有过期，不需要访问服务器了，直接就可以拿本地的缓存作为响应在本地使用了。这样节省了不少网络成本，提高了用户体验过。

3. 缓存已过期(红色线)：当满足过期的条件时，会向服务器发送请求，发送的请求一般都会进行一个验证，目的是虽然缓存文档过期了，但是文档内容不一定会有什么改变，所以服务器返回的也许是一个新的文档，这时候的HTTP状态码是200，或者返回的只是一个最新的时间戳和304状态码。

    缓存过期后，有两种方法来判定服务端的文件有没有更新。第一种在上一次服务端告诉客户端约定的有效期的同时，告诉客户端该文件最后修改的时间，当再次试图从服务端下载该文件的时候，check 下该文件有没有更新（对比最后修改时间），如果没有，则读取缓存；第二种方式是在上一次服务端告诉客户端约定有效期的同时，同时告诉客户端该文件的版本号，当服务端文件更新的时候，改变版本号，再次发送请求的时候check一下版本号是否一致就行了，如一致，则可直接读取缓存。

浏览器是依靠请求和响应中的的头信息来控制缓存的，如下：

* Expires与Cache-Control：服务端用来约定和客户端的有效时间的。Expires规定了缓存失效时间（Date为当前时间），而Cache-Control的max-age规定了缓存有效时间（2552s）。Expires是HTTP1.0的东西，而Cache-Control是HTTP1.1的，规定如果max-age和Expires同时存在，前者优先级高于后者。

* Last-Modified/If-Modified-Since：缓存过期后，check服务端文件是否更新的第一种方式。

* ETag/If-None-Match：缓存过期时check服务端文件是否更新的第二种方式。实际上ETag并不是文件的版本号，而是一串可以代表该文件唯一的字符串，当客户端发现和服务器约定的直接读取缓存的时间过了，就在请求中发送If-None-Match选项，值即为上次请求后响应头的ETag值，该值在服务端和服务端代表该文件唯一的字符串对比（如果服务端该文件改变了，该值就会变），如果相同，则相应HTTP304，客户端直接读取缓存，如果不相同，HTTP200，下载正确的数据，更新ETag值。

当然并不是所有请求都能被缓存。无法被浏览器缓存的请求：

1. HTTP信息头中包含Cache-Control:no-cache，pragma:no-cache（HTTP1.0），或Cache-Control:max-age=0等告诉浏览器不用缓存的请求
2. 需要根据Cookie，认证信息等决定输入内容的动态请求是不能被缓存的
3. POST请求无法被缓存

浏览器缓存过程还和用户行为有关。譬如先打开一个主页有个 jquery 的请求（假设访问后会缓存下来）。接着如果直接在地址栏输入 jquery 地址，然后回车，响应HTTP200（from cache），因为有效期还没过直接读取的缓存；如果ctrl+r进行刷新，则会相应HTTP304（Not Modified），虽然还是读取的本地缓存，但是多了一次服务端的请求；而如果是ctrl+shift+r强刷，则会直接从服务器下载新的文件，响应HTTP200。

## HTTP 代理

Web代理（proxy）服务器是网络的中间实体。代理位于Web客户端和Web服务器之间，扮演“中间人”的角色。HTTP的代理服务器即是Web服务器又是Web客户端。（Fiddler 是以代理web服务器的形式工作的,它使用代理地址:127.0.0.1, 端口:8888. 当Fiddler退出的时候它会自动注销代理，这样就不会影响别的程序。）

![][4]

代理服务器有许多用处：

* 跨过网络障碍。翻墙技术：局域网不能上网，只能通过局域网内的一台代理服务器上网。
* 匿名访问。HTTP代理服务器通过删除HTTP报文中的身份特性（比如客户端的IP地址，或cookie,或URI的会话ID），从而对远端服务器隐藏原始用户的IP地址以及其他细节。同时HTTP代理服务器上也不会记录原始用户访问记录的log。
* 通过代理缓存，加快上网速度。大部分代理服务器都具有缓存的功能，不断将新取得数据存储到它本地的存储器上，如果浏览器所请求的数据在它本机的存储器上已经存在而且是最新的，那么直接将存储器上的数据传给用户，这样就能显著提高浏览速度。
* 过滤指定内容。比如儿童过滤器，很多教育机构，会利用代理来阻止学生访问成人内容。

代理服务器和抓包工具（比如Fiddler）都能看到http request中的数据。如果我们发送的request中有敏感数据，比如用户名，密码，信用卡号码，就会被代理服务器看到。所以我们一般都是用HTTPS来加密Http request。

# 参考

[深入理解HTTP协议（二）——协议详解篇](http://www.voidcn.com/blog/huangjianxiang1875/article/p-1596378.html)  
[深入理解HTTP协议（三）——深入了解篇](http://www.voidcn.com/blog/huangjianxiang1875/article/p-1596379.html)  
[RFC2616 is Dead](https://www.mnot.net/blog/2014/06/07/rfc2616_is_dead)  
[HTTP协议 (四) 缓存](http://www.cnblogs.com/TankXiao/archive/2012/11/28/2793365.html)  
[HTTP cookies 详解](http://bubkoo.com/2014/04/21/http-cookies-explained/)  
[细说 Cookie](http://www.cnblogs.com/fish-li/archive/2011/07/03/2096903.html)  
[HTTP/1.1与HTTP/1.0的区别](http://blog.csdn.net/forgotaboutgirl/article/details/6936982)  
[浏览器缓存机制浅析](http://web.jobbole.com/82997/)  
[HTTP缓存机制](http://oohcode.com/2015/05/28/http-cache/)  
[Http状态码查询，各种返回码的详解](http://www.bkjia.com/headlines/491296.html)  
[HTTP协议详解(五) http协议代理](http://www.bkjia.com/headlines/491855.html)  
[Http(二)-消息报头](http://xfhnever.com/2014/10/08/http-header/)  
[CSRF 攻击的应对之道](https://www.ibm.com/developerworks/cn/web/1102_niugang_csrf/) 
[99%的人都理解错了HTTP中GET与POST的区别](http://mp.weixin.qq.com/s?__biz=MzI3NzIzMzg3Mw==&mid=100000054&idx=1&sn=71f6c214f3833d9ca20b9f7dcd9d33e4#rd)  


[1]: http://www.ruanyifeng.com/blogimg/asset/2016/bg2016081901.jpg
[2]: http://7xrlu9.com1.z0.glb.clouddn.com/Network_HTTP_2.png
[3]: http://7xrlu9.com1.z0.glb.clouddn.com/Network_HTTP_3.png
[4]: http://7xrlu9.com1.z0.glb.clouddn.com/Network_HTTP_4.png

