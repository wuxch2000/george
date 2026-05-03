#! /usr/local/bin/python3

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

class TankattackView(arcade.View):
    castle = arcade.SpriteList()
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

        return
    def on_key_press(self, key, modifiers):
        return 
    def on_key_release(self, key, modifiers):
        return
    def on_draw(self):
        self.clear()
        self.castle.draw()
        return
    def on_update(self, delta_time):
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
