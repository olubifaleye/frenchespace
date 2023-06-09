#imports
import pygame, sys
import os
from os import path
import time
import random
from button import Button

pygame.init();

#initialize pygame
successes, failures = pygame.init()
print("Initializing pygame: {0} successes and {1} failures.".format(successes, failures))

from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import AudioClip
from moviepy.editor import concatenate_videoclips,concatenate_audioclips,TextClip,CompositeVideoClip
from moviepy.video.fx.accel_decel import accel_decel
from moviepy.video.fx.blackwhite import blackwhite
from moviepy.video.fx.blink import blink
from moviepy.video.fx.colorx import colorx
from moviepy.video.fx.crop import crop
from moviepy.video.fx.even_size import even_size
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from moviepy.video.fx.freeze import freeze
from moviepy.video.fx.freeze_region import freeze_region
from moviepy.video.fx.gamma_corr import gamma_corr
from moviepy.video.fx.headblur import headblur
from moviepy.video.fx.invert_colors import invert_colors
from moviepy.video.fx.loop import loop
from moviepy.video.fx.lum_contrast import lum_contrast
from moviepy.video.fx.make_loopable import make_loopable
from moviepy.video.fx.margin import margin
from moviepy.video.fx.mask_and import mask_and
from moviepy.video.fx.mask_color import mask_color
from moviepy.video.fx.mask_or import mask_or
from moviepy.video.fx.mirror_x import mirror_x
from moviepy.video.fx.mirror_y import mirror_y
from moviepy.video.fx.painting import painting
from moviepy.video.fx.resize import resize
from moviepy.video.fx.rotate import rotate
from moviepy.video.fx.scroll import scroll
from moviepy.video.fx.speedx import speedx
from moviepy.video.fx.supersample import supersample
from moviepy.video.fx.time_mirror import time_mirror
from moviepy.video.fx.time_symmetrize import time_symmetrize

from moviepy.audio.fx.audio_fadein import audio_fadein
from moviepy.audio.fx.audio_fadeout import audio_fadeout
from moviepy.audio.fx.audio_left_right import audio_left_right
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.fx.audio_normalize import audio_normalize
from moviepy.audio.fx.volumex import volumex

#function to allow resources to be loaded in one file when the script is compiled
def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#Initiate fonts in pygame
pygame.font.init();
pygame.mixer.init();

#Initiate the main font
main_font = pygame.font.Font(resource_path("slkscreb.ttf"), 70);

#Initiate the translation font
translation_font = pygame.font.Font(resource_path("Spinnaker-Regular.ttf"), 20);

#Load Images from assets folder
#From pygame module use the image.load method
#Located at os.path.join method
#name of the folder images are in and name of the file
RED_SPACE_SHIP = pygame.image.load(resource_path("assets/pixel_ship_red_small.png"));
GREEN_SPACE_SHIP = pygame.image.load(resource_path("assets/pixel_ship_green_small.png"));
BLUE_SPACE_SHIP = pygame.image.load(resource_path("assets/pixel_ship_blue_small.png"));

#Player Spaceship
YELLOW_SPACE_SHIP = pygame.image.load(resource_path("assets/pixel_ship_yellow.png"));

#Load in lasers
RED_LASER = pygame.image.load(resource_path("assets/pixel_laser_red.png"));
BLUE_LASER = pygame.image.load(resource_path("assets/pixel_laser_blue.png"));
GREEN_LASER = pygame.image.load(resource_path("assets/pixel_laser_green.png"));
YELLOW_LASER = pygame.image.load(resource_path("assets/pixel_laser_yellow.png"));

#Load in sounds
explosion_sfx = pygame.mixer.Sound(resource_path("assets/explosion.mp3"));
laser_sfx = pygame.mixer.Sound(resource_path("assets/player_laser.mp3"));
button_sfx = resource_path("assets/button_press.mp3");
correct_sfx = pygame.mixer.Sound(resource_path("assets/correct_answer.mp3"));
incorrect_sfx = pygame.mixer.Sound(resource_path("assets/incorrect_answer.mp3"));

#Set up pygame window size
WIDTH, HEIGHT = 750, 750;
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT));

