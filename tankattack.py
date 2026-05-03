#! /usr/local/bin/python3

import arcade

class TankattackWindow(arcade.Window):
    def __init__(self):
        super().__init__(500,500,"Tank Attack")
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE
        return
    
class TankattackView(arcade.View):
    def __init__(self):
        super().__init__()
        return
    def on_draw():
        super.on_draw()
        return

def main():
    print("Game Start")
    window = TankattackWindow()
    arcade.run()
    return

if __name__ == "__main__":
    main()
