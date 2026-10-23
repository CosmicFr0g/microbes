import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Microbe:
    #constructor to intialize attributes
    def __init__(self,id, x, y, size, age, energy, consumed,reproduction_timer):
        self.id = id
        self.x = x
        self.y = y
        self.size = size
        self.age = age
        self.consumed = consumed
        self.energy = energy
        self.reproduction_timer = reproduction_timer
        self.dx = random.uniform(-0.2, 0.2)
        self.dy = random.uniform(-0.2, 0.2)

    def wander(self):
        self.x += self.dx
        self.y += self.dy

        if random.random() < 0.05:
            self.dx += random.uniform(-0.005, 0.005)
            self.dy += random.uniform(-0.005, 0.005)
            # keep speed roughly constant
            speed = (self.dx**2 + self.dy**2)**0.5
            if speed > 0.45:
                self.dx = (self.dx / speed) * 0.35
                self.dy = (self.dy / speed) * 0.35
            elif speed < 0.05:
                self.dx = random.uniform(-0.2, 0.2)
                self.dy = random.uniform(-0.2, 0.2)
        # if random.random() < 0.02:
        #     self.dx = random.uniform(-0.2, 0.2)
        #     self.dy = random.uniform(-0.2, 0.2)
            
        if self.x < self.size or self.x > SCREEN_WIDTH - self.size:
            self.dx *= -1
        if self.y < self.size or self.y > SCREEN_HEIGHT - self.size:
            self.dy *= -1
