from tkinter import *
from Pixel import Pixel
import numpy as np

class Dino(Pixel):
    def __init__(self, canv, nrow, ncol, scale, c=2):
        '''initiates the dino object with the given parameters.'''
        self.canvas = canv
        self.nrow = nrow
        self.ncol = ncol
        self.scale = scale
        self.color = Pixel.color[c]  # set the color of the dino
        self.pattern = self.get_pattern()
        self.i = 20  # start at the bottom of the canvas
        self.j = 40  # start in the middle of the canvas
        self.jumping = False
    # Remove the pass statement and implement the __init__ method as described in the PDF.


    def get_pattern(self):
        '''returns the pattern of the dino object as a numpy array.'''
        return np.array([[0, 0, 1, 1, 1, 1],
                         [0, 0, 1, 1, 0, 1],
                         [0, 0, 1, 1, 1, 1],
                         [0, 0, 1, 1, 0, 0],
                         [1, 0, 1, 1, 1, 1],
                         [1, 0, 1, 1, 0, 0],
                         [1, 1, 1, 1, 0, 0],
                         [0, 1, 0, 1, 0, 0],
                         [0, 1, 0, 1, 0, 0]])
    # Remove the pass statement and implement the get_pattern method as described in the PDF.


    def activate(self):
        '''iterates through the pattern array and creates pixel objects for every non-zero values'''
        for i in range(self.pattern):
            for j in range(i):
                if self.pattern[i, j] != 0:
                    # create a pixel object at the correct position
                    pixel = Pixel(self.canvas, self.i + i, self.j + j, self.nrow, self.ncol, self.scale, self.color)
            
    # Remove the pass statement and implement the activate method as described in the PDF.
        

    def down(self):
        '''moves the dino object down by one step.'''
        # check if the dino can move down
        if self.i < self.nrow - 1:
            # delete the current dino
            self.delete()
            # move down
            self.i += 1
            # activate the dino at the new position
            self.activate()
    # Remove the pass statement and implement the down method as described in the PDF.


    def up(self):
        '''moves the dino object up by one step.'''
        # check if the dino can move up
        if self.i > 0:
            # delete the current dino
            self.delete()
            # move up
            self.i -= 1
            # activate the dino at the new position
            self.activate()
    # Remove the pass statement and implement the up method as described in the PDF.


    def jump(self):
        '''initiates a jump animation for the dinosaur'''
        if self.jumping == False: # check if the dino can jump
            self.jumping = True # set jumping to True
            
        for r in range(10):
            self.activate_jump(1) # activate the jump method
            self.canvas.after(50) # wait for 20 milliseconds

        for c in range(10):
            self.activate_jump(-1)
            self.canvas.after(50) # wait for 20 milliseconds

        self.jumping = False # set jumping to False
        
     # start the jump animation
            
    # Remove the pass statement and implement the jump method as described in the PDF.


    def activate_jump(self, step):
        '''moves the dino object up by a certain step and then back down'''
        if step == 1:
            self.up()
            
        elif step == -1:
            self.down()
            
        
    # Remove the pass statement and implement the perform_jump method as described in the PDF.
    

#=============================================================================
# Testing Functions for Dinosaur Class - DO NOT MODIFY
#=============================================================================

def delete_all(canvas):
    canvas.delete("all")

def test1(root, canvas, nrow, ncol, scale):
    d = Dino(canvas, nrow, ncol, scale)
    # Activate the dino in the middle left of the canvas
    d.activate()
    
    # Bind only up and down arrow keys to test basic movement
    root.bind("<Up>", lambda e: d.up())
    root.bind("<Down>", lambda e: d.down())
    
    # Add a visual indicator for test1
    print("\nPress Up/Down arrow keys to move the dinosaur up and down.\n")

def test2(root, canvas, nrow, ncol, scale):
    d = Dino(canvas, nrow, ncol, scale)
    # Activate the dino in the middle of the canvas.
    d.activate()
    
    # Bind arrow keys to move the dino
    root.bind("<space>", lambda e: d.jump())  # Bind spacebar to jump

    print("\nPress Spacebar to make the dinosaur jump.\n")



def main():
    """Initialize the game window and start the application."""
    root = Tk()
    nrow = 40
    ncol = 80
    scale = 20
    canvas = Canvas(root, width=ncol * scale, height=nrow * scale, bg="black")
    canvas.pack()

    # Bind a key for clearing the canvas.
    root.bind("1", lambda e: test1(root, canvas, nrow, ncol, scale))
    root.bind("2", lambda e: test2(root, canvas, nrow, ncol, scale))
    root.bind("d", lambda e: delete_all(canvas))

    instructions = """
    Press '1' to test basic up/down movement.
    Press '2' to test jump movement.
    Press 'd' to clear the canvas.
    """
    print(instructions)

    root.mainloop()

if __name__ == "__main__":
    main()