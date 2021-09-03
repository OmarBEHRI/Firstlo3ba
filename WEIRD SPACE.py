import pygame
import sys
from pygame.locals import*
import os
import math
import random
import time
import tkinter
from tkinter import filedialog
from pygame import mixer
import json

pygame.init()
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
data = {
    'coins': 0,
    'ship_speed_list': [1, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.4, 2.6, 2.8, 3, 3, 3, 3, 3, 3],
    'ship_body_damage_list': [100, 200, 300, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000],
    'ship_health_list': [1500, 2500, 3000, 3500, 4000, 5000, 5500, 6000, 8000, 11000, 13000, 15000, 17000, 20000,
                         23000, 60000],
    'ship_bullet_min_damage_list': [50, 100, 150, 200, 250, 300, 350, 450, 500, 550, 700, 800, 950, 1150, 2000, 3000],
    'buy_status_list': [True, False, False, False, False, False, False, False, False, False, False, False, False, False,
                        False, False],
    'select_ship_list': [True, False, False, False, False, False, False, False, False, False, False, False, False,
                         False, False, False],
    'level_index': -1
}
try:
    with open('data_text.txt') as data_text:
        data = json.load(data_text)
except:
    pass
screen = pygame.display.set_mode((960, 540), pygame.RESIZABLE)
# ARROW TO GET BACK TO THE MAIN SCREEN
arrow_img_1 = pygame.image.load(os.path.join('images', 'back-arrow.png'))
arrow_img_2 = pygame.image.load(os.path.join('images', 'back-arrow (1).png'))
white_opac_bg = pygame.Surface([42, 42])
arrow_x = 10
arrow_y = 10


def display_back_arrow():
    global x_mouse, y_mouse
    white_opac_bg.fill((255, 255, 255))
    white_opac_bg.set_alpha(127)
    screen.blit(white_opac_bg, (5, 5))
    if arrow_x <= x_mouse <= arrow_x + 32 and arrow_y <= y_mouse <= arrow_y + 32:
        screen.blit(arrow_img_2, (arrow_x, arrow_y))
    else:
        screen.blit(arrow_img_1, (arrow_x, arrow_y))


def click_arrow():
    global game_status, player
    if arrow_x <= x_mouse <= arrow_x + 32 and arrow_y <= y_mouse <= arrow_y + 32:
        game_status = 'Main'
    # RESETTING THE PLAYER COMPETANCES
    player_img = ship_img_list_64[select_ship_list.index(True)]
    playerhealth = ship_health_list[select_ship_list.index(True)]
    playerbodydamage = ship_body_damage_list[select_ship_list.index(True)]
    playerbulletdamage = ship_bullet_min_damage_list[select_ship_list.index(True)]
    playerspeed = ship_speed_list[select_ship_list.index(True)]
    player = Player(player_img, (playerx, playery), playerhealth, playerbodydamage, playerbulletdamage, playerspeed,
                    player_shoot_load, player_shoot_wait)


# MAIN SCREEN INPUTS
#
#
#
bg_img = pygame.image.load(os.path.join('images', 'space-background.png'))
font = pygame.font.Font('Edge Of Madness.otf', 50)
font1 = pygame.font.Font('Edge Of Madness.otf', 10)

ButtonImg = pygame.image.load(os.path.join('images', 'Button.png'))
ButtonImg1 = pygame.image.load(os.path.join('images', 'Button.png'))
Side_Button1 = pygame.image.load(os.path.join('images', 'square_button.png'))
Side_Button2 = pygame.image.load(os.path.join('images', 'square_button.png'))
Side_Button3 = pygame.image.load(os.path.join('images', 'square_button.png'))
Side_Button4 = pygame.image.load(os.path.join('images', 'square_button.png'))
parameter = 'parameter.png'
music1 = 'music.png'
upgrade = 'upgrade.png'
shop = 'shop.png'

color1 = 191
color2 = 191

# SETTING THE KEY TO STRING LIST
keys_list = [K_BACKSPACE, K_TAB, K_CLEAR, K_RETURN, K_PAUSE, K_ESCAPE, K_SPACE, K_EXCLAIM, K_QUOTEDBL, K_HASH,
            K_DOLLAR, K_AMPERSAND, K_QUOTE, K_LEFTPAREN, K_RIGHTPAREN, K_ASTERISK, K_PLUS, K_COMMA, K_MINUS,
            K_PERIOD, K_SLASH, K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_COLON, K_SEMICOLON, K_LESS,
            K_EQUALS, K_GREATER, K_QUESTION, K_AT, K_LEFTBRACKET, K_BACKSLASH, K_RIGHTBRACKET, K_CARET,
            K_UNDERSCORE, K_BACKQUOTE, K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k, K_l, K_m, K_n, K_o,
            K_p, K_q, K_r, K_s, K_t, K_u, K_v, K_w, K_x, K_y, K_z, K_KP0, K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6,
            K_KP7, K_KP8, K_KP9, K_KP_PERIOD, K_KP_DIVIDE, K_KP_MULTIPLY, K_KP_MINUS, K_KP_PLUS, K_KP_ENTER,
            K_KP_EQUALS, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_INSERT, K_HOME, K_END, K_PAGEUP, K_PAGEDOWN, K_F1, K_F2,
            K_F3, K_F4, K_F5, K_F6, K_F7, K_F8, K_F9, K_F10, K_F11, K_F12, K_F13, K_F14, K_F15, K_NUMLOCK,
            K_CAPSLOCK, K_SCROLLOCK, K_RSHIFT, K_LSHIFT, K_RCTRL, K_LCTRL, K_RALT, K_LALT, K_RMETA, K_LMETA,
            K_LSUPER, K_RSUPER, K_MODE, K_HELP, K_PRINT, K_SYSREQ, K_BREAK, K_MENU, K_POWER, K_EURO]
keys_text_list = ['BACKSPACE', 'TAB', 'CLEAR', 'RETURN', 'PAUSE', 'ESCAPE', 'SPACE', 'EXCLAIM!', '"QUOTE"', '#',
                '$DOLLAR$', '&', 'QUOTE', '(', ')', '*', '+PLUS+', ',COMMA,', '-MINUS-', '.PERIOD.',
                '/SLASH/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':COLON:', ';SEMICOLON;', '<LESS<',
                '=EQUALS=', '>GREATER>', '?QUESTION?', '@AT@', '[', 'BACKSLASH', ']', '^^', '_UNDERSCORE_',
                '`BACKQUOTE`', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'K 0', 'K 1', 'K 2', 'K 3', 'K 4', 'K 5', 'K 6',
                'K 7', 'K 8', 'K 9', 'K .', 'K /', 'K *', 'K -', 'K +', 'K ENTER', 'K EQUAL', 'UP', 'DOWN',
                'RIGHT', 'LEFT', 'INSER', 'HOME', 'END', 'PAGEUP', 'PAGEDOWN', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6',
                'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F13', 'F14', 'F15', 'NUMLOCK', 'CAPSLOCK', 'SCROLLLOCK',
                'R SHIFT', 'L SHIFT', 'R CTRL', 'L CTRL', 'R ALT', 'L ALT', 'R META', 'L META', 'L SUPER',
                'R SUPER', 'MODE', 'HELP', 'PRINT', 'SYREQ', 'BREAK', 'MENU', 'POWER', 'EURO']


def button_onscreen():
    music_icon = pygame.image.load(os.path.join('images', music1))
    upgrade_icon = pygame.image.load(os.path.join('images', upgrade))
    parameter_icon = pygame.image.load(os.path.join('images', parameter))
    shop_icon = pygame.image.load(os.path.join('images', shop))
    screen.blit(ButtonImg, (220, 120))
    screen.blit(ButtonImg, (220, 270))
    screen.blit(Side_Button1, (20, 190))
    screen.blit(Side_Button2, (20, 340))
    screen.blit(Side_Button3, (800, 190))
    screen.blit(Side_Button4, (800, 340))
    screen.blit(parameter_icon, (53, 223))
    screen.blit(music_icon, (53, 373))
    screen.blit(upgrade_icon, (833, 223))
    screen.blit(shop_icon, (833, 373))


name_font = pygame.font.Font('Edge Of Madness.otf', 60)


def title_on_screen():
    title = name_font.render('WEIRD SPACE', True, (255, 68, 11))
    screen.blit(title, (screen.get_width()/2-title.get_width()/2, 80))
    button1_text = font.render('ACRCADE', True, (color1, color1, color1))
    screen.blit(button1_text, (350, 215))
    button1_text = font.render('LEVELS', True, (color2, color2, color2))
    screen.blit(button1_text, (375, 365))


def background_display():
    screen.blit(bg_img, (0, 0))


# PARAMETER INPUTS
#
#
#
parameters_container = pygame.image.load(os.path.join('images', 'parameters_container1.png'))
parameters_container_bg = pygame.image.load(os.path.join('images', 'parameters_container1_bg.png'))
parameters_container_bg.set_alpha(127)
up_button = K_UP
down_button = K_DOWN
left_button = K_LEFT
right_button = K_RIGHT
shoot_button = 'MOUSE_CLICK'


def display_parameter_elements():
    global left_button, down_button, up_button, left_button, keys_text_list, keys_list
    parameters_font = pygame.font.Font('Edge Of Madness.otf', 25)
    down_text = parameters_font.render('DOWN: ', True, (255, 255, 255))
    left_text = parameters_font.render('LEFT: ', True, (255, 255, 255))
    up_text = parameters_font.render('UP: ', True, (255, 255, 255))
    right_text = parameters_font.render('RIGHT', True, (255, 255, 255))
    shoot_text = parameters_font.render('SHOOT: ', True, (255, 255, 255))
    screen.blit(parameters_container, (screen.get_width()/2-parameters_container.get_width()/2,
                              screen.get_height()/2-parameters_container.get_height()/2))
    screen.blit(parameters_container_bg, (screen.get_width()/2-parameters_container.get_width()/2+5,
                                 screen.get_height()/2-parameters_container.get_height()/2+5))
    screen.blit(up_text, (screen.get_width() / 2 - parameters_container.get_width() / 2 + 30,
                          screen.get_height() / 2 - parameters_container.get_height() / 2 + 40))
    screen.blit(down_text, (screen.get_width() / 2 - parameters_container.get_width() / 2 + 30,
                          screen.get_height() / 2 - parameters_container.get_height() / 2 + 120))
    screen.blit(left_text, (screen.get_width() / 2 - parameters_container.get_width() / 2 + 30,
                          screen.get_height() / 2 - parameters_container.get_height() / 2 + 200))
    screen.blit(right_text, (screen.get_width() / 2 - parameters_container.get_width() / 2 + 30,
                          screen.get_height() / 2 - parameters_container.get_height() / 2 + 280))
    screen.blit(shoot_text, (screen.get_width() / 2 - parameters_container.get_width() / 2 + 30,
                             screen.get_height() / 2 - parameters_container.get_height() / 2 + 360))
    screen.blit(select_button, (screen.get_width() / 2 - parameters_container.get_width() / 2 + 130,
                                screen.get_height() / 2 - parameters_container.get_height() / 2 + 20))
    screen.blit(select_button, (screen.get_width() / 2 - parameters_container.get_width() / 2 + 130,
                                screen.get_height() / 2 - parameters_container.get_height() / 2 + 95))
    screen.blit(select_button, (screen.get_width() / 2 - parameters_container.get_width() / 2 + 130,
                                screen.get_height() / 2 - parameters_container.get_height() / 2 + 175))
    screen.blit(select_button, (screen.get_width() / 2 - parameters_container.get_width() / 2 + 130,
                                screen.get_height() / 2 - parameters_container.get_height() / 2 + 255))
    screen.blit(select_button, (screen.get_width() / 2 - parameters_container.get_width() / 2 + 130,
                                screen.get_height() / 2 - parameters_container.get_height() / 2 + 330))
    key_up = keys_text_list[keys_list.index(up_button)]
    key_up_text = parameters_font.render(key_up, True, (255, 255, 255))
    key_down = keys_text_list[keys_list.index(down_button)]
    key_down_text = parameters_font.render(key_down, True,  (255, 255, 255))
    key_left = keys_text_list[keys_list.index(left_button)]
    key_left_text = parameters_font.render(key_left, True, (255, 255, 255))
    key_right = keys_text_list[keys_list.index(right_button)]
    key_right_text = parameters_font.render(key_right, True, (255, 255, 255))
    try:
        key_shoot = keys_text_list[keys_list.index(shoot_button)]
    except:
        key_shoot = str(shoot_button)
    key_shoot_text = parameters_font.render(key_shoot, True, (255, 255, 255))
    screen.blit(key_up_text, (
        screen.get_width() / 2 - parameters_container.get_width() / 2 + 130 + select_button.get_width()/2-key_up_text.get_width()/2,
        screen.get_height() / 2 - parameters_container.get_height() / 2 + 20 + select_button.get_height()/2-key_up_text.get_height()/2))
    screen.blit(key_down_text, (
        screen.get_width() / 2 - parameters_container.get_width() / 2 + 130 + select_button.get_width() / 2 - key_up_text.get_width() / 2,
        screen.get_height() / 2 - parameters_container.get_height() / 2 + 95 + select_button.get_height() / 2 - key_up_text.get_height() / 2))
    screen.blit(key_left_text, (
        screen.get_width() / 2 - parameters_container.get_width() / 2 + 130 + select_button.get_width()/2-key_up_text.get_width()/2,
        screen.get_height() / 2 - parameters_container.get_height() / 2 + 175 + select_button.get_height()/2-key_up_text.get_height()/2))
    screen.blit(key_right_text, (
        screen.get_width() / 2 - parameters_container.get_width() / 2 + 130 + select_button.get_width()/2-key_up_text.get_width()/2,
        screen.get_height() / 2 - parameters_container.get_height() / 2 + 255 + select_button.get_height()/2-key_up_text.get_height()/2))
    screen.blit(key_shoot_text, (
        screen.get_width() / 2 - parameters_container.get_width() / 2 + 130 + select_button.get_width() / 2 - key_up_text.get_width() / 2,
        screen.get_height() / 2 - parameters_container.get_height() / 2 + 330 + select_button.get_height() / 2 - key_up_text.get_height() / 2))


# GAME INPUTS
#
#
#
# SHIPS 64 IMAGES

# PAUSE IMAGES AND BUTTON TO PU THEM ON
pause = pygame.image.load(os.path.join('music_icons', 'pause.png'))
pause1 = pygame.image.load(os.path.join('music_icons', 'pause(1).png'))
button69 = pygame.image.load(os.path.join('images', 'bg_button1.png'))
pause_status = False
# FONT INITIALISATION
font2 = pygame.font.Font('Edge Of Madness.otf', 20)

# PLAYER INITIALISATION
playerImg = pygame.image.load(os.path.join('images', 'spaceship.png'))
playerx = 448
playery = 460
player_health = 2000
player_body_damage = 300
player_bullet_damage = 150
player_speed = 3
player_shoot_load = 150
player_shoot_wait = 2000


# INITIALISING THE GAME STATE
game_over = False
# INITIALISING CURRENT AND STATIC TIME
current_time = 0
static_skin_time = 0
static_shoot_time = 0

# RECOMPENSES FOM KILLING THE ENEMIES VARIABLES AND LISTS
ini_positions_list = []
recompense_list = []
recompense_genre_list = []
enemy_coin_recompense_list = []
medkit_img = pygame.image.load(os.path.join('images', 'medkit.png'))
meds_img = pygame.image.load(os.path.join('images', 'med.png'))
fire_img = pygame.image.load(os.path.join('images', 'fire.png'))
# IMPORTING COIN IMAGES
coin_1 = pygame.image.load(os.path.join('coins', 'gold_coin_round_star_1.png'))
coin_2 = pygame.image.load(os.path.join('coins', 'gold_coin_round_star_2.png'))
coin_3 = pygame.image.load(os.path.join('coins', 'gold_coin_round_star_3.png'))
coin_4 = pygame.image.load(os.path.join('coins', 'gold_coin_round_star_4.png'))
coin_5 = pygame.image.load(os.path.join('coins', 'gold_coin_round_star_5.png'))
coin_6 = pygame.image.load(os.path.join('coins', 'gold_coin_round_star_6.png'))
coin_img_list = [coin_1, coin_2, coin_3, coin_4, coin_5, coin_6]
coin_index = 0

# TIME DELTA TIME
prev_time = time.time()
static_coin_time = 0

# FONT FOR THE RESTART AND DKCHI
restart_font = pygame.font.Font('Edge Of Madness.otf', 20)


def display_recompenses(ini_positions_list_p):
    global recompense_list, coin_img_list, coin_index, static_coin_time
    if current_time - static_coin_time <= 66:
        pass
    else:
        for recompense_img in recompense_list:
            if recompense_genre_list[recompense_list.index(recompense_img)] == 'coin':
                if coin_index < len(coin_img_list) - 1:
                    coin_index += 1
                else:
                    coin_index = 0
                recompense_list[recompense_list.index(recompense_img)] = coin_img_list[coin_index]
                static_coin_time = current_time
    for recompense_img in recompense_list:
        screen.blit(recompense_img, ini_positions_list_p[recompense_list.index(recompense_img)])
        ini_positions_list_p[recompense_list.index(recompense_img)][1] += 100 * dt
        if ini_positions_list_p[recompense_list.index(recompense_img)][1] > 960:
            ini_positions_list_p.pop(recompense_list.index(recompense_img))
            recompense_genre_list.pop(recompense_list.index(recompense_img))
            enemy_coin_recompense_list.pop(recompense_list.index(recompense_img))
            recompense_list.pop(recompense_list.index(recompense_img))