#Load in background
#scale window and background to be size of width and height
BACKGROUND = pygame.transform.scale(
    pygame.image.load(resource_path("assets/background-black.png")), (WIDTH, HEIGHT));

#Set up caption of python window
pygame.display.set_caption("Space Invaders");

#starting dictionary of all the english and french words in english:french word key:value
dictionary = {
              "red": "rouge",
              "yellow": "jaune",
              "green": "vert",
              "blue": "bleu",
              "white": "blanc",
              "black": "noir",

              "family": "famille",
              "father": "père",
              "mother": "mère",
              "brother": "frère",
              "sister": "sœur",
              "baby": "bébé",

              "good morning": "bonjour",
              "hi": "salut",
              "good": "bonne",
              "afternoon": "après-midi",
              "goodbye": "au revoir",

              "my": "Je",
              "name is": "m'appelle",
              "daniel": "daniel",

              "i am": "je suis",
              "tall": "grand",

              "i live": "j'habite",
              "in": "à",
              "london": "londres",
             
              "how": "comment",
              "are": "ça",
              "you": "va",
              
              "fine": "bien",
              "thanks": "merci",
              "and   you": "et vous-même",

              "i have": "j'ai",
              "two": "deux",
              "brothers": "frères",
              "and": "et", 
              "sisters": "sœurs",
              "i like": "j'aime",
              "fish": "poisson",

              "how old": "quel âge",
              "are you": "as-tu",

              "the": "la",
              "dogs": "chiens",
              "are infront of": "sont devant",
              "the car": "la voiture",

              "there is": "il ya",
              "a cat": "un chat"
              };

#create 2 lists, one containing english and one containing french
englishArray = list(dictionary.keys());
frenchArray = list(dictionary.values());

#to allow the french array to be altered without
frenchArrayEnemy = frenchArray.copy();

listSentences = [
                 "red",
                 "yellow",
                 "green",
                 "blue",
                 "white",
                 "black",

                 "family",
                 "father",
                 "mother",
                 "brother",
                 "sister",
                 "baby",

                 "goodmorning",
                 "hi",
                 "good afternoon",
                 "goodbye",

                 "my nameis daniel",
                 "iam tall",
                 "ilive in london",
                 "how are you",
                 "fine thanks andyou",
                 "ihave two brothers and sisters",
                 "ilike fish",
                 "howold areyou",
                 "the dogs areinfrontof thecar",
                 "thereis acat"
                 ];
listSentenceLength = [];

#for loop to calculate the number of words in each sentence from the list listSentences
for i in range(0, len(listSentences)):
    sentenceLength = len(listSentences[i].split());
    listSentenceLength.append(sentenceLength);

#set variable counterWidth to be the number of the first index of the number of words
    
counterWidth = listSentenceLength[0];
listWidth = [];

# for loop to dynamically create a list for the label width x position for each translation label
for i in range (0, listSentenceLength[0]):
    if counterWidth == 1:
        counterWidth = 2;
    listWidth.append(counterWidth);
    counterWidth = (counterWidth/2) + 0.5;

#create empty dictionaries 
tempDict = {}
englishArrayTemp = [];
frenchArrayTemp = [];

#populate tempDict with english french pairs
for i in range(0, listSentenceLength[0]):
    tempDict[englishArray[i]] = frenchArray[i];
    
#populate english and french arrays with key and values 
englishArrayTemp = list(tempDict.keys());
frenchArrayTemp = list(tempDict.values());

#create copies of variables
newTempDict = tempDict.copy();
newEnglishArrayTemp = englishArrayTemp.copy();
newFrenchArrayTemp = frenchArrayTemp.copy();
newListWidth = listWidth.copy();
newListSentenceLength = listSentenceLength.copy();
newEnglishArray = englishArray.copy();
newFrenchArray = frenchArray.copy();
newFrenchArrayEnemy = frenchArrayEnemy.copy();

#function to play the background music
def playMusic():
    background_music = pygame.mixer.music.load(resource_path("assets/background_music.mp3"));
    pygame.mixer.music.set_volume(0)
    pygame.mixer.music.play(-1);

