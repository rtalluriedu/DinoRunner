
from tkinter import *
import time, random
from Obstacles import Obstacles
from Dino import Dino
from pygame import mixer

class DinoGame:
    
    #-------------------------------------------------------------------------
    # Initialization and Setup
    #-------------------------------------------------------------------------
    
    def __init__(self, root, nrow, ncol, scale):
        '''Initializes the game with the given parameters.'''

        ### SELF VARIABLES ###
        
        self.root = root
        self.nrow = nrow
        self.ncol = ncol
        self.scale = scale
        self.__canvas = Canvas(root, width=ncol*scale, height=nrow*scale, bg='white')
        self.__canvas.pack()

        ### SETTER / GETTER METHODS ### 

        self.__game_over = False
        self.__pause = False
        self.__started = False
        self.__score = 0
        self.__pause_time = 0
        self.__next_spawn_time = random.uniform(1,3) + time.time() # spawns obstacle at a radnom interval between 1-3 secs
        self.__high_score = 0 # initializing high score
        self.__score_display = None # initializing score display
        self.__high_score_display = None # initializing high score display
    
        ### CANVAS OBJECTS ###

        self.__score_display = self.__canvas.create_text(ncol * scale - 100, 20, # displays current score
                                                         text="Score: 0",
                                                         font=('Arial', 14),
                                                         fill='black',
                                                         anchor='ne')
        
        self.__high_score_display = self.__canvas.create_text(ncol * scale - 100, 40, # displays high score
                                                              text="High Score: 0",
                                                              font=('Arial', 14),
                                                              fill='black',
                                                              anchor='ne')

        self.__start_msg = self.__canvas.create_text((ncol * scale) / 2, (nrow * scale) / 2, # displays start message
                                                     text="Hit 'S' to start game", 
                                                     font=('Times', 25),
                                                     fill='black')
        
        ### INTIALIZE DINO OBJECT AND OBSTACLE LIST ###

        self.__obstacles = [] #empty list to store obstacles
        self.__dino = Dino(self.__canvas, self.nrow, self.ncol, self.scale)
        

        # vv remove comments to test sound files vv
        ''' 
        #sound files initializ
        mixer.init()
        self.jump_sound = mixer.Sound('jump.wav.wav')
        self.collision_sound = mixer.Sound('collision.flac')
        '''
        
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
        '''Starts the game.'''
        if not self.__started and not self.__game_over: # make sure game started
            self.__canvas.delete(self.__start_msg)  # take away begining message

            self.__score = 0
            self.__start_time = time.time()

            self.__dino.activate()  #makes dinosaur appear
            self.__canvas.itemconfig(self.__score_display, # resets score display
                                     text=f"Score: {self.__score}")
            
            self.__started = True
            print("Game started!")
        
        
    def next(self):
        '''Updates the game state.'''
        if not self.__started or self.__pause or self.__game_over: # make sure game is running
            return
        
        # UPDATES SCORE AND CHECKS FOR OBSTACLES #

        self.update_survival_score()

        current_time = time.time()

        if len(self.__obstacles) == 0 and current_time >= self.__next_spawn_time: # if no obstacles are present, create a new one and set next spawn time
            new_obstacle = Obstacles.random_select(self.__canvas, self.nrow, self.ncol, self.scale)
            new_obstacle.activate()
            self.__obstacles.append(new_obstacle)

            self.__next_spawn_time = current_time + random.uniform(1, 3) # new obstacles every 1-3s

        # MOVES OBSTACLES #

        for obstacle in self.__obstacles: # move obstacles
            obstacle.left(self.__score) # move obstacles left

        # CHECKS FOR COLLISION #

        collision = self.check_collision(self.__obstacles) # check for collision with dino and obstacles
        
        if collision:
            self.collision_sound.play()

            if self.__score > self.__high_score:
                self.__high_score = self.__score # updates high score if recent score is greater than previous high score

            self.__canvas.create_text(self.ncol * self.scale / 2,
                                          self.nrow * self.scale / 2 - 30,
                                          text=f"Final Score: {self.__score}",
                                          font=('Times', 20),
                                          fill='black')
            self.__canvas.create_text(self.ncol * self.scale / 2,
                                          self.nrow * self.scale / 2,
                                          text="GAME OVER",
                                          font=('Times', 30),
                                          fill='red')
            self.__game_over = True
            return

        # REMOVES OFF SCREEN OBSTACLES #
                
        for obstacle in self.__obstacles[:]: # checks for and removes any off screen obstacles
            if obstacle.j + obstacle.w < 0:
                for pixel in obstacle.pixels:
                    pixel.delete()
                self.__obstacles.remove(obstacle)
            continue

    
    def check_collision(self, obstacles):
        '''Checks if the dino collides with any obstacles.'''
        for obstacle in obstacles: 
            for dino_pixel in self.__dino.dino_pixels:
                for pixel in obstacle.pixels:
                    if (dino_pixel.i == pixel.i and #check if dino/obstacle pixels are overlapping
                        dino_pixel.j == pixel.j):
                        print("Collision detected!")
                        return True  # returns true if overlap
        return False # returns false if no overlap
    

    def jump(self):
        '''Calls for the dino to jump.'''
        if self.__started and not self.__game_over and not self.__dino.jumping: # make sure game is running
            self.__dino.jump()
            self.jump_sound.play()


    def pause(self):
        '''Pauses or resumes the game.'''
        if not self.__started: # pause if game has started
            return
        
        if not self.__pause:
            self.__pause = True
            self.__pause_start = time.time() # track time of pause
            print("Game paused")

        else: #resumes game
            self.__pause = False
            pause_duration = time.time() - self.__pause_start #make up for paused game so timer is consitent
            self.__start_time += pause_duration
            print("Game resumed")


    
    def update_survival_score(self):
        '''Updates the score based on survival time.'''

        # UPDATE SCORE #

        if self.__started and not self.__pause and not self.__game_over:
            current_time = time.time()
            seconds_survived = current_time - self.__start_time  # keep as float for more precision
            base_score = int(seconds_survived * 10)  # multiply to make score increase faster
            bonus_multiplier = 1.0 + 0.1 * (int(seconds_survived)) // 30  # bonus every 30 seconds
            self.__score = int(base_score * bonus_multiplier)
    
            if self.__score > self.__high_score:
                self.__high_score = self.__score
    
        # UPDATE DISPLAYS #

            self.__canvas.itemconfig(
            self.__score_display,
            text=f"Score: {self.__score}")
            self.__canvas.itemconfig(
            self.__high_score_display,
            text=f"High Score: {self.__high_score}")
            

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
