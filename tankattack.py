#! /usr/local/bin/python3

import math
import time
import random
import arcade
from pyglet.math import Vec2 as Vec2

castle_list = arcade.SpriteList()
tank_list = arcade.SpriteList()
bullet_list = arcade.SpriteList()
tower_list = arcade.SpriteList()
tower_part_list = arcade.SpriteList()
range_list = arcade.SpriteList()

NANO_SECOND = 1_000_000_000

NEW_TANK_INTERVAL=5
NEW_TOWER_INTERVAL=1.5
NEW_BOMB_INTERVAL=2.5

STARTING_COIN_VALUE = 500

COIN_FOR_TANK = 80
COIN_FOR_TOWER = 100
COIN_FOR_BOMB = 200

TOWER_SHOOT_INTERVAL=1
TANK_SHOOT_INTERVAL=2

TOWER_HEALTH = 6

WINDOW_WIDTH =1600 
WINDOW_HEIGHT=1000

SELECT_VIEW_WIDTH=100
SELECT_VIEW_HEIGHT=WINDOW_HEIGHT/2
SELECT_VIEW_X, SELECT_VIEW_Y=0, WINDOW_HEIGHT/2
SELECT_BG_COLOR=arcade.color.BLUE_GRAY

ITEM_GAP=10
ITEM_WIDTH=SELECT_VIEW_WIDTH-2*ITEM_GAP
ITEM_HEIGHT=ITEM_WIDTH
ITEM_BG_COLOR=arcade.color.BRASS
ITEM_BG_COLOR_AVAILABLE=arcade.color.CELADON_GREEN
ITEM_HOLD_BG_COLOR=arcade.color.GRAY
ITEM_HOVER_COLOR=arcade.color.WHITE_SMOKE
ITEM_HOVER_FONT=10

SCORE_VIEW_WIDTH=SELECT_VIEW_WIDTH
SCORE_VIEW_HEIGHT=WINDOW_HEIGHT/2
SCORE_VIEW_X, SCORE_VIEW_Y = 0, 0
SCORE_BG_COLOR=arcade.color.BLEU_DE_FRANCE

SCORE_TEXT_X_GAP=8
SCORE_TEXT_Y_GAP=30
SCORE_TEXT_COLOR=arcade.color.YELLOW
SCORE_TEXT_SIZE=12

ATTACK_VIEW_WIDTH=WINDOW_WIDTH-SELECT_VIEW_WIDTH
ATTACK_VIEW_HEIGHT=WINDOW_HEIGHT
ATTACK_BG_COLOR=arcade.color.DARK_GRAY
ATTACK_X, ATTACK_Y=SELECT_VIEW_WIDTH, 0

CASTLE_HEALTH = 20

show_range=False
game_over=False
 
class Brick(arcade.SpriteSolidColor):
    def __init__(self, x, y, width, heigh, angle=0):
        super().__init__(center_x=x, center_y=y, width=width, height=heigh, angle=angle, color=arcade.color.ROSE_EBONY)
        return

class Castle(arcade.Sprite):
    castle_radius = 100
    castle_color = arcade.color.DARK_BLUE
    def __init__(self):
        global window
        super().__init__()
        self._new_radius()
        self.center_x=WINDOW_WIDTH/2
        self.center_y=WINDOW_HEIGHT/2
        self.delta_radius = int(self.castle_radius/window.castle_health)
        self.hit_sound = arcade.sound.load_sound(":resources:/sounds/hurt5.wav")
        return
    def _new_radius(self):
        if self.castle_radius > 0:
            self.texture = arcade.make_circle_texture(self.castle_radius , self.castle_color)
        return
    def hit(self):
        global game_over, window
        window.castle_health -= 1
        self.castle_radius -= self.delta_radius
        self._new_radius()
        arcade.play_sound(self.hit_sound)
        if window.castle_health == 0:
            print("Castle is destroied")
            game_over = True
            self.kill()

class Bullet(arcade.Sprite):
    def __init__(self, x, y, target_x, target_y, speed, distance):
        super().__init__(":resources:images/space_shooter/laserBlue01.png", 0.8)
        r = math.atan2(target_y - y, target_x - x)
        self.center_x = x+distance*math.cos(r)
        self.center_y = y+distance*math.sin(r)
        self.speed = speed
        self.radians = -r
        self.change_x = self.speed * math.cos(r)
        self.change_y = self.speed * math.sin(r)
    def update(self, delta_time: float = 1/60):
        self.center_x += self.change_x
        self.center_y += self.change_y
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
            if not self._can_be_hit(s):
                continue
            s.hit()
            self.kill()
            break
        return
