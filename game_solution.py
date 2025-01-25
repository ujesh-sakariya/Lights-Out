# get the libraries needed
import tkinter as tk
import random
from PIL import Image, ImageTk
import csv
import ast

# global co-ords of miner
global miner_x
global miner_y

# Maze dimensions
maze_width = 10  # number of cells wide
maze_height = 10  # number of cells tall
cell_size = 30  # size of each cell in pixels

# boulders
num_boulders = 4
boulders = []
boulder_speed = 500

# lights
num_lights = 10
lights = []

# penalty
penalty = 25

# name of the user

name = None
# speed values
boulder_speed = 500
light_speed = 500
circle_speed = 500

# current level
level = 1
# images
miner_image = None

# boss key
boss_key = False
boss = None
background_image = None

# start animation
animation_running = False

# Dictionary to track if an arrow key is being held down
keys_pressed = {"Up": False, "Down": False, "Left": False, "Right": False}
is_handling_key = False


class boulder:
    def __init__(self, x, y):
        ''' initialise  boulder object'''
        self.x = x
        self.y = y
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.id = None
        self.image = None
        self.draw()

    def draw(self):
        '''Draw the boulder at the current positon'''

        # get the miner and vison radius details
        global miner_x, miner_y, vision_radius

        # find the centre of the boulder
        boulder_pixel_x = self.x * cell_size + cell_size // 2 + 10
        boulder_pixel_y = self.y * cell_size + cell_size // 2 + 10

        # find the centre of the miner
        miner_pixel_x = miner_x * cell_size + cell_size // 2 + 10
        miner_pixel_y = miner_y * cell_size + cell_size // 2 + 10

        # Calculate distance from miner to boulder using euclidean distance
        distance = ((miner_pixel_x - boulder_pixel_x) ** 2 +
                    (miner_pixel_y - boulder_pixel_y) ** 2) ** 0.5

        # Check if boulder is within vision radius
        if distance <= vision_radius:

            # If within vision radius, draw or update its position
            if not self.id:
                # draw the boulder image
                # image source =
                # https://www.freepik.com/free-vector/rolling-stone_3115046.htm#fromView=search&page=1&position=2&uuid=ea0d96ce-7901-4345-98d7-f3214c615065
                original = Image.open('boulder.png')
                # resize the image
                resized_image = original.resize((30, 30))
                # convert to tkinter compatible
                self.image = ImageTk.PhotoImage(resized_image)
                self.id = canvas.create_image(
                    boulder_pixel_x,
                    boulder_pixel_y,
                    image=self.image
                )
            else:
                canvas.coords(
                    self.id,
                    boulder_pixel_x,
                    boulder_pixel_y,
                )
                canvas.itemconfig(self.id, state="normal")
        else:
            # Hide boulder if it's outside the vision radius
            if self.id:
                canvas.itemconfig(self.id, state="hidden")

    def move(self):
        '''Move the boulder using direction '''
        dx, dy = 0, 0
        if self.direction == 'up':
            dy = -1
        elif self.direction == 'down':
            dy = 1
        elif self.direction == 'left':
            dx = -1
        elif self.direction == 'right':
            dx = 1

        new_x = self.x + dx
        new_y = self.y + dy

        # make sure it doesnt go through a wall
        if is_valid_move(new_x, new_y, self.x, self.y):

            self.x, self.y = new_x, new_y
            self.collision()

        else:
            self.change_direction()

        self.draw()
        # Redraw the boulder in its new position

    def collision(self):
        '''Check if the miner had collided with boulder '''
        global miner_x, miner_y, vision_radius, penalty, boulders
        # check if same grid ref
        if self.x == miner_x and self.y == miner_y:
            # add penalty
            vision_radius -= penalty
            # delete from canvas
            canvas.delete(self.id)
            if self in boulders:
                boulders.remove(self)
            del self

    def change_direction(self):
        '''Change the direction of the boulder'''
        self.direction = random.choice(['up', 'down', 'left', 'right'])

    def get_position(self):
        ''' function that returns the co-ords of each object '''
        return self.x, self.y


class light:
    ''' class for the light bulbs to collect '''

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = None
        self.image = None
        self.hidden = True
        self.draw()

    def draw(self):
        ''' draw the light bulbs on the map '''
        # get the miner and vison radius details
        global miner_x, miner_y, vision_radius

        # find the centre of the light bulb
        light_pixel_x = self.x * cell_size + cell_size // 2 + 10
        light_pixel_y = self.y * cell_size + cell_size // 2 + 10

        # find the centre of the miner
        miner_pixel_x = miner_x * cell_size + cell_size // 2 + 10
        miner_pixel_y = miner_y * cell_size + cell_size // 2 + 10
        if self.hidden:
            # Calculate distance from miner to light using euclidean distance
            distance = ((miner_pixel_x - light_pixel_x) ** 2 +
                        (miner_pixel_y - light_pixel_y) ** 2) ** 0.5

            # Check if the light is within vision radius
            if distance <= vision_radius:

                # If within vision radius, draw or update its position
                if not self.id:
                    # draw the light image
                    # image source =
                    # https://www.freepik.com/free-vector/burning-candle-sticker-design-element-vector_25519482.htm#fromView=search&page=1&position=19&uuid=82a73eb0-8f75-4d00-8dbc-ca1999b0407f
                    original = Image.open('light.png')
                    # resize the image
                    resized_image = original.resize((30, 30))
                    # convert to tkinter compatible
                    self.image = ImageTk.PhotoImage(resized_image)
                    self.id = canvas.create_image(
                        light_pixel_x,
                        light_pixel_y,
                        image=self.image
                    )
                else:
                    canvas.coords(
                        self.id,
                        light_pixel_x,
                        light_pixel_y,
                    )
                    canvas.itemconfig(self.id, state="normal")
            else:
                # Hide light if it's outside the vision radius
                if self.id:
                    canvas.itemconfig(self.id, state="hidden")
        else:
            # If within vision radius, draw or update its position
            if not self.id:
                # draw the light image
                # image source =
                # https://www.freepik.com/free-vector/burning-candle-sticker-design-element-vector_25519482.htm#fromView=search&page=1&position=19&uuid=82a73eb0-8f75-4d00-8dbc-ca1999b0407f
                original = Image.open('light.png')
                # resize the image
                resized_image = original.resize((30, 30))
                # convert to tkinter compatible
                self.image = ImageTk.PhotoImage(resized_image)
                self.id = canvas.create_image(
                    light_pixel_x,
                    light_pixel_y,
                    image=self.image
                )
            else:
                canvas.coords(
                    self.id,
                    light_pixel_x,
                    light_pixel_y,
                )
                canvas.itemconfig(self.id, state="normal")

    def found(self):
        global miner_y, miner_x, vision_radius, lights
        ''' Check if miner has collected bulb'''
        if self.x == miner_x and self.y == miner_y:
            vision_radius += 50
            # delete from the canvas
            canvas.delete(self.id)
            # remove from lights array
            if self in lights:
                lights.remove(self)
            # delete object
            del self
            # check if the user has won
            check_win()

    def get_position(self):
        ''' function that returns the x and y position of the object'''
        return self.x, self.y

    def show(self):
        ''' make the lights visable'''
        self.hidden = not self.hidden
        self.draw()


