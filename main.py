from microbe import Microbe
from ecosystem import Ecosystem
from config import SCREEN_WIDTH, SCREEN_HEIGHT
import random
import pygame

pygame.init()

simulation_font = pygame.font.SysFont(None, 24)
simulation_font_sm = pygame.font.SysFont(None, 12)
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Window")

microbes = [
    Microbe(id=1,x=SCREEN_WIDTH/2,y=SCREEN_HEIGHT/2,size=1,age=0,energy=400,consumed=False,reproduction_timer=50),
    Microbe(id=2,x=SCREEN_WIDTH/2,y=SCREEN_HEIGHT/2,size=1,age=0,energy=400,consumed=False,reproduction_timer=50),
]

World = Ecosystem(nutrientPool=2000,population=len(microbes))
REPRODUCTION_TIMER = 50

food = []
for _ in range(25):
    food.append([
        random.randint(50, SCREEN_WIDTH-50),
        random.randint(50, SCREEN_HEIGHT-50),
        5,
    ])

detritus = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))

    GROWTH_RATE = 0.001
    AGING_RATE = 0.001

    # DRAW FOOD BLOBS
    for f in food:
        blob_size = int(f[2])
        pygame.draw.circle(screen, (0,0,170), (int(f[0]), int(f[1])), blob_size)

    for mc in microbes:
        # DRAW MICROBES
        mc.draw_microbe(screen,mc)

        #deplete energy of microbe every tick
        mc.energy -= 0.1
        #nutrient pool drain
        if World.nutrientPool > 0:
            #if mc.energy < 400:
            World.nutrientPool -= 0.02
            mc.energy += 0.15
 
        #Displays current population
        population = simulation_font.render(f"Population: {len(microbes)}", True, (0,250,0))

        #growth and age every frame
        if mc.size < 10 and mc.energy > 100:
            mc.size += GROWTH_RATE 

        mc.age += AGING_RATE

        #reproduction
        if len(microbes) < 40 and mc.energy > 100 and mc.reproduction_timer <= 0 and mc.age >= 5:
            new_microbe = Microbe(
                id=len(microbes) + 1,
                x=mc.x + random.uniform(-5,5),
                y=mc.y + random.uniform(-5,5),
                size=1,age=0,
                energy=300,
                consumed=False,
                reproduction_timer=50
            )
            microbes.append(new_microbe)
            #Reset timer for reproduction
            mc.reproduction_timer = 100

        #Fooood
        target=None
        closest_dist=80

        #Finds distance of food using pythagorean theorem 
        for f in food:
            dist = ((mc.x - f[0])**2 + (mc.y - f[1])**2)**0.5    
            if dist < closest_dist:
                closest_dist = dist
                target = f

        if target:
            # direction toward the food blob
            dx = target[0] - mc.x
            dy = target[1] - mc.y
            length = (dx**2 + dy**2)**0.5
            if length > 0:
                #Normalize and scale to speed 
                mc.dx = (dx/length) * 0.2
                mc.dy = (dy/length) * 0.2

        #delete food blob
        for f in food[:]:
            dist = ((mc.x - f[0])**2 + (mc.y - f[1])**2)**0.5 
            if dist < mc.size:
                food.remove(f)
                mc.energy += 50
                #caps size at 20
                if mc.size < 20:
                    mc.size += 1
                food.append([
                        random.randint(50, SCREEN_WIDTH-50),
                        random.randint(50, SCREEN_HEIGHT-50),
                        5,
                    ])
                break
        else:
            #if no food is in range
            mc.wander()
            if random.random() < 0.05:
                mc.dx += random.uniform(-0.005, 0.005)
                mc.dy += random.uniform(-0.005, 0.005)
            
        mc.reproduction_timer -= 0.03
    #-------------------END OF MC LOOP ---------------------#  
        

        
    #death and creation of detritus
    #To be continued
    for mc in microbes:
        if mc.age > 50:
            #detritus.append([mc.x, mc.y,])
            microbes.remove(mc)
            break

        #This boy ain't right 
        #for _ in detritus[:]:
                # if detritus:
                #     pygame.draw.circle(screen, (90, 0, 0), (detritus[0], detritus[1]), mc.size)

# <-----this is while running main loop still

    # KEEPS MICROBES FROM OVERLAPPING 
    Microbe.separate(microbes)

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
