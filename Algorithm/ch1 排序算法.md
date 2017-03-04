# 排序算法

## 冒泡排序

优化细节：

- 第k次遍历时，不需要考虑最后k-1个元素
- 如果在某次遍历中没有发生交换，则排序结束

## 归并排序

- 主排序部分——mergesort(seq)：决定什么情况下递归以及什么情况下停止递归，返回值为排序完成的序列
- 归并部分——merge(left,right)：合并两个给出的序列，返回值为合并后的序列

```
# python示例代码

def mergesort(seq):  
    if len(seq)<=1:            #当子数组只有一个元素时，停止递归
        return seq  
    mid=int(len(seq)/2)  
    left=mergesort(seq[:mid])  
    right=mergesort(seq[mid:])  
    return merge(left,right)  
  
def merge(left,right):  
    result=[]  
    i,j=0,0  
    while i<len(left) and j<len(right):  
        if left[i]<=right[j]:  
            result.append(left[i])  
            i+=1  
        else:  
            result.append(right[j])  
            j+=1  
    result+=left[i:]  
    result+=right[j:]  
    return result  
  
if __name__=='__main__':  
    seq=[4,5,7,9,7,5,1,0,7,-2,3,-99,6]  
    print(mergesort(seq))  
```

## 快速排序
从数组中选择一个元素作为 pivot ，将数组分为两部分，使得第一部分中的所有元素小于等于 pivot ，而第二部分所有元素都大于 pivot ，然后对这两部分都递归地应用快速排序算法。

```
# python示例代码
# 默认数组第一个数为pivot

def quicksort(arr,first,last):
	if last > first:
		mid = partition(arr,first,last)
		quicksort(arr,first,mid-1)
		quicksort(arr,mid+1,last)

def partition(arr,first,last):
	hign,low = last,first+1
	pivot = arr[first]
	
	while low < hign:
		while low <= hign and arr[low] <= pivot:
			low += 1
		while hign >= low and arr[hign] > pivot:
			hign -= 1
		if low < hign:
			arr[low],arr[hign] = arr[hign],arr[low]
	
	# 此处的意义在于：
	# hign终止时，可能指向一个等于pivot的数（因为low指向等于pivot的数时不会停下）
	# 此时与位置为first的数交换也等于没有交换
	# 因此需把hign继续向左推，直到hign指向小于pivot的数或指向first
	while hign > first and arr[hign] >= pivot:
		hign -= 1
	
	# 如果主元被移动，方法返回将子数组分为两部分的主元的新下标
	# 否则返回主元的原始下标
	if arr[hign] < pivot: 
		arr[hign],arr[first] = arr[first],arr[hign]
		return hign
	else:
		return first
```

## 与归并排序的比较

- 归并排序归并时需要临时数组，而快排不需要额外的空间，因此快排的空间效率高
- 平均情况下两者效率相同
- 最差情况下归并排序的效率高于快排
