#! /usr/local/bin/python3

import math
import time
import random
import arcade

castle_list = arcade.SpriteList()
tank_list = arcade.SpriteList()
bullet_list = arcade.SpriteList()
tower_list = arcade.SpriteList()
tower_part_list = arcade.SpriteList()
range_list = arcade.SpriteList()

WINDOW_WIDTH =1600 
WINDOW_HEIGHT=1000 
show_range=False
game_over=False
    
class Brick(arcade.SpriteSolidColor):
    def __init__(self, x, y, width, heigh, angle=0):
        super().__init__(center_x=x, center_y=y, width=width, height=heigh, angle=angle, color=arcade.color.ROSE_EBONY)
        return

class Castle(arcade.Sprite):
    castle_radius = 100
    health = 20
    castle_color = arcade.color.DARK_LIVER
    def __init__(self):
        super().__init__()
        # self.texture=arcade.make_circle_texture(self.castle_radius , self.castle_color)
        self._new_radius()
        self.center_x=WINDOW_WIDTH/2
        self.center_y=WINDOW_HEIGHT/2
        self.delta_radius = int(self.castle_radius/self.health)
        # self.list.append(Brick(700, 450, 100, 10))
        # self.list.append(Brick(700, 300, 100, 10))
        # self.list.append(Brick(625, 375, 10, 100))
        # self.list.append(Brick(775, 375, 10, 100))
        # self.list.append(Brick(762, 314, 10, 50, angle=45))
        # self.list.append(Brick(638, 313, 10, 50, angle=-45))
        # self.list.append(Brick(760, 435, 10, 50, angle=-45))
        # self.list.append(Brick(638, 435, 10, 50, angle=45))
        return
    def _new_radius(self):
        if self.castle_radius > 0:
            self.texture = arcade.make_circle_texture(self.castle_radius , self.castle_color)
            # self.hit_box = self.texture.hit_box_points
        return
    def hit(self):
        global game_over
        self.health -= 1
        self.castle_radius -= self.delta_radius
        print(f"castle: health={self.health}, {self.castle_radius}")
        self._new_radius()
        if self.health == 0:
            print("Castle is destroied")
            game_over = True
            self.kill()

class Bullet(arcade.Sprite):
    shooter = None
    def __init__(self, x, y, target_x, target_y, shooter:arcade.Sprite, speed = 5, distance=0):
        super().__init__(":resources:images/space_shooter/laserBlue01.png", 0.8)
        r = math.atan2(target_y - y, target_x - x)
        self.center_x = x+distance*math.cos(r)
        self.center_y = y+distance*math.sin(r)
        self.speed = speed
        self.radians = -r
        self.change_x = self.speed * math.cos(r)
        self.change_y = self.speed * math.sin(r)
        self.shooter = shooter
        return
    def update(self, delta_time: float = 1/60):
        self.center_x += self.change_x
        self.center_y += self.change_y
        return
    def out_of_view(self):
        if self.top >= WINDOW_HEIGHT or self.bottom <= 0 or self.left <=0 or self.right >= WINDOW_WIDTH:
            return True
        return False
    def check_hit(self, sl:arcade.SpriteList):
        if self.out_of_view():
            self.kill()
            return
        if not sl:
            return
        hit_list = self.collides_with_list(sl)
        for s in hit_list:
            if s is self.shooter:
                continue
            s.hit()
            self.kill()
            break
        return
class Tower(arcade.SpriteCircle):
    target = None
    shoot_time = 0
    base_radius = 10
    shoot_interval = 2
    tower_color = arcade.color.VIOLET_BLUE
    def __init__(self, x, y, health=3, range=300):
        self.health = health
        self.range = range
        super().__init__(self.base_radius, color=self.tower_color, center_x=x, center_y=y)
        self.range_spirte = arcade.SpriteCircle(range, color=arcade.color.DARK_YELLOW, center_x=x, center_y=y)
        self.cannon_width=self.base_radius*2
        self.cannon_height=self.base_radius/2
        self.cannon = arcade.SpriteSolidColor(color=self.tower_color, center_x=x+self.cannon_width/2, center_y=y, width=self.cannon_width, height=self.cannon_height)
        return
    def aim(self, s:arcade.Sprite):
        r = math.atan2(s.center_y - self.cannon.center_y, s.center_x - self.cannon.center_x)
        self.cannon.center_x = self.center_x + ((self.cannon_width)/2)*math.cos(r)
        self.cannon.center_y = self.center_y + ((self.cannon_width)/2)*math.sin(r)
        self.cannon.radians = -r
        self.target = s
        return
    def shoot(self):
        if self.target:
            bullet = Bullet(self.center_x, self.center_y, self.target.center_x, self.target.center_y, self)
            bullet_list.append(bullet)
        return
    def update(self, delta_time: float = 1/60):
        current_time = time.time()
        if self.target:
            if self.shoot_time == 0 or current_time - self.shoot_time >= self.shoot_interval:
                self.shoot_time = current_time
                self.shoot()
        return
    def hit(self):
        self.health-=1
        if self.health == 2:
            self.color = arcade.color.YELLOW
            self.cannon.color = arcade.color.YELLOW
        elif self.health == 1:
            self.color = arcade.color.RED
            self.cannon.color = arcade.color.RED
        if self.health == 0:
            self.kill()
        return
    def kill(self):
        self.cannon.kill()
        self.range_spirte.kill()
        super().kill()
        return