#function to stop the music
def stopMusic():
    pygame.mixer.music.stop();

#score variable
score = 0;

#level variable
level = 1;

#label counter variables set to 0
label_counter = 0;
label_counter_1 = 0;
label_counter_2 = 0;
label_counter_3 = 0;

#function to refill the dictionary after a phrase has been translated
def refillDict():

    for i in range(0, listSentenceLength[0]):
        englishArray.pop(0);
        frenchArray.pop(0);
    
    listSentenceLength.pop(0);

    if(len(listSentenceLength) == 0):
        gameOver();
    else:
        counterWidth = listSentenceLength[0];

        if counterWidth == 1:
            counterWidth = 2;

        for i in range (0, listSentenceLength[0]):
            listWidth.append(counterWidth);
            counterWidth = (counterWidth/2) + 0.5;

        for i in range(0, listSentenceLength[0]):
            tempDict[englishArray[i]] = frenchArray[i];

        englishArrayTempHolder = list(tempDict.keys());
        frenchArrayTempHolder = list(tempDict.values());

        for i in range(0, len(englishArrayTempHolder)):
            englishArrayTemp.append(englishArrayTempHolder[i]);
            frenchArrayTemp.append(frenchArrayTempHolder[i]);
        

#Create Laser Class
class Laser:
    def __init__(self, x, y, img):
        self.x = x;
        self.y = y;
        self.img = img;
        self.mask = pygame.mask.from_surface(self.img);

    #drawing the laser
    def draw(self, WINDOW):
        WINDOW.blit(self.img, (self.x, self.y));

    #defining the movement of the laser going down
    def move(self, velocity):
        self.y += velocity;

    def off_screen(self, height):
        return not(self.y < height and self.y >= 0);

    #defining a collision method to check if laser collides with an object
    #returns value of collide function
    def collision(self, obj):
        return collide(obj, self);
    
#Create abstract ship class
class Ship:

    #cool down is set to half a second
    COOLDOWN = 30

    #define init method to initialise the starting position of the ship(s)
    def __init__(self, x, y, health = 100):

        self.x = x;
        self.y = y;
        self.health = health;

        #allows python to draw ships and lasers
        self.ship_img = None;
        self.laser_img = None;
        self.lasers = [];
        self.cool_down_counter = 0;

    #drawing the ship and its lasers
    def draw(self, WINDOW):
        WINDOW.blit(self.ship_img, (self.x, self.y));
        for laser in self.lasers:
            laser.draw(WINDOW);

    #function to move lasers
    def move_lasers(self, velocity, obj):

        #increment cooldown counter when we move the lasers
        self.cooldown();
        for laser in self.lasers:
            laser.move(velocity);

            #if the laser goes off the screen remove the laser from the lasers lists
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser);

            #else if a collision occurs reduce the health of the object
            #the laser collided with and remove the laser from the lasers list
            elif laser.collision(obj):
                obj.health -= 10;
                self.lasers.remove(laser);

    #define cooldown
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0;
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1;
            

    #define shoot method
    def shoot(self):
        
        #if cool down counter is 0 then create a new laser and append it to the lasers list
        if self.cool_down_counter == 0:
            #play the laser sound effect
            laser_sfx.play();
            laser = Laser(self.x,self.y, self.laser_img);
            self.lasers.append(laser);

            #start the cool down counter
            self.cool_down_counter = 1;

    #define get ship width
    def get_width(self):
        return self.ship_img.get_width();

    #define get ship height
    def get_height(self):
        return self.ship_img.get_height();


