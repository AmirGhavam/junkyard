import pygame
import random
import sys
import math
from enum import Enum

# Initialize Pygame
pygame.init()

# --- Constants & Configuration ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
FPS = 60

# Colors (Modern Casino Palette)
class Colors:
    BACKGROUND = (20, 30, 40)       # Dark Slate
    TABLE_FELT = (35, 80, 55)       # Deep Green
    TABLE_BORDER = (60, 40, 20)     # Wood-like
    CARD_BG = (245, 245, 245)       # Off-white
    CARD_BACK = (180, 40, 40)       # Deep Red
    TEXT_MAIN = (255, 255, 255)
    TEXT_ACCENT = (255, 215, 0)     # Gold
    BUTTON_IDLE = (50, 150, 200)
    BUTTON_HOVER = (70, 170, 220)
    BUTTON_DISABLED = (100, 100, 100)
    SUIT_RED = (220, 20, 60)
    SUIT_BLACK = (20, 20, 20)
    OVERLAY = (0, 0, 0, 180)

# Card Configuration
CARD_WIDTH = 100
CARD_HEIGHT = 145
CARD_RADIUS = 10

# --- Enums & Data Structures ---
class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"

class Rank(Enum):
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"

class GameState(Enum):
    BETTING = 1
    DEALING = 2
    PLAYER_TURN = 3
    DEALER_TURN = 4
    GAME_OVER = 5

# --- Classes ---