class Player:

    def __init__(self, player_img, player_pos, health, body_damage, bullet_damage_p, speed, shoot_load, shoot_wait):
        self.player_img = player_img
        self.player_pos_x = player_pos[0]
        self.player_pos_y = player_pos[1]
        self.health = health
        self.max_health = health
        self.shoot_load = shoot_load
        self.shoot_wait = shoot_wait
        self.body_damage = body_damage
        self.bullet_damage = bullet_damage_p
        self.speed = 600
        self.speed_x = speed
        self.speed_y = speed
        self.static_time = 0
        self.shoot = False
        self.bullets_list = []
        self.bullet_img = pygame.image.load(os.path.join('images', 'bullet.png'))
        self.health_bar = pygame.Surface([self.health/health * 200, 30])
        self.health_red = pygame.Surface([200, 30])
        # key presseds vars
        self.left_key_pressed = False
        self.right_key_pressed = False
        self.up_key_pressed = False
        self.down_key_pressed = False
        # BULLET
        self.bullet_speed = 6
        self.bullet_direction_list = []

    def player_move(self):
        self.speed_x = 0
        self.speed_y = 0
        if self.left_key_pressed and not self.right_key_pressed:
            self.speed_x = - self.speed
        if self.right_key_pressed and not self.left_key_pressed:
            self.speed_x = self.speed
        if self.up_key_pressed and not self.down_key_pressed:
            self.speed_y = - self.speed
        if self.down_key_pressed and not self.up_key_pressed:
            self.speed_y = self.speed
        # updating the player pos
        self.player_pos_x += self.speed_x * dt
        self.player_pos_y += self.speed_y * dt

        # MAKING SURE HE PLAYER IS NOT OFF THE SCREEN
        if self.player_pos_x < 0:
            self.player_pos_x = 0
        if self.player_pos_x > 896:
            self.player_pos_x = 896

        if self.player_pos_y < 0:
            self.player_pos_y = 0
        if self.player_pos_y > 476:
            self.player_pos_y = 476
        # MAKING SURE THAT WHEN THE BARIER IS ON THE PLAYER DOESN'T TOUCH IT
        if barier_on:
            if self.player_pos_y < 320:
                self.player_pos_y = 320

    def display_player(self):
        screen.blit(self.player_img, (self.player_pos_x, self.player_pos_y))

    def shooting(self):
        if self.shoot:
            if current_time - self.static_time <= self.shoot_load:
                pass
            else:
                bullet_posx = self.player_pos_x + self.player_img.get_width()/2-self.bullet_img.get_width()/2
                bullet_posy = self.player_pos_y + self.player_img.get_height()/2 - self.bullet_img.get_height()/2
                self.bullets_list.append([bullet_posx, bullet_posy])
                self.static_time = current_time
        for bullet_position in self.bullets_list:
            screen.blit(self.bullet_img, (bullet_position[0], bullet_position[1]))
            bullet_position[1] -= 600 * dt
            if bullet_position[1] < 0:
                self.bullets_list.pop(self.bullets_list.index(bullet_position))

    def checking_for_inputs(self):
        global pause_status
        for event_ in pygame.event.get():
            if event_.type == QUIT:
                pygame.quit()
                sys.exit()

            pressed = pygame.key.get_pressed()
            if pressed[up_button]:
                self.up_key_pressed = True
            else:
                self.up_key_pressed = False

            if pressed[down_button]:
                self.down_key_pressed = True
            else:
                self.down_key_pressed = False

            if pressed[left_button]:
                self.left_key_pressed = True
            else:
                self.left_key_pressed = False

            if pressed[right_button]:
                self.right_key_pressed = True
            else:
                self.right_key_pressed = False
            try:
                if pressed[shoot_button]:
                    self.shoot = True
                else:
                    self.shoot = False
            except:
                pass

            if event_.type == MOUSEBUTTONDOWN:
                self.shoot = True
                if screen.get_width() - button69.get_width() <= x_mouse <= screen.get_width() and 0 <= y_mouse <=\
                        button69.get_height():
                    pause_status = True
            if event_.type == MOUSEBUTTONUP:
                self.shoot = False
            if event_.type == END_SONG:
                next_song()

    def display_health_bar(self):
        if self.health > self.max_health:
            self.health = self.max_health
        self.health_bar = pygame.Surface([self.health/self.max_health * 200, 30])
        self.health_red = pygame.Surface([200, 30])
        self.health_bar.fill((76, 153, 0))
        self.health_red.fill((255, 51, 51))
        screen.blit(self.health_red, (380, 510))
        screen.blit(self.health_bar, (380, 510))


movements = ['rotation', 'dance_x', 'triangle', 'ping_pong', 'random', 'zigzag']


class Enemies(pygame.sprite.Sprite):

    def __init__(self, img_path, position, health, shoot_load, shoot_wait, bullet_damage_p, bullet_img_p):
        super().__init__()
        # For the initialisation of position
        self.initialisation = 0
        # For uploading the image of the enemie
        self.image = img_path
        # Putting the image in a rect object to facilitate its movement
        self.rect = self.image.get_rect()
        self.rect.centerx = position[0]
        self.rect.centery = position[1]

        # FOR TRIANGLE MOVEMENT
        # For rotation movement
        r = 50
        y = self.rect.centery
        x = self.rect.centerx - r
        self.rotation_x = random.randint(x-r+1, x+r-1)
        self.rotation = (x, y, r)
        # For the dance_x and rotation or idk
        self.path = []
        # INITIALISING THE ENEMIE SPEEDS IN MOVEMENTS
        self.velocity = 2
        self.velocity_y = 2
        # FIX POINT WE NEED SOME TIMES TO DO THINGS ONCE IN A LOOP
        self.know = 0
        # FIXING A TIME FOR EACH ENEMY
        self.current_time = 0
        self.static_time = 0
        self.static_shoot_time = 0
        #
        self.random_x = random.randint(0, 768)
        self.random_y = random.randint(0, 350)
        self.on_collision = 0
        self.movement = 'rotation'

        self.health = health
        self.max_health = health
        self.shoot_load = shoot_load
        self.shoot_wait = shoot_wait
        self.bullet_image = pygame.image.load(os.path.join('images', bullet_img_p))
        self.bullets_positions = []
        self.bullet_damage = bullet_damage_p

        # SETTING HEALTH BAR
        self.health_bar = pygame.Surface([self.health/self.max_health * 100, 10])
        self.health_red = pygame.Surface([100, 10])
        self.static_health_time = 0
        self.show_health = False

    def move(self):
        self.current_time = pygame.time.get_ticks()
        if self.movement == "rotation":
            if self.know == 0:
                r = 50
                y = self.rect.centery
                x = self.rect.centerx - r
                self.rotation = (x, y, r)
                self.know += 1
            if self.velocity > 0:
                if self.rect.centerx + self.velocity <= self.rotation[0] + self.rotation[2]:
                    self.rect.centerx += self.velocity
                    self.rect.centery =\
                        math.sqrt(
                            math.pow(self.rotation[2], 2) - math.pow(self.rect.centerx-self.rotation[0], 2)
                        )+self.rotation[1]
                else:
                    self.velocity = self.velocity * -1
            else:
                if self.rect.centerx + self.velocity>= self.rotation[0] - self.rotation[2]:
                    self.rect.centerx += self.velocity
                    self.rect.centery =\
                        -math.sqrt(
                            math.pow(self.rotation[2], 2) - math.pow(self.rect.centerx-self.rotation[0], 2)
                        )+self.rotation[1]
                else:
                    self.velocity = self.velocity * -1
        elif self.movement == 'triangle':
            if self.know == 0:
                self.path = [self.rect.centerx - 100, self.rect.centerx + 100, self.rect.centerx]
                if self.rect.centery - 100 < 0:
                    self.velocity = self.velocity * -1
                self.know += 1
            if self.velocity > 0:
                if self.path[0] <= self.rect.centerx + self.velocity <= self.path[1]:
                    self.rect.centerx += self.velocity
                else:
                    self.velocity = self.velocity * -1
            else:
                if self.rect.centerx > self.path[2]:
                    self.rect.centerx += self.velocity
                    self.rect.centery += -self.velocity_y
                elif self.path[2] >= self.rect.centerx > self.path[0]:
                    self.rect.centerx += self.velocity
                    self.rect.centery += self.velocity_y
                else:
                    self.velocity = self.velocity * -1
        elif self.movement == 'zigzag':
            if self.velocity > 0:
                if self.rect.centerx + self.velocity <= screen.get_width()-32:
                    self.rect.centerx += self.velocity
                    if self.velocity_y > 0:
                        if self.know < 30:
                            self.rect.centery += self.velocity_y
                            self.know += 1
                        else:
                            self.velocity_y = self.velocity_y * -1
                    else:
                        if self.know > -30:
                            self.rect.centery += self.velocity_y
                            self.know -= 1
                        else:
                            self.velocity_y = self.velocity_y * -1
                else:
                    self.velocity = self.velocity * -1
            else:
                if self.rect.centerx + self.velocity >= 0:
                    self.rect.centerx += self.velocity
                    if self.velocity_y > 0:
                        if self.know < 30:
                            self.rect.centery += self.velocity_y
                            self.know += 1
                        else:
                            self.velocity_y = self.velocity_y * -1
                    else:
                        if self.know > -30:
                            self.rect.centery += self.velocity_y
                            self.know -= 1
                        else:
                            self.velocity_y = self.velocity_y * -1
                else:
                    self.velocity = self.velocity * -1
        elif self.movement == 'random':
            if self.rect.centerx < self.random_x:
                self.rect.centerx += self.velocity
            elif self.rect.centerx > self.random_x:
                self.rect.centerx -= self.velocity
            else:
                if self.rect.centery == self.random_y:
                    self.random_x = random.randint(0, 768)
                    self.random_y = random.randint(0, 350)
                else:
                    pass
            if self.rect.centery < self.random_y:
                self.rect.centery += self.velocity
            elif self.rect.centery > self.random_y:
                self.rect.centery -= self.velocity
            else:
                if self.rect.centerx == self.random_x:
                    self.random_x = random.randint(0, 768)
                    self.random_y = random.randint(0, 350)
                else:
                    pass
        elif self.movement == 'dance_x':
            if self.velocity < 0:
                if self.know + 1 < 50:
                    self.rect.centerx += self.velocity
                    self.know += 1
                else:
                    self.velocity = self.velocity * -1
            else:
                if self.know - 1 > -50 :
                    self.rect.centerx += self.velocity
                    self.know -= 1
                else:
                    self.velocity = self.velocity * -1
        elif self.movement == 'ping_pong':
            if self.velocity > 0:
                if self.rect.centerx + self.velocity < 928:
                    self.rect.centerx += self.velocity
                else:
                    self.velocity = self.velocity * -1
            else:
                if self.rect.centerx + self.velocity > 0:
                    self.rect.centerx += self.velocity
                else:
                    self.velocity = self.velocity * -1

            if self.velocity_y > 0:
                if self.rect.centery + self.velocity_y < 318:
                    self.rect.centery += self.velocity_y
                else:
                    self.velocity_y = self.velocity_y * -1
            else:
                if self.rect.centery + self.velocity_y > 0:
                    self.rect.centery += self.velocity_y
                else:
                    self.velocity_y = self.velocity_y * -1
        if self.movement == 'follow':
            if self.rect.centerx < player.player_pos_x:
                self.velocity = 2
                self.rect.centerx += self.velocity
            elif self.rect.centerx > player.player_pos_x:
                self.velocity = -2
                self.rect.centerx += self.velocity

            if self.rect.centery < player.player_pos_y:
                self.velocity_y = 2
                self.rect.centery += self.velocity_y
            elif self.rect.centery > player.player_pos_y:
                self.velocity_y = -2
                self.rect.centery += self.velocity_y

    def shooting(self):
        if self.current_time - self.static_time < self.shoot_wait:
            if self.current_time - self.static_shoot_time < self.shoot_load:
                pass
            else:
                bullet_posx = self.rect.centerx + self.image.get_width() / 2 - self.bullet_image.get_width() / 2
                bullet_posy = self.rect.centery + 3 * self.image.get_height() / 2
                self.bullets_positions.append([bullet_posx, bullet_posy])
                self.static_shoot_time = self.current_time
        elif self.current_time - self.static_time < 2 * self.shoot_wait:
            pass
        else:
            self.static_time = self.current_time

    def display_health(self):
        if self.show_health:
            if current_time - self.static_health_time < 2000:
                if self.health < 0:
                    pass
                else:
                    self.health_bar = pygame.Surface([self.health/self.max_health * 100, 10])
                    self.health_bar.fill((76, 153, 0))
                    self.health_red.fill((255, 51, 51))
                    screen.blit(self.health_red,
                                (self.rect.centerx + self.image.get_width()/2-50, self.rect.centery - 20))
                    screen.blit(self.health_bar,
                                (self.rect.centerx + self.image.get_width()/2-50, self.rect.centery - 20))
            else:
                self.show_health = False


def display_pause_button(xmouse, ymouse):
    if screen.get_width()-button.get_width() <= xmouse <= screen.get_width() and 0 <= ymouse <= button.get_height():
        pause_img = pause1
    else:
        pause_img = pause
    white_opac_bg.set_alpha(127)
    screen.blit(white_opac_bg, (screen.get_width()-white_opac_bg.get_width()-4, +3))
    screen.blit(pause_img, (screen.get_width()-button.get_width()+8, 8))


next_wave = True
number_of_enemies = 1
propancy = 0
enemies_img = pygame.image.load(os.path.join('images', 'space-ship.png'))
enemie_health = 100
enemie_shoot_load = 2000
enemie_shoot_wait = 10000

bullet_damage = 0
bullet_img = 'bullet.png'
# ENEMIES IMAGES
space_ship_enemie = pygame.image.load(os.path.join('images', 'space-ship.png'))
ufo_enemie = pygame.image.load(os.path.join('images', 'ufo.png'))
ricardo_enemie = pygame.image.load(os.path.join('images', 'ricardo-removebg-preview (1).png'))
dababy_enemy = pygame.image.load(os.path.join('images', 'dababy.png'))
keremit_enemy = pygame.image.load(os.path.join('images', 'keremit.png'))
static_calm_time = 0
calm_time = 15000
wave_movement = random.choice(movements)
level1 = [[space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie], [0, 448, 928, 0, 448, 928], [-350, -250, -350, -250, -150, -250], [0, 100, 0, 100, 200, 100]]
level2 = [[space_ship_enemie, ufo_enemie, ufo_enemie, space_ship_enemie, space_ship_enemie, ufo_enemie, ufo_enemie, space_ship_enemie], [0, 288, 608, 928, 0, 288, 608, 928], [-350, -250, -350, -250, -150, -250, -150, -250], [0, 100, 0, 100, 200, 100, 200, 100]]
level3 = [[dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy], [0, 288, 608, 928], [-350, -250, -350, -250], [0, 100, 0, 100]]
level4 = [[ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie], [0, 288, 608, 928, 0, 288, 608, 928], [-350, -250, -350, -250, -150, -150, -150, -150], [0, 100, 0, 100, 200, 200, 200, 200]]
level5 = [[ufo_enemie, ricardo_enemie, dababy_enemy, ricardo_enemie, ufo_enemie],
          [0, 208, 448, 688, 928], [-350, -250, -150, -250, -350], [0, 100, 200, 100, 0]]
level6 = [[ufo_enemie, ricardo_enemie, keremit_enemy, ricardo_enemie, dababy_enemy],
          [0, 208, 416, 688, 928], [-350, -250, -150, -250, -350], [0, 100, 200, 100, 0]]
level7 = [[ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie],
          [0, 160, 352, 544, 736, 928, 0, 160, 352, 544, 736, 928], [-250, -250, -250, -250, -250, -250, -150, -150, -150, -150, -150, -150], [0, 0, 0, 0, 0, 0, 100, 100, 100, 100, 100, 100]]
level8 = [[dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie],
          [0, 160, 352, 544, 736, 928, 0, 160, 352, 544, 736, 928], [-250, -250, -250, -250, -250, -250, -150, -150, -150, -150, -150, -150], [0, 0, 0, 0, 0, 0, 100, 100, 100, 100, 100, 100]]
level9 = [[keremit_enemy, ricardo_enemie, ricardo_enemie, keremit_enemy, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie],
          [0, 288, 608, 928, 0, 288, 608, 928], [-250, -250, -250, -250, -150, -150, -150, -150], [0, 0, 0, 0, 100, 100, 100, 100]]
level10 = [[keremit_enemy, dababy_enemy, dababy_enemy, keremit_enemy, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie],
          [0, 288, 608, 928, 0, 288, 608, 928], [-250, -250, -250, -250, -150, -150, -150, -150], [0, 0, 0, 0, 100, 100, 100, 100]]
level11= [[ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, dababy_enemy, dababy_enemy],
          [48, 128, 208, 288, 368, 448, 528, 608, 688, 768, 848, 928, 288, 608], [-250, -250, -250, -250, -250, -250, -250, -250, -250, -250, -250, -250, -150, -150], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 100]]
level12 = [[ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, dababy_enemy, dababy_enemy],
           [48, 128, 208, 288, 368, 448, 528, 608, 688, 768, 848, 928, 288, 608], [-250, -250, -250, -250, -250, -250, -250, -250, -250, -250, -250, -250, -150, -150], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 100]]
level13 = [[ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, keremit_enemy, keremit_enemy],
           [48, 128, 208, 288, 368, 448, 528, 608, 688, 768, 848, 928, 288, 608], [-250, -250, -250, -250, -250, -250, -250, -250, -250, -250, -250, -250, -150, -150], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 100]]
level14 = [[dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, keremit_enemy, keremit_enemy],
           [48, 128, 208, 288, 368, 448, 528, 608, 688, 768, 848, 928, 288, 608], [-250, -250, -250, -250, -250, -250, -250, -250, -250, -250, -250, -250, -150, -150], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 100]]
level15 = [[keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie],
          [0, 208, 416, 688, 928, 0, 208, 416, 688, 928], [-250, -250, -250, -250, -250, -150, -150, -150, -150, -150], [0, 0, 0, 0, 0, 100, 100, 100, 100, 100]]