#Create Player class which will inherit from Ship class
class Player(Ship):
    def __init__(self, x, y, health = 100):
        #use Ships initialisation method on Player class
        super().__init__(x, y, health);

        #initialise players ship colour and laser
        self.ship_img = YELLOW_SPACE_SHIP;
        self.laser_img = YELLOW_LASER;

        #pygame function to allow seemless collision
        #makes a mask of ship_img
        #tells pygame where pixels are in ship_img so collision between pixels can be detected
        self.mask = pygame.mask.from_surface(self.ship_img);

        #initialise player max health
        self.max_health = health;

    #function to move lasers
    def move_lasers(self, velocity, objs):
    
        changeColorCorrect = (0,255,0)
        changeColorIncorrect = (255,0,0)

        #make variable score global
        global score;

        global level;
        
        #increment cooldown counter when we move the lasers
        self.cooldown();
        for laser in self.lasers:
            laser.move(velocity);

            #if the laser goes off the screen remove the laser from the lasers lists
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser);
        
            else:
                for obj in objs:
                    if laser.collision(obj):

                        #play explosion sound
                        explosion_sfx.play();

                        #if the objects french word is a value in tempDict    
                        if obj.frenchArrayEnemy in tempDict.values():

                            #if the player shoots the the correct enemy in the sentence +1 point
                            score += 1;

                            #if the objects french word is the first word to be translated
                            if obj.frenchArrayEnemy in frenchArrayTemp[0]:

                                #if the player shoots the correct enemy and it is in the correct position in the sentence +5 points 
                                score += 5;

                                #find the index of the word and remove it
                                removeIndex =(frenchArrayTemp.index(frenchArrayTemp[0]));
                                removeEnemyIndex = frenchArrayEnemy.index(obj.frenchArrayEnemy);

                                #remove the word from the dictionary and frenchArrayEnemy
                                tempDict.pop(englishArrayTemp[removeIndex]);
                                frenchArrayEnemy.pop(removeEnemyIndex);

                                #remove the french/english word pair from their respective arrays
                                englishArrayTemp.pop(removeIndex);
                                frenchArrayTemp.pop(removeIndex);

                                #remove the index from listWidth
                                listWidth.pop(removeIndex);
                                
                                #if the tempDicT and french array and english array is empty
                                #call refillDict()
                                #increse to a new level i.e. a new sentence
                                if bool(tempDict) == False and len(frenchArrayTemp) == 0 and len(englishArrayTemp) == 0:
                                    level += 1;
                                    refillDict();

                            #draw label indicating destroyed enemy is correct
                            translation_correct_label = translation_font.render("CORRECT", 1, changeColorCorrect);
                            translation_correct_label_rect = translation_correct_label.get_rect(center=(WIDTH/2, 50));

                            #play correct answer sound
                            correct_sfx.play();
                            
                            #show label on screen and pause the movement for 400ms
                            WINDOW.blit(translation_correct_label, translation_correct_label_rect);
                            pygame.display.update();
                            pygame.event.pump()
                            pygame.time.delay(400)

                        else:

                            #reduce player score by 1
                            score -= 1;

                            #draw label indicating destroyed enemy is incorrect
                            translation_correct_label = translation_font.render("INCORRECT", 1, changeColorIncorrect);
                            translation_correct_label_rect = translation_correct_label.get_rect(center=(WIDTH/2, 50));

                            #play incorrect answer sound
                            incorrect_sfx.play();
                            
                            #show label on screen and pause the movement for 400ms
                            WINDOW.blit(translation_correct_label, translation_correct_label_rect);
                            pygame.display.update();
                            pygame.event.pump()
                            pygame.time.delay(400)
                            
                        objs.remove(obj);
                        if laser in self.lasers:
                            self.lasers.remove(laser);

    #override draw method from parent class Ship
    def draw(self, WINDOW):
        super().draw(WINDOW);
        self.healthbar(WINDOW);

    #function to implement the healthbar
    def healthbar(self, WINDOW):
        pygame.draw.rect(WINDOW, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10));
        pygame.draw.rect(WINDOW, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10));