class Card:
    def __init__(self, suit, rank, x=0, y=0, target_x=0, target_y=0, face_up=True):
        self.suit = suit
        self.rank = rank
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.face_up = face_up
        self.scale = 1.0
        self.rotation = 0
        self.is_moving = False
        
    def update(self):
        # Smooth movement animation (Linear Interpolation)
        speed = 0.15
        if abs(self.x - self.target_x) > 1 or abs(self.y - self.target_y) > 1:
            self.x += (self.target_x - self.x) * speed
            self.y += (self.target_y - self.y) * speed
            self.is_moving = True
        else:
            self.x = self.target_x
            self.y = self.target_y
            self.is_moving = False

    def draw(self, surface):
        # Draw card body
        rect = pygame.Rect(self.x, self.y, CARD_WIDTH, CARD_HEIGHT)
        
        if self.face_up:
            # Main card background
            pygame.draw.rect(surface, Colors.CARD_BG, rect, border_radius=CARD_RADIUS)
            pygame.draw.rect(surface, (200, 200, 200), rect, width=1, border_radius=CARD_RADIUS) # Border
            
            # Determine Color
            color = Colors.SUIT_RED if self.suit in [Suit.HEARTS, Suit.DIAMONDS] else Colors.SUIT_BLACK
            
            # Draw Rank (Top Left)
            font = pygame.font.SysFont("Arial", 24, bold=True)
            rank_text = font.render(self.rank.value, True, color)
            surface.blit(rank_text, (self.x + 8, self.y + 8))
            
            # Draw Suit (Small Top Left)
            suit_font = pygame.font.SysFont("Segoe UI Symbol", 20) # Use a font that supports symbols
            suit_text = suit_font.render(self.suit.value, True, color)
            surface.blit(suit_text, (self.x + 8, self.y + 32))
            
            # Draw Rank (Bottom Right - Rotated)
            rank_text_rot = pygame.transform.rotate(rank_text, 180)
            surface.blit(rank_text_rot, (self.x + CARD_WIDTH - 8 - rank_text_rot.get_width(), 
                                         self.y + CARD_HEIGHT - 8 - rank_text_rot.get_height()))
            
            # Draw Center Suit (Large)
            center_font = pygame.font.SysFont("Segoe UI Symbol", 64)
            center_suit = center_font.render(self.suit.value, True, color)
            center_rect = center_suit.get_rect(center=(self.x + CARD_WIDTH//2, self.y + CARD_HEIGHT//2))
            surface.blit(center_suit, center_rect)
            
        else:
            # Card Back
            pygame.draw.rect(surface, Colors.CARD_BACK, rect, border_radius=CARD_RADIUS)
            pygame.draw.rect(surface, (255, 255, 255), rect, width=2, border_radius=CARD_RADIUS)
            # Pattern on back
            inner_rect = pygame.Rect(self.x + 10, self.y + 10, CARD_WIDTH - 20, CARD_HEIGHT - 20)
            pygame.draw.rect(surface, (160, 30, 30), inner_rect, border_radius=CARD_RADIUS//2)

class Deck:
    def __init__(self):
        self.cards = []
        self.reset()
    
    def reset(self):
        self.cards = []
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(suit, rank))
        random.shuffle(self.cards)
        
    def deal(self):
        if not self.cards:
            self.reset()
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []
        
    def add_card(self, card):
        self.cards.append(card)
        
    def get_value(self):
        value = 0
        aces = 0
        for card in self.cards:
            if card.rank in [Rank.JACK, Rank.QUEEN, Rank.KING]:
                value += 10
            elif card.rank == Rank.ACE:
                aces += 1
                value += 11
            else:
                value += int(card.rank.value)
        
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
            
        return value
    
    def is_blackjack(self):
        return self.get_value() == 21 and len(self.cards) == 2

    def clear(self):
        self.cards = []

class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
        self.is_hovered = False
        self.enabled = True
        
    def draw(self, surface):
        if not self.enabled:
            color = Colors.BUTTON_DISABLED
        else:
            color = Colors.BUTTON_HOVER if self.is_hovered else Colors.BUTTON_IDLE
            
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        
        # Text
        font = pygame.font.SysFont("Arial", 24, bold=True)
        text_surf = font.render(self.text, True, Colors.TEXT_MAIN)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        
    def click(self):
        if self.enabled and self.action:
            self.action()

class BlackjackGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("✨ Beautiful Blackjack 21")
        self.clock = pygame.time.Clock()
        
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.state = GameState.BETTING
        
        self.message = "Place your bet!"
        self.chips = 1000
        self.current_bet = 0
        
        # UI Elements
        self.buttons = []
        self.setup_buttons()
        
        # Animation queue
        self.animations = [] # List of (card, target_x, target_y, delay)
        
    def setup_buttons(self):
        btn_y = SCREEN_HEIGHT - 100
        self.btn_hit = Button("HIT", SCREEN_WIDTH//2 - 160, btn_y, 140, 50, self.player_hit)
        self.btn_stand = Button("STAND", SCREEN_WIDTH//2 + 20, btn_y, 140, 50, self.player_stand)
        self.btn_deal = Button("DEAL", SCREEN_WIDTH//2 - 70, btn_y, 140, 50, self.start_round)
        self.btn_reset = Button("PLAY AGAIN", SCREEN_WIDTH//2 - 90, btn_y, 180, 50, self.reset_game)
        
        self.buttons = [self.btn_hit, self.btn_stand, self.btn_deal, self.btn_reset]
        
    def update_buttons(self):
        # Reset all
        for btn in self.buttons:
            btn.enabled = False
            
        if self.state == GameState.BETTING:
            self.btn_deal.enabled = True
        elif self.state == GameState.PLAYER_TURN:
            self.btn_hit.enabled = True
            self.btn_stand.enabled = True
        elif self.state == GameState.GAME_OVER:
            self.btn_reset.enabled = True

    def start_round(self):
        if self.chips < 10:
            self.message = "Out of chips! Resetting..."
            self.chips = 1000
            
        self.current_bet = 50 # Fixed bet for simplicity
        self.chips -= self.current_bet
        self.player_hand.clear()
        self.dealer_hand.clear()
        self.deck.reset() # Shuffle every round for simplicity
        
        self.state = GameState.DEALING
        self.message = "Dealing..."
        
        # Deal initial cards with animation delays
        self.deal_card(self.player_hand, 0)
        self.deal_card(self.dealer_hand, 20) # Dealer hole card (hidden initially logic handled in draw)
        self.deal_card(self.player_hand, 40)
        self.deal_card(self.dealer_hand, 60)
        
    def deal_card(self, hand, delay_frames):
        card = self.deck.deal()
        # Start position (Deck pile)
        card.x = SCREEN_WIDTH - 150
        card.y = 50
        
        # Target position calculation
        is_player = (hand == self.player_hand)
        idx = len(hand.cards)
        
        base_x = SCREEN_WIDTH // 2 - CARD_WIDTH // 2
        offset_x = (idx - 0.5) * 30 # Overlap cards slightly
        
        if is_player:
            target_y = SCREEN_HEIGHT - 250
        else:
            target_y = 150
            
        card.target_x = base_x + offset_x
        card.target_y = target_y
        
        # If it's the dealer's first card, it should be face down initially? 
        # Actually standard is one up one down. Let's say 2nd card is hole card.
        if hand == self.dealer_hand and len(hand.cards) == 0:
            card.face_up = False
            
        hand.add_card(card)
        self.animations.append({"card": card, "delay": delay_frames})

    def player_hit(self):
        self.deal_card(self.player_hand, 0)
        
    def player_stand(self):
        self.state = GameState.DEALER_TURN
        self.message = "Dealer's Turn..."
        
        # Reveal dealer hole card
        if self.dealer_hand.cards:
            self.dealer_hand.cards[0].face_up = True
            
        # Dealer logic
        while self.dealer_hand.get_value() < 17:
            self.deal_card(self.dealer_hand, len(self.dealer_hand.cards) * 20)
            
    def check_game_over(self):
        p_val = self.player_hand.get_value()
        d_val = self.dealer_hand.get_value()
        
        # Check if animations are done before deciding result
        if any(c.is_moving for c in self.player_hand.cards + self.dealer_hand.cards):
            return

        if self.state == GameState.DEALING:
            # Check for initial Blackjack
            if len(self.player_hand.cards) == 2 and len(self.dealer_hand.cards) == 2:
                if p_val == 21 or d_val == 21:
                    self.state = GameState.GAME_OVER
                    self.resolve_winner()
                else:
                    self.state = GameState.PLAYER_TURN
                    self.message = "Your Turn: Hit or Stand?"
                    
        elif self.state == GameState.PLAYER_TURN:
            if p_val > 21:
                self.state = GameState.GAME_OVER
                self.resolve_winner()
            elif p_val == 21:
                self.player_stand() # Auto stand on 21
                
        elif self.state == GameState.DEALER_TURN:
            # Wait for dealer animations to finish
            if not any(c.is_moving for c in self.dealer_hand.cards):
                self.state = GameState.GAME_OVER
                self.resolve_winner()

    def resolve_winner(self):
        p_val = self.player_hand.get_value()
        d_val = self.dealer_hand.get_value()
        
        # Reveal hole card if not already
        if self.dealer_hand.cards:
            self.dealer_hand.cards[0].face_up = True
        
        if p_val > 21:
            self.message = "Bust! You lose."
        elif d_val > 21:
            self.message = "Dealer Busts! You Win!"
            self.chips += self.current_bet * 2
        elif p_val > d_val:
            self.message = "You Win!"
            self.chips += self.current_bet * 2
        elif p_val < d_val:
            self.message = "Dealer Wins."
        else:
            self.message = "Push (Tie)."
            self.chips += self.current_bet

    def reset_game(self):
        self.state = GameState.BETTING
        self.message = "Place your bet!"
        
    def run(self):
        running = True
        frame_count = 0
        
        while running:
            self.screen.fill(Colors.BACKGROUND)
            
            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for btn in self.buttons:
                            if btn.is_hovered:
                                btn.click()
            
            # Logic Update
            self.update_buttons()
            
            # Handle delayed animations
            if self.animations:
                # Process animations that are ready
                remaining = []
                for anim in self.animations:
                    if anim["delay"] <= 0:
                        # Start moving the card
                        # The card is already in the hand, just need to make sure update() is called
                        pass 
                    else:
                        anim["delay"] -= 1
                        remaining.append(anim)
                self.animations = remaining

            # Update Cards
            for card in self.player_hand.cards + self.dealer_hand.cards:
                card.update()
                
            # Game Logic Check
            self.check_game_over()
            
            # --- Drawing ---
            
            # Draw Table
            table_rect = pygame.Rect(50, 100, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 200)
            pygame.draw.rect(self.screen, Colors.TABLE_BORDER, table_rect, border_radius=100)
            pygame.draw.rect(self.screen, Colors.TABLE_FELT, table_rect.inflate(-20, -20), border_radius=90)
            
            # Draw Deck Pile
            deck_rect = pygame.Rect(SCREEN_WIDTH - 150, 50, CARD_WIDTH, CARD_HEIGHT)
            for i in range(3):
                r = deck_rect.move(-i*2, -i*2)
                pygame.draw.rect(self.screen, Colors.CARD_BACK, r, border_radius=CARD_RADIUS)
                pygame.draw.rect(self.screen, (255,255,255), r, width=1, border_radius=CARD_RADIUS)

            # Draw Hands
            for card in self.dealer_hand.cards:
                card.draw(self.screen)
            for card in self.player_hand.cards:
                card.draw(self.screen)
                
            # Draw Scores
            font = pygame.font.SysFont("Arial", 30, bold=True)
            
            # Player Score
            if self.player_hand.cards:
                p_score = f"Player: {self.player_hand.get_value()}"
                p_surf = font.render(p_score, True, Colors.TEXT_MAIN)
                self.screen.blit(p_surf, (SCREEN_WIDTH//2 - p_surf.get_width()//2, SCREEN_HEIGHT - 280))
            
            # Dealer Score (Hide if playing)
            if self.dealer_hand.cards:
                if self.state == GameState.PLAYER_TURN and not self.dealer_hand.cards[0].face_up:
                    d_score = "Dealer: ?"
                else:
                    d_score = f"Dealer: {self.dealer_hand.get_value()}"
                d_surf = font.render(d_score, True, Colors.TEXT_MAIN)
                self.screen.blit(d_surf, (SCREEN_WIDTH//2 - d_surf.get_width()//2, 110))

            # Draw UI (Chips, Message, Buttons)
            
            # Chips
            chip_text = font.render(f"Chips: ${self.chips}", True, Colors.TEXT_ACCENT)
            self.screen.blit(chip_text, (50, 50))
            
            # Message Overlay
            if self.message:
                msg_font = pygame.font.SysFont("Arial", 40, bold=True)
                msg_surf = msg_font.render(self.message, True, Colors.TEXT_ACCENT)
                
                # Add a semi-transparent background for the message if game over
                if self.state == GameState.GAME_OVER:
                    overlay = pygame.Surface((SCREEN_WIDTH, 100), pygame.SRCALPHA)
                    overlay.fill((0,0,0,150))
                    self.screen.blit(overlay, (0, SCREEN_HEIGHT//2 - 50))
                    
                self.screen.blit(msg_surf, (SCREEN_WIDTH//2 - msg_surf.get_width()//2, SCREEN_HEIGHT//2 - msg_surf.get_height()//2))

            # Buttons
            mouse_pos = pygame.mouse.get_pos()
            for btn in self.buttons:
                if btn.enabled:
                    btn.check_hover(mouse_pos)
                    btn.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)
            frame_count += 1

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = BlackjackGame()
    game.run()
