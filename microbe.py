import random
import pygame
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

    def draw_microbe(self,screen, mc):
        base_green = 160 + min(int(mc.age * 3), 80)
        if mc.age < 15:
            aging_green = mc.age * 5
        elif mc.age >= 15:
            aging_green = 99
        color = (40, base_green, 70)
        pygame.draw.circle(screen, (20, 100 - aging_green, 40), (int(mc.x), int(mc.y)), int(mc.size))
        pygame.draw.circle(screen, color, (int(mc.x), int(mc.y)), int(mc.size), 1)

    def separate(microbes):
        for i in range(len(microbes)):
                    for j in range(i + 1, len(microbes)):
                        a = microbes[i]
                        b = microbes[j]
                        dx = b.x - a.x
                        dy = b.y - a.y
                        dist = (dx*dx + dy*dy)**0.5
                        min_dist = a.size + b.size
        
                        if dist < min_dist and dist > 0:
                            overlap = min_dist - dist
                            nx = dx / dist
                            ny = dy / dist
                            push = overlap * 0.25          # softness
                            a.x -= nx * push 
                            a.y -= ny * push
                            b.x += nx * push 
                            b.y += ny * push 
                            a.squish = 0.8                 # temporary visual flag
                            b.squish = 0.8
        