#Create Enemy class which will inherit from Ship class
class Enemy(Ship):

    #create a dictionary to hold strings of colours to map them to enemy ship color and laser
    COLOR_MAP = {
                "red" : (RED_SPACE_SHIP, RED_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        };

    def __init__(self, x, y, frenchArrayEnemy, color, health = 100):
        #use Ships initialisation method on Enemy class
        super().__init__(x, y, health);
        self.ship_img, self.laser_img = self.COLOR_MAP[color];
        self.mask = pygame.mask.from_surface(self.ship_img);
        self.frenchArrayEnemy = frenchArrayEnemy;

    #get enemy ship to only move down
    def move(self, velocity):

        #add colour for french word
        color = (255, 255, 255)
        self.y += velocity;

        #add french word to the enemy object
        enemy_french_label = translation_font.render(self.frenchArrayEnemy, 1, color);
        enemy_french_rect = enemy_french_label.get_rect(center = (self.x, self.y));

        #draw the french word
        WINDOW.blit(enemy_french_label, enemy_french_rect);
        pygame.display.update();
        

    #override shoot method to offset where bullets are shot from
    def shoot(self):
        #if cool down counter is 0 then create a new laser and append it to the lasers list
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 18, self.y, self.laser_img);
            self.lasers.append(laser);

            #start the cool down counter
            self.cool_down_counter = 1;


#create a class for the dynamics for collision
def collide(obj1, obj2):

    #offset of the 2 objects if and when they overlap
    offset_x = obj2.x - obj1.x;
    offset_y = obj2.y - obj1.y;

    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None;
    
        
