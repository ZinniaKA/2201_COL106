class heapq:
    #A min-oriented priority queue implemented with a heap
    def __init__(self,list):
        #takes alist which will be converted to priority queue
        self.list=list 

    def __len__(self):
        #Return the number of items in the priority queue
        return len(self.list)
    
    def is_empty(self):
        #Return True if the priority queue is empty
        return len(self.list)==0

    def parent(self,j): #returns the index of parent of the j_th element in heap
        return (j-1)//2
    
    def left(self,j): #returns the index of left child of j_th element in the heap
        return 2*j+1
    
    def right(self,j): #returns the index of right child of j_th element in the heap
        return 2*j+2
    
    def has_left(self,j): #returns True if j_th element has a left child
        return self.left(j)<len(self.list)
    
    def has_right(self,j): #returns True if j_th element has a right child
        return self.right(j)<len(self.list)
    
    def swap(self,i,j): #Swap the elements at indices i and j
        self.list[i],self.list[j] = self.list[j],self.list[i]

    def upheap(self,j): #pushes an element to correct position up the heap starting from bottom
        parent = self.parent(j)
        if j > 0 and self.list[j] < self.list[parent]: #if j_th element is not the root and j_th element is less than its parent it needs to be pushed up
            self.swap(j, parent) #swap the j_th element with its parent
            self.upheap(parent) #recurse on the parent

    def downheap(self, j): #pushes an element to correct position down the heap starting from top
        if self. has_left(j):
            left = self.left(j)
            small_child = left  #assumes left child is smaller
            if self.has_right(j):
                right = self. right(j)
                if self.list[right] < self.list[left]: #if right child is smaller than left child
                    small_child = right
            if self.list[small_child] < self.list[j]: #if j_th element is greater than its smaller child it needs to be pushed down
                self. swap(j, small_child)
                self. downheap(small_child) #recurse on the child with the smaller time

    def enqueue(self,key):
        #Add an element to the priority queue
        self.list.append(key)
        self.upheap(len(self.list)-1) #upheap newly added element to correct position

    def dequeue(self):
        #Remove and return the smallest element from the priority queue
        if self.is_empty():
            print('Priority queue is empty')
        self.swap(0,len(self.list)-1) #swap the root with the last element
        item=self.list.pop()
        self.downheap(0) #downheap the root to correct position
        return item
    
    def min(self):
        #Return but do not remove the element with minimum key
        if self.is_empty():
            print('Priority queue is empty')
        return self.list[0]
    
    def pop(self,i):
        #removing element at i th index
        self.list.pop(i)    

def listCollisions(M,x,v,m,T):
    '''
        this function returns a list of collisions in chronological order 
        It returns the first m collisions  or all collisions till time reaches T (whichever earlier)
    '''
    #INPUT:
    # M: list of positive floats - where M[i] is the mass of the i’th object,
    # x: sorted list of floats - where x[i] is the initial position of the i’th object,
    # v: list of floats - v[i] is the initial velocity of the i’th object,
    # m: a non-negative integer- limit on the no. of collisions that have to be returned
    # T: a non-negative float - the time limit till which collisions have to be calculated

    if len(M)==0 or len(M)==1 : #No collisions occur -- no particles or a single particle then no collision happens
        return []

    if m==0 or T ==0 : #nothing to be returned
        return []

    collision=[] #list of collisions to be returned
    time_initial = [] #list of initial time for collision between i and i+1 th particles
    t = 0 #current time
    count = 0 # store no. of collisions till time t
    last_collision = [0]*len(M)  #store time of last collision for each index
    future_collision = [-1]*len(M) #store time of next collision for each index
    T_array =heapq(time_initial) #min-heap to store time of collision between i and i+1 th particles
 
    for i in range(len(v)-1): #loop to make list of initial time for possible collision between i and i+1 th particle particles
    
        if v[i]-v[i+1]>0: #only in this case collison will be possible
            time_initial.append([(x[i+1]-x[i])/(v[i]-v[i+1]),i]) #storing time of collsion and the index as a list
            future_collision[i]=(x[i+1]-x[i])/(v[i]-v[i+1]) #updating the upcoming collision list
    
    for j in range(len(time_initial)-1,-1,-1):
            T_array.downheap(j) #convert time_initial to min-heap

        
    while t < T and count<m: #m is the limit on the no. of collisions to be returned and T is the time limit till which collisions have to be calculated
            
            if len(T_array)==0: #no more collisions possible
                return collision
            
            coll = T_array.dequeue() #remove the root of min-heap
            k,t = coll[1],coll[0] #k is the index of i th particle and t is the time of collision

            # print(f"\nCollision at time: {t}")
            # print(f"Collision index: {k}")
            # print(f"Last collision times: {last_collision}")
            # print(f"Future collision times: {future_collision}")
            # print(f"Current positions: {x}")
            # print(f"Current velocities: {v}")

            if t==future_collision[k] and t<=T : #checks if the collision is still valid and time of collision is less than T
                p = x[k] +v[k]*(t-last_collision[k])        #position of k th  and k+i th particle during collision
                v_last=v[k] #velocity of k th particle before collision

                v[k]= ((M[k]-M[k+1])*v[k])/(M[k]+M[k+1]) + (2*M[k+1]*v[k+1])/(M[k]+M[k+1]) #velocity of k th particle after collision
                v[k+1]= ((M[k+1]-M[k])*v[k+1])/(M[k]+M[k+1]) +(2*M[k]*v_last)/(M[k]+M[k+1]) #velocity of k+i th particle after collision
                
                x[k]=p #update position of k th particle
                x[k+1]=p #update position of k+i th particle

                last_collision[k]=t #update time of last collision for k th particle
                last_collision[k+1]=t #update time of last collision for k+i th particle
                
                collision.append((round(t,4),k,round(p,4))) 
                count +=1 #update no. of collisions till time t
                
                if k>=1: 
                    if v[k-1] > v[k]: #check if collision is possible between k-1 th and k th particle
                        T_array.enqueue([t+(x[k]-x[k-1]-v[k-1]*(t-last_collision[k-1]))/(v[k-1]-v[k]),k-1]) #add time of collision and index of k-1 th particle to min-heap
                        future_collision[k-1]=t+(x[k]-x[k-1]-v[k-1]*(t-last_collision[k-1]))/(v[k-1]-v[k]) #update time of next collision for k-1 th particle
                
                if k+2<len(v): #check if collision is possible between k+1 th and k+2 th particle
                    if v[k+1] > v[k+2]:
                        T_array.enqueue([t+(x[k+1]-x[k+2]-v[k+2]*(t-last_collision[k+2]))/(v[k+2]-v[k+1]),k+1]) #add time of collision and index of k+1 th particle to min-heap
                        future_collision[k+1]=t+(x[k+1]-x[k+2]-v[k+2]*(t-last_collision[k+2]))/(v[k+2]-v[k+1])

    return collision
