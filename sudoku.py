import tkinter
import tkinter.filedialog
import tkinter.messagebox

import pygame
import pygame.color

# initialise the pygame font
pygame.font.init()
 
# Total window
screen = pygame.display.set_mode((500, 600))

baseSet = set()
baseSet.update([ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9" ]) 

# Title and Icon
pygame.display.set_caption("Sudoku")
img = pygame.image.load('icon.png')
pygame.display.set_icon(img)

red = pygame.color.Color( 255, 0, 0)
blue = pygame.color.Color( 0, 255, 0)
green = pygame.color.Color( 0, 0, 255 )
black = pygame.color.Color( 255, 255, 255 )

hint = ""
x = 0
y = 0
dif = 500 / 9
val = 0
drawcount = 0
# Default Sudoku Board.
ogrid = []
for i in range(0,9):
    ogrid.append( [1,2,3,4,5,6,7,8,9] )

grid =[
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]
for row in range(9):
        for column in range(9):
            ogrid[row][column] = grid[row][column]

# Load test fonts for future use
font1 = pygame.font.SysFont("comicsans", 40)
font2 = pygame.font.SysFont("comicsans", 20)

def writeGrid( filename, grid):
    with open( filename, "w") as f:
        f.write("grid = [\n")
        r = 0
        for l1 in grid:
            f.write( "        [" )
            i = 0
            for l2 in l1:
                i += 1
                f.write( str(l2) )
                if i < 9:
                    f.write(", ")
            f.write(']')
            r += 1
            if r < 9 :
                f.write(',')
            f.write('\n')
        f.write("    ]\n")
    print(f"cat {filename}")

writeGrid( "/dev/stdout", grid)
def get_cord(pos):
    global x, y, hint
    x1 = int(pos[0]//dif)
    y1 = int(pos[1]//dif)
    
    if x1 <= 8 and y1 <= 8:  # Range Check
        x = x1
        y = y1
def get_guess():
    if ( grid[x][y] != 0 ):
        return ""
    aset = set()
    for i in range( 0, 9 ):
        aset.add( str( int(grid[x][i]) ))
        aset.add( str( int(grid[i][y]) ))
    for r in range(int(x /3 )*3, int(x / 3 )*3+3 ):
        for c in range(int(y / 3 )*3, int(y / 3 )*3+3 ):
            aset.add( str( int(grid[r][c]) ))
    return sorted(baseSet.difference( aset ))

# Highlight the cell selected
def draw_box():
    for i in range(2):
        pygame.draw.line(screen, red, (x * dif-3, (y + i)*dif), (x * dif + dif + 3, (y + i)*dif), 7)
        pygame.draw.line(screen, red, ( (x + i)* dif, y * dif ), ((x + i) * dif, y * dif + dif), 7)  
# Function to draw required lines for making Sudoku grid        
#  AND draw the numbers in the grid
def draw():
    global drawcount
    drawcount = drawcount + 1

    print(f"Draw {drawcount}")
    # Draw the lines and fill the cells

    for i in range (9):
        for j in range (9):
            if grid[i][j]!= 0:

                # Fill blue color in already numbered grid

                # Fill grid with default numbers specified
                if grid[i][j] == ogrid[i][j]:
                    pygame.draw.rect(screen, (0, 153, 153), (i * dif, j * dif, dif + 1, dif + 1))
                    text1 = font1.render(str(grid[i][j]), 1, (0, 0, 0))
                else:
                    pygame.draw.rect(screen, (67, 152, 122), (i * dif, j * dif, dif + 1, dif + 1))
                    text1 = font1.render(str(grid[i][j]), 1, green)
                screen.blit(text1, (i * dif + 15 + 7, j * dif + 15))
    # Draw lines horizontally and verticallyto form grid          
    for i in range(10):
        if i % 3 == 0 :
            thick = 7
        else:
            thick = 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * dif), (500, i * dif), thick)
        pygame.draw.line(screen, (0, 0, 0), (i * dif, 0), (i * dif, 500), thick)     
    text3 = font2.render(hint, 1, (0, 0, 0))
    screen.blit(text3, (20, 560))
 
# Fill value entered in cell     
def draw_val(val, c):
    text1 = font1.render(str(val), 1, (50, 50, 50))
    screen.blit(text1, (x * dif + 15, y * dif + 15))   
 
# Raise error when wrong value entered
def raise_error1():
    text1 = font1.render("WRONG !!!", 1, (0, 0, 0))
    screen.blit(text1, (20, 570)) 
def raise_error2():
    text1 = font1.render("Wrong !!! Not a valid Key", 1, (0, 0, 0))
    screen.blit(text1, (20, 570)) 
 
# Check if the value entered in board is valid
def valid(m, i, j, val):
    for it in range(9):
        if m[i][it]== val:
            return False
        if m[it][j]== val:
            return False
    it = i//3
    jt = j//3
    for i in range(it * 3, it * 3 + 3):
        for j in range (jt * 3, jt * 3 + 3):
            if m[i][j]== val:
                return False
    return True
 
# Solves the sudoku board using Backtracking Algorithm
def solve(grid, i, j):
     
    while grid[i][j]!= 0:
        if i<8:
            i+= 1
        elif i == 8 and j<8:
            i = 0
            j+= 1
        elif i == 8 and j == 8:
            return True
    pygame.event.pump()   
    for it in range(1, 10):
        if valid(grid, i, j, it)== True:
            grid[i][j]= it
            global x, y
            x = i
            y = j
            # white color background
            screen.fill(black)
            draw()
            draw_box()
            pygame.display.update()
            pygame.time.delay(20)
            if solve(grid, i, j)== 1:
                return True
            else:
                grid[i][j]= 0
            # white color background
            screen.fill(black)
         
            draw()
            draw_box()
            pygame.display.update()
            pygame.time.delay(50)   
    return False 
 
# Display instruction for the game
def instruction():
    text1 = font2.render("PRESS R TO RESET TO DEFAULT / E TO EMPTY", 1, (0, 0, 0))
    text2 = font2.render("ENTER VALUES AND PRESS ENTER TO VISUALIZE", 1, (0, 0, 0))
    screen.blit(text1, (20, 520))       
    screen.blit(text2, (20, 540))

# Display options when solved
def result():
    text1 = font1.render("FINISHED PRESS R or D", 1, (0, 0, 0))
    screen.blit(text1, (20, 570))   
run = True
flag1 = 0
flag2 = 0
rs = 0
error = 0
clock = pygame.time.Clock()
# The loop thats keep the window running
while run:
     
    # White color background
    screen.fill(black)
    # Loop through the events stored in event.get()
    for event in pygame.event.get():
        # Quit the game window
        if event.type == pygame.QUIT:
            run = False 
        # Get the mouse position to insert number   
        if event.type == pygame.MOUSEBUTTONDOWN:
            flag1 = 1
            pos = pygame.mouse.get_pos()
            get_cord(pos)
        # Get the number to be inserted if key pressed   
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if x > 0:
                    x-= 1
                    flag1 = 1
            if event.key == pygame.K_RIGHT:
                if x < 8:
                    x+= 1
                    flag1 = 1
            if event.key == pygame.K_UP:
                if y > 0:
                    y-= 1
                    flag1 = 1
            if event.key == pygame.K_DOWN:
                if y < 8:
                    y+= 1
                    flag1 = 1   
            if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                val = 1
            if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                val = 2   
            if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                val = 3
            if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                val = 4
            if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                val = 5
            if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                val = 6
            if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                val = 7
            if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                val = 8
            if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                val = 9 
            if event.key == pygame.K_RETURN  or event.key == pygame.K_KP_ENTER:
                flag2 = 1  
            if event.key == pygame.K_0 or event.key == pygame.K_KP0 or event.key == pygame.K_DELETE:
                val = 99
                flag1 = 1
            if event.key == pygame.K_o:
                file_path = tkinter.filedialog.asksaveasfilename( filetypes= [("CSV Game Files", "*.csv")] )
                if (not file_path is None ) or ( len(file_path) == 0):
                    tkinter.messagebox.showinfo("Saving to", file_path)
                    writeGrid( file_path, ogrid)
            if event.key == pygame.K_w:
                writeGrid( "/dev/stdout", grid)
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                run = False 
            # If R pressed clear the sudoku board
            if event.key == pygame.K_e:
                rs = 0
                error = 0
                flag2 = 0
                grid =[
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
                ]
            # If R is pressed reset the board to default
            if event.key == pygame.K_r:
                rs = 0
                error = 0
                flag2 = 0
                for row in range(9):
                        for column in range(9):
                            grid[row][column] = ogrid[row][column]
    if flag2 == 1:
        if solve(grid, 0, 0)== False:
            error = 1
        else:
            rs = 1
        flag2 = 0   
    if val != 0:           
        draw_val(val, "red")
        if val == 99:
            grid[int(x)][int(y)]= 0
            val = 0
        if valid(grid, int(x), int(y), val)== True:
            grid[int(x)][int(y)]= val
            #flag1 = 0
        else:
            grid[int(x)][int(y)]= 0
            raise_error2()  
        val = 0   
   
    if error == 1:
        raise_error1() 
    if rs == 1:
        result()       
    draw() 
    if flag1 == 1:
        draw_box()      
    hint = str(get_guess())
    instruction()   
 
    # Update window
    pygame.display.update() 
    clock.tick(30) # 30 FPS is fast enough for this
 
# Quit pygame window   
pygame.quit()
