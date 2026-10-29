# Microbe Ecosystem Simulation

A simple interactive simulation of microbes moving, bouncing, and living in a shared space. Built with Pygame as a hands-on way to practice object-oriented structure, basic physics, and iterative feature building.

## What it does

Microbes wander with random velocity, occasionally change direction, and bounce off the edges of the window. Each microbe is its own object with position, size, age, and velocity. The simulation runs continuously until you close the window.

Current features:
- Multiple microbes moving independently
- Random-walk movement with occasional direction changes
- Edge collision that reverses velocity
- Basic class structure for easy expansion

Planned next steps (not yet implemented):
- Energy drain and a shared nutrient pool
- Eating, growth, and death
- Detritus left behind when microbes die
- Soft separation so microbes can push past each other

## How to run

Requires Python 3 and Pygame.

```bash
pip install pygame-ce
python3 main.py