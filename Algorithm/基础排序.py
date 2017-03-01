#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
插入排序：
	数组分为已排序和未排序两个部分，每次从未排序部分取一个数
插入到已排序部分，直至所有数都在已排序部分里
'''
def insert_sort(arr):

	for i in range(len(arr)-1):      # i为已排序部分的最大index
		j = i + 1                # j为待排序部分的最小index
		#把该轮迭代中的新数插入已排序部分
		while j > 0 and arr[j] <= arr[j-1]:
			arr[j],arr[j-1] = arr[j-1],arr[j]
			j -= 1
		print l                  # 打印出每次迭代情况

'''
选择排序：
	每次从数组中查找最小的数与放置在其应处位置上的数进行交换，直至所有数
都取完
'''		
def select_sort(arr):
	for i in range(len(arr)):
		min = float('inf')
		index = -1
		for j in range(i,len(arr)):
			if arr[j] < min:
				min = arr[j]
				index = j
		arr[i],arr[index] = arr[index],arr[i]

'''
冒泡排序
'''
def bubble_sort(arr):
	for i in range(len(arr)-1):
		Need_Next = False
		for j in range(len(arr)-i-1):
			if arr[j] > arr[j+1]:
				arr[j],arr[j+1] = arr[j+1],arr[j]
				Need_Next = True
		if Need_Next == False :
			break


# l = [4,5,7,9,7,5,1,0,7,-2,3,-99,6]
# print l 