class Tank(arcade.Sprite):
    final_target_sprite=None
    target_sprite = None
    def __init__(self, x, y, speed = 1, health = 3, range=300, shoot_interval=2, target_sprite:arcade.Sprite=None):
        # super().__init__("image/tank.blue.png", 1)
        super().__init__()
        super().append_texture(arcade.load_texture("image/tank.blue.png"))
        super().append_texture(arcade.load_texture("image/tank.yellow.png"))
        super().append_texture(arcade.load_texture("image/tank.red.png"))
        super().set_texture(0)
        self.range = range
        self.range_spirte = arcade.SpriteCircle(range, color=arcade.color.DARK_TAN, center_x=x, center_y=y)
        self.center_x = x
        self.center_y = y
        self.speed = speed
        self.health = health
        self.shoot_interval = shoot_interval
        self.shoot_time=time.time()
        self.shoot_sound = arcade.sound.load_sound(":resources:sounds/laser1.wav")
        if target_sprite:
            self.final_target_sprite = target_sprite
            self._set_dest_pos()
        return
    def set_radians(self, r):
        self.radians = (math.pi/2)-r
        return
    def _set_dest_pos(self):
        s = self.target_sprite
        if not s:
            s = self.final_target_sprite
        if s:
            r = math.atan2(s.center_y - self.center_y, s.center_x - self.center_x)
            self.set_radians(r)
            self.change_x = self.speed * math.cos(r)
            self.change_y = self.speed * math.sin(r)
        return
    def aim(self, target: arcade.Sprite):
        self.target_sprite = target
        return self._set_dest_pos()
    def reset_aim(self):
        self.target_sprite = None
        return self._set_dest_pos()
    def shoot(self):
        s = self.target_sprite
        if not s:
            s = self.final_target_sprite
        if s:
            arcade.play_sound(self.shoot_sound)
            bullet = Bullet(self.center_x, self.center_y, s.center_x, s.center_y, self)
            bullet_list.append(bullet)
        return
    def update(self, delta_time: float = 1/60):
        current_time = time.time()
        if current_time - self.shoot_time >= self.shoot_interval:
            self.shoot()
            self.shoot_time = current_time
        if self.target_sprite and arcade.check_for_collision(self.target_sprite, self):
            return
        if self.final_target_sprite and arcade.check_for_collision(self.final_target_sprite, self):
            return
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.range_spirte.center_x += self.change_x
        self.range_spirte.center_y += self.change_y
        return
    def hit(self):
        self.health-=1
        if self.health == 2:
            super().set_texture(1)
        elif self.health == 1:
            super().set_texture(2)
        if self.health == 0:
            self.kill()
        return
    def kill(self):
        self.range_spirte.kill()
        super().kill()
        return

class TankattackView(arcade.View):
    new_tank_interval = 3
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.DARK_GRAY
        self.castle = Castle()
        castle_list.append(self.castle)
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
            tower_part_list.append(tower.cannon)
            range_list.append(tower.range_spirte)
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            pass
        return
    def _new_tank(self):
        random_x = random.randint(0, 400)
        random_y = random.randint(0, 400)
        if random.randint(-1,1) >= 0:
            random_x = WINDOW_WIDTH-random_x
        if random.randint(-1,1) >= 0:
            random_y = WINDOW_HEIGHT-random_y
        tank = Tank(random_x,random_y,target_sprite=self.castle)
        tank_list.append(tank)
        range_list.append(tank.range_spirte)
        return
    def on_update(self, delta_time):
        global game_over
        if game_over:
            return
        tank_list.update()
        bullet_list.update()
        tower_list.update()
        cur_time = time.time()
        if self.new_tank_time == 0 or cur_time - self.new_tank_time >= self.new_tank_interval:
            self.new_tank_time = cur_time
            self._new_tank()
        if tank_list:
            for tower in tower_list:
                closest_sprite, distance = arcade.get_closest_sprite(tower, tank_list)
                if closest_sprite and distance <= tower.range:
                    tower.aim(closest_sprite)
                else:
                    tower.target = None
        if tower_list:
            for tank in tank_list:
                closest_sprite, distance = arcade.get_closest_sprite(tank, tower_list)
                if closest_sprite and distance <= tank.range:
                    tank.aim(closest_sprite)
                else:
                    tank.reset_aim()
        else:
            for tank in tank_list:
                tank.reset_aim()
        for bullet in bullet_list:
            bullet.check_hit(tank_list)
            bullet.check_hit(tower_list)
            bullet.check_hit(castle_list)
        return
    def on_draw(self):
        global show_range
        self.clear()
        if show_range:
            range_list.draw()
        castle_list.draw()
        tank_list.draw()
        bullet_list.draw()
        tower_list.draw()
        tower_part_list.draw()
        # bullet_list.draw_hit_boxes(arcade.color.RED)
        # tank_list.draw_hit_boxes(arcade.color.RED)
        return

class TankattackWindow(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH,WINDOW_HEIGHT,"Tank Attack")
        return
    def on_key_press(self, key, modifiers):
        global show_range
        if key == arcade.key.ESCAPE or key == arcade.key.Q:
            print("Game Over")
            self.close()
        if key == arcade.key.R:
            show_range = not show_range
            print(f"show range:{show_range}")
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