level16 = [[keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy],
           [0, 208, 416, 688, 928, 0, 208, 416, 688, 928], [-250, -250, -250, -250, -250, -150, -150, -150, -150, -150], [0, 0, 0, 0, 0, 100, 100, 100, 100, 100]]
level17 = [[space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy],
           [48, 128, 208, 288, 368, 448, 528, 608, 688, 768, 848, 928, 0, 160, 352, 544, 736, 928], [-250, -250, -250, -250, -250, -250, -250, -250, -250, -250, -250, -250, -150, -150, -150, -150, -150, -150], [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 0, 0, 0, 0, 0, 0]]
level18 = [[ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy],
           [48, 128, 208, 288, 368, 448, 528, 608, 688, 768, 848, 928, 0, 160, 352, 544, 736, 928], [-250, -250, -250, -250, -250, -250, -250, -250, -250, -250, -250, -250, -150, -150, -150, -150, -150, -150], [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 0, 0, 0, 0, 0, 0]]
level19 = [[space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy],
           [0, 288, 608, 928, 0, 288, 608, 928, 0, 288, 608, 928], [-350, -350, -350, -350, -250, -250, -250, -250, -150, -150, -150, -150], [0, 0, 0, 0, 100, 100, 100, 100, 200, 200, 200, 200]]
level20 = [[ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy],
            [0, 288, 608, 928, 0, 288, 608, 928, 0, 288, 608, 928], [-350, -350, -350, -350, -250, -250, -250, -250, -150, -150, -150, -150], [0, 0, 0, 0, 100, 100, 100, 100, 200, 200, 200, 200]]
level21 = [[ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy],
           [0, 288, 608, 928, 0, 288, 608, 928, 0, 288, 608, 928], [-350, -350, -350, -350, -250, -250, -250, -250, -150, -150, -150, -150], [0, 0, 0, 0, 100, 100, 100, 100, 200, 200, 200, 200]]
level22 = [[dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy],
           [0, 288, 608, 928, 0, 288, 608, 928, 0, 288, 608, 928], [-350, -350, -350, -350, -250, -250, -250, -250, -150, -150, -150, -150], [0, 0, 0, 0, 100, 100, 100, 100, 200, 200, 200, 200]]
level23 = [[dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy],
            [0, 288, 608, 928, 0, 288, 608, 928, 0, 288, 608, 928], [-350, -350, -350, -350, -250, -250, -250, -250, -150, -150, -150, -150], [0, 0, 0, 0, 100, 100, 100, 100, 200, 200, 200, 200]]
level24 = [[keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy],
           [0, 288, 608, 928, 0, 288, 608, 928, 0, 288, 608, 928], [-350, -350, -350, -350, -250, -250, -250, -250, -150, -150, -150, -150], [0, 0, 0, 0, 100, 100, 100, 100, 200, 200, 200, 200]]
level25 = [[ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie],
           [48, 128, 208, 288, 368, 448, 528, 608, 688, 768, 848, 928], [-150, -150, -150, -150, -150, -150, -150, -150, -150, -150, -150, -150], [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]]
level26 = [[dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy],
           [48, 128, 208, 288, 368, 448, 528, 608, 688, 768, 848, 928],
           [-150, -150, -150, -150, -150, -150, -150, -150, -150, -150, -150, -150],
           [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]]
level27 = [[keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy],
           [16, 96, 176, 256, 336, 416, 496, 576, 656, 736, 816, 896],
           [-150, -150, -150, -150, -150, -150, -150, -150, -150, -150, -150, -150],
           [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]]
level28 = [[space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie,
            space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie,
            space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie],
           [48, 128, 208, 288, 368, 448, 528, 608, 688, 768, 848, 928, 48, 128, 208, 288, 368, 448, 528, 608, 688, 768, 848, 928, 48, 128, 208, 288, 368, 448, 528, 608, 688, 768, 848, 928],
           [-350, -350, -350, -350, -350, -350, -350, -350, -350, -350, -350, -350, -250, -250, -250, -250, -250, -250, -250, -250, -250, -250, -250, -250, -150, -150, -150, -150, -150, -150, -150, -150, -150, -150, -150, -150],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200]]
level29 = [[space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie,
            ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie, ufo_enemie,
            ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie],
           [48, 128, 208, 288, 368, 448, 528, 608, 688, 768, 848, 928, 48, 128, 208, 288, 368, 448, 528, 608, 688,
            768, 848, 928, 48, 128, 208, 288, 368, 448, 528, 608, 688, 768, 848, 928],
           [-350, -350, -350, -350, -350, -350, -350, -350, -350, -350, -350, -350, -250, -250, -250, -250, -250, -250,
            -250, -250, -250, -250, -250, -250, -150, -150, -150, -150, -150, -150, -150, -150, -150, -150, -150, -150],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 200, 200,
            200, 200, 200, 200, 200, 200, 200, 200, 200, 200]
           ]
level30 = [[space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie, space_ship_enemie,
            ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie, ricardo_enemie,
            dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy, keremit_enemy, keremit_enemy, keremit_enemy, keremit_enemy, dababy_enemy, dababy_enemy, dababy_enemy, dababy_enemy],
           [48, 128, 208, 288, 368, 448, 528, 608, 688, 768, 848, 928, 48, 128, 208, 288, 368, 448, 528, 608, 688,
            768, 848, 928, 48, 128, 208, 256, 336, 416, 496, 608, 688, 768, 848, 928],
           [-350, -350, -350, -350, -350, -350, -350, -350, -350, -350, -350, -350, -250, -250, -250, -250, -250, -250,
            -250, -250, -250, -250, -250, -250, -150, -150, -150, -150, -150, -150, -150, -150, -150, -150, -150, -150],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 200, 200,
            200, 200, 200, 200, 200, 200, 200, 200, 200, 200]
           ]
levels_list = [level1, level2, level3, level4, level5, level6, level7, level8, level9, level10, level11, level12, level13, level14, level15, level16, level17, level18, level19, level20, level21, level22, level23, level24, level25, level26, level27, level28, level29, level30]
level_recompense_list = [250, 350, 500, 1000, 1500, 2500, 3500, 5000, 7500, 10000, 15000, 20000, 30000, 50000, 80000, 100000, 120000, 140000, 160000, 180000, 200000, 220000, 240000, 260000, 280000, 300000, 320000, 340000, 360000, 380000]
level_index = data['level_index']
level_names_list = ['LEVEL 1', 'LEVEL 2', 'LEVEL 3', 'LEVEL 4', 'LEVEL 5', 'LEVEL 6', 'LEVEL 7', 'LEVEL 8', 'LEVEL 9',
                    'LEVEL 10', 'LEVEL 11', 'LEVEL 12', 'LEVEL 13', 'LEVEL 14', 'LEVEL 15', 'LEVEL 16', 'LEVEL 17',
                    'LEVEL 18', 'LEVEL 19', 'LEVEL 20', 'LEVEL 21', 'LEVEL 22', 'LEVEL 23', 'LEVEL 24', 'LEVEL 25',
                    'LEVEL 26', 'LEVEL 27', 'LEVEL 28', 'LEVEL 29', 'LEVEL 30']
level_text_alpha = 254
game_type = 'Arcade'
level_text_static = -1
show_level_text = False


def wave():
    global next_wave, number_of_enemies, enemies_img, enemie_shoot_load, enemie_health,\
        enemie_shoot_wait, bullet_damage, bullet_img, calm_time, wave_movement, static_calm_time, game_type,\
        levels_list, level_index, level_text_alpha, show_level_text, level_text_static, barier_on, all_in_pos
    if next_wave:
        static_calm_time = current_time
        wave_movement = random.choice(movements)
        barier_on = True
        all_in_pos = 0
        player.player_pos_x = 448
        player.player_pos_y = 460
        number_of_enemies += 1
        enemy_to_get_y_w = []
        enemy_list_w = []
        in_pos_w = []
        enemy_alive_w = []
        if game_type == 'Arcade':
            for a in range(number_of_enemies):
                enemies_img_index = random.randint(0, 100)
                if 0 <= enemies_img_index <= 60 - 2*propancy:
                    enemies_img = space_ship_enemie
                    enemie_health = 400
                    bullet_damage = 50
                    bullet_img = 'bullet.png'
                    enemie_shoot_load = 4000
                    enemie_shoot_wait = 10000
                if 61 - 2 * propancy <= enemies_img_index <= 80 - propancy:
                    enemies_img = ufo_enemie
                    enemie_health = 1000
                    bullet_damage = 100
                    bullet_img = 'alien_bullet.png'
                    enemie_shoot_load = 2000
                    enemie_shoot_wait = 10000
                if 81 - propancy <= enemies_img_index <= 90 - propancy/2:
                    enemies_img = ricardo_enemie
                    enemie_health = 2000
                    bullet_damage = 200
                    bullet_img = 'ricardo_bullet.png'
                    enemie_shoot_load = 4000
                    enemie_shoot_wait = 10000
                if 91 - propancy/2 <= enemies_img_index <= 95 - propancy/4:
                    enemies_img = dababy_enemy
                    enemie_health = 5200
                    bullet_damage = 250
                    bullet_img = 'dababy_bullet.png'
                    enemie_shoot_load = 500
                    enemie_shoot_wait = 10000
                if 96 - propancy/4 <= enemies_img_index <= 100:
                    enemies_img = keremit_enemy
                    enemie_health = 10000
                    bullet_damage = 350
                    bullet_img = 'keremit_bullet.png'
                    enemie_shoot_load = 250
                    enemie_shoot_wait = 10000
                enemy_to_get_y_w.append(random.randint(0, 300-enemies_img.get_height()))
                in_pos_w.append(False)
                enemy_alive_w.append(True)
                enemy_w = Enemies(enemies_img, [random.randint(0, 960-enemies_img.get_width()),
                                  random.randint(-350, 0-enemies_img.get_height())], enemie_health, enemie_shoot_load,
                                  enemie_shoot_wait, bullet_damage, bullet_img)
                enemy_list_w.append(enemy_w)
        elif game_type == 'Levels':
            if level_index < len(levels_list) - 1:
                level_index += 1
            show_level_text = True
            level_text_static = current_time
            level_text_alpha = 254
            for enemy_lvl_index in range(len(levels_list[level_index][0])):
                if levels_list[level_index][0][enemy_lvl_index] == space_ship_enemie:
                    enemies_img = space_ship_enemie
                    enemie_health = 400
                    bullet_damage = 50
                    bullet_img = 'bullet.png'
                    enemie_shoot_load = 4000
                    enemie_shoot_wait = 10000
                elif levels_list[level_index][0][enemy_lvl_index] == ufo_enemie:
                    enemies_img = ufo_enemie
                    enemie_health = 1000
                    bullet_damage = 100
                    bullet_img = 'alien_bullet.png'
                    enemie_shoot_load = 2000
                    enemie_shoot_wait = 10000
                elif levels_list[level_index][0][enemy_lvl_index] == ricardo_enemie:
                    enemies_img = ricardo_enemie
                    enemie_health = 2000
                    bullet_damage = 200
                    bullet_img = 'ricardo_bullet.png'
                    enemie_shoot_load = 4000
                    enemie_shoot_wait = 10000
                elif levels_list[level_index][0][enemy_lvl_index] == dababy_enemy:
                    enemies_img = dababy_enemy
                    enemie_health = 5200
                    bullet_damage = 250
                    bullet_img = 'dababy_bullet.png'
                    enemie_shoot_load = 500
                    enemie_shoot_wait = 10000
                elif levels_list[level_index][0][enemy_lvl_index] == keremit_enemy:
                    enemies_img = keremit_enemy
                    enemie_health = 10000
                    bullet_damage = 350
                    bullet_img = 'keremit_bullet.png'
                    enemie_shoot_load = 250
                    enemie_shoot_wait = 10000
                try:
                    enemy_to_get_y_w.append(levels_list[level_index][3][enemy_lvl_index])
                except Exception as e:
                    print(e)
                    print(level_index)
                in_pos_w.append(False)
                enemy_alive_w.append(True)
                enemy_w = Enemies(enemies_img, [levels_list[level_index][1][enemy_lvl_index], levels_list[level_index][2][enemy_lvl_index]], enemie_health, enemie_shoot_load,
                                  enemie_shoot_wait, bullet_damage, bullet_img)
                enemy_list_w.append(enemy_w)

        next_wave = False
        return enemy_to_get_y_w, enemy_list_w, enemy_alive_w, in_pos_w


collision1 = False
collision2 = False
collision4 = False
collision3 = False
collision9 = False
collision10 = False
collision11 = False
collision12 = False
x = 0
Level_status = 'Win'
sounds_volume = 0.5


def checking_for_collision():
    global player_health, playerImg, enemy_list, collision1, collision2, collision3, collision4,\
        enemy, game_over, collision9, collision10, collision11, collision12, score, coins_collected, recompense_list,\
        recompense_genre_list, ini_positions_list, x, coins, Level_status, sounds_volume

    # CHECKING FOR COLLISION BETWEEN THE PLAYER AND THE RECOMPENSES
    for position in ini_positions_list:
        if recompense_genre_list[ini_positions_list.index(position)] == 'coin':
            x = 50
        elif recompense_genre_list[ini_positions_list.index(position)] == 'med':
            x = 24
        elif recompense_genre_list[ini_positions_list.index(position)] == 'fire':
            x = 24
        elif recompense_genre_list[ini_positions_list.index(position)] == 'medkit':
            x = 32
        collision17 = bool(position[0] <= player.player_pos_x <= position[0] + x)
        collision18 = bool(player.player_pos_x <= position[0] <= player.player_pos_x + 64)
        collision19 = bool(position[1] <= player.player_pos_y <= position[1] + x)
        collision20 = bool(player.player_pos_y <= position[1] <= player.player_pos_y + 64)
        if (collision17 or collision18) and (collision19 or collision20):
            if recompense_genre_list[ini_positions_list.index(position)] == 'coin':
                coins_collected += enemy_coin_recompense_list[ini_positions_list.index(position)]
                coins += enemy_coin_recompense_list[ini_positions_list.index(position)]
            elif recompense_genre_list[ini_positions_list.index(position)] == 'med':
                player.health += 100
                if player.health > player.max_health:
                    player.health = player.max_health
            elif recompense_genre_list[ini_positions_list.index(position)] == 'fire':
                player.shoot_load -= 15
                player.bullet_speed += 0.2
            elif recompense_genre_list[ini_positions_list.index(position)] == 'medkit':
                player.health += 300
                if player.health > player.max_health:
                    player.health = player.max_health
            position[1] = 980

    # CHECK FOR COLLISION BETWEEN THE ENEMY BULLETS AND THE PLAYER
    for enemy in enemy_list:
        for b_position in enemy.bullets_positions:
            collision1 = bool(b_position[0] <= player.player_pos_x <= b_position[0] + enemy.bullet_image.get_width())
            collision2 =\
                bool(player.player_pos_x <= b_position[0] <= player.player_pos_x + player.player_img.get_width())
            collision3 = bool(b_position[1] <= player.player_pos_y <= b_position[1] + enemy.bullet_image.get_height())
            collision4 =\
                bool(player.player_pos_y <= b_position[1] <= player.player_pos_y + player.player_img.get_height())
            if (collision1 or collision2) and (collision3 or collision4):
                player.health -= enemy.bullet_damage
                b_position[1] = 600
                uh_sound = mixer.Sound('wahya.mp3')
                uh_sound.set_volume(sounds_volume)
                uh_sound.play()

    # CHECK FOR COLLISION BETWEEN THE PLAYER AND THE ENEMY
    for enemy in enemy_list:
        collision5 =\
            bool(player.player_pos_x <= enemy.rect.centerx <= player.player_pos_x + player.player_img.get_width())
        collision6 = bool(enemy.rect.centerx <= player.player_pos_x <= enemy.rect.centerx + enemy.image.get_width())
        collision7 =\
            bool(player.player_pos_y <= enemy.rect.centery <= player.player_pos_y + player.player_img.get_height())
        collision8 = bool(enemy.rect.centery <= player.player_pos_y <= enemy.rect.centery + enemy.image.get_width())
        if (collision5 or collision6) and (collision7 or collision8):
            player_current_health = player.health
            enemy_current_health = enemy.health
            player.health -= enemy_current_health
            enemy.health -= player_current_health

    # CHECK FOR COLLISION BETWEEN THE ENEMY AND THE PLAYER BULLETS:
    for enemy in enemy_list:
        for bullet_position in player.bullets_list:
            collision9 = \
                bool(bullet_position[0] <= enemy.rect.centerx <= bullet_position[0] + player.bullet_img.get_width())
            collision10 = bool(enemy.rect.centerx <= bullet_position[0] <= enemy.rect.centerx + enemy.image.get_width())
            collision11 = \
                bool(bullet_position[1] <= enemy.rect.centery <= bullet_position[1] + player.bullet_img.get_height())
            collision12 =\
                bool(enemy.rect.centery <= bullet_position[1] <= enemy.rect.centery + enemy.image.get_height())
            if (collision9 or collision10) and (collision11 or collision12):
                enemy.health -= player.bullet_damage
                bullet_position[1] = -30
                enemy.static_health_time = current_time
                enemy.show_health = True

    # CHECKING FOR COLLISION BETWEEN THE PLAYER BULLETS AND THE ENEMY BULLETS

    for enemy in enemy_list:
        for e_bullet_position in enemy.bullets_positions:
            for bullet_position in player.bullets_list:
                collision13 = bool(
                    e_bullet_position[0] <= bullet_position[0] <= e_bullet_position[0] + enemy.bullet_image.get_width())
                collision14 = bool(
                    bullet_position[0] <= e_bullet_position[0] <= bullet_position[0] + player.bullet_img.get_width())
                collision15 = bool(
                    e_bullet_position[1] <= bullet_position[1] <= e_bullet_position[1] +
                    enemy.bullet_image.get_height())
                collision16 = bool(
                    bullet_position[1] <= e_bullet_position[1] <= bullet_position[1] + player.bullet_img.get_height())
                if (collision13 or collision14) and (collision15 or collision16):
                    bullet_position[1] = -30
                    e_bullet_position[1] = 580

    # CHECKING FOR COLLISION BETWEEN THE PLAYER BULLETS AND THE BARIER
    if barier_on:
        for bullet_position in player.bullets_list:
            if 300 <= bullet_position[1] <= 320:
                bullet_position[1] = -30
    for enemy in enemy_list:
        if enemy.health <= 0:
            if enemy.image == keremit_enemy:
                keremit_sound = mixer.Sound('UUUH.mp3')
                keremit_sound.set_volume(sounds_volume)
                keremit_sound.play()
                enemy_coin_recompense_list.append(100)
            elif enemy.image == ufo_enemie:
                alien_sound = mixer.Sound('UUUH.mp3')
                alien_sound.set_volume(sounds_volume)
                alien_sound.play()
                enemy_coin_recompense_list.append(25)
            elif enemy.image == space_ship_enemie:
                space_ship_sound = mixer.Sound('UUUH.mp3')
                space_ship_sound.set_volume(sounds_volume)
                space_ship_sound.play()
                enemy_coin_recompense_list.append(10)
            elif enemy.image == ricardo_enemie:
                ricardo_sound = mixer.Sound('UUUH.mp3')
                ricardo_sound.set_volume(sounds_volume)
                ricardo_sound.play()
                enemy_coin_recompense_list.append(50)
            elif enemy.image == dababy_enemy:
                dababy_sound = mixer.Sound('UUUH.mp3')
                dababy_sound.set_volume(sounds_volume)
                dababy_sound.play()
                enemy_coin_recompense_list.append(75)
            score += 100
            in_pos.pop(enemy_list.index(enemy))
            percentage = random.randint(0, 100)
            if 0 <= percentage <= 55:
                recompense_list.append(coin_img_list[0])
                recompense_genre_list.append('coin')
            elif 55 < percentage <= 75:
                recompense_list.append(meds_img)
                recompense_genre_list.append('med')
            elif 75 < percentage <= 90:
                recompense_list.append(fire_img)
                recompense_genre_list.append('fire')
            else:
                recompense_list.append(medkit_img)
                recompense_genre_list.append('medkit')
            ini_positions_list.append([enemy.rect.centerx, enemy.rect.centery])
            enemy_list.pop(enemy_list.index(enemy))
    if player.health <= 0:
        if game_type == 'Arcade':
            game_over = True
        else:
            game_over = True
            Level_status = 'Lost'