class BulletFromTank(Bullet):
    def __init__(self, x, y, target_x, target_y, speed = 5, distance=0):
        super().__init__(x,y,target_x,target_y, speed, distance)
    def _can_be_hit(self, s:arcade.Sprite):
        return not isinstance(s, Tank)
class BulletFromTower(Bullet):
    def __init__(self, x, y, target_x, target_y, speed = 5, distance=0):
        super().__init__(x,y,target_x,target_y, speed, distance)
    def _can_be_hit(self, s:arcade.Sprite):
        return isinstance(s,Tank)
class Tower(arcade.SpriteCircle):
    target = None
    shoot_time = 0
    base_radius = 10
    health_color = [
        arcade.color.RED,
        arcade.color.RED,
        arcade.color.YELLOW,
        arcade.color.VIOLET_BLUE,
    ]
    def _color_by_health(health):
        if health < len(Tower.health_color):
            return Tower.health_color[health]
        return arcade.color.VIOLET_BLUE
    def __init__(self, x, y, shoot_interval=TOWER_SHOOT_INTERVAL, health=TOWER_HEALTH, range=400):
        self.health = health
        self.range = range
        self.shoot_interval = shoot_interval * NANO_SECOND
        super().__init__(self.base_radius, color=Tower._color_by_health(self.health), center_x=x, center_y=y)
        self.range_spirte = arcade.SpriteCircle(range, color=arcade.color.DARK_YELLOW, center_x=x, center_y=y)
        self.cannon_width, self.cannon_height=self.base_radius*2,self.base_radius/2
        self.cannon = arcade.SpriteSolidColor(color=Tower._color_by_health(self.health), center_x=x+self.cannon_width/2, center_y=y, width=self.cannon_width, height=self.cannon_height)
        self.shoot_sound = arcade.sound.load_sound(":resources:/sounds/hurt2.wav")
        self.explsion_sound = arcade.sound.load_sound(":resources:/sounds/explosion1.wav")
        global window
        window.tower_total += 1
        window.tower_number += 1
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
            arcade.play_sound(self.shoot_sound)
            bullet = BulletFromTower(self.center_x, self.center_y, self.target.center_x, self.target.center_y)
            bullet_list.append(bullet)
        return
    def update(self, delta_time: float = 1/60):
        current_time = time.time_ns()
        if self.target:
            global window
            if self.shoot_time == 0 or current_time - self.shoot_time >= self.shoot_interval:
                self.shoot_time = current_time
                self.shoot()
        return
    def hit(self):
        self.health-=1
        color = Tower._color_by_health(self.health)
        self.color, self.cannon.color = color,color
        if self.health == 0:
            arcade.play_sound(self.explsion_sound)
            self.kill()
        return
    def kill(self):
        global window
        self.cannon.kill()
        self.range_spirte.kill()
        super().kill()
        window.tower_number -= 1
        return

class Tank(arcade.Sprite):
    final_target_sprite=None
    target_sprite = None
    def __init__(self, x, y, speed = 1, health = 3, range=600, shoot_interval=TANK_SHOOT_INTERVAL, target_sprite:arcade.Sprite=None):
        super().__init__()
        super().append_texture(arcade.load_texture("image/tank.blue.png"))
        super().append_texture(arcade.load_texture("image/tank.yellow.png"))
        super().append_texture(arcade.load_texture("image/tank.red.png"))
        super().set_texture(0)
        self.range = range
        self.range_spirte = arcade.SpriteCircle(range, color=arcade.color.DARK_TAN, center_x=x, center_y=y)
        self.center_x, self.center_y = x, y
        self.speed = speed
        self.health = health
        self.shoot_interval = shoot_interval * NANO_SECOND
        self.shoot_time=time.time_ns()
        self.shoot_sound = arcade.sound.load_sound(":resources:sounds/laser1.wav")
        self.explsion_sound = arcade.sound.load_sound(":resources:/sounds/explosion2.wav")
        if target_sprite:
            self.final_target_sprite = target_sprite
            self._set_dest_pos()
        global window
        window.tank_number += 1
        window.tank_total += 1
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
        if s and arcade.get_distance_between_sprites(self, s) <= self.range:
            arcade.play_sound(self.shoot_sound)
            bullet = BulletFromTank(self.center_x, self.center_y, s.center_x, s.center_y)
            bullet_list.append(bullet)
        return
    def update(self, delta_time: float = 1/60):
        current_time = time.time_ns()
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
            arcade.play_sound(self.explsion_sound)
            self.kill()
    def kill(self):
        global window
        self.range_spirte.kill()
        super().kill()
        window.tank_number -= 1
        window.coin += COIN_FOR_TANK

