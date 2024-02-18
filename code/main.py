import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import random
import matplotlib.colors as mcolors
from faker import Faker
import pygame
import random

class Character:
    def __init__(self, name):
        self.name = name
        self.base_class = random.choice(['Warrior', 'Mage', 'Thief'])
        self.subclass = None
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.health = 100
        self.special_ability = random.choice(['HighGround', 'SwiftStrike', 'MindControl'])
        
        # Assign initial stats based on class
        if self.base_class == 'Warrior':
            self.strength = random.randint(6, 10)
            self.agility = random.randint(1, 5)
            self.intelligence = 15 - self.strength - self.agility
        elif self.base_class == 'Mage':
            self.intelligence = random.randint(6, 10)
            self.strength = random.randint(1, 5)
            self.agility = 15 - self.intelligence - self.strength
        elif self.base_class == 'Thief':
            self.agility = random.randint(6, 10)
            self.intelligence = random.randint(1, 5)
            self.strength = 15 - self.agility - self.intelligence

    def __repr__(self):
        class_info = f"{self.base_class}/{self.subclass}" if self.subclass else self.base_class
        return f"{self.name} ({class_info}): (S: {self.strength}, A: {self.agility}, I: {self.intelligence})"

    def reset_health(self):
        self.health = 100
        
    def upgrade_to_subclass(self):
        if self.base_class == 'Warrior':
            self.subclass = random.choice(['Barbarian', 'Fighter'])
        elif self.base_class == 'Mage':
            self.subclass = random.choice(['Wizard', 'Sorcerer'])
        elif self.base_class == 'Thief':
            self.subclass = random.choice(['Rogue', 'Assassin'])

def generate_characters(num_characters=64):
    characters = []
    fake = Faker()
    for _ in range(num_characters):
        name = fake.name()
        character = Character(name)
        characters.append(character)
    return characters

def calculate_win_probability(character, opponent, env_factor):
    # Higher stats increase the win probability, but the difference matters
    strength_advantage = character.strength - opponent.agility
    agility_advantage = character.agility - opponent.intelligence
    intelligence_advantage = character.intelligence - opponent.strength

    # Base win probability
    win_probability = 0.5

    # Adjust win probability based on stat advantages
    win_probability += strength_advantage * 0.05
    win_probability += agility_advantage * 0.05
    win_probability += intelligence_advantage * 0.05

    if character.special_ability == 'HighGround' and env_factor == 'Rainy':
        win_probability += 0.1
    elif character.special_ability == 'SwiftStrike' and env_factor == 'Windy':
        win_probability += 0.1
    elif character.special_ability == 'MindControl' and env_factor == 'Sunny':
        win_probability += 0.1

    # Ensure probability is within 0-1 range
    win_probability = max(0, min(win_probability, 1))
    return win_probability

def increase_winner_stats(winner):
    # Randomly choose which stat to increase
    stat_to_increase = random.choice(['strength', 'agility', 'intelligence'])

    # Determine the increase amount (between 1 and 4)
    increase_amount = random.randint(1, 4)

    # Increase the chosen stat
    if stat_to_increase == 'strength':
        winner.strength += increase_amount
    elif stat_to_increase == 'agility':
        winner.agility += increase_amount
    else:
        winner.intelligence += increase_amount

    return winner

def apply_subclass_ability(character, opponent):
    if character.subclass == 'Barbarian' and character.health < 20:
        # Increase strength when health is critically low
        character.strength += 5
    elif character.subclass == 'Fighter':
        # Counterattack chance
        if random.random() < 0.15:
            opponent.health -= 5  # Reflect damage
    elif character.subclass == 'Wizard':
        # Arcane Blast
        if random.random() < 0.2:
            opponent.intelligence = max(1, opponent.intelligence - 3)
    elif character.subclass == 'Sorcerer':
        # Enchant
        if random.random() < 0.2:
            character.agility += 3
    elif character.subclass == 'Rogue':
        # Shadow Blend
        if random.random() < 0.25:
            character.agility += 5
    elif character.subclass == 'Assassin':
        # Deadly Poison
        if random.random() < 0.2:
            opponent.health -= 10  # Ongoing damage
    # Reset increased stats after each round if necessary

