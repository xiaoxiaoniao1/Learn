# 泛型
泛型是指参数化类型的能力。定义了带泛型类型的类或方法，在编译过程中编译器会用具体类型替换它。主要优点在于能够在编译时而不是在运行时检测出错误。

``` java
/* 使用泛型前 */
public interface Comparable{
	public int compareTo(object o);
} 

/* 使用泛型后 */
public interface Comparable<T>{
	public int compareTo(T o);
} 
```

## 泛型类和泛型方法

- 为了定义一个类为泛型类型，需要将泛型类型放在类名之后，如：`GenericStack<E>`。
- 受限泛型类型：可将泛型制定为另外一种类型的子类型。如：`<E extends GeometricObject>`。
- 为了定义一个方法为泛型类型，需要把泛型类型放在方法返回类型之前，如`<E> void max(E o1,E o2)`。
- 为了调用泛型方法，需要将实际类型放在尖括号内作为方法名的前缀，如`GenericStack.<String>print(strings)`。
 
## 原始类型和向后兼容

- **使用**泛型类时可以无需指定具体类型，如：`GenericStack stack = new GenericStack();`，其大体等价于`GenericStack<Object> stack = new GenericStack<Object>();`。
- 像 GenericStack 和 ArrayList 这样不使用类型参数的泛型类称为”原始类型“。
- 原始类型并不安全，但使用原始类型是为了向后兼容 JDK 较早的版本。

## 通配泛型

- 尽管 Integer 是 Number 的子类型，但是 `GenericStack<Interger>`并不是`GenericStack<Number>`的子类型。为了避免该问题，可以使用通配泛型类型。
- 通配泛型有三种形式`?`、`? extends T`和`? super T`（此处的T代表某个泛型类型）：
    -  `?`：称为非受限通配，等价于`? extends Object`。
    - `? extends T`：称为受限通配，代表T的一个未知子类型。
    - `? super T`：称为下限通配，表示T的一个未知父类型。

## 消除泛型与使用泛型的限制

泛型是使用一种称为类型消除的方法来实现的：在编译时一旦编译器确认泛型类型是安全的，就会将它转换为原始类型。
```java
/*编译器转换前*/
ArrayList<String> list = new ArrayList<String>();
list.add("Trump");
String state = list.get(0);

/*编译器转换后*/
ArrayList list = new ArrayList();
list.add("Trump");
String state = (String)(list.get(0));
```

由于泛型在运行时已被消除，因此对于如何使用泛型类型是有一些限制的：

- 不能使用`new E()`。
- 不能使用`new E[]`。
- 在静态环境下不允许类的参数是泛型类型。
- 异常类不能是泛型的。

## 备注

 - 泛型类型必须是引用类型
 - 尽管在编译时`ArrayList<String>`与`ArrayList<Integer>`是两种类型，但是在运行时只有一个 ArrayList 类会被加载到 JVM 中