class HoldPath():
    def __init__(self, speed, path:list):
        self._path = path.copy()
        self.speed = speed
        self.cursor = None
        self.passed_path = []
    def _move_to(self, target, distance):
       if distance == 0:
           return self.cursor
       v = target-self.cursor
       random = math.atan2(v.y, v.x)
       self.cursor += Vec2(distance*math.cos(random), distance*math.sin(random))
       return self.cursor
    def move(self, delta_time) -> Vec2:
        if len(self._path) < 1:
            return None
        if not self.cursor:
            self.cursor = self._path.pop(0)
            self.passed_path.append(self.cursor)
        target = self._path[0]
        diff_vec = target - self.cursor
        distance = diff_vec.distance(Vec2(0,0))
        real_speed = self.speed / (1/delta_time)
        # print(f"cursor=Vec2({self.cursor.x:.2f},{self.cursor.y:.2f}), target=Vec2({target.x:.2f},{target.y:.2f}),"
        #       f"diff_vec=Vec2({diff_vec.x:.2f},{diff_vec.y:.2f}), speed={real_speed:.2f}, dist={distance:.2f}")
        if real_speed <= distance:
            return self._move_to(target, real_speed)
        self.cursor = self._path.pop(0)
        self.passed_path.append(self.cursor)
        if not self._path:
            return None
        target = self._path[0]
        # print(f"-------> new cursor=Vec2({self.cursor.x:.2f}, {self.cursor.y:.2f}),",
        #       f"new target: Vec2({target.x:.2f},{target.y:.2f})",
        #       "passed_path=", self.passed_path)
        return self._move_to(target, real_speed-distance)

class Item():
    hold_time = 0
    hold_path = None
    def __init__(self, pos:Vec2):
        self.width = ITEM_WIDTH
        self.height = ITEM_HEIGHT
        self.point_bottom_left = pos
        self.point_top_right = pos+Vec2(self.width, self.height)
        self.point_bottom_right=pos+Vec2(self.width, 0)
        self.point_top_left=pos+Vec2(0, self.height)
        self.point_center = pos+Vec2(self.width/2, self.height/2)
        self.point_top_middle = self.point_top_left + Vec2(self.height/2, 0)
        self.point_center = pos+Vec2(self.width/2, self.height/2)
        self.hold_polygon = None
        self.available = False
        self.hover = {}
        self.hover_gap = 10
        self.hover['name']=arcade.Text("hover", self.point_center.x , self.point_center.y, color=ITEM_HOVER_COLOR, font_size=ITEM_HOVER_FONT, bold=True)
        self.hover['price']=arcade.Text("hover", self.point_center.x , self.point_center.y-self.hover_gap, color=ITEM_HOVER_COLOR, font_size=ITEM_HOVER_FONT, bold=True)
    def _draw_back_ground(self):
        if self.available:
            bg_color = ITEM_BG_COLOR_AVAILABLE
        else:
            bg_color = ITEM_BG_COLOR
        arcade.draw_lbwh_rectangle_filled(self.point_bottom_left.x, self.point_bottom_left.y, self.width, self.height, bg_color)
        if self.hold_polygon:
            arcade.draw_polygon_filled(self.hold_polygon, ITEM_HOLD_BG_COLOR)
    def _start_draw_circle(self):
        if self.hold_path:
            print('holding is running')
            return
        item_length = self.width *2 + self.height *2
        speed = item_length / self.hold_time
        print("start draw circle: item_length=", item_length, "hold_time=", self.hold_time, "spped=", speed)
        l = [self.point_top_middle, self.point_top_right, self.point_bottom_right, self.point_bottom_left, self.point_top_left, self.point_top_middle]
        self.hold_path = HoldPath(speed, l)
        self.cursor = None
    def _is_drawing_circle(self) -> bool:
        return bool(self.hold_path)
    def _draw_circle(self, delta_time):
        if self.hold_time == 0 or not self.hold_path:
            return
        self.hold_polygon = []
        point_move = self.hold_path.move(delta_time)
        if not point_move:
            print('holding is finished')
            self.hold_path = None
            self.hold_polygon = None
            self.available = True
            return
        self.hold_polygon.append(self.point_center)
        for i in self.hold_path.passed_path:
            self.hold_polygon.append(i)
        self.hold_polygon.append(point_move)
        # poly = f'poly(len={len(self.hold_polygon)}):'
        # for i in self.hold_polygon:
        #     poly += f',({i.x:.2f},{i.y:.2f})'
        # print(poly)
    def _can_build(self) -> bool:
        global window
        return window.coin > self.price
    def _build(self):
        global window
        if not self._can_build():
            return
        window.coin -= self.price
        if not self._is_drawing_circle():
            self._start_draw_circle()
    def _mouse_is_in(self, point:Vec2):
        return arcade.geometry.is_point_in_box(self.point_bottom_left, point, self.point_top_right)
    def check_select(self, point:Vec2):
        global window
        if not self._mouse_is_in(point):
            return
        if self.available:
            self.selected()
            window.selected_item = self
            return
        self._build()
    def on_update(self, delta_time):
        self._draw_circle(delta_time)
        return
    def selected(self):
        pass
    def _hover_price_text(self, key) -> str:
        if key == 'name':
            return self.name
        if key == 'price':
            return f"price: {self.price}"
    def _draw_item(self):
        rect = arcade.XYWH(self.point_center.x, self.point_center.y, self.width, self.height)
        arcade.draw_texture_rect(self.textture, rect)
    def _draw_hover(self, pos: Vec2):
        gap = 0
        for key, value in self.hover.items():
            value.text = self._hover_price_text(key)
            value.x = pos.x
            value.y = pos.y + gap
            value.draw()
            gap -= self.hover_gap
    def on_draw(self, vec_mouse:Vec2):
        self._draw_back_ground()
        self._draw_item()
        if vec_mouse and self._mouse_is_in(vec_mouse):
            self._draw_hover(vec_mouse)

