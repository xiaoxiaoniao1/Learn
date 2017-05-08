
Spring 提供了三种主要的装配机制来描述对 bean 的装配：

- 在 XML 中进行显式配置
- 在 Java 中进行显式配置
- 隐式的 bean 发现机制和自动装配

# 自动化装配

Spring 从两个角度实现自动化装配：

- 组件扫描：Spring 会自动发现应用上下文中所创建的 bean
- 自动装配：Spring 自动满足 bean 之间的依赖

以下以 CD 播放器为例阐述如何进行自动化装配：首先创建 CD 类，让 Spring 将其自动创建为 bean，然后创建一个 CDPlayer 类，让 Spring 把 CD bean 注入进来。

```
/* 创建CD类并声明为bean */
package main;
import org.springframework.stereotype.Component;

@Component // 该注解把该类声明为bean,也可以用Component("name")形式进行命名
public class CD {
    private String message = "this is my cd";
    public void play(){
        System.out.println(message);
    }
}
```

但组件扫描是默认不启用的，因此还需要显式配置 Spring 从而让其寻找带有 @Component 注解的类并为其创建 bean。类 CDPlayerConfig 通过 Java 代码而非配置文件来定义了装配规则（虽然为空），并使用了 @ComponentScan 注解启用了组件扫描。

```
package main;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;

@Configuration
@ComponentScan
public class CDPlayerConfig {
}
```
> @ComponentScan 默认会以配置类所在的包作为基础包来扫描组件。若想扫描多个基础包，则可以设置注解的属性如`@ComponentScan(basePackages={"soundsystem","video"})`
> 
创建了这两个类后，现在我们可以对功能进行测试，观察 bean 是否注入成功。
```
package main;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import static org.junit.Assert.*;

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(classes = CDPlayerConfig.class) // 该注解指定从哪个配置类加载配置
public class CDPlayerTest {
	// 使用 Autowird 自动装配；该注解可适用于类的任何方法上
	// 若有且只有一个bean匹配依赖需求的话，则spring会加载这个bean；否则会抛出异常
    @Autowired 
    private CD cd;

    @Test
    public void myTest(){
        assertNotNull(cd);
    }
}
```

# 使用 Java 代码装配 bean

虽然很多场景下通过组件扫描和自动装配实现 Spring 的自动化配置是更为推荐的方式，但有时自动化配置的方案行不通，因此需要显式地配置 Spring。显式配置有两种方案：Java 和 XML，其中 JavaConfig 由于更为强大、类型安全以及对重构友好，因此是较好的方案。

### 1. 创建配置类

创建 JavaConfig 类的关键在于为其添加 @Configuration 注解，表明该类是一个配置类，该类应该包含**在 Spring 应用上下文中如何创建 bean** 的细节。

```
import org.springframework.context.annotation.Configuration;

@Configuration
public class CDPlayerConfig{
}
```

### 2. 声明简单的 bean

在 JavaConfig 中声明 bean，需要编写一个方法，该方法会创建所需类型的实例，然后为这个方法添加 @Bean 注解。@Bean 注解会告诉 Spring 这个方法会返回一个对象，该对象注册为 Spring 应用上下文中的 bean。

```
// 声明一个返回CD类型的实例的bean
@Bean
public CD sgtPeppers(){
	return new SgtPeppers(); //此处SgtPeppers是CD的子类
}
```

默认情况下 bean 的 ID 与带有 @Bean 注解的方法名是一样的，也可以通过 @Bean(name="name") 的形式为其命名。

### 3. 借助 JavaConfig 实现注入

在配置中，我们往往需要声明一个依赖于其他 bean 的 bean，因此在声明一个复杂的 bean 时往往也需要同时注入其他的 bean。

装配 bean 的最简单方式是引用创建 bean 的方法：

```
@Bean // 带有@Bean注解的方法可以采用任何必要的Java功能来产生bean实例
public CDPlayer cdPlayer(){
	return new CDPlayer(sgtPeppers());// sgtPeppers()是已经声明的、被@Bean所注解的方法
}
```

> 看起来 CD 是通过 sgtPeppers() 得到的，但实际上，由于 sgtPeppers() 方法上添加了 @Bean 注解，Spring 会拦截所有对它的调用，确保直接返回该方法的 bean，而不是每次都进行实际的调用。**默认情况下，Spirng 中的 bean 都是单例**。

但也可用以下更容易理解的方式来装配 bean：

```
@Bean
public CDPlayer cdPlayer(CD cd){
	CDPlayer cdPlayer = new CDPlayer(cd);
	cdPlayer.setCD(cd);
	return cdPlayer;
}
```

此处 cdPlayer() 方法请求一个 CD 实例作为参数，当 Spring 调用 cdPlayer() 创建  CDPlayer bean 时，它会自动装配一个 CD bean 到配置方法中，而无需明确引用 CD 的 @Bean 方法。通过该方式引用其它的 bean 是最佳选择（因为它不会要求将 CD bean 声明到同一个配置类中，这样可以实现分散配置文件）。  

