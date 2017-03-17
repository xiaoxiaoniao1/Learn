# 进阶排序

## 堆排序
堆是一棵具有以下属性的二叉树：

- 它是一棵完全二叉树
- 每个节点大于等于它的任意一个子节点

堆可存储在一个数组中。对于位置 i 处的节点，它的左子节点在位置 2i+1 ，右子节点在位置 2i+2 ，而其父节点在位置 (i-1)/2。

添加一个新节点时，首先添加其到堆的末尾，然后重新构建堆；删除根节点时，把堆末尾的节点移到根节点处，重新构建堆。

由于堆的高度是O(logn)，因此构建一个由 n 个元素组成的堆需要O(nlogn)时间。

```
// java 手写堆代码
public class Heap<E extends Comparable<E>> {
	private List<E> list = new ArrayList<E>();
	public Heap() {}
	public Heap(E[] objects){
		for(E e : objects)
			list.add(e);
	}
	// 堆加入新元素并重新形成堆
	public void add(E newObject){
		int newIndex = list.size();
		list.add(newObject);
		int parentIndex = (newIndex - 1) / 2;
		
		while(newIndex > 0){
			if(list.get(newIndex).compareTo(list.get(parentIndex)) <= 0)
				break;
			else{
				swap(newIndex,parentIndex);
				newIndex = parentIndex;
				parentIndex = (newIndex - 1) / 2;
			}
		}
	}
	private void swap(int index1,int index2){
		E temp = list.get(index1);
		list.set(index1, list.get(index2));
		list.set(index2, temp);
	}
	// 堆移除并返回根元素
	public E remove(){
		if(list.size()>0){
			E root = list.get(0);
			swap(0,list.size()-1);
			list.remove(list.size()-1);
			// 从根节点重新构成堆
			int curIndex = 0;
			while(curIndex < list.size()-1){
				int leftChild = curIndex * 2 + 1;
				int rightChild = curIndex * 2 + 2;
				if(leftChild >= list.size())
					break;
				else if(rightChild >= list.size()){
					if(list.get(leftChild).compareTo(list.get(curIndex))>0)
						swap(curIndex,leftChild);
					break;
				}
				if(list.get(curIndex).compareTo(list.get(leftChild))>=0 && list.get(curIndex).compareTo(list.get(rightChild))>=0)
					break;
				if(list.get(leftChild).compareTo(list.get(rightChild)) > 0){
					swap(curIndex,leftChild);
					curIndex = leftChild;
				}
				else{
					swap(curIndex,rightChild);
					curIndex = rightChild;
				}
			}
			return root;
		}			
		else return null;
	}
	
	public int getSize(){
		return list.size();
	}
}
```
## 桶排序和基数排序
 桶排序和基数排序是**针对整数键值**的特定排序算法。不通过比较键值而是使用桶来对键值排序，因此比一般的排序算法效率要高。
 
桶排序：

- 假设键值的范围是从 0 到 N-1 ，则需要N个标记为 0，1，...，N-1 的桶
- 若元素的键值是 i，则将该元素放入桶 i 中，则每个桶中都存在与键值具有相同值的元素
- 桶排序是稳定的，即，若原始线性表中两个元素有相同键值，则在有序线性表中两元素也顺序不变

但当 N 的范围太大时，桶的数量过多，不可取。此时可使用基数排序，它是基于桶排序的，但只使用十个桶。基数排序将键值基于它们的基数位置分成小组，然后重复地从最显著的基数位置开始，对其上的键值应用桶排序。

## 外排序
当数据过多不能全放入内存时，需要外排序算法。一般是通过归并排序的一种变体实现外排序：

1. 将大文件切割为小于内存大小的段，重复将每段从文件读入数组，用内部排序算法对数组排序，然后把数据输出到临时文件中。这样就得到了若干个有序分段。
2. 将每对有序分段归并为一个大的有序分段，并把新分段也存储到临时文件中。不断重复，直到所有数据归并为一个分段。

