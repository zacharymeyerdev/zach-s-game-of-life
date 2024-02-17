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
        total_stats = 15
        self.strength = random.randint(1, total_stats - 2)
        remaining_stats = total_stats - self.strength
        self.agility = random.randint(1, remaining_stats - 1)
        self.intelligence = remaining_stats - self.agility
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def __repr__(self):
        return f"{self.name} (S: {self.strength}, A: {self.agility}, I: {self.intelligence})"

def generate_characters(num_characters=64):
    characters = []
    fake = Faker()
    for _ in range(num_characters):
        name = fake.name()
        character = Character(name)
        characters.append(character)
    return characters

def calculate_win_probability(character, opponent):
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

def simulate_match(character1, character2):
    win_probability_1 = calculate_win_probability(character1, character2)
    win_probability_2 = calculate_win_probability(character2, character1)

    # Simulate the match based on win probabilities
    if random.random() < win_probability_1:
        winner = character1
    else:
        winner = character2

    winner = increase_winner_stats(winner)

    match_result = f"{character1.name} vs {character2.name}: {winner.name} Wins"
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
        print(f"{character1.name} vs {character2.name}: {winner.name} Wins")
    return winners, match_results

def run_tournament(characters):
    rounds = [characters.copy()]
    all_match_results = []
    while len(characters) > 1:
        characters, match_results = tournament_round(characters)
        rounds.append(characters)
        all_match_results.extend(match_results)
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

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and current_round < len(tournament_rounds) - 1:
                    current_round += 1

        window.fill((0, 0, 0))
        draw_bracket(window, tournament_rounds, current_round, window_width, window_height)  # Update this line
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
