class XNode:
    # Initialize an XNode object with a given x-value
    def __init__(self,x):
        self.value = x
        self.Ytree = None
        self.left = None
        self.right = None

class YArray:
	def __init__(self,array):
		# Initialize a YArray object with a sorted array of y-values
		self.item = array
	
	def binary_search(self,start,end,value,index):
		# Binary search in the YArray to find the insertion position for x
		# Returns he index where x should be inserted or found in the YArray, if search unsuccesfult returns default index

		if len(self.item) == 0:
			return None
			
		m = (start + end)//2
		mid = self.item[m]  
		if start < end:
			if mid >= value: #search in left subtree
				return self.binary_search(start,m-1,value,index)
			else: #search in right subtree
				return self.binary_search(mid+1,end,value,m)
		elif start == end:
			if mid >= value:
				return index
			else:
				return m
		else:
			return index

	def y_search_in_range(self,y_range):
		# Search for y-values within a given range in the YArray
		ind = self.binary_search(0,len(self.item)-1,y_range[0],None)
		range = []
		if ind == None: #empty YArray
			ind = -1
		ind+=1
		while ind < len(self.item):
			if self.item[ind] <= y_range[1]:
				range.append(self.item[ind])
			else:
				break
			ind+=1
		return range		

class PointDatabase:
	def __init__(self,pointlist):
		# Initialize a PointDatabase object with a list of points
		self.root = None               # Root XNode of the tree
		self.get_y_from_x = None	   # Dictionary to map x-values to y-values
		self.get_x_from_y = None       # Dictionary to map y-values to x-values
		self.build(pointlist)
		
		
	def build_help(self, get_y_from_x, get_x_from_y, x_sorted_array, array):
		# Recursively build the XNode tree
		if len(x_sorted_array) == 0:
			return None
		elif len(x_sorted_array) == 1:
			# Create a leaf XNode with associated YArray
			leaf = XNode(x_sorted_array[0])
			leaf.YTree = YArray([array[0]])
			return leaf
			
		t = len(x_sorted_array)//2
		median = x_sorted_array[t]
		v = XNode(median)
		
		v.YTree = YArray(array)
		
		y_left, y_right = [], []
		
		for y in array:
			a = get_x_from_y[y]
			if a < median:
				y_left.append(y)
			elif a > median:
				y_right.append(y)
				
		v.left = self.build_help(get_y_from_x, get_x_from_y, x_sorted_array[:t], y_left)
		v.right = self.build_help(get_y_from_x, get_x_from_y, x_sorted_array[t+1:], y_right)
		return v
		
	def build(self,array):
		# Build the XNode tree and dictionaries from a list of points
		x_array = [i[0] for i in array]
		get_y_from_x = {}
		for i in array:
			get_y_from_x[i[0]] = i[1]
			
		YArray = [i[1] for i in array]
		get_x_from_y = {}
		for i in array:
			get_x_from_y[i[1]] = i[0]
        
		x_array.sort()
		YArray.sort()
		
		self.get_y_from_x = get_y_from_x
		self.get_x_from_y = get_x_from_y
		self.root = self.build_help(get_y_from_x, get_x_from_y, x_array, YArray)
		
		
	def inorder_traversal(self,p):
		# Perform an inorder traversal of the XNode tree
		if p is not None:
			self.inorder_traversal(p.left)
			print(p.value, end = " ")
			p.YTree.inorder_traversal(p.YTree.root)
			print()
			self.inorder_traversal(p.right)
		return
		
	def search_help(self,x_range,y_range):
		# Helper function to perform a search for nearby points
		separator = self.root
		
		if separator is None:
			return []
		
		while True:
			#if separator.left is None and separator.right is None:
			#	break
			if separator.value < x_range[0]:
				if separator.right is not None:
					separator = separator.right 
				else:
					separator = None
					break
			elif separator.value > x_range[1]:
				if separator.left is not None:
					separator = separator.left
				else:
					separator = None
					break
			else:
				break
				
		if separator is None:
			return []
		elif separator.left == None and separator.right == None:
			# Leaf node case, check if it's within y_range
			t = self.get_y_from_x[separator.value]
			if t >= y_range[0] and t <= y_range[1]:
				return [t]
		else:
			# Internal node case, traverse left and right
			v = separator.left
			left = []
			while True:
				if v is None:
					break
				elif v.value >= x_range[0]:
					t = self.get_y_from_x[v.value]
					if t >= y_range[0] and t <= y_range[1]:
						left.append(t)
					if v.right is not None:
						left += v.right.YTree.y_search_in_range(y_range)
					v = v.left
				else:
					v = v.right
			
			v = separator.right
			right = []
			while True:
				if v is None:
					break
				elif v.value <= x_range[1]:
					t = self.get_y_from_x[v.value]
					if t >= y_range[0] and t <= y_range[1]:
						right.append(t)
					if v.left is not None:
						right += v.left.YTree.y_search_in_range(y_range)
					v = v.right
				else:
					v = v.left

			# Check the separator node itself		
			t = self.get_y_from_x[separator.value]
			if t >= y_range[0] and t <= y_range[1]:
				return [t] + left + right
			return left + right 
				
	def searchNearby(self,q,d):
		#Perform a search for nearby points given a query point and distance
		x_range = [q[0]-d,q[0]+d]
		y_range = [q[1]-d, q[1]+d]
		
		y_list = self.search_help(x_range, y_range)
		
		result = []
		if y_list is None:
			return []
		else:
			for y in y_list:
				result.append((self.get_x_from_y[y], y))
		return result
		

test = PointDatabase([(1,6), (2,4), (3,7), (4,9), (5,1), (6,3), (7,8), (8,10),
(9,2), (10,5)])
print(test.searchNearby((10,2),1.5))