class ItemTower(Item):
    def __init__(self, pos:Vec2):
        super().__init__(pos)
        self.name = "Gun Tower"
        self.hold_time = NEW_TOWER_INTERVAL
        self.textture = arcade.load_texture("image/cannon.png")
        self.available = True
        self.price = COIN_FOR_TOWER
    def selected(self):
        print("select tower")

class ItemMegaBomb(Item):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "Mega Bomb"
        self.hold_time = NEW_BOMB_INTERVAL
        self.textture = arcade.load_texture("image/bomb.png")
        self.available = False
        self.price = COIN_FOR_BOMB
    def selected(self):
        print("select bomb")

class SelectSection(arcade.Section):
    item = []
    _config = {
        'top-left' : {
            'view': {'bottom-left': Vec2(SELECT_VIEW_X, SELECT_VIEW_Y), 
                     'width':SELECT_VIEW_WIDTH,
                     'height': SELECT_VIEW_HEIGHT},
            'item': {'start': Vec2(SELECT_VIEW_X+ITEM_GAP, WINDOW_HEIGHT-(ITEM_HEIGHT+ITEM_GAP)), 
                     'delta': Vec2(0, -(ITEM_GAP+ITEM_HEIGHT))},
            'bg_color': SELECT_BG_COLOR,
        },
    }
    def __init__(self, position='top-left'):
        self.position = position
        self.config = SelectSection._config[position]
        self.bottom_left = self.config['view']['bottom-left']
        self.view_width = self.config['view']['width']
        self.view_height = self.config['view']['height']
        self.mouse_x, self.mouse_y = None,None
        super().__init__(left=self.bottom_left.x, bottom=self.bottom_left.y, width=self.view_width, height=self.view_height, name='select', accept_mouse_events=True, accept_keyboard_keys=False)
        item_pos = self.config['item']['start']
        item_delta = self.config['item']['delta']
        self.item.append(ItemTower(item_pos))
        item_pos += item_delta
        self.item.append(ItemMegaBomb(item_pos))
    def on_mouse_enter(self, x: float, y: float):
        global window
        cursor = window.get_system_mouse_cursor(window.CURSOR_HAND)
        window.set_mouse_cursor(cursor)
    def on_mouse_leave(self, x: float, y: float):
        global window
        cursor = window.get_system_mouse_cursor(window.CURSOR_DEFAULT)
        window.set_mouse_cursor(cursor)
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            for i in self.item:
                i.check_select(Vec2(x,y))
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            global window
            window.selected_item = None
        return
    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x, self.mouse_y = x,y
    def on_update(self, delta_time):
        for i in self.item:
            i.on_update(delta_time)
        return
    def on_draw(self):
        arcade.draw_lbwh_rectangle_filled(self.bottom_left.x, self.bottom_left.y, self.view_width, self.view_height, self.config['bg_color'])
        for i in self.item:
            if self.mouse_x and self.mouse_y:
                i.on_draw(Vec2(self.mouse_x, self.mouse_y))
            else:
                i.on_draw(None)

