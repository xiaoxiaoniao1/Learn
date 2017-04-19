# 概述

Spring 是一个为了解决企业级应用开发的复杂性而创建的开源框架。Spring 不仅仅局限于服务器端开发，任何 Java 应用都能在简单性、可测试性和松耦合等方面从 Spring 中获益。**简化 Java 开发是 Spring 最根本的使命**。

为了降低 Java 开发的复杂性，Spring 采取了以下策略：

- 基于 POJO 的轻量级和最小侵入性编程（侵入性：强迫应用继承框架的类或接口从而和框架绑死）
- 通过依赖注入和面向接口实现松耦合
- 基于切面和惯例进行声明式编程
- 通过切面和模板减少样板式代码

# 依赖注入（DI）

任何一个有实际意义的应用都由两个以上的类组成，这些类互相协作来完成特定的业务逻辑。但如果按照传统的做法，让每个对象负责管理与自己相互协作的对象（即所依赖的对象）的引用，将会导致高度耦合和难以测试的代码。

> 耦合具有两面性：一方面紧密耦合的代码难以测试与复用，另一方面一定程度的耦合是必须的——完全没有耦合的代码什么也做不了。因此耦合是必须的，但应当谨慎管理。

通过依赖注入（DI），对象的依赖关系将由系统中负责协调各对象的第三方组件在创建对象的时候进行设定，对象无需自行创建或管理它们的依赖关系，从而实现**松耦合**。而且如果一个对象只通过接口（而非具体实现）来表明依赖关系，则这种依赖就能在对象本身无感知的情况下，用不同的具体实现进行替换。

创建应用组件之间协作的行为称为**装配**。Spring 有多种装配 bean 的方式，其中使用 XML 配置文件是一种常见的装配方式。

```xml
<!-- knignt.xml  -->
<?xml version="1.0" encoding="UTF-8" ?>
<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
	xsi:schemaLocation="http://www.springframework.org/schema/beans 
       http://www.springframework.org/schema/beans/spring-beans-4.0.xsd">
<!-- 注入Quest bean -->
<bean id="knight" class="com.war.knights.BravaKnight">
	<constructor-arg ref="quest" />
</bean>
<!-- 创建SavaGirlQuest bean -->
<bean id="quest" class="com.war.knights.SavaGirlQuest">
	<constructor-arg value="Mary" />
</bean>

</beans>
```
Spring 也支持使用 **Java 注解** 来描述配置。
```
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.war.knights.Knight;
import com.war.knights.BraveKnight;
import com.war.knights.Quest;
import com.war.knights.SaveGirlQuest;

@Configuration
public class KnightConfig{
	@Bean
	public Knight knight(){
		return new BraveKnignt(quest());
	}
	
	@Bean
	public Quest quest(){
		return new SaveGirlQuest("Mary");
	}
}
```

Spring 通过应用上下文（Application Context）装载 bean 的定义并把它们组装起来。Spring 有多种应用上下文的实现，主要区别在于用何种方式加载配置。

```
// 使用上下文加载配置文件并读取bean
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class KnightMain{
	public static void main(String[] args) throws Exception{
		// 加载上下文
		ClassPathXmlApplicationContext context = new ClassPathXmlApplicationContext("META-INF/spring/knight.xml");
		// 获取 knight bean
		Knight knight = context.getBean(Knight.class);
		// 使用 knight
		knight.embarkOnQuest();
		context.close();
	}
}
```

main() 方法基于 knight.xml 文件创建了 Spring 应用上下文，并调用上下文获取了 ID 为 knight 的 bean。注意：该类完全不知道骑士接受何种探险任务，而且完全没有意识到是由 BraveKnight 来执行的，只有 knight.xml 知道哪个骑士执行哪种探险任务。

# 面向切面编程（AOP）

DI 能够让相互协作的软件实体保持松耦合，而 AOP 则允许把遍布应用组件各处的系统职责从组件中分离出来。

系统由不同组件组成，每个组件负责一块特定功能。除了实现自身核心的功能外，这些组件还经常承担着额外职责（诸如日志、事务管理、安全等，这些额外的职责经常融入到自身具有核心业务逻辑的组件中去）。
这些需额外承担的系统服务被称为**横切关注点**，因为它们会跨越系统的多个组件。

如果按照传统方式把这些关注点分散到多个组件中去，则代码会有双重的复杂性：

- 实现系统关注点功能的代码重复出现在多个组件中（即使把关注点抽象为了一个独立模块，其他模块只是调用其方法，但方法的调用还是会重复出现在各个模块中）。
- 组件会因为那些与自身核心业务逻辑无关的代码而变得混乱。

AOP 能够使这些服务模块化，并以声明的方式把它们应用到它们需要影响的组件中去。这样做的好处在于：这些组件会具有更高的内聚性与简单性（组件甚至不知道系统服务的存在）。

