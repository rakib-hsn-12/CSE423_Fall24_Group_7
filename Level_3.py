
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import cos, sin, pi, sqrt
import random

# Global Variables
window_width = 800
window_height = 600
paddle_width = 100
paddle_height = 20
paddle_x = (window_width - paddle_width) // 2
paddle_y = 20
ball_radius = 10
ball_x = window_width // 2
ball_y = window_height // 2
ball_dx = 5
ball_dy = 5
brick_rows = 4
brick_cols = 10
brick_width = 60
brick_height = 20
bricks = []

# Spinning Wheel Constants
wheel_radius = 30
wheel_speed = 0.03
wheel_y = window_height // 2
left_wheel_x = wheel_radius
right_wheel_x = window_width - wheel_radius
wheel_angle = 0

# Initialize Bricks
def init_bricks():
    global bricks
    bricks = [[random.randint(0, 1) for _ in range(brick_cols)] for _ in range(brick_rows)]

# Initialize OpenGL
def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(0, window_width, 0, window_height)
    init_bricks()

# Render Paddle
def draw_paddle():
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glVertex2f(paddle_x, paddle_y)
    glVertex2f(paddle_x + paddle_width, paddle_y)
    glVertex2f(paddle_x + paddle_width, paddle_y + paddle_height)
    glVertex2f(paddle_x, paddle_y + paddle_height)
    glEnd()

# Render Ball
def draw_ball():
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_POLYGON)
    for i in range(360):
        angle = i * pi / 180
        x = ball_x + ball_radius * cos(angle)
        y = ball_y + ball_radius * sin(angle)
        glVertex2f(x, y)
    glEnd()

# Render Bricks
def draw_bricks():
    brick_y = window_height - brick_height
    for row in range(brick_rows):
        brick_x = 0
        for col in range(brick_cols):
            if bricks[row][col] == 1:
                glColor3f(0.5, 0.5, 0.5)
                glBegin(GL_QUADS)
                glVertex2f(brick_x, brick_y)
                glVertex2f(brick_x + brick_width, brick_y)
                glVertex2f(brick_x + brick_width, brick_y + brick_height)
                glVertex2f(brick_x, brick_y + brick_height)
                glEnd()
            brick_x += brick_width
        brick_y -= brick_height

# Function to draw the spinning wheels
def draw_wheels():
    glColor3f(0.5, 0.5, 0.5)
    
    # Left Wheel
    glBegin(GL_POLYGON)
    for i in range(360):
        angle = i * pi / 180
        x = left_wheel_x + wheel_radius * cos(angle + wheel_angle)
        y = wheel_y + wheel_radius * sin(angle)
        glVertex2f(x, y)
    glEnd()
    
    # Right Wheel
    glBegin(GL_POLYGON)
    for i in range(360):
        angle = i * pi / 180
        x = right_wheel_x + wheel_radius * cos(angle - wheel_angle)
        y = wheel_y + wheel_radius * sin(angle)
        glVertex2f(x, y)
    glEnd()

# Update Wheel Rotation
def update_wheel_rotation():
    global wheel_angle
    wheel_angle += wheel_speed

# Check Collision with Paddle
def check_paddle_collision():
    if paddle_x <= ball_x <= paddle_x + paddle_width and ball_y - ball_radius <= paddle_y + paddle_height:
        return True
    return False

# Check Collision with Bricks
def check_brick_collision():
    global bricks
    row = int((window_height - ball_y) / brick_height)
    col = int(ball_x / brick_width)
    if 0 <= row < brick_rows and 0 <= col < brick_cols and bricks[row][col] == 1:
        bricks[row][col] = 0
        return True
    return False

# Display Function
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_paddle()
    draw_ball()
    draw_bricks()
    draw_wheels()
    glutSwapBuffers()

# Timer Function
def timer(value):
    global ball_x, ball_y, ball_dx, ball_dy

    update_wheel_rotation()

    if check_paddle_collision():
        paddle_center = paddle_x + paddle_width / 2
        angle = (ball_x - paddle_center) / (paddle_width / 2) * (pi / 4)
        ball_dx = 5 * cos(angle)
        ball_dy = 5 * sin(angle)

    if ball_x - ball_radius < 0 or ball_x + ball_radius > window_width:
        ball_dx = -ball_dx

    if ball_y + ball_radius > window_height:
        ball_dy = -ball_dy

    if check_brick_collision():
        ball_dy = -ball_dy

    if ball_y - ball_radius < 0:
        ball_dy = -ball_dy

    ball_x += ball_dx
    ball_y += ball_dy

    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)

# Mouse Input Handling
def mouse_motion(x, y):
    global paddle_x
    paddle_x = x - paddle_width / 2

# Main Function
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"DX-Ball Game")
    init()
    glutDisplayFunc(display)
    glutTimerFunc(16, timer, 0)
    glutPassiveMotionFunc(mouse_motion)
    glutMainLoop()

if __name__ == "__main__":
    main()
