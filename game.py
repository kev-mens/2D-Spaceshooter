import arcade
import random
import os


#window
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = 'learning module'

#scalings
ASTEROID_SCALING = 1
SHIP_SCALING = 1
LASER_SCALING = 1
 
#speeds
SHIP_SPEED = 10
LASER_SPEED = 5

ASTEROID_NUMBER = 80

class Explosion(arcade.Sprite):
    def __init__(self, texture_list):
        super().__init__('Images/Space/Explosions/Ship_Explosion/explosion0000.png')      
        self.current_texture = 0 
        self.textures = texture_list
        
    def update(self):
        self.current_texture +=1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.remove_from_sprite_lists()
            self.center_x = 2000

def Asteroid(size):
        
    main_path = 'Images/Space/Meteors'
    
    #choosing asteroid sizes
    if size == 'big':
        x = random.randint(1,4) #have up to 8 big meteors to choose from
        asteroid = arcade.Sprite(f'{main_path}/meteor_big{x}.png', ASTEROID_SCALING)
        
        #setting collision points for each asteroid
        #placed into desmos with scaling = resultion
        #take vertices
        
        if x ==1:
            asteroid.points = [[50,0], [24,41], [-33, 41], [-51, 9], [-21, -41], [10, -29], [34,-32]]
        elif x == 2:
            asteroid.points = [[28,29], [-10,41], [-45,19], [-42,-15], [-27,-34], [20,-41], [44, -1]]
        elif x == 3:
            asteroid.points = [[28,29], [-10,41], [-45,19], [-42,-15], [-27,-34], [20,-41], [44, -1]]
        elif x == 4:
            asteroid.points = [[60,29], [7,49], [-40,40], [-60,4], [-54,-27], [-26,-49], [-9,-33], [46,-18]]
        
    elif size == 'medium':
        x = random.randint(1,4)
        asteroid = arcade.Sprite(f'{main_path}/meteor_med{x}.png', ASTEROID_SCALING)
        if x == 1:
            asteroid.points = [[17,18], [-9,20], [-22,4],[-14,-15], [0,-22], [22,-6]]
        if x == 2:
            asteroid.points = [[23,2], [9,19], [-16,15], [-23,-4], [-9,-18], [6,-20]]
        if x == 3:
            asteroid.points = [[23,2], [9,19], [-16,15], [-23,-4], [-9,-18], [6,-20]]
        if x == 4:
            asteroid.points = [[17,18], [-9,20], [-22,4],[-14,-15], [0,-22], [22,-6]]
            
            
    elif size == 'small':
        x = random.randint(1,4)
        asteroid = arcade.Sprite(f'{main_path}/meteor_small{x}.png', ASTEROID_SCALING)
        if x == 1: 
            asteroid.points = [[11,12], [-7,13], [-14, 2], [-10,-10], [0, -14], [13, -5]]
        if x == 2:
            asteroid.points = [[15,1], [5,13], [-10,10], [-15,-2], [-5,-12], [5,-12]]
        if x == 3:
            asteroid.points = [[11,12], [-7,13], [-14, 2], [-10,-10], [0, -14], [13, -5]]
        if x == 4:
            asteroid.points = [[15,1], [5,13], [-10,10], [-15,-2], [-5,-12], [5,-12]]
            
    elif size == 'tiny':
        x = random.randint(1,4)
        asteroid = arcade.Sprite(f'{main_path}/meteor_tiny{x}.png', ASTEROID_SCALING)
        if x == 1:
            asteroid.points = [[8,5], [-1,9], [-8, 0], [-3,-8], [5,-8]]
        if x == 2:
            asteroid.points = [[8,2], [0,8], [-8,0], [2,-8]]
        if x == 3:
            asteroid.points = [[8,5], [-1,9], [-8, 0], [-3,-8], [5,-8]]
        if x == 4:
            asteroid.points = [[8,2], [0,8], [-8,0], [2,-8]]
            
        #bless desmos
    
    #spawn loaction
    asteroid.center_x = random.randint(1,1920)
    asteroid.center_y = random.randint(1080,3000)
    
    #rotation and movement
    asteroid.change_y = random.randrange(-6, -1)
    asteroid.change_angle = random.randrange(-2, 2)
    if asteroid.change_angle == 0:                          #recursion to prevent non-spinning asteroids
        asteroid.change_angle = random.randrange(-2, 2)
        
    return asteroid 
        