#Main Function loop of the game
def main():

    playMusic();

    #While loop condition
    run = True;

    #Initiate Lost Count
    lost_count = 0;

    #Set FPS value 
    FPS = 60;

    #Initiate the main font
    main_font = pygame.font.Font(resource_path("slkscreb.ttf"), 19);

    #Initiate the pause font
    pause_font = pygame.font.Font(resource_path("slkscreb.ttf"), 14);

    color = (255,255,255)
       
    #Set Level
    global level;

    #Set Lives
    lives = 5;

    #Set Enemies
    enemies = [];

    #Set Enemy Speed
    enemy_speed = 2;

    #Set Wave Length
    wave_length = 5;

    #Set Player Speed
    player_speed = 6;

    #Set Laser Speed
    laser_speed = 6;

    player_ship = Player(300,620);

    #create clock object
    clock = pygame.time.Clock();

    #nested function only called inside main function
    def redraw_window():

        global label_counter;
        global label_counter_1;
        global label_counter_2;
        global label_counter_3;
        
        #takes an image turns into a surface and draws it into location on pygame
        WINDOW.blit(BACKGROUND, (0,0));


        #create and populate transition label 
        for i in range(0, len(tempDict)):
            translation_label = translation_font.render(englishArrayTemp[i], 1, color);
            translation_label_rect = translation_label.get_rect(center=(WIDTH/listWidth[i], 20));
            WINDOW.blit(translation_label, translation_label_rect);
        
        
        #draw the text
        #turn text into a surface and put it on the window
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255));
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255));
        score_label = pause_font.render(f"Score: {score}", 1, (255,255,255));
        pause_label = pause_font.render("Press P to Pause", 1, (255,255,255));
        enemies_label = pause_font.render(f"Enemies: {len(enemies)}", 1, (255,255,255));

        #area on the window to put the text when blit
        WINDOW.blit(enemies_label, (WIDTH - enemies_label.get_width() - 10, 50));
        WINDOW.blit(pause_label, (WIDTH - pause_label.get_width() - 10, HEIGHT - 20));
        WINDOW.blit(lives_label,(10, 10));
        WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 10, 10));
        WINDOW.blit(score_label,(10, 50));

        #refresh the enemy for each enemy movement
        #redraw enemy before player ship so enemy overlap doesnt occur
        for enemy in enemies:
            enemy.draw(WINDOW);

        #draw the player ship
        player_ship.draw(WINDOW);

        #topics labels 
        colours_label = main_font.render("COLOURS", 1, (255, 255, 255));
        family_label = main_font.render("FAMILY", 1, (255, 255, 255));
        greetings_label = main_font.render("GREETINGS", 1, (255, 255, 255));
        sentences_label = main_font.render("SENTENCES", 1, (255, 255, 255));

        #if statements to check the length of the array englishArray
        #if the array is a certain length, display the correct topic label for the words
        #coming up to be translated
        if len(englishArray) == 46:
            label_counter += 1;
            if label_counter < 100:
                WINDOW.blit(colours_label, (WIDTH/2 - colours_label.get_width()/2, 350));    
        
        if len(englishArray) == 40:
            label_counter_1 += 1;
            if label_counter_1 <  100:
                WINDOW.blit(family_label, (WIDTH/2 - family_label.get_width()/2, 350));

        if len(englishArray) == 34:
            label_counter_2 += 1;
            if label_counter_2 <  100:
                WINDOW.blit(greetings_label, (WIDTH/2 - greetings_label.get_width()/2, 350));

        if len(englishArray) == 29:
            label_counter_3 += 1;
            if label_counter_3 < 100:
                WINDOW.blit(sentences_label, (WIDTH/2 - sentences_label.get_width()/2, 350));
                
         
        #refresh the display
        pygame.display.update();

    while run: 

        #constantly redraw the window
        clock.tick(FPS);
        redraw_window();

        #if statemtent to end game when lives reaches 0
        if lives <= 0 or player_ship.health <= 0:
            run = False;
            stopMusic();
            gameOver();
           
        #once the amount of enemies on the window reaches 0 increase the level
        #and increase the amount of enemies for the next level
        if len(enemies) == 0:
            if player_ship.health != 100:
                player_ship.health += 10;
            wave_length += 1;

            for i in range(wave_length):
                #spawn new enemies and append them to enemy list
                enemy = Enemy(random.randrange(50, WIDTH -180), random.randrange(-1500, -100), frenchArrayEnemy[0], random.choice(["red", "blue", "green"]));
                enemies.append(enemy);

                tempWord = frenchArrayEnemy.pop(0);
                frenchArrayEnemy.append(tempWord);
                
    
        #Check if event has occured
        for event in pygame.event.get():

            #if statement to check if user attempts to quit the game
            #set run to false and quit the loop and the game
            if event.type == pygame.QUIT:
                run = False;
                leaveGame();
                #quit();
                
        #variable to store keys pressed during FPS, returns true if a key in key
        #dictionary is pressed
        keys = pygame.key.get_pressed();
        #adding player speed to current x value, if not off the screen move left otherwise dont move
        if keys[pygame.K_LEFT] and player_ship.x - player_speed > 0: #moving left
            player_ship.x -= player_speed;

        #add width of the player_ship to allow for correct constraints
        if keys[pygame.K_RIGHT] and player_ship.x + player_speed + player_ship.get_width() < WIDTH: #moving right
            player_ship.x += player_speed;

        if keys[pygame.K_UP] and player_ship.y - player_speed > 0: #moving up
            player_ship.y -= player_speed;

        #adding player speed to current y value, if not off the screen move down otherwise dont move
        #add width of the player_ship to allow for correct constraints
        if keys[pygame.K_DOWN] and player_ship.y + player_speed + player_ship.get_height() + 20 < HEIGHT: #moving down
            player_ship.y += player_speed;

        #when space key is pressed, shoot laser 
        if keys[pygame.K_SPACE]:
            player_ship.shoot();

        if keys[pygame.K_p]:
            paused();

        #move the enemies
        for enemy in enemies[:]:
            enemy.move(enemy_speed);
            enemy.move_lasers(laser_speed, player_ship);

            #allow enemy ships to shoot at random
            if random.randrange(0, 3*60) == 1:
                enemy.shoot();

            #collision between player ship and enemy ship
            #if there is a collision reduce player ship health by 10 and remove the enemy ship
            if collide(enemy, player_ship):
                #play explosion sound
                explosion_sfx.play();
                player_ship.health -= 10;
                enemies.remove(enemy);
                
            #if enemy goes past the player ship remove a life
            elif enemy.y + enemy.get_height() > HEIGHT:

                #remove an enemy ship from the enemy ship list
                enemies.remove(enemy);

                #if the enemy's french word is present in the tempDict values, the sentence to be translated
                #remove a life
                if(enemy.frenchArrayEnemy in tempDict.values()):
                    lives -= 1;
                
                    #refresh the display
        pygame.display.update();
                
        player_ship.move_lasers(-laser_speed, enemies);

