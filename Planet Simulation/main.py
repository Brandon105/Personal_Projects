import pygame
import math
pygame.init()

WIDTH, HEIGTH = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
DARK_GRAY = (80, 78, 81)

VEL_SCALE = 100
ROGUE_MASS = 2 * 10**12

FONT = pygame.font.SysFont("comicsans",  16)

class Planet:
    AU = 149.6e6 * 1000 # au to m
    G = 6.67428e-11
    SCALE = 200 / AU # 1AU = 100 pixels
    TIMESTEP = 3600 * 24 # 1 day

    def __init__ (self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        
        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0
    
    def draw(self, WIN):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGTH / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGTH / 2
                updated_points.append((x, y))

            pygame.draw.lines(WIN, self.color, False, updated_points, 2)
        
        pygame.draw.circle(WIN, self.color, (x, y), self.radius)
        
        #if not self.sun:
            #distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
            #WIN.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))

        

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
    
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

def create_rogue_planet(location, mouse):
    t_x, t_y = location
    m_x, m_y = mouse
    #x_vel = (m_x - t_x) / VEL_SCALE
    #y_vel = (m_y - t_y) / VEL_SCALE
    obj = Planet(t_x, t_y, 3, WHITE, ROGUE_MASS)
    return obj


def main():
    running = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GRAY, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    planets = [sun, earth, mars, mercury, venus]
    
    temp_rogue_pos = None

    while running:
        clock.tick(60)
        WIN.fill((0,0,0))

        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_rogue_pos:
                    t_x, t_y = temp_rogue_pos
                    obj = create_rogue_planet(temp_rogue_pos, mouse_pos)
                    planets.append(obj)
                    temp_rogue_pos = None
                else:
                    temp_rogue_pos = mouse_pos

        #if temp_rogue_pos:
            #pygame.draw.line(WIN, WHITE, temp_rogue_pos, mouse_pos, 2)
            #pygame.draw.circle(WIN, RED, temp_rogue_pos, 3)

        for planet in planets:
            #planet.update_position(planets)
            planet.draw(WIN)
            planet.update_position(planets)
        
        pygame.display.update()

    pygame.quit()

main()