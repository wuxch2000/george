#! /usr/local/bin/python3

import arcade

class TankattackWindow(arcade.Window):
    def __init__(self):
        super().__init__(500,500,"Tank Attack")
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE
        return
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE or key == arcade.key.Q:
            print("Game Over")
            self.close()
        return 
    def on_key_release(self, key, modifiers):
        return

class TankattackView(arcade.View):
    def __init__(self):
        super().__init__()
        return
    def on_key_press(self, key, modifiers):
        return 
    def on_key_release(self, key, modifiers):
        return
    def on_draw(self):
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
