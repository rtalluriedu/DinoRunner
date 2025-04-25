from tkinter import *
import time, random
from Obstacles import Obstacles
from Dino import Dino

class DinoGame:
    
    #-------------------------------------------------------------------------
    # Initialization and Setup
    #-------------------------------------------------------------------------
    
    def __init__(self, root, nrow, ncol, scale):
        self.root = root
        self.nrow = nrow
        self.ncol = ncol
        self.scale = scale
        #setter/getter methods
        self.__game_over = False
        self.__pause = False
        self.__started = False
        self.__score = 0
        self.__pause_time = 0
        self.__next_spawn_time = random.uniform(1,3) + time.time() #spawns obstacle at a radnom interval between 1-3 secs
        
        self.__start_msg = self.__canvas.create_text( #start message displayed
            ncol*scale/2, nrow*scale/2,
            text="Hit 'S' to start game", 
            font=('Times', 25)
        )
        
        #initialize dino and obstacle classes
        self.__obstacles = [] #empty list to store obstacles
        self.__dino = Dino(self.__canvas, 20, nrow-10, scale)
        
        
    #-------------------------------------------------------------------------
    # Game State Methods
    #-------------------------------------------------------------------------
    
    def is_game_over(self):
        return self.__game_over
    
    
    def set_game_over(self, value):
        self.__game_over = value
    
        
    def is_pause(self):
        return self.__pause
    
    
    def set_pause(self, value):
        self.__pause = value
   
        
    def is_started(self):
        return self.__started
    
    
    def set_started(self, value):
        self.__started = value
      
        
    def get_next_spawn_time(self):
        return self.__next_spawn_time
    
    
    def set_next_spawn_time(self, value):
        self.__next_spawn_time = value
     
        
    def get_score(self):
        return self.__score
    
    
    def set_score(self, value):
        self.__score = value
    
        
    def get_pause_time(self):
        return self.__pause_time
    
    
    def set_pause_time(self, value):
        self.__pause_time = value
    
    #-------------------------------------------------------------------------
    # Game Logic
    #-------------------------------------------------------------------------
    
    def start_game(self):
        if self.is_game_over is False and self.is_started is False:
            self.__canvas.delete(self.__start_msg)
            self.__score = 0 #set score to 0
            self.__started = True #start game
            print("Game started.")
            self.__start_time = time.time() #record time from start

    
    def next(self):
        pass

    
    def check_collision(self):
        pass
    # Remove the pass statement and implement the check_collision method as described in the PDF.
    

    def jump(self):
        pass
    # Remove the pass statement and implement the jump method as described in the PDF.


    def pause(self):
        pass
    # Remove the pass statement and implement the pause method as described in the PDF.

    def update_survival_score(self):
        pass
    # Remove the pass statement and implement the update_survival_score method as described in the PDF.


#=============================================================================
# Main Game Runner - DO NOT MODIFY
#=============================================================================

def update_obstacles(game, root):
    if not game.is_pause() and (game.is_started() or game.is_game_over()):
        game.next()  # Unified method with feature flag
            
        if game.is_game_over():
            return  # Don't schedule another update if game is over
    
    # Schedule next update (50ms = 20 FPS)
    root.after(50, update_obstacles, game, root)

def main():
    """
    Main function to set up and run the game.
    """
    # Create the main window
    root = Tk()
    root.title("Dino Run Game")
    
    # Create the game instance
    game = DinoGame(root, nrow=80, ncol=160, scale=10)

    # Set up key bindings
    root.bind("<space>", lambda e: game.jump())
    root.bind("<p>", lambda e: game.pause())
    root.bind("<s>", lambda e: game.start_game())
    
    # Start the game loop
    root.after(10, update_obstacles, game, root)
    
    # Start Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
