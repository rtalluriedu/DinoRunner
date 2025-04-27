from tkinter import *
from Pixel import Pixel
import numpy as np

class Dino(Pixel):
    def __init__(self, canv, nrow, ncol, scale, c=2):
        '''initiates the dino object with the given parameters.'''
        self.canvas = canv
        self.i = nrow - (1 * scale)  # start at the bottom of the canvas
        self.j = ncol / 2 # start in the middle of the canvas
        self.nrow = nrow
        self.ncol = ncol
        self.scale = scale
        self.color = c  # set the color of the dino
        self.pattern = self.get_pattern()
        self.jumping = False


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

    def activate(self):
        '''iterates through the pattern array and creates pixel objects for every non-zero values'''
        dino_pixels = []
        
        for r in range(self.pattern.shape[0]):
            for c in range(self.pattern.shape[1]):
                if (self.pattern[r, c]) == 1:
                    pixel = Pixel(self.canvas,
                                 (self.i + r),
                                 (self.j + c),
                                 self.nrow,
                                 self.ncol,
                                 self.scale,
                                 self.color
                                 )
                    dino_pixels.append(pixel)

        self.dino_pixels = dino_pixels
    

    def down(self):
        '''moves the dino object down by one step.'''
        new_dino_pixels = []

        for pixel in reversed(self.dino_pixels):
            if pixel.i < self.nrow - .5 * self.scale: # check if the dino can move down
                pixel.delete() # delete the current dino
                pixel.i += 1 # move down
                pixel = Pixel(pixel.canvas,
                             pixel.i,
                             pixel.j,
                             self.nrow,
                             self.ncol,
                             self.scale,
                             self.color
                             ) # activate the dino at the new position
                new_dino_pixels.append(pixel)
            elif pixel.i >= self.nrow - .5 * self.scale: # check if the dino is at the bottom
                print("Dino at the bottom!")
                break

        self.dino_pixels = new_dino_pixels
    

    def up(self):
        '''moves the dino object up by one step.'''
        new_dino_pixels = []

        for pixel in self.dino_pixels:
            if pixel.i > .5 * self.scale: # check if the dino can move up
                pixel.delete() # delete the current dino
                pixel.i -= 1
                pixel = Pixel(pixel.canvas,
                              pixel.i, pixel.j,
                              self.nrow,
                              self.ncol,
                              self.scale, 
                              self.color
                              )
                new_dino_pixels.append(pixel)
            elif pixel.i <= .5 * self.scale: # check if the dino is at the top
                print("Dino at the top!")
                break

        self.dino_pixels = new_dino_pixels

    def jump(self):
        '''initiates a jump animation for the dinosaur'''
        if self.jumping == False: # check if the dino can jump
            self.jumping = True # set jumping to True

            for r in range(10):
                self.canvas.after(50, self.activate_jump(1)) # wait for 50 milliseconds
                self.canvas.update()

            for c in range(10):
                self.canvas.after(50, self.activate_jump(-1)) # wait for 50 milliseconds
                self.canvas.update()
                
        elif self.jumping == True: # check if the dino is already jumping
            print("Dino already jumping!")
            return

        self.jumping = False # set jumping to False
        
     # start the jump animation


    def activate_jump(self, step):
        '''moves the dino object up by a certain step and then back down'''
        if step == 1:
            self.up()
            
        elif step == -1:
            self.down()
     


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
    scale = 10
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
