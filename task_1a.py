
'''
*****************************************************************************************
*
*        		===============================================
*           		Rapid Rescuer (RR) Theme (eYRC 2019-20)
*        		===============================================
*
*  This script is to implement Task 1A of Rapid Rescuer (RR) Theme (eYRC 2019-20).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
'''


# Team ID:			[ 4568]
# Author List:		[Vibhor Kolte, Prathamesh Shende]
# Filename:			task_1a.py
# Functions:		readImage, solveMaze
# 					[ class QUEUE, get_neighbours, ]
# Global variables:	CELL_SIZE
# 					[ rear, front, queue, N ]


# Import necessary modules
# Do not import any other modules
import cv2
import numpy as np
import os

########################################
#  Used for class QUEUE
########################################
rear=-1
front=-1
queue=[[] for i in range(10000)]
N=len(queue)
#######################################


# To enhance the maze image
import image_enhancer


# Maze images in task_1a_images folder have cell size of 20 pixels
CELL_SIZE = 20


def readImage(img_file_path):
    """
	Purpose:
	---
	the function takes file path of original image as argument and returns it's binary form

	Input Arguments:
	---
	`img_file_path` :		[ str ]
		file path of image

	Returns:
	---
	`original_binary_img` :	[ numpy array ]
		binary form of the original image at img_file_path

	Example call:
	---
	original_binary_img = readImage(img_file_path)

    """
    binary_img = None
    #############  Add your Code here   ################
    np.set_printoptions(threshold=np.inf)
    img= cv2.imread(img_file_path,0)
    ret, binary_img = cv2.threshold(img, 10, 255, cv2.THRESH_BINARY)
    #####################################################
    return binary_img


def solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width):
    """
	Purpose:
	---
	the function takes binary form of original image, start and end point coordinates and solves the maze
	to return the list of coordinates of shortest path from initial_point to final_point

	Input Arguments:
	---
	`original_binary_img` :	[ numpy array ]
		binary form of the original image at img_file_path
	`initial_point` :		[ tuple ]
		start point coordinates
	`final_point` :			[ tuple ]
		end point coordinates
	`no_cells_height` :		[ int ]
		number of cells in height of maze image
	`no_cells_width` :		[ int ]
		number of cells in width of maze image

	Returns:
	---
	`shortestPath` :		[ list ]
		list of coordinates of shortest path from initial_point to final_point

	Example call:
	---
	shortestPath = solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

	"""
    
    shortestPath = []
    #############	Add your Code here	###############
    
    #####################################################
    #           BREADTH-FIRST-SEARCH
    #####################################################
    
    R,C=no_cells_height,no_cells_width
    sr,sc=0,0
    er,ec=no_cells_height-1,no_cells_width-1
    
    # Use class QUEUE 
    rq=QUEUE()
    cq=QUEUE()
    
    visited=[]
    prev=[]

    for i in range (0,R):
        visited.append([])
        prev.append([])
    for i in range(0,C):
        for j in range(0,C):
            visited[i].append([j])
            visited[i][j]=False
            
            prev[i].append([j])
            prev[i][j]=None
            
    visited[sr][sc]=True
    #--------------------------------------------------
    ## Performing BFS graph traversal
    rq.enqueue(sr)
    cq.enqueue(sc)
    while rq.empty() == False:
        x=rq.dequeue() 
        y=cq.dequeue()
        
        #Getting all the neighbours of node
        neighbours=get_Neighbours(original_binary_img,x,y,no_cells_height,no_cells_width)          #  Getting valid neighbours               
        for next_Node in neighbours:
            nextR=next_Node[0]
            nextC=next_Node[1]
            
            if visited[nextR][nextC]==False:
                rq.enqueue(nextR)
                cq.enqueue(nextC)
                
                visited[nextR][nextC]=True
                prev[nextR][nextC]=(x,y)
    #---------------------------------------------------
    # Reconstructing Path
    path=[]
    currentR=er
    currentC=ec
    
    path.append((currentR,currentC))
    
    while prev[currentR][currentC] != None:
        path.append(prev[currentR][currentC])
        node=prev[currentR][currentC]
        currentR=node[0]
        currentC=node[1]
        
    path.reverse()
    if path[0]==(sr,sc):
        shortestPath=path.copy()
    else:
        print("Path not found")
    ############################################
        
    return shortestPath

	
	


#############	You can add other helper functions here		#############
    
###############################################################################
#               IMPLEMENTING QUEUE
###############################################################################

class QUEUE:
        #-------------------------------
        def __init__(self):
            pass
        def enqueue(self,x): # Enqueueing element in queue
            global rear
            global front
            if  (front==rear+1 or rear==N-1) :
                print('Queue is full')
                return
            elif (front==rear==-1):
                front=rear=0
                queue[rear]=x
            elif (rear==N-1):
                rear=0
                queue[rear]=x
            else:
                rear=rear+1
                queue[rear]=x
        #---------------------------------        
        def dequeue(self):  # Dequeueing element from queue
            global rear
            global front
            if (front==rear==-1):
                return
            elif front==rear:
                temp = queue[front]
                front=rear=-1
                return temp
            elif front==N-1:
                temp = queue[front]
                front=0
                return temp
            else:
                temp = queue[front]
                front= front+1
                return temp
        #-----------------------------------    
        def empty(self): # to check weather queue is empty or not
            if (front==rear==-1):
                return True
            else:
                return False
