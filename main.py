import pygame
import random
import sys

# --- Initialization ---
pygame.init()
# Use a flexible resolution for mobile screens
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 800 
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Fonts - Using default font for compatibility
font_score = pygame.font.SysFont(None, 32)
font_big = pygame.font.SysFont(None, 80)
font_upg = pygame.font.SysFont(None, 24)

# Replaced PyAutoGUI with a generated texture for mobile
def get_ui_slice(w, h):
    s = pygame.Surface((w, h))
    s.fill((random.randint(50, 150), random.randint(50, 150), 255))
    pygame.draw.rect(s, (255, 255, 255), (0, 0, w, h), 2)
    return s

class Particle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, random.randint(4, 8), random.randint(4, 8))
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-5, -1)
        self.life = 255
        self.color = (100, 200, 255)

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.vy += 0.2
        self.life -= 10
        return self.life > 0

class Platform:
    def __init__(self, x, y, width=None, is_milestone=False):
        self.is_milestone = is_milestone
        self.width = width if width else random.randint(min_p_width, max_p_width)
        self.height = 40 if is_milestone else 25
        self.img = pygame.transform.scale(get_ui_slice(100, 20), (self.width, self.height))
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.pulse_val = 0
        self.upgrades = []
        if is_milestone:
            spacing = SCREEN_WIDTH // 4
            self.upgrades = [
                {"name": "JUMP+", "type": "jump", "pos": [spacing * 1, y - 60], "color": (0, 255, 150)},
                {"name": "SIZE+", "type": "size", "pos": [spacing * 2, y - 60], "color": (200, 100, 255)},
                {"name": "LIFE+", "type": "life", "pos": [spacing * 3, y - 60], "color": (255, 100, 100)}
            ]

def reset_game():
    global platforms, player_rect, vel_y, score, next_milestone, milestone_gap, resting, game_over, lives, jump_power, min_p_width, max_p_width, particles, shake_intensity
    player_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
    vel_y, score, shake_intensity = 0, 0, 0
    next_milestone, milestone_gap = 1000, 1000 
    resting, game_over = False, False
    lives, jump_power = 3, -15
    min_p_width, max_p_width = 80, 180
    particles = []
    platforms = []
    cy = SCREEN_HEIGHT - 50
    for _ in range(10):
        cy -= random.randint(150, 200)
        platforms.append(Platform(random.randint(0, SCREEN_WIDTH-150), cy))
    platforms.append(Platform(0, SCREEN_HEIGHT - 40, width=SCREEN_WIDTH))

# Global Setup
player_base_img = get_ui_slice(50, 50)
player_rect = player_base_img.get_rect()
min_p_width, max_p_width = 80, 180
gravity = 0.6
clock = pygame.time.Clock()
particles = []
shake_intensity = 0

reset_game()

