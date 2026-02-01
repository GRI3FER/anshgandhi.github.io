import pygame
import random

# --- 1. Settings & Aesthetics ---
WIDTH, HEIGHT = 800, 900
FPS = 60
LANE_HEIGHT = 80 
VIEW_OFFSET = 30 # For 3D depth effect

# Voxel-ish Palette
GRASS_BASE, GRASS_TOP = (45, 160, 70), (58, 185, 84)
ROAD_BASE, ROAD_LINE = (35, 35, 40), (70, 70, 80)
WATER_BASE, WATER_TOP = (30, 100, 200), (50, 150, 255)
LOG_BASE, LOG_TOP = (80, 40, 20), (120, 70, 40)
CHICKEN_BODY, CHICKEN_RED = (255, 255, 255), (220, 30, 30)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crossy Road 2.5D - Advanced Collisions")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 24, bold=True)

# --- 2. 2.5D Sprite Generator ---
def get_chicken_sprite():
    surf = pygame.Surface((50, 60), pygame.SRCALPHA)
    pygame.draw.rect(surf, (200, 200, 200), (5, 15, 40, 40), border_radius=8)
    pygame.draw.rect(surf, CHICKEN_BODY, (5, 5, 40, 35), border_radius=8)
    pygame.draw.rect(surf, CHICKEN_RED, (20, 0, 10, 10), border_radius=2)
    pygame.draw.polygon(surf, (255, 165, 0), [(45, 15), (55, 22), (45, 30)])
    return surf

def get_car_sprite(color):
    surf = pygame.Surface((110, 70), pygame.SRCALPHA)
    dark_color = [max(0, c - 40) for c in color]
    pygame.draw.rect(surf, dark_color, (5, 15, 100, 50), border_radius=12)
    pygame.draw.rect(surf, color, (5, 5, 100, 45), border_radius=12)
    pygame.draw.rect(surf, color, (30, 10, 50, 25), border_radius=5)
    pygame.draw.rect(surf, (200, 230, 255), (35, 12, 40, 12), border_radius=2)
    return surf

def get_log_sprite():
    surf = pygame.Surface((180, 60), pygame.SRCALPHA)
    pygame.draw.rect(surf, LOG_BASE, (0, 10, 180, 50), border_radius=20)
    pygame.draw.rect(surf, LOG_TOP, (0, 0, 180, 45), border_radius=20)
    return surf

# Pre-bake assets
ASSETS = {
    "chicken": get_chicken_sprite(),
    "car": get_car_sprite((220, 50, 50)),
    "log": get_log_sprite()
}

class Lane:
    def __init__(self, index, type, score):
        self.index = index
        self.type = type
        self.objects = []
        self.speed = random.choice([-4, -3, 3, 4]) * (1 + score/500)
        curr_x = random.randint(0, WIDTH)
        for _ in range(3):
            self.spawn_obj(curr_x)
            curr_x += 300 + random.randint(50, 150)

    def spawn_obj(self, x=None):
        if x is None: x = -200 if self.speed > 0 else WIDTH + 50
        if self.type == "road": self.objects.append(pygame.Rect(x, 0, 90, 50))
        elif self.type == "water": self.objects.append(pygame.Rect(x, 0, 170, 55))

    def update(self):
        for obj in self.objects:
            obj.x += self.speed
        if len(self.objects) < 4 and random.random() < 0.01: self.spawn_obj()
        self.objects = [o for o in self.objects if -500 < o.x < WIDTH + 500]