volume_icon1_x = 364 + mixer.music.get_volume()*200
volume_icon2_x = 364 + sounds_volume * 200
volume_icon1_y = 0
volume_icon2_y = 0
music_sounds_rect_x = 0
music_sounds_rect_y = 0
sounds_rect_x = 0
sounds_rect_y = 0
music_sounds_rect_width = mixer.music.get_volume()*200
sounds_rect_width = sounds_volume * 200
click_sounds = False
click_music = False


def set_volume_graph_pause(mousex):
    global volume_icon2_x, volume_icon1_x, click_sounds, click_music, music_sounds_rect_x, sounds_rect_x,\
        music_sounds_rect_width, sounds_rect_width, sounds_volume
    if click_music:
        if music_sounds_rect_x < mousex <= music_sounds_rect_x + 200:
            volume_icon1_x = mousex - 10
            music_sounds_rect_width = mousex - music_sounds_rect_x
            mixer.music.set_volume(music_sounds_rect_width / 200)
    if click_sounds:
        if sounds_rect_x < mousex <= sounds_rect_x + 200:
            volume_icon2_x = mousex - 10
            sounds_rect_width = mousex - sounds_rect_x
            sounds_volume = sounds_rect_width/200


def show_score(x_, y):
    global score, show_level_text, level_text_static, level_text_alpha
    score_text_p = font2.render("SCORE: " + str(score), True, (150, 50, 80))
    screen.blit(score_text_p, (x_, y))
    level_text = restart_font.render(level_names_list[level_index], True, (250, 250, 250))

    if show_level_text:
        if current_time - level_text_static < 2000:
            screen.blit(level_text, (screen.get_width()/2 - level_text.get_width()/2,
                                     screen.get_height()/2 - level_text.get_height()/2))
            level_text_alpha -= 254 / (2000 / dt)
            level_text.set_alpha(level_text_alpha)
        else:
            show_level_text = False


enemy_to_get_y = []
enemy_list = []
in_pos = []
all_in_pos = 0
barier_on = True
barier = pygame.Surface([960, 20])
move = False
movement_initialisation = 0
player_pas_x = 0
player_pas_y = 0
# GAME OVER FONT
game_over_font = pygame.font.Font('Edge Of Madness.otf', 50)
score = 0
coins_collected = 0
restart_button_img = pygame.image.load(os.path.join('images', 'selected_button.png'))
menu_button_img = pygame.image.load(os.path.join('images', 'selecte_button.png'))

# MUSIC INTERFACE INPUTS
#
#
#
# BUTTON BACKGROUND
button = pygame.image.load(os.path.join('images', 'bg_button1.png'))

music_font = pygame.font.Font('Edge Of Madness.otf', 10)
# LABEL IMAGE
label_list = ['blank-button2.png', 'blank-button3.png', 'blank-button4.png', 'blank-button5.png', 'blank-button6.png']
label_img_lista = []
for label_name in label_list:
    label_img = pygame.image.load(os.path.join('images', label_name))
    label_img_lista.append(label_img)


# INITIALISING THE ICONS
music = 'music-album.png'
previous = 'previous.png'
next_name = 'next.png'

play_man = 'play.png'
volume = 'volume.png'

# INITIALISING THE POSITIONS OF THE ICONS
xp, yp = (448, 450)
xv, yv = (920, 0)
xn, yn = (548, 450)
xpr, ypr = (348, 450)
xm, ym = (448, 10)
END_SONG = pygame.USEREVENT+1

# VOLUME SETTING
icon = pygame.image.load(os.path.join('images', 'volume_button.png'))
rect_height = mixer.music.get_volume() * 100
rect_posy1 = 60

widget_posx11 = 44
widget_posy1 = 44 + rect_height
rect_surface = pygame.Surface([20, rect_height])
music_rect_surface1 = pygame.Surface([20, 100])
click = False


def set_volume_graph(mousey):
    global widget_posx11, widget_posy1, rect_height, rect_posy1, click
    if click:
        if rect_posy1 < y_mouse <= rect_posy1 + 100:
            widget_posy1 = mousey-10
            rect_height = mousey - rect_posy1
            mixer.music.set_volume(rect_height/100)


def display():
    screen.blit(music_rect_surface1, (50, rect_posy1))
    screen.blit(rect_surface, (50, rect_posy1))
    screen.blit(icon, (widget_posx11, widget_posy1))


# DEFINING A FUNCTION THAT WILL REFRESH IMGS OF THE ICONS
def icons_screen():
    global xp, yp, xpr, ypr, xn, yn, xm, ym, xv, yv
    play_icon = pygame.image.load(os.path.join('music_icons', play_man))
    previous_icon = pygame.image.load(os.path.join('music_icons', previous))
    next_icon = pygame.image.load(os.path.join('music_icons', next_name))
    music_icon = pygame.image.load(os.path.join('music_icons', music))
    volume_icon = pygame.image.load(os.path.join('music_icons', volume))
    screen.blit(button, (xp - 8, yp - 8))
    screen.blit(play_icon, (xp, yp))
    screen.blit(button, (xv - 8, yv - 8))
    screen.blit(volume_icon, (xv, yv))
    screen.blit(button, (xn - 8, yn - 8))
    screen.blit(next_icon, (xn, yn))
    screen.blit(button, (xpr - 8, ypr - 8))
    screen.blit(previous_icon, (xpr, ypr))
    screen.blit(button, (xm - 8, ym - 8))
    screen.blit(music_icon, (xm, ym))


song_list = []
song_list_path = []
root = tkinter.Tk()
root.wm_withdraw()

current_song = ''


def previous_song():
    global current_song, song_list, status_play
    try:
        i = song_list.index(current_song)
        if i > 0:
            current_song = song_list[i-1]
        else:
            current_song = song_list[-1]
        mixer.music.load(current_song)
        mixer.music.play(0)
        mixer.music.set_endevent(END_SONG)
        status_play = False
    except:
        pass


def next_song():
    global current_song, song_list, status_play
    try:
        i = song_list_path.index(current_song)
        if i < len(song_list_path)-1:
            current_song = song_list_path[i+1]
        else:
            current_song = song_list_path[0]
        mixer.music.load(current_song)
        mixer.music.play(0)
        mixer.music.set_endevent(END_SONG)
        status_play = False
    except:
        pass


def add_song():
    global song_list, song_list_path, current_song
    song = filedialog.askopenfilename(initialdir='c:/', title='choose a song', filetypes=(("mp3 Files", "*.mp3"), ))
    if len(song_list) < 5:
        if song in song_list_path:
            pass
        else:
            song_list.append(song)
            song_list_path.append(song)
            current_song = song_list_path[0]
            root.iconify()


status_play = True
static_play = 0
play_endevent = 0


class Pause(object):

    def __init__(self):
        global status_play
        self.paused = status_play

    def initial_status_play(self):
        self.paused = status_play

    def pause_unpause(self):
        global current_song
        try:
            if self.paused:
                pygame.mixer.music.unpause()
            if not self.paused:
                pygame.mixer.music.pause()
        except:
            pass

    def play_initial(self):
        try:
            mixer.music.play(0)
            mixer.music.set_endevent(END_SONG)
        except:
            pass

PLAY = Pause()
labl_img_list = []
on_top = False
song_on_top = 6
velocity = 1
know = 0
delete_song_status = False


def display_song(click_, click_song_index_p):
    global song_list, positions, labl_img_list, on_top, song_on_top, velocity, know, delete_song_status, current_song
    for song_index in range(len(song_list)):
        if click_ and song_index == click_song_index_p:
            pass
        else:
            if song_index == song_list_path.index(current_song):
                if velocity < 0:
                    if know + 1 < 50:
                        positions[song_index][0] += velocity
                        know += 1
                    else:
                        velocity = velocity * -1
                else:
                    if know - 1 > -50:
                        positions[song_index][0] += velocity
                        know -= 1
                    else:
                        velocity = velocity * -1
            else:
                positions[song_index] = [250, positions[song_index][1]]
            img_labl = random.choice(label_img_lista)
            song_name = song_list[song_index].split("/")
            song_name = song_name[-1].replace(".mp3", "")
            labl_img_list.append(img_labl)
            screen.blit(labl_img_list[song_index], positions[song_index])
            song_text = music_font.render(song_name, True, (255, 255, 255))
            screen.blit(song_text,
                    (positions[song_index][0] + 230 - song_text.get_width() / 2,
                     positions[song_index][1] + 10 + song_text.get_height()/2))
    if click_:
        screen.blit(labl_img_list[click_song_index_p], (x_mouse-230, y_mouse-30))
        song_name = song_list[click_song_index_p].split("/")
        song_name = song_name[-1].replace(".mp3", "")
        song_text = music_font.render(song_name, True, (255, 255, 255))
        screen.blit(song_text,
                          (x_mouse - song_text.get_width() / 2, y_mouse -20 + song_text.get_height()/2))
        for position in positions:
            if position == positions[click_song_index_p]:
                pass
            else:
                if position[0] <= x_mouse <= position[0]+460 and position[1] <= y_mouse <= position[1]+60:
                    on_top = True
                    song_on_top = positions.index(position)
                if 500 <= y_mouse <= 540:
                    delete_song_status = True
                else:
                    delete_song_status = False

    else:
        if on_top:
            try:
                song_on_top_name = song_list[song_on_top]
                song_to_replace = song_list[click_song_index_p]
                img_on_top_name = labl_img_list[song_on_top]
                img_to_replace = labl_img_list[click_song_index_p]
                song_list_path.remove(song_on_top_name)
                song_list_path.remove(song_to_replace)
                song_list.remove(song_on_top_name)
                song_list.remove(song_to_replace)
                labl_img_list.remove(img_on_top_name)
                labl_img_list.remove(img_to_replace)
                if song_on_top < click_song_index_p:
                    song_list.insert(song_on_top, song_to_replace)
                    song_list.insert(click_song_index_p, song_on_top_name)
                    labl_img_list.insert(song_on_top, img_to_replace)
                    labl_img_list.insert(click_song_index_p, img_on_top_name)
                    song_list_path.insert(song_on_top, song_to_replace)
                    song_list_path.insert(click_song_index_p, song_on_top_name)
                else:
                    song_list.insert(song_on_top-1, song_to_replace)
                    song_list.insert(click_song_index_p, song_on_top_name)
                    labl_img_list.insert(song_on_top-1, img_to_replace)
                    labl_img_list.insert(click_song_index_p, img_on_top_name)
                    song_list_path.insert(song_on_top-1, song_to_replace)
                    song_list_path.insert(click_song_index_p, song_on_top_name)
                on_top = False
            except:
                pass
        if delete_song_status:
            if click_song_index_p == song_list_path.index(current_song):
                mixer.music.unload()
            song_list.pop(click_song_index_p)
            song_list_path.pop(click_song_index_p)
            labl_img_list.pop(click_song_index_p)
            delete_song_status = False


def get_index_song():
    global click_song_index, clicking
    for position_ in positions:
        if position_[0] <= x_mouse <= position_[0] + 460 and position_[1] <= y_mouse <= position_[1] + 60:
            click_song_index = positions.index(position_)
            clicking = True


volume_on = True
clicking = False
click_song_index = 0
status_volume = True
positions = [[250, 50], [250, 130], [250, 210], [250, 290], [250, 370]]

# UPGRADES INPUTS
#
#
#

# IMPORTING THE SHIP IMAGES 256
ship_lvl1_img = pygame.image.load(os.path.join('ships', 'ship_lvl1_256.png'))
ship_lvl2_img = pygame.image.load(os.path.join('ships', 'ship_lvl2_256.png'))
ship_lvl3_img = pygame.image.load(os.path.join('ships', 'ship_lvl3_256.png'))
ship_lvl4_img = pygame.image.load(os.path.join('ships', 'ship_lvl4_256.png'))
ship_lvl5_img = pygame.image.load(os.path.join('ships', 'ship_lvl5_256.png'))
ship_lvl6_img = pygame.image.load(os.path.join('ships', 'ship_lvl6_256.png'))
ship_lvl7_img = pygame.image.load(os.path.join('ships', 'ship_lvl7_256.png'))
ship_lvl8_img = pygame.image.load(os.path.join('ships', 'ship_lvl8_256.png'))
ship_lvl9_img = pygame.image.load(os.path.join('ships', 'ship_lvl9_256.png'))
ship_lvl10_img = pygame.image.load(os.path.join('ships', 'ship_lvl10_256.png'))
ship_lvl11_img = pygame.image.load(os.path.join('ships', 'ship_lvl11_256.png'))
ship_lvl12_img = pygame.image.load(os.path.join('ships', 'ship_lvl12_256.png'))
ship_lvl13_img = pygame.image.load(os.path.join('ships', 'ship_lvl13_256.png'))
ship_lvl14_img = pygame.image.load(os.path.join('ships', 'ship_lvl14_256.png'))
ship_lvl15_img = pygame.image.load(os.path.join('ships', 'ship_lvl15_256.png'))
ship_lvl16_img = pygame.image.load(os.path.join('ships', 'ship_lvl16_256.png'))
# IMPORTING SHIP IMAGES 64
ship_lvl1_img_64 = pygame.image.load(os.path.join('ships', 'ship_lvl1_64.png'))
ship_lvl2_img_64 = pygame.image.load(os.path.join('ships', 'ship_lvl2_64.png'))
ship_lvl3_img_64 = pygame.image.load(os.path.join('ships', 'ship_lvl3_64.png'))
ship_lvl4_img_64 = pygame.image.load(os.path.join('ships', 'ship_lvl4_64.png'))
ship_lvl5_img_64 = pygame.image.load(os.path.join('ships', 'ship_lvl5_64.png'))
ship_lvl6_img_64 = pygame.image.load(os.path.join('ships', 'ship_lvl6_64.png'))
ship_lvl7_img_64 = pygame.image.load(os.path.join('ships', 'ship_lvl7_64.png'))
ship_lvl8_img_64 = pygame.image.load(os.path.join('ships', 'ship_lvl8_64.png'))
ship_lvl9_img_64 = pygame.image.load(os.path.join('ships', 'ship_lvl9_64.png'))
ship_lvl10_img_64 = pygame.image.load(os.path.join('ships', 'ship_lvl10_64.png'))
ship_lvl11_img_64 = pygame.image.load(os.path.join('ships', 'ship_lvl11_64.png'))
ship_lvl12_img_64 = pygame.image.load(os.path.join('ships', 'ship_lvl12_64.png'))
ship_lvl13_img_64 = pygame.image.load(os.path.join('ships', 'ship_lvl13_64.png'))
ship_lvl14_img_64 = pygame.image.load(os.path.join('ships', 'ship_lvl14_64.png'))
ship_lvl15_img_64 = pygame.image.load(os.path.join('ships', 'ship_lvl15_64.png'))
ship_lvl16_img_64 = pygame.image.load(os.path.join('ships', 'ship_lvl16_64.png'))
ship_img_list_64 = [ship_lvl1_img_64, ship_lvl2_img_64, ship_lvl3_img_64, ship_lvl4_img_64, ship_lvl5_img_64,
                    ship_lvl6_img_64, ship_lvl7_img_64, ship_lvl8_img_64, ship_lvl9_img_64, ship_lvl10_img_64,
                    ship_lvl11_img_64, ship_lvl12_img_64,ship_lvl13_img_64, ship_lvl14_img_64, ship_lvl15_img_64,
                    ship_lvl16_img_64]