class cheatcode:
    def __init__(self, sequence, action):
        self.sequence = sequence
        self.input = []
        self.action = action

    def check_input(self, event):
        ''' check if the user entered the cheatcode '''
        key = event.keysym
        self.input.append(key)
        # If the sequence length exceeds, remove the first key
        if len(self.input) > len(self.sequence):
            self.input.pop(0)
        # If the sequence matches, activate the action
        if self.input == self.sequence:
            self.activate_cheat()

    def activate_cheat(self):
        ''' function that activates the cheat '''
        if self.action == 'increase radius':
            self.increase_radius()
        if self.action == 'boulder positive':
            self.boulder_positive()
        if self.action == 'show lights':
            self.show_lights()

    def increase_radius(self):
        ''' cheat to increase the radius of the circle'''
        global vision_radius
        # add 25 to the radius
        vision_radius += 25

    def boulder_positive(self):
        ''' when the user hits the boulder, they get a bonus'''
        global penalty
        penalty = -(penalty)

    def show_lights(self):
        ''' show all the lights on the screen'''
        global lights
        for obj in lights:
            obj.show()


# Initialize Tkinter and Canvas
root = tk.Tk()
root.title("lights Out")

# initialising the canvas
canvas = tk.Canvas(
    root,
    width=maze_width *
    cell_size +
    15,
    height=maze_height *
    cell_size +
    15,
    bg="black")
# add the maze to the window 0
canvas.pack()

# dictioanry to hold the maze
maze = {}

# Vision radius in pixels (the radius of the vision circle)
vision_radius = 100

# pause
pause = False
pause_menu = None

# dict to store the keybinds
keybinds = {
    'Left': 'Left',
    'Right': 'Right',
    'Up': 'Up',
    'Down': 'Down',
    'Pause': [
        'p',
        'P'],
    'Boss': [
        'b',
        'B']}

# activate cheat codes
cheat_codes = [cheatcode(['L', 'E', 'O'], "increase radius"), cheatcode(
    ['U', 'J'], "boulder positive"), cheatcode(['T', 'V'], "show lights")]


def init_maze():
    ''' Function to initialise the maze dictionary'''
    global maze
    for x in range(maze_width):
        for y in range(maze_height):
            # Each cell starts with all walls intact and is unvisited
            cell = {
                'visited': False,
                'walls': {
                    'top': True,
                    'right': True,
                    'bottom': True,
                    'left': True
                }
            }
            # Add the cell to the maze dictionary with (x, y) as the key
            maze[(x, y)] = cell


# define the movements needed to remove walls (because we go from to to
# bottom, the top is going below ( increasing y means going down the
# screen)
directions = {'top': (0, -1, 'bottom'), 'right': (1, 0, 'left'),
              'bottom': (0, 1, 'top'), 'left': (-1, 0, 'right')}


def generate_maze(x, y):
    '''  function generates maze using DFS'''
    # Mark cell as visited
    maze[(x, y)]['visited'] = True
    # convert the dictioanry into a list so we can shuffle the order in which
    # the walls will be accessed
    dir_keys = list(directions.keys())
    random.shuffle(dir_keys)

    # for all the walls, assign the neighbouring x-y co-rds
    for direction in dir_keys:
        dx, dy, opposite = directions[direction]
        nx, ny = x + dx, y + dy

        # Check if the neighbouring cell is within the maze bounds and
        # unvisited
        if 0 <= nx < maze_width and 0 <= ny < maze_height and not maze[(
                nx, ny)]['visited']:

            # Remove the wall between the current cell and the neighbor
            maze[(x, y)]['walls'][direction] = False
            maze[(nx, ny)]['walls'][opposite] = False

            # Recursively visit the neighbouring cell. The recursion will
            # recurse back to the previous cell once it reaches a cell that it
            # has visited or a cell that is on the edge
            generate_maze(nx, ny)


def draw_maze():
    ''' This function draws the maze on the canvas '''
    # for all the cells on the grid
    for x in range(maze_width):
        for y in range(maze_height):
            # call the function to draw the cell
            draw_single_cell(x, y)


