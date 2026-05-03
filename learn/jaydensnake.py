import turtle
import time
import random
 
t = turtle.Turtle()
t.penup()
t.shape("square")
t.color("green")
t.shapesize(1.2)
t.speed(0)
 
screen = turtle.Screen()
 
score = 0
 
move_x = 0
move_y = 0
 
a = turtle.Turtle()
a.penup()
a.speed(0)
a.shape("circle")
a.color("red")
 
running = True
 
speed = 100
 
def move_right():
    global move_x, move_y
    if move_x != -25:
        move_x = 25
        move_y = 0
def move_left():
    global move_x, move_y
    if move_x != 25:
        move_x = -25
        move_y = 0
def move_up():
    global move_x, move_y
    if move_y != -25:
        move_x = 0
        move_y = 25
def move_down():
    global move_x, move_y
    if move_y != 25:
        move_x = 0
        move_y = -25
 
screen.listen()
screen.onkeypress(move_up, "Up")
screen.onkeypress(move_down, "Down")
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
 
def spawn_apple():
    x = random.randint(-12, 12)
    y = random.randint(-12, 12)
    a.goto(25*x, 25*y)
 
spawn_apple()
 
o = 1
 
snakes = []
 
c = 1
 
def update():
    global score, a, ID, o, c, t, running, speed
    if t.distance(a) < 10:
        score += 1
        if speed > 25:
            speed -= 1
        spawn_apple()
        b = turtle.Turtle()
        b.penup()
        b.shape("square")
        b.speed(0)
        b.color("green")
        b.goto(t.xcor(), t.ycor())
        b.my_id = o
        b.no_kill = 1
        snakes.append(b)
        o += 1
    if t.xcor() < -300 or 300 < t.xcor() or t.ycor() < -300 or 300 < t.ycor():
        running = False
        t.clear()
        t.hideturtle()
        del t
        print("you lost. Your score is: " + str(score))
        time.sleep(1000000)
    for b in snakes[:]:
        if b.distance(t) < 25:
            if b.no_kill == 0:
                t.clear()
                t.hideturtle()
                running = False
                print("You lost. Your score is: ", score)
                time.sleep(1000000)
    screen.ontimer(update, 10)
update()
 
def snake_move():
    global o, c
    for b in snakes[:]:
        if b.my_id == c:
            b.no_kill = 1
            b.goto(t.xcor(), t.ycor())
            break
    c += 1
    if c > o-1:
        c = 1
 
def move():
    global move_x, move_y, t, running, speed
    if running is True:
        t.goto(t.xcor()+move_x, t.ycor()+move_y)
        snake_move()
    screen.ontimer(move, speed)
move()
 
def thing():
    for b in snakes[:]:
        if b.distance(t) > 25:
            b.no_kill = 0
    screen.ontimer(thing, 1)
thing()
turtle.done()
