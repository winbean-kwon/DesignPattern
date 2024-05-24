import time
import sys
import os

def draw_car(position):
    car = """
      ______
     //  ||\\ \\
 ___//___||_\\ \___
|  _          - |   |
'-(_)--------(_)-'
    """
    lines = car.split('\n')
    for line in lines:
        print(' ' * position + line)

def clear_screen():
    # Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # Mac and Linux
    else:
        _ = os.system('clear')

def animate_car():
    width = os.get_terminal_size().columns
    car_length = 23  # Length of the car in characters (approximate)
    for position in range(width - car_length + 1):
        clear_screen()
        draw_car(position)
        time.sleep(0.05)

if __name__ == "__main__":
    animate_car()