###################################################################
#                   Explore Neighbours
###################################################################
def get_Neighbours(original_binary_img,x,y,no_cells_height,no_cells_width):
    # ..........Getting centre pixel of each cell..........
    NSEW=[]
    height,width=original_binary_img.shape
    
    for i in range (0,(no_cells_height)):
        NSEW.append([])
    for i in range(0,(no_cells_height)):
        for j in range(0,(no_cells_width)):
            NSEW[i].append([j])
            NSEW[i][j]=0
    #..........Traverse through each coordinate............
    k=0 # Iteration Count
    for i in range(10,height,CELL_SIZE):
        l=0
        for j in range(10,width,CELL_SIZE):
            if original_binary_img[i+9,j]==255:
                S=1                 # 0 is for black & 1 is for white
            else:
                S=0
            if original_binary_img[i-9,j]==255:
                N=1
            else :
                N=0
            if original_binary_img[i,j+9]==255:
                E=1
            else :
                E=0
            if original_binary_img[i+1,j-9]==255:
                W=1
            else :
                W=0
            NSEW[k][l]= [N,S,E,W]    # Direction vectors of cells    
            l=l+1
        k=k+1
        
        
    valid_neighbours=[]
    
    valid_neighbours.clear()
    if NSEW[x][y][0]==1 and x-1>=0:
        valid_neighbours.append((x-1,y))
    if NSEW[x][y][1]==1 and x+1<=(no_cells_height-1):
        valid_neighbours.append((x+1,y))
    if NSEW[x][y][2]==1 and y+1<=(no_cells_height-1):
        valid_neighbours.append((x,y+1))
    if NSEW[x][y][3]==1 and y-1>=0:
        valid_neighbours.append((x,y-1))
        
    return valid_neighbours

#########################################################################


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:	main
# Inputs:			None
# Outputs: 			None
# Purpose: 			the function first takes 'maze00.jpg' as input and solves the maze by calling readImage
# 					and solveMaze functions, it then asks the user whether to repeat the same on all maze images
# 					present in 'task_1a_images' folder or not

if __name__ == '__main__':

	curr_dir_path = os.getcwd()
	img_dir_path = curr_dir_path + '/../task_1a_images/'				# path to directory of 'task_1a_images'
	
	file_num = 0
	img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'		# path to 'maze00.jpg' image file

	print('\n============================================')

	print('\nFor maze0' + str(file_num) + '.jpg')

	try:
		
		original_binary_img = readImage(img_file_path)
		height, width = original_binary_img.shape

	except AttributeError as attr_error:
		
		print('\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
		exit()
	
	no_cells_height = int(height/CELL_SIZE)							# number of cells in height of maze image
	no_cells_width = int(width/CELL_SIZE)							# number of cells in width of maze image
	initial_point = (0, 0)											# start point coordinates of maze
	final_point = ((no_cells_height-1),(no_cells_width-1))			# end point coordinates of maze

	try:

		shortestPath = solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

		if len(shortestPath) > 2:

			img = image_enhancer.highlightPath(original_binary_img, initial_point, final_point, shortestPath)
			
		else:

			print('\n[ERROR] shortestPath returned by solveMaze function is not complete !\n')
			exit()
	
	except TypeError as type_err:
		
		print('\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
		exit()

	print('\nShortest Path = %s \n\nLength of Path = %d' % (shortestPath, len(shortestPath)))
	
	print('\n============================================')
	
	cv2.imshow('canvas0' + str(file_num), img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	choice = input('\nWant to run your script on all maze images ? ==>> "y" or "n": ')

	if choice == 'y':

		file_count = len(os.listdir(img_dir_path))

		for file_num in range(file_count):

			img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

			print('\n============================================')

			print('\nFor maze0' + str(file_num) + '.jpg')

			try:
				
				original_binary_img = readImage(img_file_path)
				height, width = original_binary_img.shape

			except AttributeError as attr_error:
				
				print('\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
				exit()
			
			no_cells_height = int(height/CELL_SIZE)							# number of cells in height of maze image
			no_cells_width = int(width/CELL_SIZE)							# number of cells in width of maze image
			initial_point = (0, 0)											# start point coordinates of maze
			final_point = ((no_cells_height-1),(no_cells_width-1))			# end point coordinates of maze

			try:

				shortestPath = solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

				if len(shortestPath) > 2:

					img = image_enhancer.highlightPath(original_binary_img, initial_point, final_point, shortestPath)
					
				else:

					print('\n[ERROR] shortestPath returned by solveMaze function is not complete !\n')
					exit()
			
			except TypeError as type_err:
				
				print('\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
				exit()

			print('\nShortest Path = %s \n\nLength of Path = %d' % (shortestPath, len(shortestPath)))
			
			print('\n============================================')

			cv2.imshow('canvas0' + str(file_num), img)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
	
	else:

		print('')


