import pygame
import random
import sys
from enum import Enum
from collections import deque

# Initialize Pygame
pygame.init()

# Color Palette - Modern and Vibrant
class Colors:
    BACKGROUND = (15, 23, 42)  # Dark blue-gray
    GRID_LINE = (30, 41, 59)  # Slightly lighter for grid
    SNAKE_HEAD = (34, 211, 238)  # Cyan
    SNAKE_BODY_START = (6, 182, 212)  # Lighter cyan
    SNAKE_BODY_END = (14, 165, 233)  # Blue
    FOOD = (251, 146, 60)  # Orange
    FOOD_GLOW = (249, 115, 22)  # Darker orange for glow
    TEXT_PRIMARY = (248, 250, 252)  # Almost white
    TEXT_SECONDARY = (148, 163, 184)  # Gray
    SCORE_BG = (30, 41, 59, 180)  # Semi-transparent
    GAME_OVER_BG = (15, 23, 42, 230)  # Semi-transparent overlay
    BUTTON_BG = (34, 211, 238)  # Cyan
    BUTTON_HOVER = (6, 182, 212)  # Darker cyan
    BUTTON_TEXT = (15, 23, 42)  # Dark

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class SnakeGame:
    def __init__(self):
        # Game settings
        self.GRID_SIZE = 25
        self.CELL_SIZE = 30
        self.WINDOW_WIDTH = self.GRID_SIZE * self.CELL_SIZE
        self.WINDOW_HEIGHT = self.GRID_SIZE * self.CELL_SIZE + 100  # Extra space for header
        self.FPS = 12
        
        # Create window
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("🐍 Snake Game")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        self.font_tiny = pygame.font.Font(None, 24)
        
        # Game state
        self.reset_game()
        
    def reset_game(self):
        """Reset game to initial state"""
        # Snake starts in the middle
        start_x = self.GRID_SIZE // 2
        start_y = self.GRID_SIZE // 2
        self.snake = deque([(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)])
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        self.high_score = getattr(self, 'high_score', 0)
        
    def spawn_food(self):
        """Spawn food at random location not occupied by snake"""
        while True:
            food = (random.randint(0, self.GRID_SIZE - 1), 
                   random.randint(0, self.GRID_SIZE - 1))
            if food not in self.snake:
                return food
    
    def handle_events(self):
        """Handle keyboard and window events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.reset_game()
                else:
                    # Prevent 180-degree turns
                    if event.key == pygame.K_UP and self.direction != Direction.DOWN:
                        self.next_direction = Direction.UP
                    elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                        self.next_direction = Direction.DOWN
                    elif event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                        self.next_direction = Direction.LEFT
                    elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                        self.next_direction = Direction.RIGHT
                    elif event.key == pygame.K_ESCAPE:
                        return False
        
        return True
    
    def update(self):
        """Update game state"""
        if self.game_over:
            return
        
        # Update direction
        self.direction = self.next_direction
        
        # Calculate new head position
        head_x, head_y = self.snake[0]
        dx, dy = self.direction.value
        new_head = ((head_x + dx) % self.GRID_SIZE, (head_y + dy) % self.GRID_SIZE)
        
        # Check collision with self
        if new_head in self.snake:
            self.game_over = True
            self.high_score = max(self.high_score, self.score)
            return
        
        # Add new head
        self.snake.appendleft(new_head)
        
        # Check if food eaten
        if new_head == self.food:
            self.score += 10
            self.food = self.spawn_food()
            # Speed up slightly as score increases
            self.FPS = min(20, 12 + self.score // 50)
        else:
            # Remove tail if no food eaten
            self.snake.pop()
    
    def draw_grid(self):
        """Draw subtle grid lines"""
        for x in range(0, self.WINDOW_WIDTH, self.CELL_SIZE):
            pygame.draw.line(self.screen, Colors.GRID_LINE, 
                           (x, 100), (x, self.WINDOW_HEIGHT), 1)
        for y in range(100, self.WINDOW_HEIGHT, self.CELL_SIZE):
            pygame.draw.line(self.screen, Colors.GRID_LINE, 
                           (0, y), (self.WINDOW_WIDTH, y), 1)
    
    def draw_snake(self):
        """Draw snake with gradient effect"""
        for i, (x, y) in enumerate(self.snake):
            # Calculate color gradient from head to tail
            if i == 0:
                color = Colors.SNAKE_HEAD
                # Draw head with glow effect
                rect = pygame.Rect(x * self.CELL_SIZE, y * self.CELL_SIZE + 100, 
                                 self.CELL_SIZE, self.CELL_SIZE)
                pygame.draw.rect(self.screen, color, rect, border_radius=8)
                # Add eyes
                eye_size = 4
                eye_offset = 8
                if self.direction == Direction.RIGHT:
                    pygame.draw.circle(self.screen, Colors.BACKGROUND, 
                                     (rect.centerx + eye_offset, rect.centery - 5), eye_size)
                    pygame.draw.circle(self.screen, Colors.BACKGROUND, 
                                     (rect.centerx + eye_offset, rect.centery + 5), eye_size)
                elif self.direction == Direction.LEFT:
                    pygame.draw.circle(self.screen, Colors.BACKGROUND, 
                                     (rect.centerx - eye_offset, rect.centery - 5), eye_size)
                    pygame.draw.circle(self.screen, Colors.BACKGROUND, 
                                     (rect.centerx - eye_offset, rect.centery + 5), eye_size)
                elif self.direction == Direction.UP:
                    pygame.draw.circle(self.screen, Colors.BACKGROUND, 
                                     (rect.centerx - 5, rect.centery - eye_offset), eye_size)
                    pygame.draw.circle(self.screen, Colors.BACKGROUND, 
                                     (rect.centerx + 5, rect.centery - eye_offset), eye_size)
                else:  # DOWN
                    pygame.draw.circle(self.screen, Colors.BACKGROUND, 
                                     (rect.centerx - 5, rect.centery + eye_offset), eye_size)
                    pygame.draw.circle(self.screen, Colors.BACKGROUND, 
                                     (rect.centerx + 5, rect.centery + eye_offset), eye_size)
            else:
                # Gradient from light to dark
                ratio = i / len(self.snake)
                r = int(Colors.SNAKE_BODY_START[0] + (Colors.SNAKE_BODY_END[0] - Colors.SNAKE_BODY_START[0]) * ratio)
                g = int(Colors.SNAKE_BODY_START[1] + (Colors.SNAKE_BODY_END[1] - Colors.SNAKE_BODY_START[1]) * ratio)
                b = int(Colors.SNAKE_BODY_START[2] + (Colors.SNAKE_BODY_END[2] - Colors.SNAKE_BODY_START[2]) * ratio)
                color = (r, g, b)
                
                rect = pygame.Rect(x * self.CELL_SIZE + 2, y * self.CELL_SIZE + 102, 
                                 self.CELL_SIZE - 4, self.CELL_SIZE - 4)
                pygame.draw.rect(self.screen, color, rect, border_radius=6)
    
    def draw_food(self):
        """Draw food with glow effect"""
        x, y = self.food
        center_x = x * self.CELL_SIZE + self.CELL_SIZE // 2
        center_y = y * self.CELL_SIZE + 100 + self.CELL_SIZE // 2
        
        # Outer glow
        pygame.draw.circle(self.screen, Colors.FOOD_GLOW, (center_x, center_y), 
                         self.CELL_SIZE // 2 + 2)
        # Inner circle
        pygame.draw.circle(self.screen, Colors.FOOD, (center_x, center_y), 
                         self.CELL_SIZE // 2 - 2)
        # Highlight
        pygame.draw.circle(self.screen, (255, 200, 150), 
                         (center_x - 4, center_y - 4), 4)
    
    def draw_header(self):
        """Draw header with score and controls"""
        # Header background
        header_rect = pygame.Rect(0, 0, self.WINDOW_WIDTH, 100)
        pygame.draw.rect(self.screen, Colors.BACKGROUND, header_rect)
        
        # Score panel
        score_text = self.font_medium.render(f"Score: {self.score}", True, Colors.TEXT_PRIMARY)
        self.screen.blit(score_text, (20, 25))
        
        # High score
        high_score_text = self.font_small.render(f"Best: {self.high_score}", True, Colors.TEXT_SECONDARY)
        self.screen.blit(high_score_text, (20, 65))
        
        # Controls hint
        controls_text = self.font_tiny.render("Arrow Keys to Move • ESC to Quit", True, Colors.TEXT_SECONDARY)
        controls_rect = controls_text.get_rect(right=self.WINDOW_WIDTH - 20, centery=50)
        self.screen.blit(controls_text, controls_rect)
        
        # Separator line
        pygame.draw.line(self.screen, Colors.GRID_LINE, (0, 99), (self.WINDOW_WIDTH, 99), 2)
    
    def draw_game_over(self):
        """Draw game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        overlay.set_alpha(230)
        overlay.fill(Colors.GAME_OVER_BG[:3])
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = self.font_large.render("GAME OVER", True, Colors.TEXT_PRIMARY)
        game_over_rect = game_over_text.get_rect(center=(self.WINDOW_WIDTH // 2, 
                                                          self.WINDOW_HEIGHT // 2 - 100))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final score
        score_text = self.font_medium.render(f"Final Score: {self.score}", True, Colors.SNAKE_HEAD)
        score_rect = score_text.get_rect(center=(self.WINDOW_WIDTH // 2, 
                                                  self.WINDOW_HEIGHT // 2 - 20))
        self.screen.blit(score_text, score_rect)
        
        # High score
        if self.score >= self.high_score:
            high_score_text = self.font_small.render("🎉 NEW HIGH SCORE! 🎉", True, Colors.FOOD)
        else:
            high_score_text = self.font_small.render(f"High Score: {self.high_score}", True, Colors.TEXT_SECONDARY)
        high_score_rect = high_score_text.get_rect(center=(self.WINDOW_WIDTH // 2, 
                                                            self.WINDOW_HEIGHT // 2 + 30))
        self.screen.blit(high_score_text, high_score_rect)
        
        # Restart button
        button_text = self.font_small.render("Press SPACE to Restart", True, Colors.TEXT_SECONDARY)
        button_rect = button_text.get_rect(center=(self.WINDOW_WIDTH // 2, 
                                                    self.WINDOW_HEIGHT // 2 + 100))
        
        # Animated button (pulsing effect)
        pulse = abs((pygame.time.get_ticks() % 1000) - 500) / 500
        button_bg = pygame.Rect(button_rect.left - 20, button_rect.top - 10,
                               button_rect.width + 40, button_rect.height + 20)
        
        alpha = int(100 + 100 * pulse)
        button_surf = pygame.Surface((button_bg.width, button_bg.height))
        button_surf.set_alpha(alpha)
        button_surf.fill(Colors.BUTTON_BG)
        self.screen.blit(button_surf, button_bg)
        
        self.screen.blit(button_text, button_rect)
    
    def draw(self):
        """Draw everything"""
        # Clear screen
        self.screen.fill(Colors.BACKGROUND)
        
        # Draw header
        self.draw_header()
        
        # Draw grid
        self.draw_grid()
        
        # Draw game elements
        self.draw_food()
        self.draw_snake()
        
        # Draw game over screen if needed
        if self.game_over:
            self.draw_game_over()
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