# CREATING A LIST CONTAINING ALL THE SHIP IMAGES
ship_img_list = [ship_lvl1_img, ship_lvl2_img, ship_lvl3_img, ship_lvl4_img, ship_lvl5_img, ship_lvl6_img,
                 ship_lvl7_img, ship_lvl8_img, ship_lvl9_img, ship_lvl10_img, ship_lvl11_img, ship_lvl12_img,
                 ship_lvl13_img, ship_lvl14_img, ship_lvl15_img, ship_lvl16_img]
# GIVING POSITIONS
a = 0
img_positions = [(352+a, 142), (832+a, 142), (1312+a, 142), (1792+a, 142), (2271+a, 142), (2752+a, 142), (3232+a, 142),
             (3712+a, 142), (4192+a, 142), (4672+a, 142), (5152+a, 142), (5632+a, 142), (6112+a, 142), (6592+a, 142),
             (7072+a, 142), (7552+a, 142)]
# NAMES RENDERING AND PUTTING IN A LIST TO BLIT AFTER
names_font = pygame.font.Font('Edge Of Madness.otf', 30)
ship_names_list = ['ALI BABA', 'AL FANOUS', 'LES ORANGER', 'SAROUKH', 'UFO', 'OMPA LOMPPA', 'LE RENARD', 'WAR-SHIP',
                   'B-52', 'BIG-1', 'B-2', 'SA7N-TA2IR', 'CAPSULE', 'CLOUD', "L'IMBECILE", "UR MOMMA'S SHIP"]
ship_name_graph_list = []

for text in ship_names_list:
    text_graphics = names_font.render(str(text), True, (255, 153, 153))
    ship_name_graph_list.append(text_graphics)
names_positions = [(352+a+126-ship_name_graph_list[0].get_width()/2, 62),
                   (832+a+126-ship_name_graph_list[1].get_width()/2, 62),
                   (1312+a+126-ship_name_graph_list[2].get_width()/2, 62),
                   (1792+a+126-ship_name_graph_list[3].get_width()/2, 62),
                   (2271+a+126-ship_name_graph_list[4].get_width()/2, 62),
                   (2752+a+126-ship_name_graph_list[5].get_width()/2, 62),
                   (3232+a+126-ship_name_graph_list[6].get_width()/2, 62),
                   (3712+a+126-ship_name_graph_list[7].get_width()/2, 62),
                   (4192+a+126-ship_name_graph_list[8].get_width()/2, 62),
                   (4672+a+126-ship_name_graph_list[9].get_width()/2, 62),
                   (5152+a+126-ship_name_graph_list[10].get_width()/2, 62),
                   (5632+a+126-ship_name_graph_list[11].get_width()/2, 62),
                   (6112+a+126-ship_name_graph_list[12].get_width()/2, 62),
                   (6592+a+126-ship_name_graph_list[13].get_width()/2, 62),
                   (7072+a+126-ship_name_graph_list[14].get_width()/2, 62),
                   (7552+a+126-ship_name_graph_list[15].get_width()/2, 62)]


def displaying_names():
    global ship_name_graph_list, names_positions
    for name in ship_name_graph_list:
        screen.blit(name, names_positions[ship_name_graph_list.index(name)])


click_nx = False
b = 0
ship_num = 0


def next_button():
    global a, img_positions, names_positions, click_nx, b, ship_num, index_changed
    if ship_num == 15:
        pass
    else:
        if click_nx:
            if b > 0:
                a -= 20
                b -= 1
            else:
                b = 24
                click_nx = False
                ship_num += 1
                index_changed = True
        img_positions = [(352 + a, 102), (832 + a, 102), (1312 + a, 102), (1792 + a, 102), (2271 + a, 102), (2752 + a, 102),
                     (3232 + a, 102),
                     (3712 + a, 102), (4192 + a, 102), (4672 + a, 102), (5152 + a, 102), (5632 + a, 102), (6112 + a, 102),
                     (6592 + a, 102), (7072 + a, 102),
                     (7552 + a, 102)]
        names_positions = [(352 + a + 126 - ship_name_graph_list[0].get_width() / 2, 22),
                           (832 + a + 126 - ship_name_graph_list[1].get_width() / 2, 22),
                           (1312 + a + 126 - ship_name_graph_list[2].get_width() / 2, 22),
                           (1792 + a + 126 - ship_name_graph_list[3].get_width() / 2, 22),
                           (2271 + a + 126 - ship_name_graph_list[4].get_width() / 2, 22),
                           (2752 + a + 126 - ship_name_graph_list[5].get_width() / 2, 22),
                           (3232 + a + 126 - ship_name_graph_list[6].get_width() / 2, 22),
                           (3712 + a + 126 - ship_name_graph_list[7].get_width() / 2, 22),
                           (4192 + a + 126 - ship_name_graph_list[8].get_width() / 2, 22),
                           (4672 + a + 126 - ship_name_graph_list[9].get_width() / 2, 22),
                           (5152 + a + 126 - ship_name_graph_list[10].get_width() / 2, 22),
                           (5632 + a + 126 - ship_name_graph_list[11].get_width() / 2, 22),
                           (6112 + a + 126 - ship_name_graph_list[12].get_width() / 2, 22),
                           (6592 + a + 126 - ship_name_graph_list[13].get_width() / 2, 22),
                           (7072 + a + 126 - ship_name_graph_list[14].get_width() / 2, 22),
                           (7552 + a + 126 - ship_name_graph_list[15].get_width() / 2, 22)]


click_pr = False
index_changed = True


def previous_button():
    global a, img_positions, names_positions, click_pr, b, ship_num, index_changed
    if ship_num == 0:
        pass
    else:
        if click_pr:
            if b < 24:
                a += 20
                b += 1
            else:
                b = 0
                click_pr = False
                ship_num -= 1
                index_changed = True
        img_positions = [(352 + a, 102), (832 + a, 102), (1312 + a, 102), (1792 + a, 102), (2271 + a, 102),
                         (2752 + a, 102), (3232 + a, 102), (3712 + a, 102), (4192 + a, 102), (4672 + a, 102),
                         (5152 + a, 102), (5632 + a, 102), (6112 + a, 102), (6592 + a, 102), (7072 + a, 102),
                         (7552 + a, 102)]
        names_positions = [(352 + a + 126 - ship_name_graph_list[0].get_width() / 2, 22),
                           (832 + a + 126 - ship_name_graph_list[1].get_width() / 2, 22),
                           (1312 + a + 126 - ship_name_graph_list[2].get_width() / 2, 22),
                           (1792 + a + 126 - ship_name_graph_list[3].get_width() / 2, 22),
                           (2271 + a + 126 - ship_name_graph_list[4].get_width() / 2, 22),
                           (2752 + a + 126 - ship_name_graph_list[5].get_width() / 2, 22),
                           (3232 + a + 126 - ship_name_graph_list[6].get_width() / 2, 22),
                           (3712 + a + 126 - ship_name_graph_list[7].get_width() / 2, 22),
                           (4192 + a + 126 - ship_name_graph_list[8].get_width() / 2, 22),
                           (4672 + a + 126 - ship_name_graph_list[9].get_width() / 2, 22),
                           (5152 + a + 126 - ship_name_graph_list[10].get_width() / 2, 22),
                           (5632 + a + 126 - ship_name_graph_list[11].get_width() / 2, 22),
                           (6112 + a + 126 - ship_name_graph_list[12].get_width() / 2, 22),
                           (6592 + a + 126 - ship_name_graph_list[13].get_width() / 2, 22),
                           (7072 + a + 126 - ship_name_graph_list[14].get_width() / 2, 22),
                           (7552 + a + 126 - ship_name_graph_list[15].get_width() / 2, 22)]


previous_img = pygame.image.load(os.path.join('music_icons', 'previous.png'))
next_img = pygame.image.load(os.path.join('music_icons', 'next.png'))


def display_next_pre_buttons():
    screen.blit(button, (screen.get_width()/2 - button.get_width()/2 - 350,
                         screen.get_height()/2 - button.get_height()/2 - 100))
    screen.blit(button, (screen.get_width() / 2 - button.get_width() / 2 + 350,
                         screen.get_height() / 2 - button.get_height() / 2 - 100))
    screen.blit(previous_img, (screen.get_width()/2 - button.get_width()/2 - 350 + 8,
                            screen.get_height()/2 - button.get_height()/2 - 100 + 8))
    screen.blit(next_img, (screen.get_width() / 2 - button.get_width() / 2 + 350 + 8,
                            screen.get_height() / 2 - button.get_height() / 2 -100 + 8))

def display_ship_imgs():
    for img in ship_img_list:
        screen.blit(img, img_positions[ship_img_list.index(img)])


icon1 = pygame.image.load(os.path.join('images', 'volume_button.png'))
icon2 = pygame.image.load(os.path.join('images', 'volume_button.png'))
icon3 = pygame.image.load(os.path.join('images', 'volume_button.png'))
icon4 = pygame.image.load(os.path.join('images', 'volume_button.png'))
rect_width_speed = 200
rect_width_health = 200
rect_width_body_damage = 200
rect_width_bullet = 200
rect_posx = 475
rect_posy = 380
widget_posx1 = 659
widget_posx2 = 659
widget_posx3 = 659
widget_posx4 = 659
widget_posy = 376
rect_surface_speed = pygame.Surface([rect_width_speed, 20])
rect_surface_health = pygame.Surface([rect_width_health, 20])
rect_surface_body_damage = pygame.Surface([rect_width_body_damage, 20])
rect_surface_bullet = pygame.Surface([rect_width_bullet, 20])
rect_surface1 = pygame.Surface([200, 20])
click1 = False
click2 = False
click3 = False
click4 = False
ship_speed_list = data['ship_speed_list']
ship_body_damage_list = data['ship_body_damage_list']
ship_health_list = data['ship_health_list']
ship_bullet_min_damage_list = data['ship_bullet_min_damage_list']
#  UPGRADE LIMITS FOR EACH SHIP

health_limit = [2500, 3000, 3500, 4000, 5000, 5500, 6000, 8000, 11000, 13000, 15000, 17000, 20000, 23000, 60000, 60000]
speed_limit = [1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.4, 2.6, 2.8, 3, 3, 3, 3, 3, 3, 3]
body_damage_limit = [200, 300, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1000]
bullet_damage_limit = [100, 150, 200, 250, 300, 350, 450, 500, 550, 700, 800, 950, 1150, 2000, 3000, 3000]
upgrade_names_font = pygame.font.Font('Edge Of Madness.otf', 20)
values_font = pygame.font.Font('Edge Of Madness.otf', 10)
# IMPORTING BG AND COVER IMAGES
cover_bg = pygame.image.load(os.path.join('images', 'cover_n_bg.png'))
cover = pygame.image.load(os.path.join('images', 'upgrades-cover.png'))
upgrade_button = pygame.image.load(os.path.join('images', 'upgrade_button.png'))


def display_upgrade_names():
    text_posx = 285
    text_posy = 380
    health_text = upgrade_names_font.render('HEALTH:', True, (255, 255, 255))
    speed_text = upgrade_names_font.render('SPEED:', True, (255, 255, 255))
    body_damage_text = upgrade_names_font.render('BODY DAMAGE:', True, (255, 255, 255))
    bullet_text = upgrade_names_font.render('BULLET DAMAGE:', True, (255, 255, 255))
    screen.blit(health_text, (text_posx, text_posy))
    screen.blit(speed_text, (text_posx, text_posy + 40))
    screen.blit(body_damage_text, (text_posx, text_posy + 80))
    screen.blit(bullet_text, (text_posx, text_posy + 120))


def display_mouse(mouse_x, mouse_y):
    mousex_cor = values_font.render('x = ' + str(mouse_x), True, (255, 255, 255))
    mousey_cor = values_font.render('y = ' + str(mouse_y), True, (255, 255, 255))
    screen.blit(mousex_cor, (0, 0))
    screen.blit(mousey_cor, (60, 0))


def display_bg_cover():
    cover_bg.set_alpha(190)
    screen.blit(cover, (230, 0))
    screen.blit(cover_bg, (0, 0))


payed = False

# DISPLAYING COIN COUNT
# COINS COUNT
coins = data['coins']
# IMPORTING COIN IMAGES
coin_1 = pygame.image.load(os.path.join('coins', 'gold_coin_round_star_1.png'))
coin_2 = pygame.image.load(os.path.join('coins', 'gold_coin_round_star_2.png'))
coin_3 = pygame.image.load(os.path.join('coins', 'gold_coin_round_star_3.png'))
coin_4 = pygame.image.load(os.path.join('coins', 'gold_coin_round_star_4.png'))
coin_5 = pygame.image.load(os.path.join('coins', 'gold_coin_round_star_5.png'))
coin_6 = pygame.image.load(os.path.join('coins', 'gold_coin_round_star_6.png'))
coin_img_list1 = [coin_1, coin_2, coin_3, coin_4, coin_5, coin_6]
current_coin_index = 0


def display_coins_count():
    global current_coin_index
    coins_text_ = upgrade_names_font.render(str(coins), True, (255, 153, 153))
    screen.blit(coins_text_, (790, 8))
    screen.blit(coin_img_list1[current_coin_index], (800 + coins_text_.get_width(), 0))
    if current_time - static_coin_time <= 66:
        pass
    else:
        if current_coin_index < 5:
            current_coin_index += 1
        else:
            current_coin_index = 0


def pay_ur_bills(index_p):
    global ship_health_list, ship_speed_list, ship_body_damage_list, ship_bullet_min_damage_list, speed_limit,\
        health_limit, bullet_damage_limit, body_damage_limit, rect_width_body_damage, rect_width_speed,\
        rect_width_health, rect_width_bullet, payed, coins, coin_1, static_skin_time, sorry_text
    coin_1_mini = pygame.transform.scale(coin_1, (32, 32))
    price_health = (rect_width_health - ship_health_list[index_p] / ship_health_list[-1] * 200) * 100 * (index_p + 1)
    price_body_damage = \
        (rect_width_body_damage - ship_body_damage_list[index_p] / ship_body_damage_list[-1] * 200) * 100 * (index_p + 1)

    price_speed = (rect_width_speed - ship_speed_list[index_p] / ship_speed_list[-1] * 200) * 100 * (index_p + 1)
    price_bullet = \
        (rect_width_bullet - ship_bullet_min_damage_list[index_p] / ship_bullet_min_damage_list[-1] * 200) * 100 * (index_p + 1)
    text_font = pygame.font.Font('Edge Of Madness.otf', 20)
    price = int(price_health + price_speed + price_bullet + price_body_damage)
    screen.blit(upgrade_button, (770, 310))
    if 770 <= x_mouse <= 920 and 310 <= y_mouse <= 370:
        color = (255, 255, 255)
    else:
        color = (0, 250, 250)
    upgrade_text = text_font.render('UPGRADE', True, color)
    screen.blit(upgrade_text, (795, 325))
    i_get_text = text_font.render('I GET: ' + str(price), True, (255, 255, 255))
    u_get_text = text_font.render('U GET: nth', True, (255, 255, 255))
    screen.blit(i_get_text, (750, 400))
    screen.blit(coin_1_mini, (760 + i_get_text.get_width(), 395))
    screen.blit(u_get_text, (750, 440))
    if payed:
        if coins >= price:
            coins -= price
            ship_health_list[index_p] = rect_width_health / 200 * ship_health_list[-1]
            ship_speed_list[index_p] = rect_width_speed / 200 * ship_speed_list[-1]
            ship_body_damage_list[index_p] = rect_width_body_damage / 200 * ship_body_damage_list[-1]
            ship_bullet_min_damage_list[index_p] = rect_width_bullet / 200 * ship_bullet_min_damage_list[-1]
            payed = False
        else:
            if current_time - static_skin_time < 3000:
                sorry_text = sorry_font.render('-_- GO GET SOME COINS AND COME BACK -_-', True, (255, 255, 255))
                screen.blit(label, ((screen.get_width() / 2 - label.get_width() / 2) + 20, 245))
                screen.blit(sorry_text, (screen.get_width() / 2 - sorry_text.get_width() / 2, 260))
            else:
                payed = False


def displaying_upgrade_values():
    global rect_posx, rect_posy
    x = rect_posx + 100
    y = rect_posy +2
    health_value = rect_width_health/200*ship_health_list[-1]
    speed_value = rect_width_speed/200*ship_speed_list[-1]
    body_damage_value = rect_width_body_damage/200*ship_body_damage_list[-1]
    bullet_damage_value = rect_width_bullet/200*ship_bullet_min_damage_list[-1]
    health_value_text = values_font.render(str(int(health_value)), True, (0, 0, 0))
    speed_value_text = values_font.render(str(round(speed_value, 2)), True, (0, 0, 0))
    body_damage_value_text = values_font.render(str(int(body_damage_value)), True, (0, 0, 0))
    bullet_damage_value_text = values_font.render(str(int(bullet_damage_value)), True, (0, 0, 0))
    health_value_text.set_alpha(127)
    speed_value_text.set_alpha(127)
    body_damage_value_text.set_alpha(127)
    bullet_damage_value_text.set_alpha(127)
    screen.blit(health_value_text, (x - health_value_text.get_width() / 2, y))
    screen.blit(speed_value_text, (x - speed_value_text.get_width() / 2, y + 40))
    screen.blit(body_damage_value_text, (x - body_damage_value_text.get_width() / 2, y + 80))
    screen.blit(bullet_damage_value_text, (x - bullet_damage_value_text.get_width() / 2, y + 120))