class ScoreSection(arcade.Section):
    _config = {
        'bottom-left' : {
            'view': {'bottom-left': Vec2(SCORE_VIEW_X, SCORE_VIEW_Y), 
                     'width':SCORE_VIEW_WIDTH,
                     'height': SCORE_VIEW_HEIGHT},
            'text': {'start': Vec2(SCORE_VIEW_X+SCORE_TEXT_X_GAP, SCORE_VIEW_HEIGHT-SCORE_TEXT_Y_GAP),
                     'delta': Vec2(0, -(SCORE_TEXT_Y_GAP)),
                     'font-size':SCORE_TEXT_SIZE,
                     'color':SCORE_TEXT_COLOR,
                     'bold': True,
                     },
            'bg_color': SCORE_BG_COLOR,
        },
    }
    def _append_text(list, key, str, pos, text_config):
        list[key]=arcade.Text(str, pos.x , pos.y, color=text_config['color'], font_size=text_config['font-size'], bold=text_config['bold'])
    def __init__(self, position='bottom-left'):
        global window 
        self.position = position
        self.config = ScoreSection._config[position]
        self.bottom_left = self.config['view']['bottom-left']
        self.view_width = self.config['view']['width']
        self.view_height = self.config['view']['height']
        super().__init__(left=self.bottom_left.x, bottom=self.bottom_left.y, width=self.view_width, height=self.view_height, name='score', accept_mouse_events=True, accept_keyboard_keys=False)
        self.text_list = {}
        text_config=self.config['text']
        text_vec = text_config['start']
        ScoreSection._append_text(self.text_list,'castle', f"Castle: {window.castle_health}", text_vec, text_config)
        text_vec += text_config['delta']
        ScoreSection._append_text(self.text_list,'tank', f"Tank  : {window.tank_number}/{window.tank_total}", text_vec, text_config)
        text_vec += text_config['delta']
        ScoreSection._append_text(self.text_list,'tower', f"Tower : {window.tower_number}/{window.tower_total}", text_vec, text_config)
        text_vec += text_config['delta']
        ScoreSection._append_text(self.text_list,'bomb', f"Bomb  : {window.bomb_number}", text_vec, text_config)
        text_vec += text_config['delta']
        ScoreSection._append_text(self.text_list,'coin', f"Coin  : {window.coin}", text_vec, text_config)
    def on_update(self, delta_time):
        self.text_list['castle'].text = f"Castle: {window.castle_health}"
        self.text_list['tank'].text   = f"Tank  : {window.tank_number}/{window.tank_total}"
        self.text_list['tower'].text  = f"Tower : {window.tower_number}/{window.tower_total}"
        self.text_list['bomb'].text   = f"Bomb  : {window.bomb_number}"
        self.text_list['coin'].text   = f"Coin  : {window.coin}"
        return super().on_update(delta_time)
    def on_draw(self):
        arcade.draw_lbwh_rectangle_filled(self.bottom_left.x, self.bottom_left.y, self.view_width, self.view_height, self.config['bg_color'])
        for t in self.text_list.values():
            t.draw()
        pass

