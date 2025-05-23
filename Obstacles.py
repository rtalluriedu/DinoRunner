from tkinter import *
from Pixel import Pixel
import random
import numpy as np

class Obstacles:
    def __init__(self, canv, nrow, ncol, scale, c=2, pattern=None):
        """Initialize an obstacle with basic properties"""
        self.canv = canv
        self.nrow = nrow  # canvas rows
        self.ncol = ncol  # canvas columns
        self.scale = scale # pixel block size
        self.c = c # color
        self.pattern = pattern # pattern/shape for obstcale
        self.pixels = []

        self.i = 0
        self.j = 0  
        self.w = 0  
        self.h = 0 

        self.speed = 0

    def activate(self):
        """Create the obstacle on the canvas using Pixel objects"""
        if self.pattern is None:
            return  # Only used when given a pattern
        
        pattern_array = np.array(self.pattern) #makes pattern an array in numpy
        self.h, self.w = pattern_array.shape
        self.i = (self.nrow * (3/4)) + 5  #Middle in terms of verticality
        self.j = self.ncol  # puts object to the right
        
        for r in range(self.h):  
            for c in range(self.w):  
                if pattern_array[r, c] != 0: #create new pixel if not empty
                    new_pixel = Pixel(
                        canv=self.canv,
                        i=self.i + r,  # Correct row position
                        j=self.j + c,  # Correct column position
                        nrow=self.nrow,
                        ncol=self.ncol,
                        scale=self.scale,
                        icolor=self.c,  # Color of the obstacle
                        vector=[0,0]  # Added default vector
                    )
                    self.pixels.append(new_pixel)

      
    def left(self, score):
        '''Moves the obstacle left by a certain speed based on the score.'''

        # DETERMINES SPEED BASED ON SCORE #
        
        if 0 <= score < 150:
            self.speed = 1
        elif 150 <= score < 300:
            self.speed = 2
        elif 300 <= score < 500:
            self.speed = 4
        elif 500 <= score < 1000:
            self.speed = 8

        # MOVES THE OBSTACLE LEFT #

        self.j -= self.speed # set position
        for pixel in self.pixels:
            pixel.delete() # remove current obstacle
            pixel.j -= self.speed # update postion
            pixel.id = self.canv.create_rectangle( # remake obstacle in new position
                pixel.j * self.scale,
                pixel.i * self.scale,
                (pixel.j + 1) * self.scale,
                (pixel.i + 1) * self.scale,
                fill=Pixel.color[self.c],
                outline='black'
            )

    @staticmethod
    def random_select(canv, nrow, ncol, scale): # randonly pick and make one of the obstacles
        obstacle_choices = [Box, Tree, Pencil]
        chosen_type = random.choice(obstacle_choices)
        return chosen_type(canv, nrow, ncol, scale)



#=============================================================================
# All Child Classes
#=============================================================================

class Box(Obstacles):
    def __init__(self, canv, nrow, ncol, scale):
        pattern = [
            [0, 0, 0, 0],
            [2, 2, 2, 0],
            [2, 2, 2, 0],
            [2, 2, 2, 0]
        ]
        super().__init__(canv, nrow, ncol, scale, c=2, pattern=pattern)
        

class Tree(Obstacles):
    def __init__(self, canv, nrow, ncol, scale):
        pattern = [
            [0, 0, 0, 0],
            [3, 3, 3, 0],
            [3, 3, 3, 0],
            [0, 3, 0, 0]
        ]
        super().__init__(canv, nrow, ncol, scale, c=3, pattern=pattern)

        
class Pencil(Obstacles):
    def __init__(self, canv, nrow, ncol, scale):
        pattern = [
            [5, 0, 0, 0],
            [5, 0, 0, 0],
            [5, 0, 0, 0],
            [5, 0, 0, 0],
        ]
        super().__init__(canv, nrow, ncol, scale, c=4, pattern=pattern)


#=============================================================================
# Testing Functions for Obstacles Class - DO NOT MODIFY
#=============================================================================

def delete_all(canvas):
    """Clear all elements from the canvas."""
    canvas.delete("all")
    print("Canvas cleared")


def test1(root, canvas, nrow, ncol, scale):
    print("\nPress left arrow key to move the obstacle left\n")
    obs = Obstacles.random_select(canvas, nrow, ncol, scale)
    obs.activate()

    def left():
        obs.left()  # Move the obstacle left

    root.bind("<Left>", lambda e: left())  # Bind left arrow key to move obstacle

def test2(root, canvas, nrow, ncol, scale):
    obstacle = None  # Only one obstacle active at a time
    paused = False   # Pause flag
    print("\nPress 'p' to pause/resume the obstacle movement\n")

    def toggle_pause(event=None):
        nonlocal paused
        paused = not paused
        print("Paused" if paused else "Resumed")

    # Bind the "p" key to toggle pause
    root.bind("<p>", toggle_pause)

    def update():
        nonlocal obstacle, paused
        if not paused:
            if obstacle is None:
                obstacle = Obstacles.random_select(canvas, nrow, ncol, scale)
                obstacle.activate()
            else:
                obstacle.left()  # Move the obstacle one step left using your updated left() method
                # Check if the obstacle is completely off-screen
                if obstacle.j + obstacle.w <= 0:  # Clear the canvas when the obstacle leaves
                    obstacle = None
                    
        # Schedule the next update after 20 milliseconds (adjust as needed)
        root.after(20, update)

    update()  # Start the update loop


def main():
    """
    Main function to set up and run the obstacle testing interface.
    """
    root = Tk()
    root.title("Obstacle Test")
    nrow = 40
    ncol = 80
    scale = 10
    canvas = Canvas(root, width=ncol*scale, height=nrow*scale, bg="black")
    canvas.pack()

    # Key bindings
    root.bind("1", lambda e: test1(root, canvas, nrow, ncol, scale))
    root.bind("2", lambda e: test2(root, canvas, nrow, ncol, scale))
    root.bind("<d>", lambda e: delete_all(canvas))

    instructions = """
    Press '1' to simulate Dino Run obstacles moving left
    Press '2' to simulate Dino Run obstacles continuously moving left
    Press 'd' to clear the canvas
    """
    print(instructions)
    
    root.mainloop()

if __name__ == "__main__":
    main()