def paused():
    
     title_font = pygame.font.Font(resource_path("slkscreb.ttf"), 70);
     paused_font = pygame.font.Font(resource_path("slkscreb.ttf"), 20);

    #create clock object
     clock = pygame.time.Clock();

     paused = True;
 
     while paused:

         #fill the screen with white 
         WINDOW.fill((255,255,255));

         #create paused label
         PAUSED_LABEL = title_font.render("PAUSED", 1, (0,0,0));
         PAUSED_RECT = PAUSED_LABEL.get_rect(center=(WIDTH/2, 250));
         WINDOW.blit(PAUSED_LABEL, PAUSED_RECT);

         #create paused label score
         PAUSED_SCORE = paused_font.render(f"Score: {score}", 1, (0,0,0));
         WINDOW.blit(PAUSED_SCORE,(WIDTH/2 - PAUSED_SCORE.get_width()/2, 350));

         #create paused instructions label
         PAUSED_LABEL_DESCRIPTION = paused_font.render("Press C to continue or Q to quit", 1, (0,0,0));
         PAUSED_RECT_DESCRIPTION = PAUSED_LABEL_DESCRIPTION.get_rect(center=(WIDTH/2, 450));
         WINDOW.blit(PAUSED_LABEL_DESCRIPTION, PAUSED_RECT_DESCRIPTION);

         #add variable to log keys pressed
         keys = pygame.key.get_pressed();
         
         for event in pygame.event.get():
        
             #if C Key is pressed, continue to the game
             if keys[pygame.K_c]:
                 paused = False;

             #if Q is pressed, quit the game
             elif keys[pygame.K_q]:
                 #pygame.quit();
                 paused = False;
                 leaveGame();
                    
         pygame.display.update();
         clock.tick(10);


def gameOver():
    global score;

    #Text file for high score
    HS_FILE = resource_path("highscore.txt");

    title_font = pygame.font.Font(resource_path("slkscreb.ttf"), 70);
    game_over_font = pygame.font.Font(resource_path("slkscreb.ttf"), 30);

    #open the and read the high score text file
    high_score_file = open(HS_FILE, "r");

    #read the first line and store the value inside of it
    high_score = high_score_file.readline().rstrip();
    high_score_int = int(high_score);

    #close the txt file 
    high_score_file.close();

    #if the score achieved by the player is higher than the highest score from the
    #txt file set score as new highest score 
    if score > high_score_int:
        high_score_int = score;

    #write new high score to the high score txt file
    high_score_file_update = open(HS_FILE, "w");
    high_score_string = str(high_score_int);
    high_score_file_update.write(high_score_string);

    #close the txt file
    high_score_file_update.close();
    
    runGameOver = True;

    while runGameOver:

        #takes an image turns into a surface and draws it into location on pygame
        WINDOW.blit(BACKGROUND, (0,0));

        #get the position of the mouse on the pygame screen
        MOUSE_INSTRUCTION_POS = pygame.mouse.get_pos();

        #game over title
        GAME_OVER_TITLE_LABEL = title_font.render("GAME OVER", 1, (255,255,255));
        GAME_OVER_TITLE_RECT = GAME_OVER_TITLE_LABEL.get_rect(center=(WIDTH/2, 50));
        WINDOW.blit(GAME_OVER_TITLE_LABEL, GAME_OVER_TITLE_RECT);

        #score and high score labels
        SCORE_LABEL = game_over_font.render(f"Score: {score}", 1, (255,255,255));
        HIGH_SCORE_LABEL = game_over_font.render(f"HIGH SCORE: {high_score_int}", 1, (255,255,255));

        #blit the score and high score labels
        WINDOW.blit(SCORE_LABEL, (WIDTH/2 - SCORE_LABEL.get_width()/2, 250));
        WINDOW.blit(HIGH_SCORE_LABEL, (WIDTH/2 - HIGH_SCORE_LABEL.get_width()/2, 350));

        #add play again button
        PLAY_AGAIN_BUTTON = Button(pos= (WIDTH/2, 550), text_input = "PLAY AGAIN", font = game_over_font, base_color = "#d7fcd4", hovering_color = "White", fileName = button_sfx);

        #for loop to go through the button and apply the button function to it
        for button in [PLAY_AGAIN_BUTTON]:
            button.changeColorHover(MOUSE_INSTRUCTION_POS)
            button.update(WINDOW);

        #refresh the display
        pygame.display.update();

        #add events when button is pressed 
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_AGAIN_BUTTON.checkInput(MOUSE_INSTRUCTION_POS):
                    #reset score to 0
                    score = 0;
                    #end the loop and go to main menu
                    runGameOver = False;
                    main_menu();
                    break;



