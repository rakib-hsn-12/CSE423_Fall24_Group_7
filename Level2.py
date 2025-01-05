import sys
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Global variables
ball_x = 300
ball_y = 50
radius = 7
ball_dx = 4
ball_dy = 3

board_x = 350
board_y = 10
board_width = 100
board_height = 10

window_width = 800
window_height = 700

box_at_x = 10
box_at_y = 7
box_width = (window_width // box_at_x)
box_height = 20

blocks = [[1 for _ in range(box_at_x)] for _ in range(box_at_y)]
block_dx = 2
board_color = (0.0, 1.0, 0.0)

game_over = False
is_paused = False
score = 0
level = 1
fireball_active = False
fireball_x, fireball_y = None, None
fireball_radius = 5
fireball_caught = False
ball_is_fireball = False

# Restart and quit button positions
restart_button = (window_width // 2 - 100, window_height // 2 - 50, 80, 30)
quit_button = (window_width // 2 + 20, window_height // 2 - 50, 80, 30)

def circle(x, y, r, color=(1.0, 1.0, 1.0)):
    glColor3f(*color)
    segments = 100
    glBegin(GL_POLYGON)
    for a in range(segments + 1):
        theta = 2.0 * math.pi * float(a) / float(segments)
        dx = r * float(math.cos(theta))
        dy = r * float(math.sin(theta))
        glVertex2f(x + dx, y + dy)
    glEnd()

def rectangle(x, y, w, h, color):
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h)
    glVertex2f(x, y + h)
    glEnd()

def draw_boxes():
    colors = [(1.0, 0.0, 0.0), (0.6, 0.0, 0.6), (1.0, 0.5, 0.0)]
    for i in range(box_at_y):
        for j in range(box_at_x):
            if blocks[i][j]:
                rectangle(j * box_width, window_height - (i + 1) * box_height, box_width, box_height, colors[(i + j) % len(colors)])

def text(x, y, t):
    glRasterPos2f(x, y)
    for char in t:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def score_board():
    glColor3f(0.0, 0.0, 0.0)
    text(window_width - 150, window_height - 30, f"Score: {score}")

def draw_fireball():
    if fireball_active:
        circle(fireball_x, fireball_y, fireball_radius, (1.0, 0.5, 0.0))

def draw_buttons():
    # Draw Restart button
    rectangle(*restart_button, (0.0, 1.0, 0.0))
    glColor3f(1.0, 1.0, 1.0)
    text(restart_button[0] + 10, restart_button[1] + 10, "Restart")
    
    # Draw Quit button
    rectangle(*quit_button, (1.0, 0.0, 0.0))
    glColor3f(1.0, 1.0, 1.0)
    text(quit_button[0] + 25, quit_button[1] + 10, "Quit")


def draw():
    global game_over

    glClear(GL_COLOR_BUFFER_BIT)

    if level == 2:
        glClearColor(0.5, 0.8, 1.0, 0.0)
    else:
        glClearColor(0.0, 0.0, 0.0, 0.0)

    if not game_over:
        circle(ball_x, ball_y, radius, (1.0, 0.0, 0.0) if ball_is_fireball else (1.0, 1.0, 1.0))
        rectangle(board_x, board_y, board_width, board_height, board_color)
        draw_boxes()
        draw_fireball()
        score_board()
    else:
        # Game Over message
        glColor3f(1.0, 0.0, 0.0)
        text(window_width // 2 - 50, window_height // 2 + 20, "Game Over")
        
        # Display the score below the "Game Over" message
        glColor3f(1.0, 1.0, 1.0)
        text(window_width // 2 - 60, window_height // 2 - 10, f"Your Score: {score}")
        
        # Draw Restart and Quit buttons
        draw_buttons()

    if is_paused and not game_over:
        glColor3f(1.0, 1.0, 0.0)
        text(window_width // 2 - 50, window_height // 2, "Paused")

    glutSwapBuffers()

def restart_game():
    global ball_x, ball_y, ball_dx, ball_dy, blocks, game_over, score, level, fireball_active
    ball_x, ball_y = 300, 50
    ball_dx, ball_dy = 4, 3
    blocks = [[1 for _ in range(box_at_x)] for _ in range(box_at_y)]
    game_over = False
    score = 0
    level = 1
    fireball_active = False

def update(value):
    global ball_x, ball_y, ball_dx, ball_dy, game_over, score, is_paused, fireball_active, fireball_x, fireball_y, ball_is_fireball

    if game_over or is_paused:
        glutTimerFunc(16, update, 0)
        return

    # Update ball position
    ball_x += ball_dx
    ball_y += ball_dy

    # Ball collision with walls
    if ball_x + radius > window_width or ball_x - radius < 0:
        ball_dx *= -1
    if ball_y + radius > window_height:
        ball_dy *= -1

    # Ball collision with paddle
    if board_x <= ball_x <= board_x + board_width and ball_y - radius <= board_y + board_height:
        ball_dy *= -1

    # Ball collision with bricks
    for i in range(box_at_y):
        for j in range(box_at_x):
            if blocks[i][j]:  # If the brick is not already broken
                brick_x = j * box_width
                brick_y = window_height - (i + 1) * box_height

                # Check if ball collides with this brick
                if (
                    brick_x <= ball_x <= brick_x + box_width
                    and brick_y <= ball_y <= brick_y + box_height
                ):
                    blocks[i][j] = 0  # Break the brick
                    score += 10  # Increment score
                    ball_dy *= -1  # Reverse vertical direction of ball

                    # Spawn fireball if this is the first fireball opportunity
                    if level == 2 and not fireball_active:
                        fireball_active = True
                        fireball_x = brick_x + box_width // 2
                        fireball_y = brick_y + box_height // 2
                    break  # Exit loop once collision is handled

    # Handle fireball mechanics
    if fireball_active and not fireball_caught:
        fireball_y -= 5  # Fireball falls down
        if (
            board_x <= fireball_x <= board_x + board_width
            and fireball_y - fireball_radius <= board_y + board_height
        ):
            fireball_caught = True
            ball_is_fireball = True  # Ball turns into a fireball
            fireball_active = False  # Remove fireball

    # Ball as fireball mechanics
    if ball_is_fireball:
        for i in range(box_at_y):
            for j in range(box_at_x):
                if blocks[i][j]:  # If the brick is not already broken
                    brick_x = j * box_width
                    brick_y = window_height - (i + 1) * box_height

                    # Check if fireball collides with this brick
                    if (
                        brick_x <= ball_x <= brick_x + box_width
                        and brick_y <= ball_y <= brick_y + box_height
                    ):
                        blocks[i][j] = 0  # Break the first brick
                        score += 10

                        # Break the brick above if it exists
                        if i + 1 < box_at_y and blocks[i + 1][j]:
                            blocks[i + 1][j] = 0
                            score += 10

                        ball_dy *= -1  # Reverse vertical direction of ball
                        ball_is_fireball = False  # Revert to normal ball
                        break

    # Ball falls below paddle
    if ball_y - radius < 0:
        game_over = True

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)



def keyboard(key, x, y):
    global board_x, is_paused, game_over

    if key == b'q':
        sys.exit(0)
    elif key == b'a' and not is_paused and board_x > 0:
        board_x -= 20
    elif key == b'd' and not is_paused and board_x + board_width < window_width:
        board_x += 20
    elif key == b'p':
        is_paused = not is_paused
    elif key == b' ':
        is_paused = not is_paused
        if is_paused:
            print("Game Paused")
        else:
            print("Game Resumed")


def mouse_click(button, state, x, y):
    global game_over, ball_x, ball_y, ball_dx, ball_dy, board_x, board_color, blocks, level, score, is_paused

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Map window coordinates to game coordinates
        game_y = window_height - y  # Invert y-axis to match OpenGL coordinates

        # Check if "Restart" button is clicked
        restart_x_start = window_width // 2 - 100
        restart_x_end = window_width // 2 - 20
        restart_y_start = window_height // 2 - 50
        restart_y_end = window_height // 2 - 20

        if restart_x_start <= x <= restart_x_end and restart_y_start <= game_y <= restart_y_end:
            restart_game()

        # Check if "Quit" button is clicked
        quit_x_start = window_width // 2 + 20
        quit_x_end = window_width // 2 + 100
        quit_y_start = window_height // 2 - 50
        quit_y_end = window_height // 2 - 20

        if quit_x_start <= x <= quit_x_end and quit_y_start <= game_y <= quit_y_end:
            sys.exit(0)
def restart_game():
    global ball_x, ball_y, ball_dx, ball_dy, board_x, board_y, board_color, blocks, level, score, game_over, is_paused, fireball_active, ball_is_fireball
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
    fireball_active = False
    ball_is_fireball = False


def init():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"DX-Ball")
    glutDisplayFunc(draw)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse_click)  # Register mouse click handler
    glutTimerFunc(16, update, 0)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    gluOrtho2D(0, window_width, 0, window_height)

if __name__ == "__main__":
    init()
    glutMainLoop()
