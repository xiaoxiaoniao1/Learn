# Java集合框架
Java 集合框架是 Java 提供的几个能有效组织和操作数据的数据结构，支持两种类型的容器：**集合**与**图**。

Java 集合框架支持三种主要类型的集合：规则集(Set)、线性表(List)和队列(Queue)。Set 的实例用于存储一组不重复的元素，List 的实例用于存储一个由元素构成的有序集合，Queue 的实例用于存储先进先出方式处理的对象。

## Collection 接口
Collection 接口是处理对象集合的根接口，提供了在集合中添加、删除元素与查询的基本操作。

![vh pt o_2 d xzxqtx4zu4](https://cloud.githubusercontent.com/assets/22606175/23020423/06d89b9e-f482-11e6-90a6-fd25d5ca02e2.png)

AbstractCollection 类是提供 Collection 接口的部分实现的便利类。

## 规则集
Set 接口扩展了 Collection 接口，并未引入新的方法或常量，只是规定 Set 的实例不包含重复的元素。以下介绍 Set 接口的三个具体类。

- 散列集 HashSet：以一个不可预知的顺序存储元素。
- 链式散列集 LinkedHashSet：以元素被插入的顺序存储元素。
- 树形集 TreeSet：存储已按照元素之间的比较原则排好序的元素；可使用元素的 Comparable 接口或者指定一个比较器。

## 比较器接口 Comparator
有时希望将元素插入到一个树集合中，而这些元素可能不是 java.lang.Comparable 的实例，此时可定义一个比较器来比较这些元素。若如此做，则需创建一个实现 java.util.Comparator 接口的比较器类。Comparator 接口有两个方法：compare 与 equals 。

要想使用比较器，必须使用构造方法 TreeSet(Comparator comparator) 来创建一个有序集，它可使用比较器中的 compare 方法进行排序。

## 线性表
线性表不仅可以存储重复的元素，而且允许用户指定它们存储的位置。

- 数组线性表类 ArrayList ：实现 List 接口的可变大小的数组
- 链表类 LinkedList ：实现了 List 接口的一个链表。此外还额外提供了从线性表两端操作元素的方法。

## 备注
- Java 集合框架中的所有实例类都实现了 Cloneable 和 Serializable 接口，因此它们的实例都是可复制和可序列化的。