def instructions():

    #set the instructional video and its position
    clip = VideoFileClip(resource_path('assets/InstructionalVideo.mp4')).resize((750,750)).set_position("center");
    #play the video as soon as the page is loaded
    clip.preview()

    #update the display to show the buttons and the title
    pygame.display.update();

    main_menu();

#function to leave the game if an exit button is pressed 
def leaveGame():
    pygame.display.quit()
    pygame.quit()
    sys.exit() 

#main menu
def main_menu():
 
    global tempDict, englishArrayTemp, frenchArrayTemp, listWidth, listSentenceLength, englishArray, frenchArray, newFrenchArrayEnemy;
    
    TITLE_FONT = pygame.font.Font(resource_path("slkscreb.ttf"), 60);
    menu_font = pygame.font.Font(resource_path("slkscreb.ttf"), 30);

    #boolean for while loop
    runMenu = True;

    while runMenu:

        #reset the screen to a clear background
        WINDOW.blit(BACKGROUND, (0,0));

        #get the position of the mouse on the pygame screen
        MOUSE_MENU_POS = pygame.mouse.get_pos();

        #Creating the text label for the title
        TITLE_LABEL = TITLE_FONT.render("FRENCHESPACE", 1, (255,255,255));
        TITLE_RECT = TITLE_LABEL.get_rect(center=(WIDTH/2, 250));
        WINDOW.blit(TITLE_LABEL, TITLE_RECT);

        #creating the buttons for start, instructions and quit using the button.py and button class
        START_BUTTON = Button(pos= (WIDTH/2, 350), text_input = "START", font = menu_font, base_color = "#d7fcd4", hovering_color = "White", fileName = button_sfx);
        INSTRUCTION_BUTTON = Button(pos= (WIDTH/2, 450), text_input = "INSTRUCTIONS", font = menu_font, base_color = "#d7fcd4", hovering_color = "White", fileName = button_sfx);
        QUIT_BUTTON = Button(pos = (WIDTH/2, 550), text_input = "EXIT", font = menu_font, base_color = "#d7fcd4", hovering_color = "White", fileName = button_sfx);
        
        #for loop to go through the buttons and apply the button functions to each of them
        for button in [START_BUTTON, INSTRUCTION_BUTTON, QUIT_BUTTON]:
            button.changeColorHover(MOUSE_MENU_POS)
            button.update(WINDOW);

        #update the display to show the buttons and the title
        pygame.display.update();

        #event for quiting the game window if so, set run to false
        #to escape the while loop and quit pygame and the sys
        for event in pygame.event.get():

            #if statements to handle the events of pressing the left click button on any of the
            #on screen button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if START_BUTTON.checkInput(MOUSE_MENU_POS):
                    runMenu = False;

                    #if tempDict is empty, refill the variables needed with
                    #the copies created by swapping
                    if tempDict == {}:
                        tempDict = newTempDict;
                        englishArrayTemp = newEnglishArrayTemp;
                        frenchArrayTemp = newFrenchArrayTemp;
                        listWidth = newListWidth;
                        listSentenceLength = newListSentenceLength;
                        englishArray = newEnglishArray;
                        frenchArray = newFrenchArray;
                        frenchArrayEnemy = newFrenchArrayEnemy;
                    
                    #call main function    
                    main();

                #chesck if instructions button is clicked call instructions function
                if INSTRUCTION_BUTTON.checkInput(MOUSE_MENU_POS):
                    runMenu = False;
                    instructions();
                    break;

                #check if quit button is clicked quit the game
                if QUIT_BUTTON.checkInput(MOUSE_MENU_POS):
                    runMenu = False;
                    leaveGame();
                    break;
    
main_menu();
