from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import *
import math
import sys

# Altura do  triângulo.
height = int (sys.argv[1]) if len(sys.argv) > 1 else 1.7

# Porcentagem de corte da altura (valor de 0 a 1). 0 significa 0% de corte, 1 significa 100% de corte.
cutPercentage = float (sys.argv[2]) if len(sys.argv) > 2 else 0.001

# Altura cortada em cutPercentage porcento.
cutH = height * (cutPercentage)

# Altura restante pós corte.
h = height * (1 - cutPercentage)

# Ângulo do triângulo
theta = math.pi/6

# Hipotenusa do triângulo cujo cateto oposto é cutH e ângulo theta.
hip = cutH/math.sin(theta)

# O valor de corte é o cateto adjacente do triângulo cujo cateto oposto é cutH e ângulo theta.
cutValue = (hip**2 - cutH**2)**0.5

vertices = (
    ( 1,-1,-1),
    ( cutValue, h,-cutValue),
    (-cutValue, h,-cutValue),
    (-1,-1,-1),
    ( 1,-1, 1),
    ( cutValue, h, cutValue),
    (-1,-1, 1),
    (-cutValue, h, cutValue),
    )

faces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

def calculaNormalFace(face):
    x = 0
    y = 1
    z = 2
    v0 = vertices[face[0]]
    v1 = vertices[face[1]]
    v2 = vertices[face[2]]
    U = ( v2[x]-v0[x], v2[y]-v0[y], v2[z]-v0[z] )
    V = ( v1[x]-v0[x], v1[y]-v0[y], v1[z]-v0[z] )
    N = ( (U[y]*V[z]-U[z]*V[y]),(U[z]*V[x]-U[x]*V[z]),(U[x]*V[y]-U[y]*V[x]))
    NLength = sqrt(N[x]*N[x]+N[y]*N[y]+N[z]*N[z])
    return (N[x]/NLength, N[y]/NLength, N[z]/NLength)

def Piramide():
    glBegin(GL_QUADS)
    i = 0
    for face in faces:
        normal = calculaNormalFace(face)
        glNormal3fv(normal)
        
        for vertex in face:
            glVertex3fv(vertices[vertex])
        i = i+1
    glEnd()

    glColor3fv((0,0.5,0))

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glRotatef(3,2,4,0)
    Piramide()
    glutSwapBuffers()
 
def timer(i):
    glutPostRedisplay()
    glutTimerFunc(50,timer,1)

def reshape(w, h):
    glViewport(0,0,w,h)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45,float(w)/float(h),0.1,50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0,1,10,0,0,0,0,1,0)

def init():
    mat_ambient = (0.4, 0.0, 0.0, 1.0)
    mat_diffuse = (1.0, 0.0, 0.0, 1.0)
    mat_specular = (0.0, 1.0, 0.0, 1.0)
    mat_shininess = (50,)
    light_position = (5.0, 5.0, 5.0)
    glClearColor(0.0,0.0,0.0,0.0)
    glShadeModel(GL_FLAT)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(800,600)
    glutCreateWindow("Pirâmide/Tronco")
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutTimerFunc(50,timer,1)
    init()
    glutMainLoop()

main()
