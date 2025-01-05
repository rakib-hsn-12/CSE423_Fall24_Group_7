#### Group_7 ###
#Sumaiya Tasnim (21201518)
#Inkiad Bin Ershad (21201516)
#Md Rakib Hossain Ontu (22101879)


import sys
import subprocess
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Global variables
ball_x = 300
ball_y = 50
radius = 7
ball_dx = 3
ball_dy = 2

board_x = 350
board_y = 10
board_width = 100
board_height = 10

window_width = 800
window_height = 700

box_at_x = 10
box_at_y= 7
box_width = (window_width // box_at_x)
box_height = 20

blocks = [[1 for _ in range(box_at_x)] for _ in range(box_at_y)]
board_color = (0.0, 1.0, 0.0)

game_over = False
is_paused = False
score = 0
restart_button = (window_width // 2 - 100, window_height // 2 - 50, 80, 30)
quit_button = (window_width // 2 + 20, window_height // 2 - 50, 80, 30)
def circle(x, y, r):
    segments = 100
    glBegin(GL_POLYGON)
    for a in range(segments + 1):
        theta = 2.0 * math.pi * float(a) / float(segments)
        dx = r * float(math.cos(theta))
        dy = r * float(math.sin(theta))
        glVertex2f(x + dx, y + dy)
    glEnd()

def rectangle(x, y, w, h, c):
    glColor3f(*c)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h)
    glVertex2f(x, y + h)
    glEnd()

def draw_boxes():
    for i in range(box_at_y):
        for j in range(box_at_x):
            if blocks[i][j]:
                if j == 4 or j == 6 or j == 8:
                    rectangle(j * box_width, window_height - (i + 1) * box_height, box_width, box_height, (0.0, 0.3, 1.7))
                elif j == 2 or j == 5 or j == 0:
                    rectangle(j * box_width, window_height - (i + 1) * box_height,box_width, box_height, (0.5, 0.3, 1.7))
                else:
                    rectangle(j * box_width, window_height - (i + 1) * box_height, box_width, box_height, (0.0, 1.0, 1.0))

def text(x, y, t):
    glRasterPos2f(x, y)
    for char in t:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def score_board():
    glColor3f(0.0, 0.0, 0.0)
    text(window_width - 150, window_height - 30, f"Score Board: {score}")
    
def draw_buttons():
    # Draw Restart button only if game is over
    if game_over:
        rectangle(*restart_button, (0.0, 1.0, 0.0))
        glColor3f(1.0, 1.0, 1.0)
        text(restart_button[0] + 10, restart_button[1] + 10, "Restart")
        
        rectangle(*quit_button, (1.0, 0.0, 0.0))
        glColor3f(1.0, 1.0, 1.0)
        text(quit_button[0] + 25, quit_button[1] + 10, "Quit")

    
    
def draw():
    global game_over

    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(1.0, 1.0, 1.0)
    circle(ball_x, ball_y, radius)

    rectangle(board_x, board_y, board_width, board_height, board_color)

    draw_boxes()

    score_board()

    draw_buttons()
    
    if game_over:
        glColor3f(1.0, 0.0, 0.0)
        text(window_width // 2 - 50, window_height // 2, "Game Over")
        glutSwapBuffers()
        return
    glutSwapBuffers()
    
    
def restart_game():
    global ball_x, ball_y, ball_dx, ball_dy, blocks, game_over, score
    ball_x, ball_y = 300, 50
    ball_dx, ball_dy = 4, 3
    blocks = [[1 for _ in range(box_at_x)] for _ in range(box_at_y)]
    game_over = False
    score = 0



def update(value):
    global ball_x, ball_y, ball_dx, ball_dy, game_over, score, board_color

    if game_over:
        return

    if not is_paused:
        if score > 20 and score <= 40:
            ball_x += ball_dx + ball_dx // 4
            ball_y += ball_dy + ball_dy // 4
        elif score > 40 and score < 50:
            ball_x += ball_dx + ball_dx // 2
            ball_y += ball_dy + ball_dy // 2
        elif score >= 50:
            glColor3f(0.0, 1.0, 1.0)
            text(window_width // 2 - 50, window_height // 2, "Proceed to Level 2")
            # Exit the current GLUT main loop
            glutLeaveMainLoop()
            subprocess.run(['python', 'CSE423_Fall24_Group_7/Leve_2.py'])

        else:
            ball_x += ball_dx
            ball_y += ball_dy

        if ball_x + radius > window_width or ball_x - radius < 0:
            ball_dx *= -1
        if ball_y + radius > window_height:
            ball_dy *= -1

        if board_x <= ball_x <= board_x + board_width and ball_y - radius <= board_y + board_height:
            ball_dy *= -1

        hit_block_y = (window_height - ball_y) // box_height
        hit_block_x = ball_x // box_width
        if 0 <= hit_block_y < box_at_y and 0 <= hit_block_x < box_at_x and blocks[hit_block_y][hit_block_x]:
            ball_dy *= -1
            blocks[hit_block_y][hit_block_x] = 0
            score += 10

        if ball_y - radius < 0:
            game_over = True

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def keyboard(key, x, y):
    global board_x, is_paused, game_over

    if key == b'q':
        game_over = True
        sys.exit(0)
    elif key == b'a' and board_x > 0:
        board_x -= 20
    elif key == b'd' and board_x + board_width < window_width:
        board_x += 20
    elif key == b'p':
        is_paused = not is_paused
        
def mouse_click(button, state, x, y):
    global game_over, ball_x, ball_y, ball_dx, ball_dy, board_x, board_color, blocks, level, score, is_paused

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        
        game_y = window_height - y 
       
        restart_x_start = window_width // 2 - 100
        restart_x_end = window_width // 2 - 20
        restart_y_start = window_height // 2 - 50
        restart_y_end = window_height // 2 - 20

        if restart_x_start <= x <= restart_x_end and restart_y_start <= game_y <= restart_y_end:
            restart_game()
        quit_x_start = window_width // 2 + 20
        quit_x_end = window_width // 2 + 100
        quit_y_start = window_height // 2 - 50
        quit_y_end = window_height // 2 - 20

        if quit_x_start <= x <= quit_x_end and quit_y_start <= game_y <= quit_y_end:
            sys.exit(0)
            
def restart_game():
    global ball_x, ball_y, ball_dx, ball_dy, board_x, board_y, board_color, blocks, level, score, game_over, is_paused
    # Reset game variables
    ball_x = 300
    ball_y = 50
    ball_dx = 3
    ball_dy = 2
    board_x = 350
    board_y = 10
    board_color = (0.0, 1.0, 0.0)
    blocks = [[1 for _ in range(box_at_x)] for _ in range(box_at_y)]
    level = 1
    score = 0
    game_over = False
    is_paused = False

def init():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Box_Breaker_1")
    glutDisplayFunc(draw)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(16, update, 0)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    gluOrtho2D(0, window_width, 0, window_height)
    glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_CONTINUE_EXECUTION) 

if __name__ == "__main__":
    init()
    glutMainLoop()