下列 xml 文件使用了 Spring 的 aop 配置把 minstrel bean 声明为一个切面，以及声明 minstrel bean 的 embarkOnQuest 方法作为切点，并声明了切点执行时的前置方法与后置方法。
```
<?xml version="1.0" encoding="UTF-8" ?>
<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
	xmlns:aop="http://www.springframework.org/schema/aop" 
	xsi:schemaLocation="http://www.springframework.org/schema/beans 
       http://www.springframework.org/schema/beans/spring-beans-4.0.xsd
       http://www.springframework.org/schema/aop
       http://www.springframework.org/schema/aop/spring-aop-4.0.xsd">
<!-- 声明 minstrel -->
<bean id="minstrel" class="com.war.knights.Minstrel">
	<constructor-arg ref="a common minstrel" />
</bean>

<aop:config>
	<aop:aspect ref="minstrel">
		<!-- 定义切点 -->
		<aop:pointcut id="embark" expression="execution(* *.embarkOnQuest(..))"/>
		<!-- 声明前置通知 -->
		<aop:before pointcut-ref="embark" method="singBeforeQuest"/>
		<!-- 声明后置通知 -->
		<aop:after pointcut-ref="embark" method="singAfterQuest"/>
	</aop:aspect>
</aop:config>

</beans>
```

# Spring 容器

在基于 Spring 的应用中，应用对象生存于 Spring 容器中。Spring 容器负责创建、装配和配置对象，并管理它们的整个生命周期。Spring 容器使用 DI 管理构成应用的组件，它会创建相互协作的组件之间的关联。

Spring 自带了两种类型的容器实现：

- BeanFactory（bean 工厂）：最简单的容器，提供基本的 DI 支持。
- Application Context（应用上下文）：基于 BeanFactory 构建，并提供应用框架级别的服务。开发者一般使用应用上下文而非底层的 bean 工厂。

## 应用上下文

Spring 自带了多种类型的应用上下文：

- AnnotationConfigApplicationContext：从一个或多个基于 Java 的配置类中加载 Spring 应用上下文
- AnnotationConfigWebApplicationContext：从一个或多个基于 Java 的配置类中加载 Spring Web 应用上下文
- ClassPathXmlApplicationContext：从类路径下的一个或多个 XML 配置文件中加载上下文定义
- FileSystemXmlapplicationcontext：从文件系统下一个或多个 XML 配置文件加载上下文定义
- XmlWebApplicationContext：从 Web 应用下的一个或多个 XML 配置文件加载上下文定义

上下文加载完毕后，就可以调用上下文的 getBean() 方法从 Spring 容器中获取 bean。

## bean 的生命周期

![bean 的生命周期](http://upload-images.jianshu.io/upload_images/3131012-0fdb736b21c8cc31.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**ApplicationContext 容器中**，Bean 的生命周期流程如上图所示，流程大致如下：

1. 容器启动，对 scope 为 singleton 且非懒加载的 bean 进行实例化
2. 按照 Bean 定义信息配置信息，注入所有的属性
3. 如果 Bean 实现了 BeanNameAware 接口，会回调该接口的 setBeanName() 方法，传入该 Bean 的 id ，此时该 Bean 就获得了自己在配置文件中的 id
4. 如果 Bean 实现了 BeanFactoryAware 接口,会回调该接口的 setBeanFactory() 方法，传入该 Bean 的 BeanFactory ，这样该 Bean 就获得了自己所在的 BeanFactory
5. 如果 Bean 实现了 ApplicationContextAware 接口,会回调该接口的 setApplicationContext() 方法，传入该 Bean 的 ApplicationContext，这样该 Bean 就获得了自己所在的 ApplicationContext
6. 如果 Bean 实现了 BeanPostProcessor 接口，则会回调该接口的 postProcessBeforeInitialzation() 方法
7. 如果 Bean 实现了 InitializingBean 接口，则会回调该接口的 afterPropertiesSet() 方法
8. 如果 Bean 配置了 init-method 方法，则会执行 init-method 配置的方法
9. 如果 Bean 实现了 BeanPostProcessor 接口，则会回调该接口的 postProcessAfterInitialization() 方法
10. 经过流程9之后，就可以正式使用该 Bean 了。对于 scope 为 singleton 的 Bean，Spring 的 IOC 容器中会缓存一份该 bean 的实例，而对于 scope 为 prototype 的 Bean，每次被调用都会 new 一个新的对象，其生命周期就交给调用方管理了，不再由 Spring 容器进行管理了
11. 容器关闭后，如果 Bean 实现了 DisposableBean 接口，则会回调该接口的 destroy() 方法
12. 如果 Bean 配置了 destroy-method 方法，则会执行 destroy-method 配置的方法。至此，整个Bean的生命周期结束

# Spring 其他模块

Spring 框架除了 DI 与 AOP 以外还有着其他大量模块，所有模块共同组成了一个构建在 Spring 核心框架之上的庞大生态圈。这些模块依据其所属功能可划分为六类。

### Spring 容器

容器是 Spring 框架最核心的部分，用于执行 bean 的创建、配置与管理。该模块包括了 bean 工厂，它为 Spring 提供了 DI 的功能。基于 bean 工厂，还有多种 Spring 应用上下文的实现，每一种都提供了配置 Spring 的不同方式。

### AOP 模块

AOP 可以把遍布系统的关注点（如事务和安全）从它们所应用的对象中解耦出来。

### 数据访问和集成

提供了模板化的 JDBC，并在多种数据库服务的错误信息上构建了语义丰富的异常层。以及允许使用 ORM 框架。

###  Web 与远程调用

Web 与远程调用模块提供了自带的 MVC 框架，此外还提供了多种构建与其他应用交互的远程调用方案，以及对 REST API 的良好支持。

### 测试

提供了自带的测试模块（如一系列的 mock 对象实现）