class MyGame(arcade.Window):
    
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, TITLE):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, fullscreen = True)
        
        self.main_path = 'Images/Space/'
        
        self.set_update_rate(1/120)
        
        self.ship_list = None
        self.asteroid_list = None
        self.laser_list = None
        self.explosion_list = None
        
        self.ship = None
        self.asteroid = None
        self.laser1 = None
        self.laser2 = None
        self.explosion = None
        
        self.physics_engine = None
        self.key = None   
        self.background = None
        self.score = None
        
        self.set_mouse_visible(False)
        
        self.sizes = ['big', 'medium', 'small', 'tiny']        
        #initializing explosion frames here so it's preloaded
        
        self.explosion_texture_list = []
        for explosion in range(60):
            texture = f'{self.main_path}Explosions/Ship_Explosion/explosion{explosion:04d}.png'
            self.explosion_texture_list.append(arcade.load_texture(texture))
        
    def setup(self):
        #creating sprite lists
        self.ship_list = arcade.SpriteList()
        self.asteroid_list = arcade.SpriteList()
        self.laser_list = arcade.SpriteList()
        self.explosion_list = arcade.SpriteList()
        
        #creating player
        self.ship = arcade.Sprite(f'{self.main_path}Player/playerShip2_blue.png', SHIP_SCALING)
        self.ship.center_x = SCREEN_WIDTH//2
        self.ship.center_y = SCREEN_HEIGHT//2
        self.ship_list.append(self.ship)
        
        
        for i in range(ASTEROID_NUMBER):
            self.asteroid = Asteroid(self.sizes[random.randint(0,3)])
            self.asteroid_list.append(self.asteroid)   
                    
        
        #background
        self.background = arcade.load_texture(f'{self.main_path}Backgrounds/blue_space.png')        
        self.score = 0        
    
    def on_key_press(self, key, modifiers):
        
        if key == arcade.key.W:
            self.ship.change_y = SHIP_SPEED
        if key == arcade.key.S:
            self.ship.change_y = -SHIP_SPEED
        if key == arcade.key.A:
            self.ship.change_x = -SHIP_SPEED
        if key == arcade.key.D:
            self.ship.change_x = SHIP_SPEED 
        if key == arcade.key.ENTER:
            self.laser1 = arcade.Sprite(f'{self.main_path}Laser/laserRed01.png', 1)
            self.laser2 = arcade.Sprite(f'{self.main_path}Laser/laserRed01.png', 1)
            
            self.laser1.center_x = self.ship.center_x - 10
            self.laser1.bottom = self.ship.top
            self.laser2.center_x = self.ship.center_x + 10
            self.laser2.bottom = self.ship.top 
            
            self.laser1.change_y, self.laser2.change_y = LASER_SPEED , LASER_SPEED
            
            
            
            self.laser_list.append(self.laser1)
            self.laser_list.append(self.laser2)
            
        self.key = key
            
    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S:
            self.ship.change_y = 0
        if key == arcade.key.A or key == arcade.key.D:
            self.ship.change_x = 0       
    
    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        
        self.ship_list.draw()
        self.asteroid_list.draw()
        self.laser_list.draw()
        self.explosion_list.draw()
        
        arcade.draw_text(f'Score: {self.score}', 1500, 200, arcade.color.WHITE)
        
        #draw sprite lists
        
    def on_update(self, delta_time):
        
        #reset asteroids after leaving screen
        for asteroid in self.asteroid_list:
            if asteroid.top < 0:
                asteroid.kill()   # prevents asteroid list from growing infinitely 
                asteroid = Asteroid(self.sizes[random.randint(0,3)])     #resets asteroid
                self.asteroid_list.append(asteroid)      
                
                
        #boundary restrictions
        if self.ship.top > (SCREEN_HEIGHT-50) and self.ship.change_y > 0:
            self.ship.change_y = 0
        if self.ship.bottom < 50 and self.ship.change_y < 0:
            self.ship.change_y = 0
        if self.ship.left < 50 and self.ship.change_x < 0:
            self.ship.change_x = 0
        if self.ship.right > (SCREEN_WIDTH-50) and self.ship.change_x > 0:
            self.ship.change_x = 0
        
        #laser physics       
        for laser in self.laser_list:
            laser.points = [[5,27], [-5,27], [-5, -27], [5,-27]]
            laser_asteroid = arcade.check_for_collision_with_list(laser, self.asteroid_list)
            if len(laser_asteroid) > 0:    
                laser.kill()
            if laser.bottom > SCREEN_HEIGHT:
                laser.kill()
        #ship explosion
        explosion_count = 0
        
        for asteroid in self.asteroid_list:
            collision_check = arcade.check_for_collision(asteroid, self.ship)
            if collision_check == True:       
                if (len(self.explosion_list) == 0) and (explosion_count == 0):
                    explosion_count +=1
                    self.explosion = Explosion(self.explosion_texture_list)
                    self.explosion.center_x = self.ship.center_x
                    self.explosion.center_y = self.ship.center_y
                    self.explosion_list.append(self.explosion)
                    self.ship.kill()                
                    break
                else:
                    self.explosion.points = None
            
        self.ship_list.update()
        self.asteroid_list.update()
        self.laser_list.update()
        self.explosion_list.update() 

        
        '''ship_asteroid = arcade.check_for_collision_with_list(self.ship, self.asteroid_list)
        if len(ship_asteroid) == 1:
            self.explosion = Explosion(self.explosion_texture_list)
            self.explosion.center_x .
            = self.ship.center_x
            self.explosion.center_y = self.ship.center_y
            self.explosion_list.append(self.explosion)
            self.ship.kill()
        elif len(ship_asteroid) > 1:
            pass'''
                        

        
def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()
    
if __name__ == '__main__':
    main()
        
            
            
        