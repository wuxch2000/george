#! /usr/local/bin/python3

import math
import time
import random
import arcade

castle_list = arcade.SpriteList()
tank_list = arcade.SpriteList()
bullet_list = arcade.SpriteList()
tower_sprite_list = arcade.SpriteList()
tower_list = []

WINDOW_WIDTH =1600 
WINDOW_HEIGHT=1000 
    
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
    def __init__(self, x, y, target_x, target_y, speed = 5, distance=80):
        super().__init__(":resources:images/space_shooter/laserBlue01.png", 0.8)
        r = math.atan2(target_y - y, target_x - x)
        self.center_x = x+distance*math.cos(r)
        self.center_y = y+distance*math.sin(r)
        self.speed = speed
        self.radians = -r
        self.change_x = self.speed * math.cos(r)
        self.change_y = self.speed * math.sin(r)
        return
    def update(self, delta_time: float = 1/60):
        self.center_x += self.change_x
        self.center_y += self.change_y
        return
    def out_of_view(self):
        if self.top >= WINDOW_HEIGHT or self.bottom <= 0 or self.left <=0 or self.right >= WINDOW_WIDTH:
            return True
        return False
    
class Tower():
    def __init__(self, x, y, shoot_interval=2):
        self.shoot_interval = shoot_interval
        self.shoot_time=time.time()
        self.tower_color = arcade.color.VIOLET_BLUE
        self.base_radius = 10
        self.cannon_width=self.base_radius*2
        self.cannon_height=self.base_radius/2
        self.base = arcade.SpriteCircle(self.base_radius, color=self.tower_color, center_x=x, center_y=y)
        self.cannon = arcade.SpriteSolidColor(color=self.tower_color, center_x=x+self.cannon_width/2, center_y=y, width=self.cannon_width, height=self.cannon_height)
        return
    def append_to_list(self, a:arcade.SpriteList):
        a.append(self.base)
        a.append(self.cannon)
        return
    def aim(self, s:arcade.Sprite):
        r = math.atan2(s.center_y - self.cannon.center_y, s.center_x - self.cannon.center_x)
        self.cannon.center_x = self.base.center_x + ((self.cannon_width)/2)*math.cos(r)
        self.cannon.center_y = self.base.center_y + ((self.cannon_width)/2)*math.sin(r)
        self.cannon.radians = -r
        self.aim_sprite = s
        return
    def shoot(self):
        if self.aim_sprite:
            bullet = Bullet(self.cannon.center_x, self.cannon.center_y, self.aim_sprite.center_x, self.aim_sprite.center_y)
            bullet_list.append(bullet)
        return
    def update(self, delta_time: float = 1/60):
        current_time = time.time()
        if current_time - self.shoot_time >= self.shoot_interval:
            self.shoot()
            self.shoot_time = current_time
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
    new_tank_interval = 3
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.DARK_GRAY
        castle = Castle(300,300,50,50)
        castle.append_to_list(castle_list)
        self.new_tank_time = 0
        return
    def on_key_press(self, key, modifiers):
        return 
    def on_key_release(self, key, modifiers):
        return
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            tower = Tower(x,y)
            tower_list.append(tower)
            tower.append_to_list(tower_sprite_list)
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            pass
        return
    def _new_tank(self):
        random_x = random.randint(0, 200)
        random_y = random.randint(0, 200)
        if random.randint(-1,1) >= 0:
            random_x = WINDOW_WIDTH-random_x
        if random.randint(-1,1) >= 0:
            random_y = WINDOW_HEIGHT-random_y
        tank = Tank(random_x,random_y)
        tank.set_dest(WINDOW_WIDTH/2,WINDOW_HEIGHT/2)
        tank_list.append(tank)
        return
    def on_update(self, delta_time):
        cur_time = time.time()
        if self.new_tank_time == 0 or cur_time - self.new_tank_time >= self.new_tank_interval:
            self.new_tank_time = cur_time
            self._new_tank()
        for s in tower_list:
            closest_sprite, distance = arcade.get_closest_sprite(s.base, tank_list)
            if closest_sprite:
                s.aim(closest_sprite)
                s.update()
        tank_list.update()
        bullet_list.update()
        tower_sprite_list.update()
        for bullet in bullet_list:
            if bullet.out_of_view():
                bullet.kill()
                continue
            hit_tank_list = bullet.collides_with_list(tank_list)
            if len(hit_tank_list) > 0:
                for t in hit_tank_list:
                    print("hit tank, bullet,box:", bullet.hit_box)
                    t.kill()
                bullet.kill()
        return
    def on_draw(self):
        self.clear()
        castle_list.draw()
        tank_list.draw()
        bullet_list.draw()
        tower_sprite_list.draw()
        # bullet_list.draw_hit_boxes(arcade.color.RED)
        # tank_list.draw_hit_boxes(arcade.color.RED)
        return

class TankattackWindow(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH,WINDOW_HEIGHT,"Tank Attack")
        return
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE or key == arcade.key.Q:
            print("Game Over")
            self.close()
        return 
    def on_key_release(self, key, modifiers):
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
