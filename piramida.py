import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

texture_enabled = False

tex_coords = [
    (0.0, 0.0),
    (1.0, 0.0),
    (0.5, 1.0),
    (0.5, 0.5)
]

def divide(v1, v2, v3, v4, n): 
    v12 = [(v1[i] + v2[i]) / 2 for i in range(3)]
    v23 = [(v2[i] + v3[i]) / 2 for i in range(3)]
    v31 = [(v3[i] + v1[i]) / 2 for i in range(3)]
    v14 = [(v1[i] + v4[i]) / 2 for i in range(3)]
    v24 = [(v2[i] + v4[i]) / 2 for i in range(3)]
    v34 = [(v3[i] + v4[i]) / 2 for i in range(3)]

    if n > 0:
        divide(v1, v12, v31, v14, n - 1)
        divide(v12, v2, v23, v24, n - 1)
        divide(v31, v23, v3, v34, n - 1)
        divide(v14, v24, v34, v4, n - 1)
    else:
        tetra(v1, v2, v3, v4) 

def triangle(a, b, c):
    glBegin(GL_TRIANGLES)
    glTexCoord2fv(tex_coords[0])
    glVertex3fv(a)

    glTexCoord2fv(tex_coords[1])
    glVertex3fv(b)

    glTexCoord2fv(tex_coords[2])
    glVertex3fv(c)
    glEnd()

def tetra(v1, v2, v3, v4): 
    glColor3f(1, 0.5, 0.6)
    triangle(v1, v2, v3) 
    triangle(v1, v3, v4) 
    triangle(v2, v3, v4) 
    triangle(v1, v2, v4) 

def draw():
    p = [
        [-0.65, -0.5, 0.5],
        [0.65, -0.5, 0.5],
        [0, 0.6, 0.5],
        [0, -0.05, -0.5]
    ]

    divide(p[0], p[1], p[2], p[3], n)

def load_texture():
    texture_surface = pygame.image.load("bricks.jpg") 
    texture_data = pygame.image.tostring(texture_surface, "RGB", True)
    width, height = texture_surface.get_size()

    
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

def toggle_texture():
    global texture_enabled
    texture_enabled = not texture_enabled
    if texture_enabled:
        glEnable(GL_TEXTURE_2D)
    else:
        glDisable(GL_TEXTURE_2D)

def set_lighting():
    glLightfv(GL_LIGHT0, GL_POSITION, (0.0, 0.0, 1.0, 0.0))  
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0)) 
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))  

    glLightfv(GL_LIGHT1, GL_POSITION, (1.0, 1.0, 1.0, 1.0))  
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))  
    glLightfv(GL_LIGHT1, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))  


def main():
    global n
    n = int(input(" "))
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -2)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_COLOR_MATERIAL)

    glEnable(GL_DEPTH_TEST)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    load_texture()
                    toggle_texture()
                    
                if event.key == pygame.K_UP:
                    glTranslatef(0,0.1,0)

                if event.key == pygame.K_DOWN:
                    glTranslatef(0,-0.1,0)

                if event.key == pygame.K_LEFT:
                    glTranslatef(-0.1,0,0)

                if event.key == pygame.K_RIGHT:
                    glTranslatef(0.1,0,0)

                if event.key == pygame.K_w:  
                    glTranslatef(0.0, 0.0, 0.1)

                if event.key == pygame.K_s: 
                    glTranslatef(0.0, 0.0, -0.1)

        if n==0:
            glRotatef(0.5*0.05, 1, 1, 1)
        elif n<4:
            glRotatef(n * 0.05, 1, 1, 1)
        else:
            glRotatef(n * n * 0.05, 1, 1, 1)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw()
        set_lighting()
        pygame.display.flip()


main()
