import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 600
GRID_SIZE = 4
CELL_SIZE = 100
GAP = 10
PADDING = 20
TOP_OFFSET = 120  # Space for score

# Colors
COLORS = {
    'bg': (187, 173, 160),
    'grid_bg': (205, 193, 180),
    'text_dark': (119, 110, 101),
    'text_light': (249, 246, 242),
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

# Fonts
FONT_LARGE = pygame.font.SysFont("arial", 48, bold=True)
FONT_MEDIUM = pygame.font.SysFont("arial", 36, bold=True)
FONT_SMALL = pygame.font.SysFont("arial", 24, bold=True)

class Game2048:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("2048")
        self.clock = pygame.time.Clock()
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.high_score = self.load_high_score()
        self.game_over = False
        self.won = False
        self.animations = []  # List of active animations
        
        self.spawn_tile()
        self.spawn_tile()

    def load_high_score(self):
        try:
            if os.path.exists("highscore.txt"):
                with open("highscore.txt", "r") as f:
                    return int(f.read())
        except:
            pass
        return 0

    def save_high_score(self):
        with open("highscore.txt", "w") as f:
            f.write(str(self.high_score))

    def spawn_tile(self):
        empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.grid[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.grid[r][c] = 2 if random.random() < 0.9 else 4
            # Add spawn animation
            self.animations.append({'type': 'spawn', 'r': r, 'c': c, 'scale': 0.1, 'speed': 0.1})

    def move(self, direction):
        if self.game_over: return

        rotated_grid = self.grid
        if direction == 'LEFT':
            pass
        elif direction == 'RIGHT':
            rotated_grid = [row[::-1] for row in self.grid]
        elif direction == 'UP':
            rotated_grid = [[self.grid[c][r] for c in range(GRID_SIZE)] for r in range(GRID_SIZE)]
        elif direction == 'DOWN':
            rotated_grid = [[self.grid[c][r] for c in range(GRID_SIZE)] for r in range(GRID_SIZE)]
            rotated_grid = [row[::-1] for row in rotated_grid]

        new_grid, points = self.merge_left(rotated_grid)
        
        # Restore orientation
        if direction == 'LEFT':
            final_grid = new_grid
        elif direction == 'RIGHT':
            final_grid = [row[::-1] for row in new_grid]
        elif direction == 'UP':
            final_grid = [[new_grid[c][r] for c in range(GRID_SIZE)] for r in range(GRID_SIZE)]
        elif direction == 'DOWN':
            final_grid = [row[::-1] for row in new_grid]
            final_grid = [[final_grid[c][r] for c in range(GRID_SIZE)] for r in range(GRID_SIZE)]

        if final_grid != self.grid:
            self.grid = final_grid
            self.score += points
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()
            self.spawn_tile()
            
            if self.check_game_over():
                self.game_over = True

    def merge_left(self, grid):
        new_grid = []
        points = 0
        for row in grid:
            # Remove zeros
            new_row = [x for x in row if x != 0]
            # Merge
            merged_row = []
            skip = False
            for i in range(len(new_row)):
                if skip:
                    skip = False
                    continue
                if i + 1 < len(new_row) and new_row[i] == new_row[i+1]:
                    merged_val = new_row[i] * 2
                    merged_row.append(merged_val)
                    points += merged_val
                    skip = True
                else:
                    merged_row.append(new_row[i])
            # Pad with zeros
            merged_row += [0] * (GRID_SIZE - len(merged_row))
            new_grid.append(merged_row)
        return new_grid, points

    def check_game_over(self):
        # Check for empty cells
        if any(0 in row for row in self.grid):
            return False
        # Check for possible merges
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                val = self.grid[r][c]
                if c + 1 < GRID_SIZE and self.grid[r][c+1] == val:
                    return False
                if r + 1 < GRID_SIZE and self.grid[r+1][c] == val:
                    return False
        return True

    def draw_tile(self, r, c, value, scale=1.0):
        x = PADDING + c * (CELL_SIZE + GAP) + GAP
        y = TOP_OFFSET + r * (CELL_SIZE + GAP) + GAP
        
        # Calculate center for scaling
        center_x = x + CELL_SIZE // 2
        center_y = y + CELL_SIZE // 2
        size = int(CELL_SIZE * scale)
        offset = (CELL_SIZE - size) // 2
        
        rect = pygame.Rect(x + offset, y + offset, size, size)
        color = COLORS.get(value, COLORS[2048])
        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        
        if value > 0:
            text_color = COLORS['text_light'] if value >= 8 else COLORS['text_dark']
            font = FONT_LARGE if value < 100 else (FONT_MEDIUM if value < 1000 else FONT_SMALL)
            text_surf = font.render(str(value), True, text_color)
            text_rect = text_surf.get_rect(center=(center_x, center_y))
            self.screen.blit(text_surf, text_rect)

    def draw(self):
        self.screen.fill(COLORS['bg'])
        
        # Header
        title_surf = FONT_LARGE.render("2048", True, COLORS['text_dark'])
        self.screen.blit(title_surf, (PADDING, 20))
        
        # Scores
        score_bg_rect = pygame.Rect(WIDTH - 220, 20, 90, 60)
        pygame.draw.rect(self.screen, COLORS['grid_bg'], score_bg_rect, border_radius=5)
        score_label = FONT_SMALL.render("SCORE", True, (238, 228, 218))
        score_val = FONT_MEDIUM.render(str(self.score), True, COLORS['text_light'])
        self.screen.blit(score_label, (score_bg_rect.centerx - score_label.get_width()//2, 25))
        self.screen.blit(score_val, (score_bg_rect.centerx - score_val.get_width()//2, 45))
        
        best_bg_rect = pygame.Rect(WIDTH - 110, 20, 90, 60)
        pygame.draw.rect(self.screen, COLORS['grid_bg'], best_bg_rect, border_radius=5)
        best_label = FONT_SMALL.render("BEST", True, (238, 228, 218))
        best_val = FONT_MEDIUM.render(str(self.high_score), True, COLORS['text_light'])
        self.screen.blit(best_label, (best_bg_rect.centerx - best_label.get_width()//2, 25))
        self.screen.blit(best_val, (best_bg_rect.centerx - best_val.get_width()//2, 45))
        
        # Grid Background
        grid_rect = pygame.Rect(PADDING, TOP_OFFSET, WIDTH - 2*PADDING, WIDTH - 2*PADDING)
        pygame.draw.rect(self.screen, COLORS['grid_bg'], grid_rect, border_radius=10)
        
        # Draw Tiles
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                # Draw empty cell background
                x = PADDING + c * (CELL_SIZE + GAP) + GAP
                y = TOP_OFFSET + r * (CELL_SIZE + GAP) + GAP
                pygame.draw.rect(self.screen, COLORS[0], (x, y, CELL_SIZE, CELL_SIZE), border_radius=8)
                
                # Draw tile if exists
                if self.grid[r][c] != 0:
                    # Check for animation
                    scale = 1.0
                    for anim in self.animations[:]:
                        if anim['type'] == 'spawn' and anim['r'] == r and anim['c'] == c:
                            scale = anim['scale']
                            anim['scale'] += anim['speed']
                            if anim['scale'] >= 1.0:
                                self.animations.remove(anim)
                                scale = 1.0
                    self.draw_tile(r, c, self.grid[r][c], scale)

        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((238, 228, 218, 180))
            self.screen.blit(overlay, (0, 0))
            
            msg = FONT_LARGE.render("Game Over!", True, COLORS['text_dark'])
            msg_rect = msg.get_rect(center=(WIDTH//2, HEIGHT//2))
            self.screen.blit(msg, msg_rect)
            
            restart_msg = FONT_SMALL.render("Press SPACE to Restart", True, COLORS['text_dark'])
            restart_rect = restart_msg.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
            self.screen.blit(restart_msg, restart_rect)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if self.game_over:
                        if event.key == pygame.K_SPACE:
                            self.__init__()
                    else:
                        if event.key == pygame.K_LEFT:
                            self.move('LEFT')
                        elif event.key == pygame.K_RIGHT:
                            self.move('RIGHT')
                        elif event.key == pygame.K_UP:
                            self.move('UP')
                        elif event.key == pygame.K_DOWN:
                            self.move('DOWN')
                        elif event.key == pygame.K_ESCAPE:
                            running = False

            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game2048()
    game.run()