def draw_combat_scene(window, character1, character2, window_width, window_height):
    font = pygame.font.SysFont(None, 24)
    
    # Draw characters
    char1_text = font.render(f"{character1.name}", True, character1.color)
    char2_text = font.render(f"{character2.name}", True, character2.color)
    window.blit(char1_text, (100, window_height // 2))
    window.blit(char2_text, (window_width - 200, window_height // 2))

    # Draw health bars
    max_health_width = 200  # Max width of the health bar
    health_bar_height = 20
    char1_health_ratio = character1.health / 100
    char2_health_ratio = character2.health / 100

    char1_health_bar = (100, window_height // 2 + 30, max_health_width * char1_health_ratio, health_bar_height)
    char2_health_bar = (window_width - 200, window_height // 2 + 30, max_health_width * char2_health_ratio, health_bar_height)

    pygame.draw.rect(window, (255, 0, 0), char1_health_bar)  # Red health bar
    pygame.draw.rect(window, (255, 0, 0), char2_health_bar)

def simulate_match(character1, character2):
    env_factor = random.choice(['Rainy', 'Sunny', 'Windy'])
    apply_subclass_ability(character1, character2)
    apply_subclass_ability(character2, character1)

    win_probability_1 = calculate_win_probability(character1, character2, env_factor)
    win_probability_2 = calculate_win_probability(character2, character1, env_factor)

    # Critical Hit and Miss Chance
    critical_hit_factor = 1.5
    critical_hit_character1 = random.random() < 0.1
    critical_hit_character2 = random.random() < 0.1

    # Base damage for a successful hit
    base_damage = 10

    # Calculate damage for each character
    damage_to_character2 = base_damage * (1.5 if critical_hit_character1 else 1)  # Increased if critical hit
    damage_to_character1 = base_damage * (1.5 if critical_hit_character2 else 1)

    # Simulate the match and apply damage
    if random.random() < win_probability_1:
        character2.health -= damage_to_character2
    else:
        character1.health -= damage_to_character1

    # Check for a winner based on remaining health
    while character1.health > 0 and character2.health > 0:
        if random.random() < win_probability_1:
            character2.health -= damage_to_character2
        else:
            character1.health -= damage_to_character1

        if character1.health <= 0:
            winner = character2
            break
        if character2.health <= 0:
            winner = character1
            break

    winner = increase_winner_stats(winner)
    match_result = f"{character1.name} vs {character2.name} in {env_factor} conditions: {winner.name} Wins. Health: {character1.health} - {character2.health}"
    return winner, match_result

def tournament_round(characters):
    winners = []
    match_results = []
    for i in range(0, len(characters), 2):
        character1 = characters[i]
        character2 = characters[i + 1]
        winner, result = simulate_match(character1, character2)
        winners.append(winner)
        match_results.append(result)
    return winners, match_results

def run_tournament(characters):
    rounds = [characters.copy()]
    all_match_results = []
    current_round = 1
    while len(characters) > 1:
        new_round_characters, match_results = tournament_round(characters)
        
        # Subclass upgrade at round 3
        if current_round == 3:
            for character in new_round_characters:
                character.upgrade_to_subclass()

        rounds.append(new_round_characters)
        all_match_results.extend(match_results)
        characters = new_round_characters
        current_round += 1

        # Reset health after each round
        for character in characters:
            character.reset_health()

    return rounds, all_match_results

def draw_character(window, character, position):
    font = pygame.font.SysFont(None, 24)
    text = font.render(f"{character.name} (S: {character.strength}, A: {character.agility}, I: {character.intelligence})", True, (255, 255, 255))
    window.blit(text, position)

def draw_line(window, start_pos, end_pos, color=(255, 255, 255), thickness=2):
    pygame.draw.line(window, color, start_pos, end_pos, thickness)

def draw_bracket(window, rounds, current_round, window_width, window_height):
    max_characters = max(len(round_chars) for round_chars in rounds)
    square_size = window_width // (max_characters * 1.01)  # Adjust for space between squares
    square_size = min(square_size, window_height // len(rounds))  # Ensure squares fit vertically
    spacing = square_size // 10

    # Dictionary to store x-positions of characters
    x_positions = {}

    for round_index, round_characters in enumerate(rounds):
        if round_index > current_round:
            break

        y_position = round_index * (square_size + spacing)

        for i, character in enumerate(round_characters):
            if round_index == 0:
                x_position = i * (square_size + spacing)
            else:
                # Find the x-positions of the two characters that the winner defeated
                prev_round_index = (i * 2, i * 2 + 1)
                prev_x_positions = [x_positions[round_index - 1][index] for index in prev_round_index]
                x_position = sum(prev_x_positions) // 2  # Place in the middle of the two competitors

            x_positions.setdefault(round_index, {})[i] = x_position  # Store x-position
            pygame.draw.rect(window, character.color, (x_position, y_position, square_size, square_size))

    # Special handling for the final winner
    if current_round == len(rounds) - 1 and len(rounds[-1]) == 1:
        winner = rounds[-1][0]
        winner_text = f"Winner: {winner.name}"
        font = pygame.font.SysFont(None, 30)
        text_surface = font.render(winner_text, True, (255, 215, 0))
        window.blit(text_surface, (10, window_height - text_surface.get_height() - 10))

    pygame.display.flip()


def main():
    # Initialize Pygame
    pygame.init()
    window_width = 1280
    window_height = 720
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Tournament Game")

    characters = generate_characters()
    tournament_rounds, match_results = run_tournament(characters)  # Get rounds and match results
    current_round = 0
    show_combat = False  # Flag to toggle between bracket view and combat view
    combat_match_index = 0  # Index to track the combat match being displayed

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Toggle between bracket view and combat view
                    show_combat = not show_combat
                    if not show_combat:
                        # Move to next round when returning to bracket view
                        current_round = min(current_round + 1, len(tournament_rounds) - 1)
                        combat_match_index = 0  # Reset combat match index

        window.fill((0, 0, 0))

        if show_combat and combat_match_index < len(tournament_rounds[current_round]) // 2:
            # Display combat scene for the current match
            char1 = tournament_rounds[current_round][combat_match_index * 2]
            char2 = tournament_rounds[current_round][combat_match_index * 2 + 1]
            draw_combat_scene(window, char1, char2, window_width, window_height)
            combat_match_index += 1  # Move to the next match after displaying current one
        else:
            # Display the tournament bracket
            draw_bracket(window, tournament_rounds, current_round, window_width, window_height)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