# 通过 XML 装配 bean

Spring 目前有了强大的自动化配置和基于 Java 的配置，XML不再是第一选择了。但是鉴于已经存在那么多基于 XML 的 Spring 配置，因此理解如何在 Spring 中使用 XML 还是很重要的。

## 1. 创建XML装配规范

最简单的 XML 配置如下：

```
<?xml version="1.0" encoding="UTF-8" ?>
<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://www.springframework.org/schema/beans 
       http://www.springframework.org/schema/beans/spring-beans-4.0.xsd
       http://www.springframework.org/schema/context">
       
	<!-- configuration details go here -->

</beans>
```

用于装配 bean 的最基本的 XML 元素包含在 spring-beans 模式中，它被定义为根命名空间。`<beans>` 是该模式中的一个元素，是所有 Spring 配置文件的根元素。

## 2. 声明一个简单的 bean

使用`<bean>`元素声明一个 bean，并设置 id 进行命名：
```
<bean id="cd1" class="soundSystem.SgtPeppers" />
```

## 3. 借助构造器注入初始化 bean

使用构造器注入 bean 引用时，有两种基本配置方案可选择：

- `<constructor-arg>` 元素，特点是配置比较冗长
- 使用 Spring 3 所引入的 c-命名空间，特点是配置比较简练，但无法装配`集合`

### 使用`<constructor-arg>`声明

```
/* 声明CDPlayer并通过id引用已有的SgtPerpers bean*/
<bean id=“cdPlayer” class="soundSystem.CDPlayer">
	<constructor-arg ref="sgtPerpers" />
</bean>
```

当 Spring 遇到`<bean>`元素时，会创建一个 CDPlayer 实例，`<constructor-arg>` 元素表明要将一个 id 为 sgtPerpers 的 bean 引用传递到 CDPlayer 的构造器中。

当把字面量注入构造器而不是引用时：

```
<bean id=“cdPlayer” class="soundSystem.CDPlayer">
	<constructor-arg value="The Love" />
</bean>
```

### 使用c-命名空间

在 XML 顶部声明其模式：`xmlns:c="http://www.springframework.org/schema/c"`，就可用其来声明构造器参数了。

一个典型的示例是 `c:cd-ref="compactDisc"`，属性名以 `c:` 开头，即命名空间前缀，接下来是要装配的构造器参数名，之后是`-ref`，表示装配的是一个 bean 的引用，这个 bean 的 ID 为 `compactDisc`。

也可使用参数索引替代直接使用参数名的方案，如：

```
<!-- 由于xml不允许数字作为属性的首字符，因此添加一个下划线作后缀 -->
<bean id=“cdPlayer” class="soundSystem.CDPlayer" c:_0-ref="compactDisc" />
```

也可以根本不标示参数（前提是只有一个构造器参数），如：

```
<bean id=“cdPlayer” class="soundSystem.CDPlayer" c:_-ref="compactDisc" />
```

当需要注入字面量而不是 bean 引用时：

- 方案一：引用构造器参数的名字
```
<bean id=“cdPlayer” class="soundSystem.CDPlayer"
	c:_title="My Love"
	c:_artist="ZZP">
```

- 方案二：使用参数索引

```
<bean id=“cdPlayer” class="soundSystem.CDPlayer"
	c:_0="My Love"
	c:_1="ZZP">
```

## 4. 属性注入

假设需要属性注入的 CDPlayer 如下所示：
```
public class CDPlayer {
	private CD cd;
	
	@Autowired
	pulic setCd(CD cd){
		this.cd = cd;
	}
}
```
声明为一个 bean：
```
<bean id=“cdPlayer” class="soundSystem.CDPlayer">
	<property name="cd" ref="cd">
</bean>
```

`<property>`元素为属性的 Setter 方法所提供的功能与 `<constructor-arg>` 提供的功能是一样的。本例中它引用了 ID 为 `CD` 的 bean（通过 ref 属性），并将其注入到 `cd` 属性中（通过 setCD() 方法）。

### p-命名空间

 p-命名空间是作为`<property>`元素的替代方案，使用时需在 XML 顶部声明其模式：`xmlns:p="http://www.springframework.org/schema/p"`。

```
<bean id=“cdPlayer” 
	class="soundSystem.CDPlayer" 
	p:cd-ref="cd"/>
<!--
	首先属性的名字使用了"p:"前缀，表面设置的是一个属性；接下来是要注入的属性名，最后属性名称以"-ref"结尾，表明装配的是一个引用而非字面量。
-->
```

当需要注入字面量时，区别在于是否带有"-ref"后缀：

```
<bean id=“cdPlayer” 
	class="soundSystem.CDPlayer" 
	p:title="My Love"
	p:artist="ZZP"/>
```

> 注意：p-命名空间同样无法装配集合，但可以通过 util-命名空间（用于创建集合类型的bean）辅助实现装配集合的功能。