def draw_single_cell(x, y):
    """Draws the walls of a single cell."""
    global maze
    cell = maze[(x, y)]
    # calcuate the pixel co-ordinates needed
    # add 10 because I was having issues where it was drawing outside of the
    # canvas
    top_left_x = x * cell_size + 10
    top_left_y = y * cell_size + 10
    bottom_right_x = top_left_x + cell_size
    bottom_right_y = top_left_y + cell_size

    # Draw each wall if it exists
    if cell['walls']['top']:
        canvas.create_line(
            top_left_x,
            top_left_y,
            bottom_right_x,
            top_left_y,
            fill="white",
            tags="maze_cells")
    if cell['walls']['right']:
        canvas.create_line(
            bottom_right_x,
            top_left_y,
            bottom_right_x,
            bottom_right_y,
            fill="white",
            tags="maze_cells")
    if cell['walls']['bottom']:
        canvas.create_line(
            top_left_x,
            bottom_right_y,
            bottom_right_x,
            bottom_right_y,
            fill="white",
            tags="maze_cells")
    if cell['walls']['left']:
        canvas.create_line(
            top_left_x,
            top_left_y,
            top_left_x,
            bottom_right_y,
            fill="white",
            tags="maze_cells")


def is_valid_move(new_x, new_y, obj_x, obj_y):
    '''Function to check if the move is valid (no wall collision)'''
    # check if it is in the maze
    if 0 <= new_x < maze_width and 0 <= new_y < maze_height:
        # Check if there is a wall in the direction of movement
        if new_x != obj_x:
            if new_x > obj_x:
                return not (maze[(obj_x, obj_y)]['walls']['right'])
            elif new_x < obj_x:
                return not (maze[(obj_x, obj_y)]['walls']['left'])
        if new_y != obj_y:
            if new_y > obj_y:
                return not (maze[(obj_x, obj_y)]['walls']['bottom'])
            elif new_y < obj_y:
                return not (maze[(obj_x, obj_y)]['walls']['top'])
    return False


def draw_miner(current_x, current_y):
    ''' Draw the miners current position on the maze '''
    global miner_image
    # Check if miner is drawn
    if canvas.find_withtag("miner"):
        # update its position instead of creating a new one
        canvas.coords(
            "miner",
            current_x,
            current_y,
        )
    else:
        # If the miner hasn't been drawn yet, create it
        # source =
        # https://www.freepik.com/free-vector/set-miner-man-working
        # -cartoon-character-collection-isolated-illustration_12953
        # 332.htm#fromView=search&page=1&position=44&uuid=893ad0bc-
        # 9b13-418e-9874-b0a4e049fb74
        original = Image.open('miner.png')
        # resize the image
        resized_image = original.resize((30, 30))
        # convert to tkinter compatible
        miner_image = ImageTk.PhotoImage(resized_image)
        canvas.create_image(
            current_x,
            current_y,
            image=miner_image, tags="miner"
        )


def move_miner(event):
    '''move  miner based on key stroke '''
    move_x, move_y = 0, 0,
    global miner_x, miner_y, is_handling_key, pause

    if not pause:
        # If we're already handling a key, ignore additional moves
        if is_handling_key:
            return

        is_handling_key = True
        # Determine which direction to move based on the key pressed
        if event.keysym in keybinds['Left']:
            move_x = -1
        elif event.keysym in keybinds['Right']:
            move_x = 1
        elif event.keysym in keybinds['Up']:
            move_y = -1
        elif event.keysym in keybinds['Down']:
            move_y = 1

        # Check if the new position is valid (not a wall)
        if is_valid_move(miner_x + move_x, miner_y + move_y, miner_x, miner_y):

            new_x = miner_x + move_x
            new_y = miner_y + move_y
            move_smoothly(new_x, new_y)
            # check if the miner is on a light bulb
            for obj in lights:
                obj.found()
            # check if the miner has hit a boulder
            for obj in boulders:
                obj.collision()
        root.after(50, reset_key_handling)


def reset_key_handling():
    global is_handling_key
    is_handling_key = False


def draw_vision_circle():
    """removes current vison circle and creates a new one """

    # get the centre of the miners position
    center_x = miner_x * cell_size + cell_size // 2 + 10
    center_y = miner_y * cell_size + cell_size // 2 + 10

    # Clear canavs to redraw the maze
    if canvas.find_withtag('maze_cells'):
        canvas.delete("maze_cells")

    canvas.delete('miner')
    # Draw only the cells within the vision radius
    for x in range(maze_width):
        for y in range(maze_height):
            # find the centre of the current cell
            cell_x = x * cell_size + cell_size // 2 + 10
            cell_y = y * cell_size + cell_size // 2 + 10

            # Calculate the distance of the cell from the miner using euclidean
            # distance
            distance = ((center_x - cell_x) ** 2 +
                        (center_y - cell_y) ** 2) ** 0.5

            # check if it should be in the visability radius anf so, draw the
            # block
            if distance <= vision_radius:
                draw_single_cell(x, y)

        # target pixel position
        target_x = miner_x * cell_size + cell_size // 2 + 10
        target_y = miner_y * cell_size + cell_size // 2 + 10

    draw_miner(target_x, target_y)

    for obj in boulders:
        obj.draw()


def move_smoothly(new_x, new_y):
    '''Funciton that moves the miner smoothly'''
    global miner_x, miner_y
    # current pixel position of the miner
    current_x = miner_x * cell_size + cell_size // 2 + 10
    current_y = miner_y * cell_size + cell_size // 2 + 10

    # calculate the difference between the current and target pixel position
    change_x = new_x * cell_size + cell_size // 2 + 10 - current_x
    change_y = new_y * cell_size + cell_size // 2 + 10 - current_y

    # Calculate the increment for each step
    step_x = change_x / 2
    step_y = change_y / 2

    # Move the miner incrementally (10 steps for smooth movement)
    def update_position(step=0):
        nonlocal current_x, current_y

        if step < 2:
            current_x += step_x
            current_y += step_y

            canvas.delete('miner')
            draw_miner(current_x, current_y)

            # Schedule the next update after 30ms
            root.after(30, update_position, step + 1)
        else:
            # last one
            global miner_x, miner_y
            miner_x = new_x
            miner_y = new_y
            draw_vision_circle()
            # draw the boulders
            for obj in boulders:
                obj.draw()

    # Start the movement animation
    update_position()