def display_upgrade_bars(mousex, index_p):
    global widget_posx1, widget_posx2, widget_posx3, widget_posx4, widget_posy, rect_width_health,\
        rect_width_body_damage, rect_width_speed, rect_width_bullet, rect_posx, click1, click2, click3,\
        click4, icon1, icon2, icon3, icon4, ship_bullet_min_damage_list, ship_health_list, ship_speed_list,\
        ship_body_damage_list, speed_limit, body_damage_limit, health_limit, bullet_damage_limit, index_changed
    # INITIALISATION OF THE WIDGET POSITION ACCORDING TO THE SHIP INDEX
    if index_changed:
        widget_posx1 = ship_health_list[index_p] / ship_health_list[-1] * 200 + 459
        rect_width_health = widget_posx1 + 16 - rect_posx
        widget_posx2 = ship_speed_list[index_p] / ship_speed_list[-1] * 200 + 459
        rect_width_speed = widget_posx2 + 16 - rect_posx
        widget_posx3 = ship_body_damage_list[index_p] / ship_body_damage_list[-1] * 200 + 459
        rect_width_body_damage = widget_posx3 + 16 - rect_posx
        widget_posx4 = ship_bullet_min_damage_list[index_p] / ship_bullet_min_damage_list[-1] * 200 + 459
        rect_width_bullet = widget_posx4 + 16 - rect_posx
        index_changed = False
    if click1:
        if rect_posx + ship_health_list[index_p]/ship_health_list[-1]*200 < mousex <= rect_posx + health_limit[index_p]/ship_health_list[-1]*200:
            widget_posx1 = mousex-16
            rect_width_health = mousex - rect_posx
        if mousex >= rect_posx + health_limit[index_p]/ship_health_list[-1]*200:
            rect_width_health = health_limit[index_p]/ship_health_list[-1]*200
    if click2:
        if rect_posx + ship_speed_list[index_p]/ship_speed_list[-1]*200 < mousex <= rect_posx + speed_limit[index_p]/ship_speed_list[-1]*200:
            widget_posx2 = mousex - 16
            rect_width_speed = mousex - rect_posx
        if mousex >= rect_posx + speed_limit[index_p]/ship_speed_list[-1]*200:
            rect_width_speed = speed_limit[index_p]/ship_speed_list[-1]*200
    if click3:
        if rect_posx + ship_body_damage_list[index_p]/ship_body_damage_list[-1]*200 < mousex <= rect_posx + body_damage_limit[index_p]/ship_body_damage_list[-1]*200:
            widget_posx3 = mousex - 16
            rect_width_body_damage = mousex - rect_posx
        if mousex >= rect_posx + body_damage_limit[index_p]/ship_body_damage_list[-1]*200:
            rect_width_body_damage = body_damage_limit[index_p]/ship_body_damage_list[-1]*200
    if click4:
        if rect_posx + ship_bullet_min_damage_list[index_p]/ship_bullet_min_damage_list[-1]*200 < mousex <= rect_posx + bullet_damage_limit[index_p]/ship_bullet_min_damage_list[-1]*200:
            widget_posx4 = mousex - 16
            rect_width_bullet = mousex - rect_posx
        if mousex >= rect_posx + bullet_damage_limit[index_p]/ship_bullet_min_damage_list[-1]*200:
            rect_width_bullet = bullet_damage_limit[index_p]/ship_bullet_min_damage_list[-1]*200
    screen.blit(rect_surface1, (rect_posx, rect_posy))
    screen.blit(rect_surface1, (rect_posx, rect_posy + 40))
    screen.blit(rect_surface1, (rect_posx, rect_posy + 80))
    screen.blit(rect_surface1, (rect_posx, rect_posy + 120))
    screen.blit(rect_surface_health, (rect_posx, rect_posy))
    screen.blit(rect_surface_speed, (rect_posx, rect_posy + 40))
    screen.blit(rect_surface_body_damage, (rect_posx, rect_posy + 80))
    screen.blit(rect_surface_bullet, (rect_posx, rect_posy + 120))
    screen.blit(icon1, (widget_posx1, widget_posy))
    screen.blit(icon2, (widget_posx2, widget_posy + 40))
    screen.blit(icon3, (widget_posx3, widget_posy + 80))
    screen.blit(icon4, (widget_posx4, widget_posy + 120))


# SKINS INPUTS NIGGA
#
#
#
skins_font = pygame.font.Font('Edge Of Madness.otf', 30)
sorry_font = pygame.font.Font('Edge Of Madness.otf', 15)
static_skin_time = 0
# setting a screen display
screen = pygame.display.set_mode((960, 540))

# setting the background image and the background low opacity
bg_img = pygame.image.load(os.path.join('images', 'space-background.png'))

# IMPORTING COIN IMAGES
coin_1 = pygame.image.load(os.path.join('coins', 'gold_coin_round_star_1.png'))
coin_2 = pygame.image.load(os.path.join('coins', 'gold_coin_round_star_2.png'))
coin_3 = pygame.image.load(os.path.join('coins', 'gold_coin_round_star_3.png'))
coin_4 = pygame.image.load(os.path.join('coins', 'gold_coin_round_star_4.png'))
coin_5 = pygame.image.load(os.path.join('coins', 'gold_coin_round_star_5.png'))
coin_6 = pygame.image.load(os.path.join('coins', 'gold_coin_round_star_6.png'))
coin_img_list = [coin_1, coin_2, coin_3, coin_4, coin_5, coin_6]


def background_display():
    screen.blit(bg_img, (0, 0))


# IMPORTING BUTTON TO BUY SELECT AND SELECTED
buy_button = pygame.image.load(os.path.join('images', 'buy_button.png'))
select_button = pygame.image.load(os.path.join('images', 'selecte_button.png'))
selected_button = pygame.image.load(os.path.join('images', 'selected_button.png'))
label = pygame.image.load(os.path.join('images', 'blank-button5.png'))
buy_status_list = data['buy_status_list']
select_ship_list = data['select_ship_list']
ship_prices = [0, 1200, 6900, 15000, 30000, 42000, 69420, 99999, 140000, 200000, 330000, 400000, 600000, 1000000,
               2500000, 10000000]

# INITIALISING THE PLAYER
player_img1 = ship_img_list_64[select_ship_list.index(True)]
playerhealth1 = ship_health_list[select_ship_list.index(True)]
playerbodydamage1 = ship_body_damage_list[select_ship_list.index(True)]
playerbulletdamage1 = ship_bullet_min_damage_list[select_ship_list.index(True)]
playerspeed1 = ship_speed_list[select_ship_list.index(True)]
player = Player(player_img1, (playerx, playery), playerhealth1, playerbodydamage1, playerbulletdamage1, playerspeed1,
                    player_shoot_load, player_shoot_wait)


def buttons_display(index_p):
    if buy_status_list[index_p]:
        if select_ship_list[index_p]:
            screen.blit(selected_button, (180, 440))
            selected_text = skins_font.render('SELECTED', True, (50, 50, 200))
            screen.blit(selected_text,
                        (180 + selected_button.get_width()/2-selected_text.get_width()/2, 450))
        else:
            screen.blit(select_button, (180, 440))
            select_text = skins_font.render('SELECT', True, (200, 50, 50))
            screen.blit(select_text,
                        (180 + selected_button.get_width() / 2 - select_text.get_width() / 2, 450))
    else:
        screen.blit(buy_button, (180, 410))
        buy_text = skins_font.render('BUY', True, (0, 250, 250))
        screen.blit(buy_text,
                    (180 + selected_button.get_width() / 2 - buy_text.get_width() / 2, 420))


sorry_text = False


def click_button(index_p):
    global static_skin_time, coins, sorry_text, x_mouse, y_mouse
    if 180 <= x_mouse <= 440 and 410 <= y_mouse <= 470:
        if buy_status_list[index_p]:
            pass
        else:
            if coins > ship_prices[index_p]:
                buy_status_list[index_p] = True
                coins -= ship_prices[index_p]
            else:
                a = 0
                if a == 0:
                    static_skin_time = current_time
                    a += 1
                sorry_text = True
    if 180 <= x_mouse <= 440 and 440 <= y_mouse <= 500:
        if buy_status_list[index_p]:
            if select_ship_list[index_p]:
                pass
            else:
                a = select_ship_list.index(True)
                select_ship_list[a] = False
                select_ship_list[index_p] = True
        else:
            pass


def display_sorry_text():
    global current_time, static_skin_time, sorry_text
    if sorry_text:
        if current_time - static_skin_time < 3000:
            sorry_text = sorry_font.render('-_- GO GET SOME COINS AND COME BACK -_-', True, (255, 255, 255))
            screen.blit(label, ((screen.get_width() / 2 - label.get_width() / 2)+20, 245))
            screen.blit(sorry_text, (screen.get_width() / 2 - sorry_text.get_width() / 2, 260))
        else:
            sorry_text = False


# UPGRADES PART
# UPLOADING IMAGES OF THE PARTS
upgrades_container = pygame.image.load(os.path.join('images', 'upgrades_container.png'))
upgrades_container_bg = pygame.image.load(os.path.join('images', 'upgraides_container_bg_opac.png'))


def display_upgrades_container():
    screen.blit(upgrades_container, (0, 120))
    screen.blit(upgrades_container_bg, (0, 130))


upgrades_font = pygame.font.Font('Edge Of Madness.otf', 12)
abilities_font = pygame.font.Font('Edge Of Madness.otf', 10)
# IMPORTING RECTANGLES TO SET THE UPGRADES VISUALS BARS
rect_width_health1 = 0
rect_width_body_damage1 = 0
rect_width_speed1 = 0
rect_width_bullet1 = 0
rect_surface_health1 = pygame.Surface([rect_width_health1, 20])
rect_surface_body_damage1 = pygame.Surface([rect_width_body_damage1, 20])
rect_surface_speed1 = pygame.Surface([rect_width_speed1, 20])
rect_surface_bullet1 = pygame.Surface([rect_width_bullet1, 20])
rect_surface11 = pygame.Surface([100, 20])


def display_upgrades(index_p):
    global rect_width_bullet1, rect_width_health1, rect_width_body_damage1, rect_width_speed1, ship_body_damage_list,\
        ship_bullet_min_damage_list, ship_health_list, ship_speed_list, rect_surface_health1, rect_surface_bullet1,\
        rect_surface_speed1, rect_surface_body_damage1
    # UPDATING THE RECTANGLES WIDTH
    rect_surface_health1 = pygame.Surface([rect_width_health1, 20])
    rect_surface_body_damage1 = pygame.Surface([rect_width_body_damage1, 20])
    rect_surface_speed1 = pygame.Surface([rect_width_speed1, 20])
    rect_surface_bullet1 = pygame.Surface([rect_width_bullet1, 20])
    # FILLING THE RECTANGLES WITH COLOR
    rect_surface_health1.fill((73, 153, 0))
    rect_surface_body_damage1.fill((73, 153, 0))
    rect_surface_speed1.fill((73, 153, 0))
    rect_surface_bullet1.fill((73, 153, 0))
    rect_surface11.fill((131, 176, 243))
    # ADJUSTING THE WIDTH OF THE RECTANGLE
    if rect_width_bullet1 < int(ship_bullet_min_damage_list[index_p]/ship_bullet_min_damage_list[-1]*100):
        rect_width_bullet1 += 1
    elif rect_width_bullet1 > int(ship_bullet_min_damage_list[index_p]/ship_bullet_min_damage_list[-1]*100):
        rect_width_bullet1 -= 1
    if rect_width_speed1 < int(ship_speed_list[index_p]/ship_speed_list[-1]*100):
        rect_width_speed1 += 1
    elif rect_width_speed1 > int(ship_speed_list[index_p]/ship_speed_list[-1]*100):
        rect_width_speed1 -= 1
    if rect_width_health1 < int(ship_health_list[index_p]/ship_health_list[-1]*100):
        rect_width_health1 += 1
    elif rect_width_health1 > int(ship_health_list[index_p]/ship_health_list[-1]*100):
        rect_width_health1 -= 1
    if rect_width_body_damage1 < int(ship_body_damage_list[index_p]/ship_body_damage_list[-1]*100):
        rect_width_body_damage1 += 1
    elif rect_width_body_damage1 > int(ship_body_damage_list[index_p]/ship_body_damage_list[-1]*100):
        rect_width_body_damage1 -= 1
    # LABELS TO KNOW WHICH ABILITY WE'RE TALKING ABOUT
    health_text = upgrades_font.render('HEALTH:', True, (255, 255, 255))
    speed_text = upgrades_font.render('SPEED:', True, (255, 255, 255))
    body_damage_text = upgrades_font.render('BODY-DAMAGE:', True, (255, 255, 255))
    ship_bullet_min_damage_text = upgrades_font.render('BULLET-DAMAGE:', True, (255, 255, 255))
    # THE NUMERIQUE VALUE OF THE ABILITY FOR EACH SHIP
    speed_a_text = abilities_font.render(str(rect_width_speed1 * ship_speed_list[-1] / 100), True, (0, 0, 0))
    speed_a_text.set_alpha(127)
    body_damage_a_text = abilities_font.render(str(rect_width_body_damage1 * ship_body_damage_list[-1] / 100), True,
                                               (0, 0, 0))
    body_damage_a_text.set_alpha(127)
    bullet_a_text = abilities_font.render(str(rect_width_bullet1 * ship_bullet_min_damage_list[-1] / 100), True,
                                          (0, 0, 0))
    bullet_a_text.set_alpha(127)
    health_a_text = abilities_font.render(str(rect_width_health1 * ship_health_list[-1] / 100), True, (0, 0, 0))
    health_a_text.set_alpha(127)
    # DISPLAYING THE TEXTS OR NAMES OF THE ABILITIES AND THE RECTANGLES WITH ORDER
    screen.blit(health_text, (0, 140))
    screen.blit(rect_surface11, (0, 170))
    screen.blit(rect_surface_health1, (0, 170))
    screen.blit(speed_text, (0, 200))
    screen.blit(rect_surface11, (0, 230))
    screen.blit(rect_surface_speed1, (0, 230))
    screen.blit(body_damage_text, (0, 270))
    screen.blit(rect_surface11, (0, 300))
    screen.blit(rect_surface_body_damage1, (0, 300))
    screen.blit(ship_bullet_min_damage_text, (0, 340))
    screen.blit(rect_surface11, (0, 370))
    screen.blit(rect_surface_bullet1, (0, 370))
    # DISPLAYING THE NUMERIQUE VALUE OF EACH ABILITY
    screen.blit(speed_a_text, (rect_surface11.get_width() / 2 - speed_a_text.get_width() / 2, 233))
    screen.blit(health_a_text, (rect_surface11.get_width() / 2 - health_a_text.get_width() / 2, 173))
    screen.blit(body_damage_a_text, (rect_surface11.get_width() / 2 - body_damage_a_text.get_width() / 2, 303))
    screen.blit(bullet_a_text, (rect_surface11.get_width() / 2 - bullet_a_text.get_width() / 2, 373))


def displaying_the_price(index_p):
    global current_coin_index, static_coin_time, current_time
    if buy_status_list[index_p]:
        pass
    else:
        coins_text = skins_font.render(str(ship_prices[index_p]), True, (0, 250, 250))
        screen.blit(coins_text, (180 + ship_img_list[index_p].get_width()/2 - coins_text.get_width()/2, 480))
        screen.blit(coin_img_list[current_coin_index],
                    (190 + ship_img_list[index_p].get_width()/2 + coins_text.get_width()/2, 480))
        if current_time - static_coin_time <= 1000:
            pass
        else:
            if current_coin_index < 5:
                current_coin_index += 1
            else:
                current_coin_index = 0
            static_coin_time = current_time

#  IMPORTING SHIP IMGS
# 32
ship_lvl1_icon = pygame.image.load(os.path.join('ships', 'ship_lvl1_32.png'))
ship_lvl2_icon = pygame.image.load(os.path.join('ships', 'ship_lvl2_32.png'))
ship_lvl3_icon = pygame.image.load(os.path.join('ships', 'ship_lvl3_32.png'))
ship_lvl4_icon = pygame.image.load(os.path.join('ships', 'ship_lvl4_32.png'))
ship_lvl5_icon = pygame.image.load(os.path.join('ships', 'ship_lvl5_32.png'))
ship_lvl6_icon = pygame.image.load(os.path.join('ships', 'ship_lvl6_32.png'))
ship_lvl7_icon = pygame.image.load(os.path.join('ships', 'ship_lvl7_32.png'))
ship_lvl8_icon = pygame.image.load(os.path.join('ships', 'ship_lvl8_32.png'))
ship_lvl9_icon = pygame.image.load(os.path.join('ships', 'ship_lvl9_32.png'))
ship_lvl10_icon = pygame.image.load(os.path.join('ships', 'ship_lvl10_32.png'))
ship_lvl11_icon = pygame.image.load(os.path.join('ships', 'ship_lvl11_32.png'))
ship_lvl12_icon = pygame.image.load(os.path.join('ships', 'ship_lvl12_32.png'))
ship_lvl13_icon = pygame.image.load(os.path.join('ships', 'ship_lvl13_32.png'))
ship_lvl14_icon = pygame.image.load(os.path.join('ships', 'ship_lvl14_32.png'))
ship_lvl15_icon = pygame.image.load(os.path.join('ships', 'ship_lvl15_32.png'))
ship_lvl16_icon = pygame.image.load(os.path.join('ships', 'ship_lvl16_32.png'))

# 256
ship_lvl1_img = pygame.image.load(os.path.join('ships', 'ship_lvl1_256.png'))
ship_lvl2_img = pygame.image.load(os.path.join('ships', 'ship_lvl2_256.png'))
ship_lvl3_img = pygame.image.load(os.path.join('ships', 'ship_lvl3_256.png'))
ship_lvl4_img = pygame.image.load(os.path.join('ships', 'ship_lvl4_256.png'))
ship_lvl5_img = pygame.image.load(os.path.join('ships', 'ship_lvl5_256.png'))
ship_lvl6_img = pygame.image.load(os.path.join('ships', 'ship_lvl6_256.png'))
ship_lvl7_img = pygame.image.load(os.path.join('ships', 'ship_lvl7_256.png'))
ship_lvl8_img = pygame.image.load(os.path.join('ships', 'ship_lvl8_256.png'))
ship_lvl9_img = pygame.image.load(os.path.join('ships', 'ship_lvl9_256.png'))
ship_lvl10_img = pygame.image.load(os.path.join('ships', 'ship_lvl10_256.png'))
ship_lvl11_img = pygame.image.load(os.path.join('ships', 'ship_lvl11_256.png'))
ship_lvl12_img = pygame.image.load(os.path.join('ships', 'ship_lvl12_256.png'))
ship_lvl13_img = pygame.image.load(os.path.join('ships', 'ship_lvl13_256.png'))
ship_lvl14_img = pygame.image.load(os.path.join('ships', 'ship_lvl14_256.png'))
ship_lvl15_img = pygame.image.load(os.path.join('ships', 'ship_lvl15_256.png'))
ship_lvl16_img = pygame.image.load(os.path.join('ships', 'ship_lvl16_256.png'))

