import math
s = math.sqrt(5000)
from turtle import *

g=Turtle()
g.penup()


g.forward(100)
g.pendown()

for i in range(0,8):
    g.left(45)
    g.forward(100)
g.right(180)
g.forward(50)
g.right(90)
g.forward(s+50)

for r in range (0,18):
    g.right(40)
    g.forward(50)



done() 