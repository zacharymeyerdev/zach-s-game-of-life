import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import random
import matplotlib.colors as mcolors
from faker import Faker

class Character:
    _id_counter = 1  # Class variable to assign unique IDs

    def __init__(self):
        self.id = Character._id_counter
        Character._id_counter += 1
        self.attack = 1
        self.health = 5
        self.movement_speed = 1
        self.attack_speed = 1
        self.experience = 0
        self.level = 1
        self.color = random.choice(list(mcolors.CSS4_COLORS.keys()))  # Assign a random color
        self.position = None
        self.name = Faker().name()  # Generate a random name using Faker

    def move(self, size):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        dx, dy = random.choice(directions)
        new_position = (self.position[0] + dx, self.position[1] + dy)
        
        # Check if the new position is within the grid boundaries
        if 0 <= new_position[0] < size and 0 <= new_position[1] < size:
            self.position = new_position
        # Else, do nothing (character stays in the same position)

class Game:
    def __init__(self, size):
        self.size = size
        self.grid = np.zeros((size, size))
        self.characters = []
        self.current_frame = 0  # Added to track the current frame
        self.color_map = {char.id: char.color for char in self.characters}
        # Automatically create and add characters
        for _ in range(size):
            character = Character()
            while True:
                position = (random.randint(0, size-1), random.randint(0, size-1))
                if self.grid[position] == 0:
                    self.add_character(character, position)
                    break

    def add_character(self, character, position):
        self.characters.append(character)
        character.position = position
        self.grid[position] = len(self.characters)

    def next_frame(self):
        self.current_frame += 1
        new_grid = np.zeros_like(self.grid)  # Create a new grid for this frame
        position_to_character = {char.position: char for char in self.characters}  # Map positions to characters

        characters_to_remove = set()
        removed_character_names = []  # List to store the names of removed characters

        for character in self.characters:
            old_position = character.position
            character.move(self.size)

            # Check for character interactions
            other = position_to_character.get(character.position)
            if other and other != character:
                other.health -= character.attack
                if other.health <= 0:
                    characters_to_remove.add(other)
                    removed_character_names.append(other.name)  # Add the name of the removed character

            # Update the new grid with the character's new position
            if character not in characters_to_remove:
                new_grid[character.position] = self.characters.index(character) + 1

        # Remove characters marked for removal
        for char in characters_to_remove:
            self.color_map.pop(char.id, None)
        self.characters = [char for char in self.characters if char not in characters_to_remove]
        self.grid = new_grid  # Update the main grid with the new grid

        # Print the names of removed characters
        for name in removed_character_names:
            print(f"Character {name} has been removed.")
    def draw(self):
        # Create a color map from the character colors
        cmap = ['white'] + [self.color_map[char.id] for char in self.characters]
        cmap = plt.cm.colors.ListedColormap(cmap)        
        plt.imshow(self.grid, cmap=cmap)
        plt.show()

# Create a game
game = Game(11)

# Create a figure for the plot
fig, ax = plt.subplots()

# Global variable to keep track of the current frame number
current_frame = 0


# Function to update the plot
def update(num):
    ax.clear()
    game.next_frame()
    cmap = plt.cm.colors.ListedColormap(['white'] + [character.color for character in game.characters])
    ax.imshow(game.grid, cmap=cmap, interpolation='nearest')  # Use nearest interpolation for clearer visuals
    plt.text(0.95, 0.05, f'Frame: {game.current_frame}', horizontalalignment='right', verticalalignment='bottom', transform=ax.transAxes, color='black')

# Option 1: Specify a save_count
ani = FuncAnimation(fig, update, frames=None, interval=200, repeat=True, cache_frame_data=False)
plt.show()