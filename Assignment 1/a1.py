def findPositionandDistance(program):
    #this function finds the final position(x,y,z) and distance d travelled by a drone after executing program
    #Input:str-sequence of instructions
    #Output:tuple-(x,y,z,d) , where type of x,y,z and d is int
    coordinate = [0, 0, 0, 0] # gives x,y,z,d values
    mapValue = {'X': 0, 'Y': 1, 'Z': 2} # index in coordinate

    stack = []
    curr_num = 1
    i = 0
    while i < len(program): #if length of program is n the time complexity==O(n)
        if program[i] in ['-', '+']: # If coordinates,i.e  ±X, ±Y, ±Z; update coordinate values
            if program[i] == '-':
                coordinate[mapValue[program[i+1]]] -= curr_num

            else: #program[i] == '+':
                coordinate[mapValue[program[i+1]]] += curr_num

            coordinate[3] += curr_num #updates distance (d)
            i += 2

        elif program[i].isdigit(): # If digit encountered, find whether we have a sequence of digits or not and get value of integer
            j = i
            while program[j].isdigit():
                j += 1
            curr_num =  int(program[i:j]) #the integer being multiplied
            i = j

        elif program[i] == '(': # If opening bracket, push existing data to stack
            stack.append((curr_num, coordinate))
            curr_num = 1
            coordinate = [0, 0, 0, 0]
            i += 1

        else: # program[i] == ')'
            # If closing bracket, pop existing data from stack and merge with current.
            old_num, old_coordinate = stack.pop()
            coordinate_multiplied = [old_num * x for x in coordinate]
            coordinate = [m + n for m,n in zip(old_coordinate, coordinate_multiplied)]
            i += 1

    return coordinate
