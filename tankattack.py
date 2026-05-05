#! /usr/local/bin/python3

import math
import time
import arcade

castle_list = arcade.SpriteList()
tank_list = arcade.SpriteList()
bullet_list = arcade.SpriteList()

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

class Castle():
    def __init__(self, x, y, width, heigh):
        self.list= []
        self.list.append(Brick(700, 450, 100, 10))
        self.list.append(Brick(700, 300, 100, 10))
        self.list.append(Brick(625, 375, 10, 100))
        self.list.append(Brick(775, 375, 10, 100))
        self.list.append(Brick(762, 314, 10, 50, angle=45))
        self.list.append(Brick(638, 313, 10, 50, angle=-45))
        self.list.append(Brick(760, 435, 10, 50, angle=-45))
        self.list.append(Brick(638, 435, 10, 50, angle=45))
        return
    def append_to_list(self, a:arcade.SpriteList):
        for i in self.list:
            a.append(i)

class Bullet(arcade.Sprite):
    def __init__(self, x, y, target_x, target_y, speed = 5):
        super().__init__(":resources:images/space_shooter/laserBlue01.png", 0.8)
        self.center_x = x
        self.center_y = y
        self.speed = speed
        r = math.atan2(target_y - self.center_y, target_x - self.center_x)
        self.radians = -r
        self.change_x = self.speed * math.cos(r)
        self.change_y = self.speed * math.sin(r)
        return
    def update(self, delta_time: float = 1/60):
        self.center_x += self.change_x
        self.center_y += self.change_y
        return
    
class Tank(arcade.Sprite):
    destin_x = None
    destin_y = None
    def __init__(self, x, y, speed = 1, health = 10, shoot_interval=2):
        super().__init__("image/tank-top-view-50.png", 1)
        self.center_x = x
        self.center_y = y
        self.speed = speed
        self.health = health
        self.shoot_interval = shoot_interval
        self.shoot_time=time.time()
        self.shoot_sound = arcade.sound.load_sound(":resources:sounds/laser1.wav")
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
    def shoot(self):
        print("shoot")
        if self.destin_x and self.destin_y:
            arcade.play_sound(self.shoot_sound)
            bullet = Bullet(self.center_x, self.center_y, self.destin_x, self.destin_y)
            bullet_list.append(bullet)
        return
    def update(self, delta_time: float = 1/60):
        current_time = time.time()
        if current_time - self.shoot_time >= self.shoot_interval:
            self.shoot()
            self.shoot_time = current_time
        if self.destin_x and self.destin_y and (self.destin_x-self.center_x) <= abs(self.change_x) and abs(self.destin_y-self.center_y) <= abs(self.change_y):
            return
        self.center_x += self.change_x
        self.center_y += self.change_y
        return

class TankattackView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.DARK_GRAY
        castle = Castle(300,300,50,50)
        castle.append_to_list(castle_list)
        tank = Tank(100,100)
        # tank.set_radians(math.pi/2)
        tank.set_dest(400,450)
        tank_list.append(tank)
        return
    def on_key_press(self, key, modifiers):
        return 
    def on_key_release(self, key, modifiers):
        return
    def on_draw(self):
        self.clear()
        castle_list.draw()
        tank_list.draw()
        bullet_list.draw()
        return
    def on_update(self, delta_time):
        tank_list.update()
        bullet_list.update()
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