def start():
    ''' Start menu to allow user to start the game'''
    global name, animation_running
    animation_running = True
    # Hide the root window while starting the game
    root.withdraw()
    # create a new top level screen
    start_game = tk.Toplevel(root)
    start_game.title('Lights Out')
    start_game.attributes('-fullscreen', True)

    # Create a canvas to place the moving shapes
    canvas = tk.Canvas(start_game, width=300, height=300, bg="black")
    canvas.pack(fill="both", expand=True)

    # Call the function to animate shapes
    animate_shapes(canvas)

    # Add welcome text and instructions to the canvas
    canvas.create_text(
        canvas.winfo_screenwidth() // 2,
        50,
        text="Welcome to Lights Out!",
        font=("Papyrus", 30, "bold"),
        fill="white"
    )
    canvas.create_text(
        canvas.winfo_screenwidth() // 2,
        100,
        text="Use your arrow keys to navigate the maze.",
        font=("Papyrus", 20),
        fill="white"
    )
    canvas.create_text(
        canvas.winfo_screenwidth() // 2,
        140,
        text=(
            "Navigate carefully to avoid the boulders, "
            "as they will dim your light. "
            "Collect all 10 candles to advance to the next level."
        ),
        font=("Papyrus", 20),
        fill="white",
    )

    canvas.create_text(
        canvas.winfo_screenwidth() // 2,
        180,
        text=(
            "Be cautious! The surrounding light will shrink unless you gather "
            "the candles!"
        ),
        font=("Papyrus", 20),
        fill="white",
    )

    # Create a text entry for the name
    canvas.create_text(
        canvas.winfo_screenwidth() // 2,
        240,
        text="Enter your name:",
        font=("Papyrus", 20),
        fill="white",
    )
    name = tk.Entry(
        start_game,
        font=(
            "Papyrus",
            16),
        highlightthickness=2,
        highlightbackground="white",
        highlightcolor="white",
        width=20)
    canvas.create_window(canvas.winfo_screenwidth() // 2, 280, window=name)

    # Common button style
    button_style = {
        "font": ("Papyrus", 16, "bold"),
        "relief": "flat",
        "highlightthickness": 2,
        "highlightbackground": "white",
        "width": 20,
        "height": 2
    }

    # Start Game button
    start_button = tk.Button(
        start_game,
        text="Start Game",
        command=lambda: load_game(start_game),
        **button_style
    )
    canvas.create_window(canvas.winfo_screenwidth() //
                         2, 340, window=start_button)

    # View Leaderboard button
    leaderboard_button = tk.Button(
        start_game,
        text="View Leaderboard",
        **button_style,
        command=lambda: leaderboard(start_game),
    )
    canvas.create_window(canvas.winfo_screenwidth() // 2,
                         400, window=leaderboard_button)

    # Load Game Session button
    load_game_button = tk.Button(
        start_game,
        text="Load a Game Session",
        command=lambda: load_prev_game(start_game),
        **button_style

    )
    canvas.create_window(
        canvas.winfo_screenwidth() // 2,
        460,
        window=load_game_button)


def animate_shapes(canvas):
    ''' Function to animate moving shapes in the background on the canvas '''
    # Initialize shape positions and movement deltas
    shape1 = canvas.create_oval(50, 50, 100, 100, fill="red")
    shape2 = canvas.create_rectangle(200, 50, 300, 150, fill="green")
    shape3 = canvas.create_line(400, 50, 500, 150, width=5, fill="blue")

    # Movement for each shape
    shape1_dx, shape1_dy = 3, 2
    shape2_dx, shape2_dy = 2, 3
    shape3_dx, shape3_dy = 4, 1

    def move_shapes():
        ''' Move the shapes and check for boundary collisions '''
        nonlocal shape1_dx, shape1_dy
        nonlocal shape2_dx, shape2_dy, shape3_dx, shape3_dy
        global animation_running

        if not animation_running:  # Stop animation if the flag is False
            return

        # Move each shape
        canvas.move(shape1, shape1_dx, shape1_dy)
        canvas.move(shape2, shape2_dx, shape2_dy)
        canvas.move(shape3, shape3_dx, shape3_dy)
        # Get current positions
        x1, y1, x2, y2 = canvas.coords(shape1)
        x3, y3, x4, y4 = canvas.coords(shape2)
        x5, y5, x6, y6 = canvas.coords(shape3)

        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        # Check for boundary collisions and reverse direction if necessary
        if x1 < 0 or x2 > canvas_width:
            shape1_dx = -shape1_dx
        if y1 < 0 or y2 > canvas_height:
            shape1_dy = -shape1_dy

        if x3 < 0 or x4 > canvas_width:
            shape2_dx = -shape2_dx
        if y3 < 0 or y4 > canvas_height:
            shape2_dy = -shape2_dy

        if x5 < 0 or x6 > canvas_width:
            shape3_dx = -shape3_dx
        if y5 < 0 or y6 > canvas_height:
            shape3_dy = -shape3_dy

        # Continue the animation after 20ms
        canvas.after(20, move_shapes)

    # Start moving the shapes
    move_shapes()


def load_prev_game(start_game):
    ''' function to load a previous game session'''
    # get the animated backgorund
    global animation_running
    animation_running = True
    start_game.destroy()

    # create a new top level screen
    enter_id = tk.Toplevel(root)
    enter_id.title('Enter a session id')
    enter_id.attributes('-fullscreen', True)

    # Create a canvas to place the moving shapes
    canvas = tk.Canvas(enter_id, width=300, height=300, bg="black")
    canvas.pack(fill="both", expand=True)

    # Call the function to animate shapes
    animate_shapes(canvas)

    # Add message
    canvas.create_text(
        canvas.winfo_screenwidth() // 2,
        50,
        text='Please enter a sesssion ID below:',
        font=("Papyrus", 30, "bold"),
        fill="white"

    )

    # Allow user to enter their name
    id = tk.Entry(
        enter_id,
        font=(
            "Papyrus",
            16),
        highlightthickness=2,
        highlightbackground="white",
        highlightcolor="white",
        width=20)
    canvas.create_window(canvas.winfo_screenwidth() // 2, 150, window=id)
    id.focus_set()

    # Common button style
    button_style = {
        "font": ("Papyrus", 16, "bold"),
        "relief": "flat",
        "highlightthickness": 2,
        "highlightbackground": "white",
        "width": 20,
        "height": 2
    }

    # Submit
    submit = tk.Button(
        enter_id,
        text="Submit",
        command=lambda: verify_session(enter_id, id),
        **button_style
    )
    canvas.create_window(canvas.winfo_screenwidth() // 2, 250, window=submit)

    # back
    back = tk.Button(
        enter_id,
        text="Back to Start",
        command=lambda: back_to_start(enter_id),
        **button_style
    )
    canvas.create_window(canvas.winfo_screenwidth() // 2, 350, window=back)

    def verify_session(enter_id, id):
        ''' function to verify if the session id is valid '''
        # open the csv and check if the session id is there

        with open('saveAndLoad.csv', 'r') as file:
            session_id = id.get()
            reader = csv.reader(file)
            for row in reader:
                # if the session id exists, get the data
                if row[0] == session_id:
                    enter_id.destroy()
                    data = row
                    root.deiconify()
                    game(data)
                    break

            # if the session id does not exist, notify the user
            else:
                canvas.create_text(
                    canvas.winfo_screenwidth() // 2,
                    450,
                    text="Invalid ID",
                    font=("Papyrus", 20),
                    fill="red"
                )


def leaderboard(start_game):
    ''' Displays the leaderboard '''

    # get the animated backgorund
    global animation_running
    animation_running = True
    # get rid of home screen

    start_game.destroy()

    # open leaderboard window
    leaderboard_window = tk.Toplevel(root)
    leaderboard_window.title('Leaderboard')
    leaderboard_window.attributes('-fullscreen', True)

    # Create a canvas to place the moving shapes
    canvas = tk.Canvas(leaderboard_window, width=300, height=300, bg="black")
    canvas.pack(fill="both", expand=True)

    # Call the function to animate shapes
    animate_shapes(canvas)

    # Add message
    canvas.create_text(
        canvas.winfo_screenwidth() // 2,
        50,
        text='Top 5 scores',
        font=("Papyrus", 30, "bold"),
        fill="white"

    )

    # array to hold the scores
    results = []

    # chck if the file exists
    try:
        with open('leaderboard.csv', 'r') as file:
            # read the data as a dictionary
            data = csv.DictReader(file)
            # for every entry, add them to theresults array as a tuple
            for entry in data:
                results.append((entry['Name'], int(entry['Level'])))
    except FileNotFoundError:
        pass
    # Sort the leaderboard by score in descending order and take the top 5
    results = sorted(results, key=lambda x: x[1], reverse=True)[:5]

    # display all the results
    for i in range(len(results)):

        # Add message
        canvas.create_text(
            canvas.winfo_screenwidth() // 2,
            (100 * (i + 1)),
            text=f'Name: {results[i][0]}         Level: {results[i][1]}',
            font=("Papyrus", 30, "bold"),
            fill="white"
        )

    # Common button style
    button_style = {
        "font": ("Papyrus", 16, "bold"),
        "relief": "flat",
        "highlightthickness": 2,
        "highlightbackground": "white",
        "width": 20,
        "height": 2
    }

    # Button to exit
    exit = tk.Button(
        leaderboard_window,
        text="Exit",
        command=lambda: back_to_start(leaderboard_window),
        **button_style
    )
    canvas.create_window(canvas.winfo_screenwidth() // 2, 600, window=exit)


def back_to_start(window):
    ''' get rid of the leaderboard screen and return user to the start menu '''
    window.destroy()
    start()


def load_game(start_game):
    '''Function to load the game window'''
    global name
    name = name.get()
    # if empty set a default name
    if name.strip() == '':
        name = 'Player'

    # get rid of home screen and start the game screen
    start_game.destroy()
    root.deiconify()
    game()


def update_boulders():
    '''Update all boulders by calling their move() method repeatedly'''
    global pause
    if not pause:
        for boulder in boulders:
            boulder.move()  # Move each boulder
        # Schedule the next update (recursively call this function after 500
        # ms)
        root.after(boulder_speed, update_boulders)


def update_light():
    '''Update whether the light should be seen or not '''
    global lights
    if not pause:
        for light in lights:
            light.draw()
        # output the level

        # Schedule the next update (recursively call this function after 500
        # ms)
        root.after(light_speed, update_light)


def update_circle():
    ''' Make the vision circle smaller '''
    global vision_radius, lights, pause
    if not pause:
        vision_radius -= 1
        # Check if the game is ended
        if len(lights) > 0:
            if vision_radius >= 0:
                draw_vision_circle()
                root.after(circle_speed, update_circle)
            else:
                # end the game if the circle has closed in on the miner
                end_game()


def game(data=None):
    ''' function to set up the game'''
    global miner_x, miner_y, maze, canvas, level, name, num_boulders
    global vision_radius, boulders, lights, maze_height, maze_width, root
    # initialising the new canvas
    canvas.destroy()
    root.focus_force()
    lights = []
    boulders = []
    # if the game is not being loaded
    if data is None:
        # add the canvas to the window
        canvas = tk.Canvas(
            root,
            width=maze_width *
            cell_size +
            15,
            height=maze_height *
            cell_size +
            15,
            bg="black")
        canvas.pack()
        # clear the maze
        if len(maze) > 0:
            maze.clear()
        # initialise the new maze
        init_maze()
        # Start the maze generation from a random position
        generate_maze(
            random.randint(
                0,
                maze_width -
                1),
            random.randint(
                0,
                maze_height -
                1))
        # miner starting position
        miner_x, miner_y = random.randint(0, maze_width - 1), \
            random.randint(0, maze_height - 1)
        # Draw the generated maze
        draw_maze()
        # For each boulder, generate random coordinates and instantiate a
        # boulder object
        for obj in range(num_boulders):
            x = random.randint(0, maze_width - 1)
            y = random.randint(0, maze_height - 1)
            boulder_instance = boulder(x, y)
            boulders.append(boulder_instance)

        # For each light, generate random coordinates and instantiate a light
        # object
        for obj in range(num_lights):
            x = random.randint(0, maze_width - 1)
            y = random.randint(0, maze_height - 1)
            light_instance = light(x, y)
            lights.append(light_instance)
    # if it is a game being loaded
    else:
        # get the variables stored
        name = data[1]
        level = int(data[2])
        maze = ast.literal_eval(data[3])
        miner_x = int(data[4])
        miner_y = int(data[5])
        num_boulders = int(data[6])
        boulders_data = ast.literal_eval(data[7])
        lights_data = ast.literal_eval(data[8])
        vision_radius = int(data[9])
        maze_height = int(data[10])
        maze_width = int(data[11])
        # add the canvas to the window
        canvas = tk.Canvas(
            root,
            width=maze_width *
            cell_size +
            15,
            height=maze_height *
            cell_size +
            15,
            bg="black")
        canvas.pack()

        # instantiate the boulders
        for obj in boulders_data:
            boulder_instance = boulder(obj[0], obj[1])
            boulders.append(boulder_instance)
        # instantiate the lights
        for obj in lights_data:
            light_instance = light(obj[0], obj[1])
            lights.append(light_instance)

    current_x = miner_x * cell_size + cell_size // 2 + 10
    current_y = miner_y * cell_size + cell_size // 2 + 10
    # draw miner
    draw_miner(current_x, current_y)

    # output the level
    canvas.create_text(
        50, 20,
        text=f"Level: {level}",
        font=("Papyrus", 16),
        fill="white"
    )
    # Set the initial size of the root window
    root.geometry(
        f"{maze_width * cell_size + 15}x{maze_height * cell_size + 15}")

    # Make the root window non-resizable
    root.resizable(False, False)
    # call the functions to startthe moving objects
    update_circle()
    update_boulders()
    update_light()
    # Create the initial text object
    text_id = canvas.create_text(
        70, 40,
        text=f"Candles: {len(lights)}",
        font=("Papyrus", 16),
        fill="white"
    )

    # Function to update the text
    def light_counter(canvas, text_id):
        '''Update the light counter variable'''
        global lights

        # Update the text on the canvas
        canvas.itemconfig(text_id, text=f"Candles: {len(lights)}")

        if len(lights) != 0:
            # Schedule the next update
            root.after(light_speed, lambda: light_counter(canvas, text_id))
        else:
            return

    # Start the light counter
    light_counter(canvas, text_id)


def end_game():
    ''' End the game and display a Game Ended window'''
    global maze_width, maze_height, num_boulders, penalty, level, name
    global vision_radius, animation_running
    animation_running = True
    # Close the game
    root.withdraw()
    # Create a new window to display the Game Ended message
    game_ended = tk.Tk()
    game_ended.title("Game Ended")
    game_ended.attributes('-fullscreen', True)

    # Create a canvas to place the moving shapes
    canvas = tk.Canvas(game_ended, width=300, height=300, bg="black")
    canvas.pack(fill="both", expand=True)

    # Call the function to animate shapes
    animate_shapes(canvas)

    # Display the Game Ended message

    # Add message
    canvas.create_text(
        canvas.winfo_screenwidth() // 2,
        50,
        text='Game ended',
        font=("Papyrus", 30, "bold"),
        fill="white"
    )
    # store the users game session in the leaderbosrd file
    with open('leaderboard.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, level])
    # rest all the variables for the next game session
    maze_width, maze_height, num_boulders, penalty = 10, 10, 4, 25
    level, name, vision_radius = 1, None, 100

    # Add a Quit button to close the application

    # Common button style
    button_style = {
        "font": ("Papyrus", 16, "bold"),
        "relief": "flat",
        "highlightthickness": 2,
        "highlightbackground": "white",
        "width": 20,
        "height": 2
    }

    # Exit button
    exit = tk.Button(
        game_ended,
        text="Exit",
        command=lambda: [game_ended.destroy(), start()],
        **button_style
    )
    canvas.create_window(canvas.winfo_screenwidth() // 2, 340, window=exit)


def check_win():
    global animation_running
    '''Check if the user has won the game'''
    if len(lights) == 0:

        root.withdraw()
        # Create a new window to display next message
        level_completed = tk.Tk()
        level_completed.title("Level Completed")
        level_completed.attributes('-fullscreen', True)
        animation_running = True
        # Create a canvas to place the moving shapes
        canvas = tk.Canvas(level_completed, width=300, height=300, bg="black")
        canvas.pack(fill="both", expand=True)
        # Call the function to animate shapes
        animate_shapes(canvas)
        # Display the level completed message
        canvas.create_text(
            canvas.winfo_screenwidth() // 2,
            50,
            text="Well done, you completed this level succesfully",
            font=("Papyrus", 30, "bold"),
            fill="white"
        )

        # Common button style
        button_style = {
            "font": ("Papyrus", 16, "bold"),
            "relief": "flat",
            "highlightthickness": 2,
            "highlightbackground": "white",
            "width": 20,
            "height": 2
        }

        # Exit button
        next = tk.Button(
            level_completed,
            text="Next Level",
            command=lambda: [level_completed.destroy(), next_level()],
            **button_style
        )
        canvas.create_window(canvas.winfo_screenwidth() // 2, 340, window=next)


def next_level():
    ''' adjust the parameters so that the gaem is harder now '''
    # increase the number of boulders,penalty for getting hit by a boulder,
    # maze_height, maze_width
    global num_boulders, penalty, maze_height, maze_width, vision_radius, level
    # next level
    level += 1
    # reset the radius
    vision_radius = 100
    # make the maze bigger
    maze_height += 2
    maze_width += 2
    # increase the number of boulders on the map and the penalty for getting
    # hit by one
    num_boulders += 2
    penalty += 5
    root.deiconify()
    game()


def toggle_pause(event=None):
    ''' function to toggle pause '''
    global pause, pause_menu
    pause = not pause
    pause_game()


def pause_game():
    global pause, pause_menu, root, animation_running
    ''' Pause meunu display '''

    # get the animated backgorund

    animation_running = True
    if pause:
        # Display pause window
        pause_menu = tk.Toplevel(root)
        pause_menu.title('Game Paused')
        pause_menu.attributes('-fullscreen', True)

        # Create a canvas to place the moving shapes
        canvas = tk.Canvas(pause_menu, width=300, height=300, bg="black")
        canvas.pack(fill="both", expand=True)

        # Call the function to animate shapes
        animate_shapes(canvas)

        # pause message
        canvas.create_text(
            canvas.winfo_screenwidth() // 2,
            50,
            text='Paused',
            font=("Papyrus", 30, "bold"),
            fill="white"
        )
        # Common button style
        button_style = {
            "font": ("Papyrus", 16, "bold"),
            "relief": "flat",
            "highlightthickness": 2,
            "highlightbackground": "white",
            "width": 20,
            "height": 2
        }

        # resume
        resume = tk.Button(
            pause_menu,
            text="Resume",
            command=toggle_pause,
            **button_style
        )
        canvas.create_window(
            canvas.winfo_screenwidth() // 2,
            340,
            window=resume)

        # changw binds  button
        changeBinds = tk.Button(
            pause_menu,
            text="Change binds",
            command=lambda: change_binds(pause_menu),
            **button_style
        )
        canvas.create_window(canvas.winfo_screenwidth() //
                             2, 440, window=changeBinds)

        # Start Game button
        saveExit = tk.Button(
            pause_menu,
            text="Save and Exit game",
            command=lambda: save_exit(pause_menu),
            **button_style
        )
        canvas.create_window(
            canvas.winfo_screenwidth() // 2,
            540,
            window=saveExit)

        pause_menu.bind('p', toggle_pause)
    else:
        # destroy pause window and resume the game
        pause_menu.destroy()
        root.focus_force()
        # resume the moving objects again
        update_circle()
        update_boulders()
        update_light()


def change_binds(pause_menu):
    ''' function to change the binds '''
    global animation_running

    def capture_key(direction, change):
        ''' function tht trakes the users keystroke value'''
        global keybinds, animation_running
        change.destroy()

        def on_key_press(event):
            global keybinds
            nonlocal pause_menu
            # Capture the pressed key
            new_key = event.keysym
            # assign it to the dict
            if new_key not in keybinds.values():
                # bind both the upper and lower case characters
                root.bind(new_key.lower(), move_miner)
                root.bind(new_key.upper(), move_miner)
                keybinds[direction] = [new_key.lower(), new_key.upper()]
            prompt.destroy()  # Close the prompt after capturing the key
            change_binds(pause_menu)

        # Create a prompt window
        prompt = tk.Toplevel(root)
        prompt.title("Press a Key")
        prompt.attributes('-fullscreen', True)

        # Create a canvas to place the moving shapes
        canvas = tk.Canvas(prompt, width=300, height=300, bg="black")
        canvas.pack(fill="both", expand=True)

        # Call the function to animate shapes
        animate_shapes(canvas)

        # Add message
        canvas.create_text(
            canvas.winfo_screenwidth() // 2,
            50,
            text='Press a key to bind',
            font=("Papyrus", 30, "bold"),
            fill="white"

        )

        # Bind keypress to the movement
        prompt.bind("<Key>", on_key_press)
        # puts the focus on the bind window
        prompt.focus_set()

    animation_running = True

    #  create the window to remap the binds
    change = tk.Toplevel(root)
    change.title('Re-map your keybinds')
    change.attributes('-fullscreen', True)

    # Create a canvas to place the moving shapes
    canvas = tk.Canvas(change, width=300, height=300, bg="black")
    canvas.pack(fill="both", expand=True)
    # Call the function to animate shapes
    animate_shapes(canvas)
    # Common button style
    button_style = {
        "font": ("Papyrus", 16, "bold"),
        "relief": "flat",
        "highlightthickness": 2,
        "highlightbackground": "white",
        "width": 20,
        "height": 2
    }

    left = tk.Button(
        change,
        text="Remap Left",
        command=lambda: capture_key('Left', change),
        **button_style
    )
    canvas.create_window(canvas.winfo_screenwidth() // 2, 50, window=left)

    right = tk.Button(
        change,
        text="Remap Right",
        command=lambda: capture_key('Right', change),
        **button_style
    )
    canvas.create_window(canvas.winfo_screenwidth() // 2, 150, window=right)

    up = tk.Button(
        change,
        text="Remap Up",
        command=lambda: capture_key('Up', change),
        **button_style
    )
    canvas.create_window(canvas.winfo_screenwidth() // 2, 250, window=up)

    down = tk.Button(
        change,
        text="Remap Down",
        command=lambda: capture_key('Down', change),
        **button_style
    )
    canvas.create_window(canvas.winfo_screenwidth() // 2, 350, window=down)

    exit = tk.Button(
        change,
        text="Exit",
        command=lambda: back_to_menu(change),
        **button_style
    )
    canvas.create_window(canvas.winfo_screenwidth() // 2, 450, window=exit)


def back_to_menu(change):
    ''' close the keybinds window and return user back to pause menu'''
    change.destroy()
    toggle_pause()


def save_exit(pause_menu):
    ''' Function to save and exit the game '''
    pause_menu.destroy()

    global maze, miner_x, miner_y, name, level, vision_radius, maze_height
    global maze_width, name, num_boulders, penalty, pause, animation_running
    # array to store the data about the boulder
    boulders_data = []
    # for each boulder, store the x and y co-ord of the object
    for obj in boulders:
        x, y = obj.get_position()
        boulders_data.append([x, y])
    lights_data = []
    # for each light, store the x and y co-ord of the object
    for obj in lights:
        x, y = obj.get_position()
        lights_data.append([x, y])

    def generate_session():
        '''generate a 16 digit session id '''
        unique = True
        session_id = random.randint(10**15, 10**16 - 1)
        with open('saveAndLoad.csv', 'r') as file:
            reader = csv.reader(file)

            # iterate through each row
            for row in reader:
                # Check if the first column matches the value
                if row[0] == session_id:
                    unique = False
        # check if it is in fact unique
        if not unique:
            generate_session()
        else:
            return session_id

    session_id = generate_session()

    # genrate a session id
    with open('saveAndLoad.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([session_id,
                         name,
                         level,
                         maze,
                         miner_x,
                         miner_y,
                         num_boulders,
                         boulders_data,
                         lights_data,
                         vision_radius,
                         maze_height,
                         maze_width])

    # initialise the starting variables

    maze_width, maze_height, num_boulders, penalty = 10, 10, 4, 25
    level, name, vision_radius, pause = 1, None, 100, False

    animation_running = True

    id_window = tk.Toplevel(root)
    id_window.title('Uniqu ID')
    id_window.attributes('-fullscreen', True)

    # Create a canvas to place the moving shapes
    canvas = tk.Canvas(id_window, width=300, height=300, bg="black")
    canvas.pack(fill="both", expand=True)
    # Call the function to animate shapes
    animate_shapes(canvas)

    canvas.create_text(
        canvas.winfo_screenwidth() // 2,
        50,
        text='Write down this unique game session ID',
        font=("Papyrus", 30, "bold"),
        fill="white"

    )

    canvas.create_text(
        canvas.winfo_screenwidth() // 2,
        150,
        text=(
            "If you lose this session id, "
            "you will not be able to continue this "
            "game session"
        ),
        font=("Papyrus", 30, "bold"),
        fill="white",
    )

    canvas.create_text(
        canvas.winfo_screenwidth() // 2,
        250,
        text=session_id,
        font=("Papyrus", 30, "bold"),
        fill="white"
    )

    # Common button style
    button_style = {
        "font": ("Papyrus", 16, "bold"),
        "relief": "flat",
        "highlightthickness": 2,
        "highlightbackground": "white",
        "width": 20,
        "height": 2
    }

    # Start Game button
    back = tk.Button(
        id_window,
        text="Back",
        command=lambda: back_to_start(id_window),
        **button_style
    )
    canvas.create_window(canvas.winfo_screenwidth() // 2, 350, window=back)


def control_boss_key(event):
    ''' function to control the boss key '''
    global boss_key, boss, background_image

    boss_key = not boss_key

    if boss_key:
        # Create boss window
        boss = tk.Toplevel(root)
        boss.title('Definitely Doing Work')
        boss.attributes('-fullscreen', True)

        # Create a canvas to place the background image
        canvas = tk.Canvas(boss)
        canvas.pack(fill="both", expand=True)
        boss.focus_set()

        # Open and resize the image
        screen_width = boss.winfo_screenwidth()
        screen_height = boss.winfo_screenheight()
        img = Image.open('boss.png')

        # Resize the image to fit the screen
        img_resized = img.resize(
            (screen_width, screen_height), Image.ANTIALIAS)
        # Convert to Tkinter PhotoImage and keep a reference
        background_image = ImageTk.PhotoImage(img_resized)

        # Add the image to the canvas
        canvas.create_image(0, 0, anchor="nw", image=background_image)
        # Pause the game
        toggle_pause()
        # bind the boss key
        boss.bind('b', control_boss_key)
    else:
        boss.destroy()
        toggle_pause()


def on_key_press(event):
    ''' Bind the key press events to check for cheat codes '''
    for cheat_code in cheat_codes:
        cheat_code.check_input(event)


# button to change binds
# Bind the arrow keys to move the miner
root.bind("<Left>", move_miner)
root.bind("<Right>", move_miner)
root.bind("<Up>", move_miner)
root.bind("<Down>", move_miner)
root.bind('p', toggle_pause)
root.bind('P', toggle_pause)
root.bind('b', control_boss_key)
root.bind('B', control_boss_key)
root.bind("<KeyPress>", on_key_press)


# Main execution
if __name__ == "__main__":

    start()
    root.mainloop()