def reset_game():
    lanes = {i: Lane(i, random.choice(["grass", "road", "water"]) if i < 10 else "grass", 0) for i in range(-50, 15)}
    return {
        "p_world": [WIDTH//2, 12],
        "lanes": lanes,
        "score": 0, "max_y": 12, "high": state["high"] if 'state' in globals() else 0,
        "over": False, "cam_y": 12 * LANE_HEIGHT - 500
    }

state = {"high": 0}
state = reset_game()

# --- 3. Main Loop ---
running = True
while running:
    screen.fill((100, 150, 100))
    state["cam_y"] += ((state["p_world"][1] * LANE_HEIGHT - 500) - state["cam_y"]) * 0.1

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN and not state["over"]:
            # WASD Controls Only
            if event.key == pygame.K_w:  # Up
                state["p_world"][1] -= 1
                if state["p_world"][1] < state["max_y"]:
                    state["max_y"], state["score"] = state["p_world"][1], state["score"] + 1
            if event.key == pygame.K_s:  # Down
                if state["p_world"][1] < state["max_y"] + 5:
                    state["p_world"][1] += 1
            if event.key == pygame.K_a:  # Left
                state["p_world"][0] -= 60
            if event.key == pygame.K_d:  # Right
                state["p_world"][0] += 60
        elif event.type == pygame.KEYDOWN and state["over"] and event.key == pygame.K_SPACE:
            state = reset_game()

    if not state["over"]:
        on_log, in_water = False, False
        visible_range = range(int(state["cam_y"]//LANE_HEIGHT) - 2, int(state["cam_y"]//LANE_HEIGHT) + 14)
        for i in sorted(state["lanes"].keys(), reverse=True):
            if i not in visible_range: continue
            
            l = state["lanes"][i]
            l.update()
            draw_y = (l.index * LANE_HEIGHT) - state["cam_y"]
            lane_rect = pygame.Rect(0, draw_y, WIDTH, LANE_HEIGHT)
            if l.type == "grass":
                pygame.draw.rect(screen, GRASS_BASE, (0, draw_y+5, WIDTH, LANE_HEIGHT))
                pygame.draw.rect(screen, GRASS_TOP, (0, draw_y, WIDTH, LANE_HEIGHT-5))
            elif l.type == "road":
                pygame.draw.rect(screen, ROAD_BASE, lane_rect)
                pygame.draw.rect(screen, ROAD_LINE, (0, draw_y + LANE_HEIGHT//2, WIDTH, 2))
            elif l.type == "water":
                pygame.draw.rect(screen, WATER_BASE, (0, draw_y+5, WIDTH, LANE_HEIGHT))
                pygame.draw.rect(screen, WATER_TOP, (0, draw_y, WIDTH, LANE_HEIGHT-5))

            player_hitbox = pygame.Rect(state["p_world"][0]+10, state["p_world"][1]*LANE_HEIGHT+20, 30, 30)
            for obj in l.objects:
                obj_world_rect = pygame.Rect(obj.x, l.index * LANE_HEIGHT, obj.width, obj.height)
                obj_draw_y = draw_y + (LANE_HEIGHT - obj.height)//2
                if l.type == "road":
                    screen.blit(ASSETS["car"], (obj.x, obj_draw_y - 10))
                    if player_hitbox.colliderect(obj_world_rect): state["over"] = True
                elif l.type == "water":
                    screen.blit(ASSETS["log"], (obj.x, obj_draw_y - 10))
                    if player_hitbox.colliderect(obj_world_rect):
                        on_log = True
                        state["p_world"][0] += l.speed
            if l.index == state["p_world"][1] and l.type == "water": in_water = True

        px = state["p_world"][0]
        py = (state["p_world"][1] * LANE_HEIGHT) - state["cam_y"]
        screen.blit(ASSETS["chicken"], (px, py))

        if (in_water and not on_log) or px < -20 or px > WIDTH - 20: state["over"] = True
        if state["score"] > state["high"]: state["high"] = state["score"]

        screen.blit(font.render(f"SCORE: {state['score']}", True, (255,255,255)), (20, 20))
        screen.blit(font.render(f"HIGH: {state['high']}", True, (255, 200, 0)), (20, 50))
    else:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0,0,0,150))
        screen.blit(overlay, (0,0))
        screen.blit(font.render("GAME OVER - SPACE TO RESTART", True, (255,255,255)), (WIDTH//2-180, HEIGHT//2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
