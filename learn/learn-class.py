#! /usr/local/bin/python3

import arcade

def add(x,y):
    return x+y+10

class Dog():
    def __init__(self, dog_name, skin_color, dog_speed):
        self.name=dog_name
        self.color=skin_color
        self.speed = dog_speed
        return
    def bark(self):
        print('my name is ', self.name, 'my color is', self.color, 'my speed is', self.speed)
        return
    def eat(self, food):
        self.speed = self.speed + food

class DanesDog(Dog):
    def __init__(self, dog_name):
        super(dog_name, 'brown', 30)
        return
    def bark(self):
        print('hei hei hei, I can''t bark ')
        return


def main():
    i = 10
    if i == 10:
        print (0)
    j = 20
    a = add(i, j)

    dog_pack = []
    k = "abc"
    kally = Dog('kally', 'white', 20)
    dog_pack.append(kally)
    illi = Dog('BrEEEEEndon', 'black', 10)
    dog_pack.append(illi)
    brendon = DanesDog('brendon')
    dog_pack.append(brendon)

    illi.eat(30)
    kally.eat(10)

    for dog in dog_pack:
        dog.bark()

    return

if __name__ == "__main__":
    main()




