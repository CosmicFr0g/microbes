import pygame
import random

pygame.init()

SCREEN_WIDTH = 840
SCREEN_HEIGHT = 680
simulation_font = pygame.font.SysFont(None, 24)
simulation_font_sm = pygame.font.SysFont(None, 12)
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Window")

class Ecosystem:
    def __init__(self, nutrientPool, population):
        self.nutrientPool = nutrientPool
        self.population = population

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
            mc.dx += random.uniform(-0.005, 0.005)
            mc.dy += random.uniform(-0.005, 0.005)
            # keep speed roughly constant
            speed = (mc.dx**2 + mc.dy**2)**0.5
            if speed > 0.45:
                mc.dx = (mc.dx / speed) * 0.35
                mc.dy = (mc.dy / speed) * 0.35
            elif speed < 0.05:
                mc.dx = random.uniform(-0.2, 0.2)
                mc.dy = random.uniform(-0.2, 0.2)
        # if random.random() < 0.02:
        #     self.dx = random.uniform(-0.2, 0.2)
        #     self.dy = random.uniform(-0.2, 0.2)
            
        if self.x < self.size or self.x > SCREEN_WIDTH - self.size:
            self.dx *= -1
        if self.y < self.size or self.y > SCREEN_HEIGHT - self.size:
            self.dy *= -1


microbes = [
    Microbe(id=1,x=SCREEN_WIDTH/2,y=SCREEN_HEIGHT/2,size=1,age=0,energy=100,consumed=False,reproduction_timer=50),
    Microbe(id=2,x=SCREEN_WIDTH/2,y=SCREEN_HEIGHT/2,size=1,age=0,energy=100,consumed=False,reproduction_timer=50),
]

World = Ecosystem(nutrientPool=10000,population=len(microbes))
REPRODUCTION_TIMER = 50

#FOOD BLOBS! - Range is amount of blobs
#Creates a random location for each
food = []
for _ in range(15):
    food.append([
        random.randint(50, SCREEN_WIDTH-50),
        random.randint(50, SCREEN_HEIGHT-50),
    ])


# MAIN LOOP
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))

    GROWTH_RATE = 0.001
    AGING_RATE = 0.001

    #Draws the food blob
    for f in food:
        pygame.draw.circle(screen, (180,140,60), (int(f[0]), int(f[1])), 4)

    #This is generally for every microbe in microbes
    
    hungry = False

    for mc in microbes:
        mc.wander()
        # inside the draw section for each microbe
        base_green = 160 + min(int(mc.age * 3), 80)
        color = (40, base_green, 70)
        pygame.draw.circle(screen, color, (int(mc.x), int(mc.y)), int(mc.size))
        # soft highlight
        pygame.draw.circle(screen, (180, 255, 180), (int(mc.x - mc.size*0.3), int(mc.y - mc.size*0.3)), max(1, int(mc.size*0.25)))
        # thin outline
        pygame.draw.circle(screen, (20, 100, 40), (int(mc.x), int(mc.y)), int(mc.size), 1)
    

        mc.energy -= 0.1
        #nutrient pool drain
        if World.nutrientPool > 0:
            if mc.energy < 400:
                World.nutrientPool -= 0.02
                mc.energy += 0.15
 
        #Displays current population
        population = simulation_font.render(f"Population: {len(microbes)}", True, (0,250,0))

        #growth and age every frame
        if mc.size < 12 and mc.energy > 100:
            mc.size += GROWTH_RATE

        mc.age += AGING_RATE

        #reproduction
        if len(microbes) < 40 and mc.energy > 100 and mc.reproduction_timer <= 0 and mc.age >= 5:
            new_microbe = Microbe(
                id=len(microbes) + 1,
                x=mc.x + random.uniform(-5,5),
                y=mc.y + random.uniform(-5,5),
                size=1,age=0,
                energy=100,
                consumed=False,
                reproduction_timer=50
            )
            microbes.append(new_microbe)

            mc.reproduction_timer = 100

        mc.reproduction_timer -= 0.03
    #Removes dead microbes from living list
    microbes = [mc for mc in microbes if mc.energy > 0]



    #Displays nutrient pool
    nutrient_text = simulation_font.render(f"Nutrients: {World.nutrientPool:.2f}", True, (0,250,0))
    screen.blit(nutrient_text, (10,10))

    screen.blit(population, (10, 35))

    #Displays HUD for info on each microbe
    ypos = 60
    for mc in microbes:
        microbe_text = simulation_font_sm.render(f"Microbe #{mc.id} energy: {mc.energy:.2f} age: {mc.age:.2f}", True, (0,250,0))
        #screen.blit(microbe_text, (10,ypos))
        ypos += 16

    # Update the display
    pygame.display.flip()






pygame.quit()