class TankattackSection(arcade.Section):
    def __init__(self):
        super().__init__(left=ATTACK_X, bottom=ATTACK_Y, width=ATTACK_VIEW_WIDTH, height=ATTACK_VIEW_HEIGHT, name="attack", accept_mouse_events=True, accept_keyboard_keys=False)
        self.bomb_sound = arcade.sound.load_sound(":resources:/sounds/upgrade4.wav")
        self.mouse_x, self.mouse_y = None, None
        return
    def on_mouse_press(self, x, y, button, modifiers):
        global window
        if button == arcade.MOUSE_BUTTON_LEFT:
            if window.selected_item:
                if isinstance(window.selected_item, ItemTower):
                    tower = Tower(x,y)
                    tower_list.append(tower)
                    tower_part_list.append(tower.cannon)
                    range_list.append(tower.range_spirte)
                elif isinstance(window.selected_item, ItemMegaBomb):
                    for t in tank_list:
                        t.kill()
                    tank_list.clear()
                    range_list.clear()
                    for t in tower_list:
                        t.target = None
                    window.bomb_number += 1
                    arcade.play_sound(self.bomb_sound)
                window.selected_item.available = False
                window.selected_item = None
                window.set_mouse_visible(True)
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            window.selected_item = None
        return
    def on_mouse_enter(self, x: float, y: float):
        global window
        if window.selected_item:
            window.set_mouse_visible(False)
        else:
            window.set_mouse_visible(True)
    def on_mouse_leave(self, x: float, y: float):
        pass
    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x, self.mouse_y = x,y
    def on_draw(self):
        arcade.draw_lbwh_rectangle_filled(ATTACK_X, ATTACK_Y, self.width, self.height, ATTACK_BG_COLOR)
        global show_range, game_over
        if show_range:
            range_list.draw()
        castle_list.draw()
        tank_list.draw()
        bullet_list.draw()
        tower_list.draw()
        tower_part_list.draw()
        if window.selected_item and self.mouse_x is not None and self.mouse_y is not None:
            rect = arcade.XYWH(self.mouse_x, self.mouse_y, 40, 40)
            arcade.draw_texture_rect(window.selected_item.textture, rect)
        if game_over:
            self.view.game_over_text.draw()
        return

class TankattackView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.DARK_GRAY
        self.castle = Castle()
        castle_list.append(self.castle)
        self.new_tank_time = 0
        self.game_over_text = arcade.Text(f"Game Over", (WINDOW_WIDTH/2), WINDOW_HEIGHT/2 + 40, anchor_x="center", anchor_y="center", color=arcade.color.YELLOW, font_size=46, bold=True, italic=True )
        return
    def setup(self):
        self.section_manager=arcade.SectionManager(self)
        self.section_manager.add_section(SelectSection())
        self.section_manager.add_section(ScoreSection())
        self.section_manager.add_section(TankattackSection())
        return
    def _new_tank(self):
        global window
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
    def on_show_view(self) -> None:
        self.section_manager.enable()
        return
    def on_hide_view(self) -> None:
        self.section_manager.disable()
        return
    def on_update(self, delta_time):
        global game_over
        if game_over:
            return
        tank_list.update()
        bullet_list.update()
        tower_list.update()
        cur_time = time.time_ns()
        new_tank_interval_ns = NEW_TANK_INTERVAL * NANO_SECOND
        if self.new_tank_time == 0 or cur_time - self.new_tank_time >= new_tank_interval_ns:
            self.new_tank_time = cur_time
            self._new_tank()
        for tower in tower_list:
            if tank_list:
                closest_sprite, distance = arcade.get_closest_sprite(tower, tank_list)
                if closest_sprite and distance <= tower.range:
                    tower.aim(closest_sprite)
                else:
                    tower.target = None
            else:
                tower.target = None
        for tank in tank_list:
            if tower_list:
                closest_sprite, distance = arcade.get_closest_sprite(tank, tower_list)
                if closest_sprite and distance <= tank.range:
                    tank.aim(closest_sprite)
                else:
                    tank.reset_aim()
            else:
                tank.reset_aim()
        for bullet in bullet_list:
            bullet.check_hit(tank_list)
            bullet.check_hit(tower_list)
            bullet.check_hit(castle_list)
        return
    def on_draw(self):
        # bullet_list.draw_hit_boxes(arcade.color.RED)
        # tank_list.draw_hit_boxes(arcade.color.RED)
        pass

class TankattackWindow(arcade.Window):
    selected_item = None
    tank_number, tank_total = 0, 0
    tower_number, tower_total = 0, 0
    bomb_number = 0
    castle_health = CASTLE_HEALTH
    coin = STARTING_COIN_VALUE
    def __init__(self):
        super().__init__(WINDOW_WIDTH,WINDOW_HEIGHT,"Tank Attack")
        return
    def on_key_press(self, key, modifiers):
        global show_range
        match key:
            case arcade.key.ESCAPE | arcade.key.Q:
                print("Game Over")
                self.close()
            case arcade.key.R:
                show_range = not show_range
                print(f"show range:{show_range}")
    def on_key_release(self, key, modifiers):
        pass

def main():
    print("Game Start")
    global window
    window = TankattackWindow()
    view = TankattackView()
    view.setup()
    window.show_view(view)
    arcade.run()
    return

if __name__ == "__main__":
    main()