# Creating a ship img list
ship_img_list = [ship_lvl1_img, ship_lvl2_img, ship_lvl3_img, ship_lvl4_img, ship_lvl5_img,
                 ship_lvl6_img, ship_lvl7_img, ship_lvl8_img, ship_lvl9_img, ship_lvl10_img, ship_lvl11_img,
                 ship_lvl12_img, ship_lvl13_img, ship_lvl14_img, ship_lvl15_img, ship_lvl16_img]


# DEFINING A FUNCTION THAT WILL SHOW THE SHIP ICONS ON THE SCREEN
def displaying_ship_icons():
    screen.blit(ship_lvl1_icon, (520, 100))
    screen.blit(ship_lvl2_icon, (610, 100))
    screen.blit(ship_lvl3_icon, (700, 100))
    screen.blit(ship_lvl4_icon, (790, 100))
    screen.blit(ship_lvl5_icon, (520, 200))
    screen.blit(ship_lvl6_icon, (610, 200))
    screen.blit(ship_lvl7_icon, (700, 200))
    screen.blit(ship_lvl8_icon, (790, 200))
    screen.blit(ship_lvl9_icon, (520, 300))
    screen.blit(ship_lvl10_icon, (610, 300))
    screen.blit(ship_lvl11_icon, (700, 300))
    screen.blit(ship_lvl12_icon, (790, 300))
    screen.blit(ship_lvl13_icon, (520, 400))
    screen.blit(ship_lvl14_icon, (610, 400))
    screen.blit(ship_lvl15_icon, (700, 400))
    screen.blit(ship_lvl16_icon, (790, 400))


def displaying_ship_img(index_p):
    global ship_img_list, ship_names_list
    ship_name = nouns_font.render(ship_names_list[index_p], True, (255, 153, 153))
    screen.blit(ship_name, (200 + ship_img_list[index_p].get_width()/2 - ship_name.get_width()/2, 351))
    screen.blit(ship_img_list[index_p], (200, 75))


# DEFINING A POSITION LIST THAT WE WILL USE TO TRACK COLLISIONS WITH THE SHIP ICONS
icon_positions = [(500, 80), (590, 80), (680, 80), (770, 80), (500, 180), (590, 180), (680, 200), (770, 180),
                  (500, 280), (590, 280), (680, 280), (770, 280), (500, 380), (590, 380), (680, 400), (770, 380)]

# SETTING SHIP NAMES LIST
nouns_font = pygame.font.Font('Edge Of Madness.otf', 30)
ship_names_list = ['ALI BABA', 'AL FANOUS', 'LES ORANGER', 'SAROUKH', 'UFO', 'OMPA LOMPPA', 'LE RENARD', 'WAR-SHIP',
                   'B-52', 'BIG-1', 'B-2', 'SA7N-TA2IR', 'CAPSULE', 'CLOUD', "L'IMBECILE", "UR MOMMA'S SHIP"]

# setting caption
pygame.display.set_caption('WEIRD SPACE')

#  Setting the icon for the window
space_icon = pygame.image.load(os.path.join('images', 'space-ship.png'))
pygame.display.set_icon(space_icon)

# SETTING THE SKINS TABLE
skins_table = pygame.image.load(os.path.join('images', 'skins_bar.png'))
skins_low_opac = pygame.image.load(os.path.join('images', 'bg_img.png'))
genres_fg = pygame.image.load(os.path.join('images', 'genres_fg.png'))
genres_bg = pygame.image.load(os.path.join('images', 'genres_bg_opac.png'))


def skins_bar_display():
    screen.blit(skins_low_opac, (480, 60))
    screen.blit(skins_table, (470, 50))
    screen.blit(genres_bg, (880, 60))
    screen.blit(genres_fg, (870, 50))


index = 0
music_rect_width = 0


