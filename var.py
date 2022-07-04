import pygame as pg

def init():
    global screen_width
    global screen_height
    screen_width, screen_height = 1024, 768
    global FPS
    FPS = 60
    
    global scene_width
    global scene_height 
    scene_width, scene_height = pg.display.get_desktop_sizes()[0]
    
    global list_wanderer
    list_wanderer = []
    global list_food
    list_food = []
    global list_shadow
    list_shadow = []
    global bg_list
    bg_list = []
    
    global day_lenght
    day_lenght = 720
    global obj_state_wanderer
    obj_state_wanderer = ['breed','food','sleep','wander']
    global total_counter
    total_counter = 0
    global deaths
    deaths = 0
    
    global obj_camera
    obj_camera = None 