# --- Main Loop ---
while True:
    display.fill((10, 10, 18))
    
    render_offset = [0, 0]
    if shake_intensity > 0:
        render_offset = [random.randint(-5, 5), random.randint(-5, 5)]
        shake_intensity -= 1

    # MOBILE TOUCH INPUT HANDLING
    mouse_pos = pygame.mouse.get_pos()
    mouse_down = pygame.mouse.get_pressed()[0]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                reset_game()
            elif resting:
                # Upgrade Selection logic for Touch
                handled = False
                for p in platforms:
                    if p.is_milestone and p.upgrades:
                        for upg in p.upgrades:
                            btn = pygame.Rect(upg["pos"][0]-50, upg["pos"][1]-20, 100, 60)
                            if btn.collidepoint(event.pos):
                                if upg["name"] == "JUMP+": jump_power -= 2
                                if upg["name"] == "SIZE+": min_p_width += 30; max_p_width += 40
                                if upg["name"] == "LIFE+": lives += 1
                                p.upgrades = []; resting = False; vel_y = jump_power
                                milestone_gap += 500
                                next_milestone = score + milestone_gap
                                handled = True; break
                if not handled and event.pos[1] < SCREEN_HEIGHT // 2:
                    resting = False; vel_y = jump_power

    if not game_over:
        # Side-to-Side movement via screen halves
        if mouse_down:
            if mouse_pos[0] < SCREEN_WIDTH // 2: player_rect.x -= 10
            else: player_rect.x += 10

        if player_rect.left > SCREEN_WIDTH: player_rect.right = 0
        if player_rect.right < 0: player_rect.left = SCREEN_WIDTH

        if not resting:
            vel_y += gravity
            player_rect.y += vel_y
        else:
            vel_y = 0

        # Collision
        for p in platforms:
            if p.is_milestone and p.upgrades:
                if player_rect.colliderect(p.rect):
                    player_rect.bottom = p.rect.top
                    resting = True; break
            elif vel_y >= 0:
                if player_rect.colliderect(p.rect) and player_rect.bottom < p.rect.bottom + 20:
                    player_rect.bottom = p.rect.top
                    p.pulse_val = 10; shake_intensity = 5
                    for _ in range(5): particles.append(Particle(player_rect.centerx, player_rect.bottom))
                    vel_y = jump_power; break

        # Scrolling
        if player_rect.top <= 400:
            diff = 400 - player_rect.top
            player_rect.top = 400
            score += int(diff // 2)
            for p in platforms: 
                p.rect.y += diff
                for upg in p.upgrades: upg["pos"][1] += diff
            
            if score >= next_milestone:
                if not any(p.is_milestone and p.upgrades for p in platforms):
                    platforms.append(Platform(0, -50, width=SCREEN_WIDTH, is_milestone=True))

            platforms = [p for p in platforms if p.rect.top < SCREEN_HEIGHT + 100]
            while len(platforms) < 10:
                hy = min(p.rect.top for p in platforms)
                platforms.append(Platform(random.randint(0, SCREEN_WIDTH-120), hy - random.randint(160, 220)))

        if player_rect.top > SCREEN_HEIGHT:
            lives -= 1
            if lives <= 0: game_over = True
            else:
                platforms.sort(key=lambda p: p.rect.y, reverse=True)
                player_rect.midbottom = platforms[0].rect.midtop
                vel_y = jump_power

    # --- Draw ---
    for pt in particles[:]:
        if not pt.update(): particles.remove(pt)
        pygame.draw.rect(display, pt.color, (pt.rect.x + render_offset[0], pt.rect.y + render_offset[1], pt.rect.w, pt.rect.h))

    for p in platforms:
        display.blit(p.img, (p.rect.x + render_offset[0], p.rect.y + render_offset[1]))
        if p.is_milestone:
            for upg in p.upgrades:
                btn = pygame.Rect(upg["pos"][0]-50, upg["pos"][1]-20, 100, 60)
                pygame.draw.rect(display, upg["color"], btn, 0, 10)
                txt = font_upg.render(upg["name"], True, (255, 255, 255))
                display.blit(txt, (btn.centerx - txt.get_width()//2, btn.centery - txt.get_height()//2))

    # Player
    pygame.draw.rect(display, (0, 255, 255), (player_rect.x + render_offset[0], player_rect.y + render_offset[1], player_rect.w, player_rect.h))

    # UI
    ui_text = font_score.render(f"Alt: {score}m | Lives: {lives}", True, (255, 255, 255))
    display.blit(ui_text, (20, 20))
    
    if resting:
        h = font_upg.render("TAP UPGRADE OR TAP TOP TO JUMP", True, (0, 255, 255))
        display.blit(h, (SCREEN_WIDTH//2 - h.get_width()//2, SCREEN_HEIGHT - 100))

    if game_over:
        msg = font_big.render("GAME OVER", True, (255, 50, 50))
        display.blit(msg, msg.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))

    pygame.display.flip()
    clock.tick(60)
