from tkinter import *
import time, random
from Obstacles import Obstacles
from Dino import Dino

class DinoGame:
    
    #-------------------------------------------------------------------------
    # Initialization and Setup
    #-------------------------------------------------------------------------
    
    def __init__(self, root, nrow, ncol, scale):
        # canvas variables
        
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
        
        self.__canvas = Canvas(root, width=ncol*scale, height=nrow*scale, bg='black') #create canvas
        self.__canvas.pack()

        self.__start_msg = self.__canvas.create_text( #start message displayed
            (ncol * scale) / 2, (nrow * scale) / 2,
            text="Hit 'S' to start game", 
            font=('Times', 25)
        )
        
        #initialize dino and obstacle classes
        self.__obstacles = [] #empty list to store obstacles
        self.__dino = Dino(self.__canvas, self.nrow//2 + 28, self.ncol - 100, self.scale)

        self.root.bind("<r>", lambda e: self.restart())

       # self.__highscore = self.load_highscore() #load high score from file
       # self.__highscore_text = self.__canvas.create_text(self.scale * 10, self.scale * 3, text=f"High Score: {self.__highscore}", font=('Times', 30), anchor='w', fill='white')
        # In __init__():
        self.__score_text = self.__canvas.create_text(
            self.scale * 10, self.scale * 2, 
            text="Score: 0", 
            font=('Times', 20), 
            anchor='w', 
            fill='white'
        )

        # In update_survival_score():
        self.__canvas.itemconfig(self.__score_text, text=f"Score: {self.__score}")                                       


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
        if not self.__started and not self.__game_over:
            self.__canvas.delete(self.__start_msg)
            self.__score = 0
            self.__started = True
            self.__start_time = time.time()
            self.__dino.activate()
            print("Game started!")

            # obstacle loop
            self.root.after(50, update_obstacles, self, self.root)
        
    def next(self):
        if not self.__started or self.__pause or self.__game_over:
            return #only runs if game is running

        current_time = time.time() #creates obstacles
        if len(self.__obstacles) == 0 and current_time >= self.__next_spawn_time: #check if any obstacles are present
            new_obstacle = Obstacles.random_select(self.__canvas, self.nrow, self.ncol, self.scale)
            new_obstacle.activate()
            self.__obstacles.append(new_obstacle)
            self.__next_spawn_time = current_time + random.uniform(1, 3) #new obstacles every 1-3s

        for obstacle in self.__obstacles[:]: 
            obstacle.left() #moves obstacle left by one
            for dino_pixel in self.__dino.dino_pixels: #check obstacle dino collison
                for pixel in obstacle.pixels:
                    if (dino_pixel.i == pixel.i and #check if pixels are equal to each other
                        dino_pixel.j == pixel.j):
                        self.__canvas.create_text( #game over message 
                            self.ncol * self.scale / 2,
                            self.nrow * self.scale / 2,
                            text="GAME OVER",
                            font=('Times', 30),
                            fill='red'
                        )
                        self.__game_over = True
                        return
                
            if obstacle.j + obstacle.w < 0:  #checks if obstacle is off screen so it can be removed
                for pixel in obstacle.pixels:
                    pixel.delete()
                self.__obstacles.remove(obstacle)
                continue
        self.update_survival_score()

    
    def check_collision(self, obstacle): #check every dino pixel with every obstacle pixel
        for dino_pixel in self.__dino.dino_pixels: 
            for obs_pixel in obstacle.pixels:
                if dino_pixel.i == obs_pixel.i and dino_pixel.j == obs_pixel.j:
                    return True  #true for overlap
        return False #false for no overlap
    

    def jump(self):
        if self.__started and not self.__game_over and not self.__pause and not self.__dino.jumping: # make sure game is running
            self.__dino.jump()

    def pause(self):
        if not self.__started: #pause if game has started
            return
        
        if not self.__pause:
            self.__pause = True
            self.__pause_start = time.time()  #track time of pause
            print("Game paused")

        else: #resumes game
            self.__pause = False
            pause_duration = time.time() - self.__pause_start #make up for paused game so timer is consitent
            self.__start_time += pause_duration
            print("Game resumed")


    def update_survival_score(self):
        if self.__started and not self.__pause and not self.__game_over:
            current_time = time.time()
            seconds_survived = int(current_time - self.__start_time)
            base_score = seconds_survived
            bonus_multiplier = 1.0 + 0.1 * (seconds_survived // 30) #bonus multiplier that increases by .1 every 30 seconds survived
            self.__score = int(base_score * bonus_multiplier) #final score adds bonus
            
            self.__canvas.itemconfig(self.__score_text, text=f"Score: {self.__score}")
            print(f"Score: {self.__score} (Time: {seconds_survived}s, Bonus: {bonus_multiplier:.1f}x)")

    def restart(self):
        self.__canvas.delete("all")

        for obs in self.__obstacles:
            for pixel in obs.pixels:
                pixel.delete()
        self.__obstacles.clear()

        self.set_game_over(False)
        self.set_started(False)
        self.set_pause(False)
        self.set_score(0)
        self.set_pause_time(0)
        self.set_next_spawn_time(time.time() + random.uniform(1, 3))
        self.__start_time = time.time()


        self.__start_msg = self.__canvas.create_text(
            (self.ncol * self.scale) / 2,
            (self.nrow * self.scale) / 2,
            text="Hit 'S' to start game",
            font=('Times', 25)
                            )
        
        self.__score_text = self.__canvas.create_text(
            self.scale * 10, self.scale * 2,
            text="Score: 0",
            font=('Times', 20),
            anchor='w',
            fill='white'
)

    # Reactivate the same Dino object — DO NOT recreate it
    # Instead, just reset its internal pixels
        self.__dino = Dino(self.__canvas, self.nrow//2 + 28, self.ncol- 100, self.scale, game = self)
        print("Game reset. Press 'S' to start.")
        
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