game_status = 'Main'
running = True
while running:
    # SETTING THE MOUSE X AND Y
    x_mouse, y_mouse = pygame.mouse.get_pos()
    current_time = pygame.time.get_ticks()
    if game_status == 'Main':
        for event in pygame.event.get():
            if event.type == QUIT:
                with open('data_text.txt', 'w') as data_text:
                    json.dump(data, data_text)
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if (150 >= x_mouse >= 20) and (470 >= y_mouse >= 340):
                    rect_height = mixer.music.get_volume()*100
                    widget_posy1 = 44 + rect_height
                    game_status = 'Music'
                elif (930 >= x_mouse >= 800) and (320 >= y_mouse >= 190):
                    game_status = 'Upgrades'
                elif (930 >= x_mouse >= 800) and (470 >= y_mouse >= 340):
                    game_status = 'Skins'
                elif (150 >= x_mouse >= 20) and (320 >= y_mouse >= 190):
                    game_status = 'Parameter'
                elif (630 >= x_mouse >= 300) and (310 >= y_mouse >= 180):
                    game_status = 'Game'
                    game_type = 'Arcade'
                    volume_icon1_x = 364 + mixer.music.get_volume() * 200
                    volume_icon2_x = 364 + sounds_volume * 200
                    music_sounds_rect_width = mixer.music.get_volume() * 200
                    sounds_rect_width = sounds_volume * 200
                    game_over = False
                elif (630 >= x_mouse >= 300) and (460 >= y_mouse >= 330):
                    game_status = 'Game'
                    game_type = 'Levels'
                    volume_icon1_x = 364 + mixer.music.get_volume() * 200
                    volume_icon2_x = 364 + sounds_volume * 200
                    music_sounds_rect_width = mixer.music.get_volume() * 200
                    sounds_rect_width = sounds_volume * 200
                    game_over = False
            if event.type == END_SONG:
                next_song()

        # SIDE BUTTON 1
        if (150 >= x_mouse >= 20) and (320 >= y_mouse >= 190):
            parameter = 'parameter1.png'
        else:
            parameter = 'parameter.png'
            # SIDE BUTTON 2
        if (150 >= x_mouse >= 20) and (470 >= y_mouse >= 340):
            music1 = 'music 1.png'
        else:
            music1 = 'music.png'
            # SIDE BUTTON 3
        if (930 >= x_mouse >= 800) and (320 >= y_mouse >= 190):
            upgrade = 'upgrade1.png'
        else:
            upgrade = 'upgrade.png'
        # SIDE BUTTON 4
        if (930 >= x_mouse >= 800) and (470 >= y_mouse >= 340):
            shop = 'shop 1.png'
        else:
            shop = 'shop.png'

        # ARCADE AND LEVELS HIGHTLIGH

        if (630 >= x_mouse >= 300) and (310 >= y_mouse >= 180):
            color1 = 255
        else:
            color1 = 191
        if (630 >= x_mouse >= 300) and (460 >= y_mouse >= 330):
            color2 = 255
        else:
            color2 = 191

        background_display()
        button_onscreen()
        title_on_screen()
        pygame.display.update()
    elif game_status == 'Parameter':
        change_button_click = True
        background_display()
        display_back_arrow()
        display_parameter_elements()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                click_arrow()
                if screen.get_width() / 2 - parameters_container.get_width() / 2 + 130 <= x_mouse <= screen.get_width() / 2 - parameters_container.get_width() / 2 + 130 + 260 and screen.get_height() / 2 - parameters_container.get_height() / 2 + 20 <= y_mouse <= screen.get_height() / 2 - parameters_container.get_height() / 2 + 20 + 60:
                    while change_button_click:
                        for event_ in pygame.event.get():
                            if event_.type == KEYDOWN:
                                up_button = event_.key
                                change_button_click = False
                if screen.get_width() / 2 - parameters_container.get_width() / 2 + 130 <= x_mouse <= screen.get_width() / 2 - parameters_container.get_width() / 2 + 130 + 260 and screen.get_height() / 2 - parameters_container.get_height() / 2 + 95 <= y_mouse <= screen.get_height() / 2 - parameters_container.get_height() / 2 + 95 + 60:
                    while change_button_click:
                        for event_ in pygame.event.get():
                            if event_.type == KEYDOWN:
                                down_button = event_.key
                                change_button_click = False
                if screen.get_width() / 2 - parameters_container.get_width() / 2 + 130 <= x_mouse <= screen.get_width() / 2 - parameters_container.get_width() / 2 + 130 + 260 and screen.get_height() / 2 - parameters_container.get_height() / 2 + 175 <= y_mouse <= screen.get_height() / 2 - parameters_container.get_height() / 2 + 175 + 60:
                    while change_button_click:
                        for event_ in pygame.event.get():
                            if event_.type == KEYDOWN:
                                left_button = event_.key
                                change_button_click = False
                if screen.get_width() / 2 - parameters_container.get_width() / 2 + 130 <= x_mouse <= screen.get_width() / 2 - parameters_container.get_width() / 2 + 130 + 260 and screen.get_height() / 2 - parameters_container.get_height() / 2 + 255 <= y_mouse <= screen.get_height() / 2 - parameters_container.get_height() / 2 + 255 + 60:
                    while change_button_click:
                        for event_ in pygame.event.get():
                            if event_.type == KEYDOWN:
                                right_button = event_.key
                                change_button_click = False
                if screen.get_width() / 2 - parameters_container.get_width() / 2 + 130 <= x_mouse <= screen.get_width() / 2 - parameters_container.get_width() / 2 + 130 + 260 and screen.get_height() / 2 - parameters_container.get_height() / 2 + 330 <= y_mouse <= screen.get_height() / 2 - parameters_container.get_height() / 2 + 330 + 60:
                    while change_button_click:
                        for event_ in pygame.event.get():
                            if event_.type == KEYDOWN:
                                shoot_button = event_.key
                                change_button_click = False

            if event.type == QUIT:
                with open('data_text.txt', 'w') as data_text:
                    json.dump(data, data_text)
                pygame.quit()
                sys.exit()
            if event.type == END_SONG:
                next_song()
    elif game_status == 'Game':
        # SETTING TIME DELTA TIME
        now = time.time()
        dt = now - prev_time
        prev_time = now
        if game_over:
            background_display()
            if game_type == 'Arcade':
                game_over_text = game_over_font.render('GAME OVER', True, (255, 255, 255))
                screen.blit(game_over_text, (480 - game_over_text.get_width() / 2, 150))
                coins_text = restart_font.render('COINS COLLECTED: ', True, (0, 250, 250))
                coins_collected_text = restart_font.render(str(coins_collected), True, (255, 255, 102))
                score_text = restart_font.render('SCORE: ', True, (0, 250, 250))
                score_num_text = restart_font.render(str(score), True, (255, 255, 102))
                screen.blit(score_num_text, (380 + score_text.get_width() / 2 + 30, 240))
                screen.blit(coins_collected_text, (380 - score_text.get_width() / 2 + coins_text.get_width() + 30, 290))
                screen.blit(score_text, (380 - score_text.get_width() / 2, 240))
                screen.blit(coins_text, (380 - score_text.get_width() / 2, 290))
                restart_button_y = 360
                restart_button_x = 650

                restart_color = (0, 0, 0)
                if restart_button_x <= x_mouse <= restart_button_x + restart_button_img.get_width() and restart_button_y <=\
                        y_mouse <= restart_button_y + restart_button_img.get_height():
                    restart_color = (255, 255, 255)
                restart_text = restart_font.render('RESTART', True, restart_color)
                screen.blit(restart_button_img, (restart_button_x, restart_button_y))
                screen.blit(restart_text, (restart_button_x + 80, restart_button_y + 15))

                menu_button_y = 360
                menu_button_x = 50

                menu_color = (0, 0, 0)
                if menu_button_x <= x_mouse <= menu_button_x + menu_button_img.get_width() and menu_button_y <= y_mouse <= \
                        menu_button_y + menu_button_img.get_height():
                    menu_color = (255, 255, 255)
                menu_text = restart_font.render('MENU', True, menu_color)
                screen.blit(menu_button_img, (menu_button_x, menu_button_y))
                screen.blit(menu_text, (menu_button_x + 80, menu_button_y + 15))

                for event in pygame.event.get():
                    if event.type == QUIT:
                        with open('data_text.txt', 'w') as data_text:
                            json.dump(data, data_text)
                        pygame.quit()
                        sys.exit()
                    if event.type == MOUSEBUTTONDOWN:
                        if restart_button_x <= x_mouse \
                                <= restart_button_x + restart_button_img.get_width() and restart_button_y <= y_mouse <= \
                                restart_button_y + restart_button_img.get_height():
                            number_of_enemies = 0
                            player.health = player.max_health
                            barier_on = True
                            next_wave = True
                            all_in_pos = 0
                            score = 0
                            coins_collected = 0
                            game_over = False
                        if menu_button_x <= x_mouse \
                                <= menu_button_x + menu_button_img.get_width() and menu_button_y <= y_mouse <= \
                                menu_button_y + menu_button_img.get_height():
                            game_status = 'Main'
                            number_of_enemies = 0
                            player.health = player.max_health
                            barier_on = True
                            next_wave = True
                            all_in_pos = 0
                            score = 0
                            coins_collected = 0
                            game_over = False
                    if event.type == END_SONG:
                        next_song()
            elif game_type == 'Levels':
                if Level_status == 'Win':
                    won_lvl_text = game_over_font.render('LEVEL COMPLETED', True, (255, 255, 255))
                    screen.blit(won_lvl_text, (480 - won_lvl_text.get_width() / 2, 150))
                    coins_text = restart_font.render('COINS COLLECTED: ', True, (0, 250, 250))
                    coins_collected_text = restart_font.render(str(coins_collected), True, (255, 255, 102))
                    level_recompense_text = restart_font.render('LEVEL BONUS: ', True, (255, 255, 255))
                    level_recompense_num_text = restart_font.render(str(level_recompense_list[level_index]), True, (250, 250, 102))
                    score_text = restart_font.render('SCORE: ', True, (0, 250, 250))
                    score_num_text = restart_font.render(str(score), True, (255, 255, 102))
                    screen.blit(score_num_text, (380 + score_text.get_width() / 2 + 30, 240))
                    screen.blit(coins_collected_text, (380 - score_text.get_width() / 2 + coins_text.get_width() + 30, 290))
                    screen.blit(score_text, (380 - score_text.get_width() / 2, 240))
                    screen.blit(coins_text, (380 - score_text.get_width() / 2, 290))
                    screen.blit(level_recompense_text, (380 - score_text.get_width() / 2, 340))
                    screen.blit(level_recompense_num_text, (380 - score_text.get_width() / 2 + level_recompense_text.get_width() + 30, 340))
                    restart_button_y = 360
                    restart_button_x = 650

                    restart_color = (0, 0, 0)
                    if restart_button_x <= x_mouse <= restart_button_x + restart_button_img.get_width() and restart_button_y <= \
                            y_mouse <= restart_button_y + restart_button_img.get_height():
                        restart_color = (255, 255, 255)
                    restart_text = restart_font.render('NEXT LEVEL', True, restart_color)
                    screen.blit(restart_button_img, (restart_button_x, restart_button_y))
                    screen.blit(restart_text, (restart_button_x + restart_text.get_width() / 2, restart_button_y + 15))

                    menu_button_y = 360
                    menu_button_x = 50

                    menu_color = (0, 0, 0)
                    if menu_button_x <= x_mouse <= menu_button_x + menu_button_img.get_width() and menu_button_y <= y_mouse <= \
                            menu_button_y + menu_button_img.get_height():
                        menu_color = (255, 255, 255)
                    menu_text = restart_font.render('MENU', True, menu_color)
                    screen.blit(menu_button_img, (menu_button_x, menu_button_y))
                    screen.blit(menu_text, (menu_button_x + 80, menu_button_y + 15))

                    for event in pygame.event.get():
                        if event.type == QUIT:
                            with open('data_text.txt', 'w') as data_text:
                                json.dump(data, data_text)
                            pygame.quit()
                            sys.exit()
                        if event.type == MOUSEBUTTONDOWN:
                            if restart_button_x <= x_mouse \
                                    <= restart_button_x + restart_button_img.get_width() and restart_button_y <= y_mouse <= \
                                    restart_button_y + restart_button_img.get_height():
                                coins += level_recompense_list[level_index]
                                player.health = player.max_health
                                barier_on = True
                                next_wave = True
                                all_in_pos = 0
                                score = 0
                                coins_collected = 0
                                game_over = False
                            if menu_button_x <= x_mouse \
                                    <= menu_button_x + menu_button_img.get_width() and menu_button_y <= y_mouse <= \
                                    menu_button_y + menu_button_img.get_height():
                                coins += level_recompense_list[level_index]
                                game_status = 'Main'
                                number_of_enemies = 0
                                player.health = player.max_health
                                barier_on = True
                                next_wave = True
                                all_in_pos = 0
                                score = 0
                                coins_collected = 0
                                game_over = False
                        if event.type == END_SONG:
                            next_song()
                else:
                    won_lvl_text = game_over_font.render('YOU DIED', True, (255, 255, 255))
                    screen.blit(won_lvl_text, (480 - won_lvl_text.get_width() / 2, 150))
                    coins_text = restart_font.render('COINS COLLECTED: ', True, (0, 250, 250))
                    coins_collected_text = restart_font.render(str(coins_collected), True, (255, 255, 102))
                    level_recompense_text = restart_font.render('LEVEL BONUS: ', True, (255, 255, 255))
                    level_recompense_num_text = restart_font.render(str(0), True,
                                                                    (250, 250, 102))
                    score_text = restart_font.render('SCORE: ', True, (0, 250, 250))
                    score_num_text = restart_font.render(str(score), True, (255, 255, 102))
                    screen.blit(score_num_text, (380 + score_text.get_width() / 2 + 30, 240))
                    screen.blit(coins_collected_text,
                                (380 - score_text.get_width() / 2 + coins_text.get_width() + 30, 290))
                    screen.blit(score_text, (380 - score_text.get_width() / 2, 240))
                    screen.blit(coins_text, (380 - score_text.get_width() / 2, 290))
                    screen.blit(level_recompense_text, (380 - score_text.get_width() / 2, 340))
                    screen.blit(level_recompense_num_text,
                                (380 - score_text.get_width() / 2 + level_recompense_text.get_width() + 30, 340))
                    restart_button_y = 360
                    restart_button_x = 650

                    restart_color = (0, 0, 0)
                    if restart_button_x <= x_mouse <= restart_button_x + restart_button_img.get_width() and restart_button_y <= \
                            y_mouse <= restart_button_y + restart_button_img.get_height():
                        restart_color = (255, 255, 255)
                    restart_text = restart_font.render('RESTART', True, restart_color)
                    screen.blit(restart_button_img, (restart_button_x, restart_button_y))
                    screen.blit(restart_text, (restart_button_x + restart_text.get_width() / 2, restart_button_y + 15))

                    menu_button_y = 360
                    menu_button_x = 50

                    menu_color = (0, 0, 0)
                    if menu_button_x <= x_mouse <= menu_button_x + menu_button_img.get_width() and menu_button_y <= y_mouse <= \
                            menu_button_y + menu_button_img.get_height():
                        menu_color = (255, 255, 255)
                    menu_text = restart_font.render('MENU', True, menu_color)
                    screen.blit(menu_button_img, (menu_button_x, menu_button_y))
                    screen.blit(menu_text, (menu_button_x + 80, menu_button_y + 15))

                    for event in pygame.event.get():
                        if event.type == QUIT:
                            with open('data_text.txt', 'w') as data_text:
                                json.dump(data, data_text)
                            pygame.quit()
                            sys.exit()
                        if event.type == MOUSEBUTTONDOWN:
                            if restart_button_x <= x_mouse \
                                    <= restart_button_x + restart_button_img.get_width() and restart_button_y <= y_mouse <= \
                                    restart_button_y + restart_button_img.get_height():
                                player.health = player.max_health
                                barier_on = True
                                level_index -= 1
                                calm_time -= 5000
                                next_wave = True
                                all_in_pos = 0
                                score = 0
                                coins_collected = 0
                                game_over = False
                            if menu_button_x <= x_mouse \
                                    <= menu_button_x + menu_button_img.get_width() and menu_button_y <= y_mouse <= \
                                    menu_button_y + menu_button_img.get_height():
                                game_status = 'Main'
                                number_of_enemies = 0
                                level_index -= 1
                                player.health = player.max_health
                                barier_on = True
                                next_wave = True
                                all_in_pos = 0
                                score = 0
                                coins_collected = 0
                                game_over = False
                        if event.type == END_SONG:
                            next_song()

        else:
            if pause_status:
                background_display()
                pause_text = game_over_font.render('PAUSE MENU', True, (255, 255, 255))
                screen.blit(pause_text, (screen.get_width() / 2 - pause_text.get_width() / 2, 50))
                game_sounds_text = restart_font.render('GAME SOUNDS', True, (255, 255, 255))
                screen.blit(game_sounds_text, (screen.get_width()/2-game_sounds_text.get_width()/2, 150))
                sounds_back_rect = pygame.Surface([200, 10])
                sounds_back_rect.fill((192, 192, 192))
                sounds_rect = pygame.Surface([sounds_rect_width, 10])
                sounds_rect.fill((0, 204, 102))
                screen.blit(sounds_back_rect, (screen.get_width()/2-sounds_back_rect.get_width()/2, 190))
                sounds_rect_x = screen.get_width()/2-sounds_back_rect.get_width()/2
                screen.blit(sounds_rect, (sounds_rect_x, 190))
                screen.blit(icon, (volume_icon2_x, 178))
                music_sounds_text = restart_font.render('MUSIC', True, (255, 255, 255))
                screen.blit(music_sounds_text, (screen.get_width() / 2 - music_sounds_text.get_width() / 2, 260))
                screen.blit(sounds_back_rect, (screen.get_width() / 2 - sounds_back_rect.get_width() / 2, 300))
                music_sounds_rect = pygame.Surface([music_sounds_rect_width, 10])
                music_sounds_rect.fill((0, 204, 102))
                music_sounds_rect_x = screen.get_width()/2-sounds_back_rect.get_width()/2
                screen.blit(music_sounds_rect, (music_sounds_rect_x, 300))
                screen.blit(icon, (volume_icon1_x, 288))

                screen.blit(restart_button_img, (screen.get_width() / 2 - restart_button_img.get_width() / 2, 450))
                set_volume_graph_pause(x_mouse)
                if screen.get_width() / 2 - restart_button_img.get_width() / 2 <= x_mouse <= screen.get_width() / 2 + \
                        restart_button_img.get_width() / 2 and 450 <= y_mouse <= 510:
                    resume_color = (255, 255, 255)
                else:
                    resume_color = (0, 0, 0)
                screen.blit(restart_button_img, (screen.get_width() / 2 - restart_button_img.get_width() / 2, 350))
                if screen.get_width() / 2 - restart_button_img.get_width() / 2 <= x_mouse <= screen.get_width() / 2 + \
                        restart_button_img.get_width() / 2 and 350 <= y_mouse <= 410:
                    menu_quit_color = (255, 255, 255)
                else:
                    menu_quit_color = (0, 0, 0)
                quit_text = restart_font.render('QUIT', True, menu_quit_color)
                resume_text = restart_font.render('RESUME', True, resume_color)
                screen.blit(resume_text, (screen.get_width() / 2 - resume_text.get_width() / 2, 465))
                screen.blit(quit_text, (screen.get_width() / 2 - quit_text.get_width() / 2, 365))
                display_mouse(x_mouse, y_mouse)
                for event in pygame.event.get():
                    if event.type == QUIT:
                        with open('data_text.txt', 'w') as data_text:
                            json.dump(data, data_text)
                        pygame.quit()
                        sys.exit()
                    if event.type == MOUSEBUTTONDOWN:
                        if screen.get_width() / 2 - restart_button_img.get_width() / 2 <= x_mouse <= \
                                screen.get_width() / 2 + restart_button_img.get_width() / 2 and 450 <= y_mouse <= 510:
                            pause_status = False
                        if screen.get_width() / 2 - restart_button_img.get_width() / 2 <= x_mouse <= screen.get_width() / 2 + \
                                restart_button_img.get_width() / 2 and 350 <= y_mouse <= 410:
                            pause_status = False
                            if game_type == 'Arcade':
                                game_over = True
                            else:
                                game_over = True
                                Level_status = 'Lost'
                        if volume_icon1_x <= x_mouse <= volume_icon1_x + 32 and 288 <= y_mouse <= 320:
                            click_music = True
                        if volume_icon2_x <= x_mouse <= volume_icon2_x + 32 and 178 <= y_mouse <= 210:
                            click_sounds = True
                    if event.type == MOUSEBUTTONUP:
                        click_music = False
                        click_sounds = False
                    if event.type == END_SONG:
                        next_song()
            else:
                display_back_arrow()
                if next_wave:
                    enemy_to_get_y, enemy_list, enemy_alive, in_pos = wave()

                if len(enemy_list) == 0:
                    if game_type == 'Arcade':
                        barier_on = True
                        next_wave = True
                        all_in_pos = 0
                    elif game_type == 'Levels':
                        game_over = True
                        Level_status = 'Win'

                for enemy in enemy_list:
                    if not in_pos[enemy_list.index(enemy)]:
                        if enemy.rect.centery < enemy_to_get_y[enemy_list.index(enemy)]:
                            enemy.rect.centery += 1
                        elif enemy.rect.centery >= enemy_to_get_y[enemy_list.index(enemy)]:
                            enemy.rect.centery = enemy_to_get_y[enemy_list.index(enemy)]
                            in_pos[enemy_list.index(enemy)] = True
                for i in range(len(in_pos)):
                    if in_pos[i]:
                        all_in_pos += 1
                if all_in_pos < len(in_pos):
                    all_in_pos = 0
                else:
                    barier_on = False
                    move = True
                    if move:
                        if current_time - static_calm_time < calm_time:
                            pass
                        else:
                            movement_initialisation = 0
                            wave_movement = 'follow'
                        for enemy in enemy_list:
                            if movement_initialisation == 0:
                                enemy.movement = wave_movement
                        movement_initialisation += 1
                        for enemy in enemy_list:
                            enemy.move()

                background_display()
                # UPDATING PLAYER SHITS

                player.checking_for_inputs()
                player.player_move()
                player.display_player()
                player.shooting()
                player.display_health_bar()
                # DISPLAYING THE PAUSE BUTTON
                display_pause_button(x_mouse, y_mouse)
                display_recompenses(ini_positions_list)

                for enemy in enemy_list:
                    screen.blit(enemy.image, (enemy.rect.centerx, enemy.rect.centery))
                    enemy.display_health()
                if barier_on:
                    barier.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                    screen.blit(barier, (0, 300))
                if move:
                    for enemy in enemy_list:
                        enemy.shooting()
                        for bullet_pos in enemy.bullets_positions:
                            if bullet_pos[1] > 960:
                                enemy.bullets_positions.remove(
                                    enemy.bullets_positions[enemy.bullets_positions.index(bullet_pos)])
                            else:
                                bullet_x = bullet_pos[0]
                                bullet_y = bullet_pos[1]
                                screen.blit(enemy.bullet_image, (bullet_x, bullet_y))
                                bullet_pos[1] += 1
                checking_for_collision()
                show_score(0, 10)
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN:
                        if screen.get_width() - button.get_width() <= x_mouse <= screen.get_width() and 0 <= y_mouse <=\
                                button.get_height():
                            pause_status = True
                        click_arrow()
                    if event.type == END_SONG:
                        next_song()
        for event in pygame.event.get():
            if event.type == QUIT:
                with open('data_text.txt', 'w') as data_text:
                    json.dump(data, data_text)
                pygame.quit()
                sys.exit()
            if event.type == END_SONG:
                next_song()
        pygame.display.update()
    elif game_status == 'Music':
        rect_surface = pygame.Surface([20, rect_height])
        rect_surface.fill((76, 153, 0))
        music_rect_surface1.fill((131, 176, 243))
        x_mouse, y_mouse = pygame.mouse.get_pos()
        if xp <= x_mouse <= xp + 32 and yp <= y_mouse <= yp + 32:
            if status_play:
                play_man = 'play(1).png'
            else:
                play_man = 'pause(1).png'
        else:
            if status_play:
                play_man = 'play.png'
            else:
                play_man = 'pause.png'

        if xv <= x_mouse <= xv + 32 and yv <= y_mouse <= yv + 32:
            if status_volume:
                volume = 'volume(1).png'
            else:
                volume = 'mute(1).png'
        else:
            if status_volume:
                volume = 'volume.png'
            else:
                volume = 'mute.png'

        if xn <= x_mouse <= xn + 32 and yn <= y_mouse <= yn + 32:
            next_name = 'next(1).png'
        else:
            next_name = 'next.png'

        if xpr <= x_mouse <= xpr + 32 and ypr <= y_mouse <= ypr + 32:
            previous = 'previous(1).png'
        else:
            previous = 'previous.png'

        if xm <= x_mouse <= xm + 32 and ym <= y_mouse <= ym + 32:
            music = 'music-album(1).png'
        else:
            music = 'music-album.png'

        for event in pygame.event.get():
            if event.type == QUIT:
                with open('data_text.txt', 'w') as data_text:
                    json.dump(data, data_text)
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                get_index_song()
                click_arrow()
                if xv <= x_mouse <= xv + 32 and yv <= y_mouse <= yv + 32:
                    status_volume = not status_volume
                    if volume_on:
                        mixer.music.set_volume(0)
                    if not volume_on:
                        mixer.music.set_volume(1)
                    volume_on = not volume_on
                    # + CODE MUTING THE MUSIC OR PUTTING THE VOLUME AT 0
                if xn <= x_mouse <= xn + 32 and yn <= y_mouse <= yn + 32:
                    next_song()
                if xpr <= x_mouse <= xpr + 32 and ypr <= y_mouse <= ypr + 32:
                    previous_song()
                if xm <= x_mouse <= xm + 32 and ym <= y_mouse <= ym + 32:
                    add_song()
                if xp <= x_mouse <= xp + 32 and yp <= y_mouse <= yp + 32:
                    try:
                        if static_play == 0:
                            mixer.music.load(current_song)
                            PLAY.play_initial()
                            static_play += 1
                            status_play = False
                        else:
                            PLAY.initial_status_play()
                            PLAY.pause_unpause()
                            status_play = not status_play
                    except:
                        pass
                        # + CODE PAUSING THE SONG
                if widget_posx11 <= x_mouse <= widget_posx11 + 30 and widget_posy1 <= y_mouse <= widget_posy1 + 30:
                    click = True
            if event.type == MOUSEBUTTONUP:
                for position_ in positions:
                    if position_[1] <= y_mouse < position_[1] + 60:
                        pass
                clicking = False
                click = False
            if event.type == END_SONG:
                next_song()

        background_display()
        display_back_arrow()
        display_song(clicking, click_song_index)
        icons_screen()
        set_volume_graph(y_mouse)
        display()
        pygame.display.update()
    elif game_status == 'Upgrades':
        rect_surface_speed = pygame.Surface([rect_width_speed, 20])
        rect_surface_health = pygame.Surface([rect_width_health, 20])
        rect_surface_body_damage = pygame.Surface([rect_width_body_damage, 20])
        rect_surface_bullet = pygame.Surface([rect_width_bullet, 20])
        rect_surface_speed.fill((76, 153, 0))
        rect_surface_bullet.fill((76, 153, 0))
        rect_surface_body_damage.fill((76, 153, 0))
        rect_surface_health.fill((76, 153, 0))
        rect_surface1.fill((131, 176, 243))
        for event in pygame.event.get():
            if event.type == QUIT:
                with open('data_text.txt', 'w') as data_text:
                    json.dump(data, data_text)
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    if click_pr:
                        pass
                    else:
                        if ship_num == 15:
                            pass
                        else:
                            if b == 0:
                                b = 24
                            click_nx = True
                if event.key == K_LEFT:
                    if click_nx:
                        pass
                    else:
                        if ship_num == 0:
                            pass
                        else:
                            if b == 24:
                                b = 0
                            click_pr = True
            if event.type == MOUSEBUTTONDOWN:
                click_arrow()
                if widget_posx1 <= x_mouse <= widget_posx1 + 32 and widget_posy <= y_mouse <= widget_posy + 32:
                    click1 = True
                if widget_posx2 <= x_mouse <= widget_posx2 + 32 and widget_posy + 40 <= y_mouse <= widget_posy + 72:
                    click2 = True
                if widget_posx3 <= x_mouse <= widget_posx3 + 32 and widget_posy + 80 <= y_mouse <= widget_posy + 112:
                    click3 = True
                if widget_posx4 <= x_mouse <= widget_posx4 + 32 and widget_posy + 120 <= y_mouse <= widget_posy + 152:
                    click4 = True
                if 770 <= x_mouse <= 920 and 310 <= y_mouse <= 370:
                    payed = True
                    static_skin_time = current_time
                if screen.get_width()/2 - button.get_width()/2 - 350 <= x_mouse <= screen.get_width()/2 - button.get_width()/2 - 302 and  screen.get_height()/2 - button.get_height()/2 - 100 <= y_mouse <= screen.get_height()/2 - button.get_height()/2 - 52:
                    if click_nx:
                        pass
                    else:
                        if ship_num == 0:
                            pass
                        else:
                            if b == 24:
                                b = 0
                            click_pr = True
                if screen.get_width()/2 - button.get_width()/2 + 350 <= x_mouse <= screen.get_width()/2 - button.get_width()/2 + 398 and  screen.get_height()/2 - button.get_height()/2 - 100 <= y_mouse <= screen.get_height()/2 - button.get_height()/2 - 52:
                    if click_pr:
                        pass
                    else:
                        if ship_num == 15:
                            pass
                        else:
                            if b == 0:
                                b = 24
                            click_nx = True
            if event.type == MOUSEBUTTONUP:
                click1, click2, click3, click4 = False, False, False, False
            if event.type == END_SONG:
                next_song()

        next_button()
        previous_button()
        background_display()
        display_ship_imgs()
        displaying_names()
        display_upgrade_bars(x_mouse, ship_num)
        display_upgrade_names()
        displaying_upgrade_values()
        display_bg_cover()
        display_coins_count()
        display_back_arrow()
        display_next_pre_buttons()
        pay_ur_bills(ship_num)
        pygame.display.update()
    elif game_status == 'Skins':
        for event in pygame.event.get():
            if event.type == QUIT:
                with open('data_text.txt', 'w') as data_text:
                    json.dump(data, data_text)
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                click_arrow()
                click_button(index)
                for position in icon_positions:
                    if position[0] <= x_mouse <= position[0] + 70 and position[1] <= y_mouse <= position[1] + 70:
                        index = icon_positions.index(position)
            if event.type == END_SONG:
                next_song()

        background_display()
        skins_bar_display()
        displaying_ship_icons()
        displaying_ship_img(index)
        display_coins_count()
        display_back_arrow()
        buttons_display(index)
        display_upgrades_container()
        display_upgrades(index)
        display_sorry_text()
        displaying_the_price(index)
        pygame.display.update()
    data = {
        'coins': coins,
        'ship_speed_list': ship_speed_list,
        'ship_body_damage_list': ship_body_damage_list,
        'ship_health_list': ship_health_list,
        'ship_bullet_min_damage_list': ship_bullet_min_damage_list,
        'buy_status_list': buy_status_list,
        'select_ship_list': select_ship_list,
        'level_index': level_index
    }