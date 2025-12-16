import random
import time
import os

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
PURPLE = "\033[38;5;129m"
BLUE = "\033[94m"
ORANGE = "\033[38;5;208m"
BROWN = "\033[38;5;130m"  # Brown color for trunk

def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def get_tree_structure():
    """Get the tree structure definition"""
    return [
        (1, 19),   # Top layer - 1 block
        (3, 18),   # Second layer - 3 blocks
        (5, 17),   # Third layer - 5 blocks
        (7, 16),   # Fourth layer - 7 blocks
        (9, 15),   # Fifth layer - 9 blocks
        (11, 14),  # Sixth layer - 11 blocks
        (13, 13),  # Bottom layer - 13 blocks
    ]

def draw_tree_with_lights(light_positions):
    """Draw the Christmas tree with lights matching pixel art style"""
    tree = []

    # Star on top (centered, directly above tree)
    tree.append(" " * 19 + YELLOW + BOLD + "★" + RESET)

    # Tree layers - bigger tree: 1, 3, 5, 7, 9, 11, 13 blocks
    tree_structure = get_tree_structure()

    for width, indent in tree_structure:
        line = " " * indent

        for i in range(width):
            # Check if this position has a light
            pos_key = f"{indent}_{i}"
            if pos_key in light_positions and light_positions[pos_key].get('on', True):
                # Draw a colorful ornament
                color = light_positions[pos_key]['color']
                symbol = light_positions[pos_key]['symbol']
                line += color + BOLD + symbol + RESET
            else:
                # Draw green tree part (pixel art style)
                line += GREEN + "█" + RESET

        tree.append(line)

    # Trunk (centered, single brown block)
    tree.append(" " * 19 + BROWN + "█" + RESET)
    tree.append("")

    # Message (light blue/cyan)
    tree.append(" " * 12 + RED + "Merry Christmas!" + RESET)

    return "\n".join(tree)

def initialize_lights():
    """Initialize lights with random positions within the tree"""
    lights = []
    tree_structure = get_tree_structure()

    # Light colors and symbols
    colors = [RED, PURPLE, BLUE, ORANGE, YELLOW]
    symbols = ["★", "◆", "●", "♦"]

    # Create 8-10 lights
    num_lights = random.randint(8, 10)
    for _ in range(num_lights):
        # Randomly assign to a layer (skip layer 0 - directly below star)
        layer_idx = random.randint(1, len(tree_structure) - 1)
        width, indent = tree_structure[layer_idx]
        # Random position within that layer, but avoid edges (pos 0 and width-1)
        # Only place lights in the middle positions
        if width > 2:
            pos = random.randint(1, width - 2)  # Exclude first and last positions
        else:
            # If layer is too narrow (width <= 2), skip this light
            continue

        lights.append({
            'layer_idx': layer_idx,
            'position': pos,
            'color': random.choice(colors),
            'symbol': random.choice(symbols),
            'on': True
        })

    return lights

def move_lights(lights):
    """Move lights to new random positions within the tree"""
    tree_structure = get_tree_structure()

    for light in lights:
        # 70% chance to move to a new position
        if random.random() < 0.7:
            # Choose a random layer (skip layer 0 - directly below star)
            new_layer_idx = random.randint(1, len(tree_structure) - 1)
            width, indent = tree_structure[new_layer_idx]
            # Avoid edges (pos 0 and width-1) - only place in middle positions
            if width > 2:
                new_pos = random.randint(1, width - 2)  # Exclude first and last positions
                light['layer_idx'] = new_layer_idx
                light['position'] = new_pos
            # If layer is too narrow (width <= 2), keep current position (don't move)

        # 15% chance to turn off, 85% chance to stay on or turn on
        if random.random() < 0.15:
            light['on'] = False
        else:
            light['on'] = True
            # Occasionally change color (20% chance)
            if random.random() < 0.2:
                colors = [RED, PURPLE, BLUE, ORANGE, YELLOW]
                light['color'] = random.choice(colors)
                symbols = ["★", "◆", "●", "♦"]
                light['symbol'] = random.choice(symbols)

    return lights

def lights_to_positions(lights):
    """Convert light objects to position dictionary for drawing"""
    light_positions = {}
    tree_structure = get_tree_structure()

    for light in lights:
        if light['on']:
            layer_idx = light['layer_idx']
            # Skip layer 0 (directly below star) - no lights allowed there
            if 1 <= layer_idx < len(tree_structure):
                width, indent = tree_structure[layer_idx]
                pos = light['position']
                # Only place lights in middle positions, not on edges (pos 0 or width-1)
                if width > 2 and 1 <= pos < width - 1:
                    pos_key = f"{indent}_{pos}"
                    light_positions[pos_key] = {
                        'color': light['color'],
                        'symbol': light['symbol'],
                        'on': True
                    }

    return light_positions

def main():
    """Main function to animate the Christmas tree"""
    # Initialize lights
    lights = initialize_lights()

    try:
        while True:
            clear_screen()
            # Move lights to new positions
            lights = move_lights(lights)
            # Convert to position dictionary
            light_positions = lights_to_positions(lights)
            # Draw tree
            tree = draw_tree_with_lights(light_positions)
            print(tree)
            time.sleep(0.4)  # Update every 0.4 seconds
    except KeyboardInterrupt:
        clear_screen()
        print("\n" + CYAN + "Merry Christmas! 🎄" + RESET + "\n")

if __name__ == "__main__":
    main()
