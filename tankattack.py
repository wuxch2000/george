#! /usr/local/bin/python3

import math
import arcade

class TankattackWindow(arcade.Window):
    def __init__(self):
        super().__init__(1400,750,"Tank Attack")
        return
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE or key == arcade.key.Q:
            print("Game Over")
            self.close()
        return 
    def on_key_release(self, key, modifiers):
        return
    
class Brick(arcade.SpriteSolidColor):
    def __init__(self, x, y, width, heigh, angle=0):
        super().__init__(center_x=x, center_y=y, width=width, height=heigh, angle=angle, color=arcade.color.ROSE_EBONY)
        return
    
class Tank(arcade.Sprite):
    destin_x = None
    destin_y = None
    move_radians = None
    def __init__(self, x, y, speed = 1, health = 10):
        super().__init__("image/tank-top-view-50.png", 1)
        self.center_x = x
        self.center_y = y
        self.speed = speed
        self.health = health
        return
    def set_radians(self, r):
        self.radians = (math.pi/2)-r
        return
    def set_dest(self, x, y):
        self.destin_x, self.destin_y = x, y
        r = math.atan2(self.destin_y - self.center_y,self.destin_x - self.center_x)
        self.set_radians(r)
        self.change_x = self.speed * math.cos(r)
        self.change_y = self.speed * math.sin(r)
        return
    def update(self, delta_time: float = 1/60):
        self.center_x += self.change_x
        self.center_y += self.change_y
        return

class TankattackView(arcade.View):
    castle = arcade.SpriteList()
    tank_list = arcade.SpriteList()
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.DARK_GRAY
        self.castle.append(Brick(700, 450, 100, 10))
        self.castle.append(Brick(700, 300, 100, 10))
        self.castle.append(Brick(625, 375, 10, 100))
        self.castle.append(Brick(775, 375, 10, 100))
        self.castle.append(Brick(762, 314, 10, 50, angle=45))
        self.castle.append(Brick(638, 313, 10, 50, angle=-45))
        self.castle.append(Brick(760, 435, 10, 50, angle=-45))
        self.castle.append(Brick(638, 435, 10, 50, angle=45))

        tank = Tank(300,300)
        # tank.set_radians(math.pi/2)
        tank.set_dest(400,450)
        self.tank_list.append(tank)
        return
    def on_key_press(self, key, modifiers):
        return 
    def on_key_release(self, key, modifiers):
        return
    def on_draw(self):
        self.clear()
        self.castle.draw()
        self.tank_list.draw()
        return
    def on_update(self, delta_time):
        self.tank_list.update()
        return


def main():
    print("Game Start")
    window = TankattackWindow()
    view = TankattackView()
    window.show_view(view)
    arcade.run()
    return

if __name__ == "__main__":
    main()
