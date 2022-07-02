def init():
    global screen_width
    screen_width = 1024
    global screen_height
    screen_height = 768
    global FPS
    FPS = 60
    
    global scene_width
    scene_width = 2000
    global scene_height 
    scene_height = 2000
    
    global list_wanderer
    list_wanderer = []
    global list_food
    list_food = []
    global list_shadow
    list_shadow = []
    
    global day_lenght
    day_lenght = 72
    global obj_state_wanderer
    obj_state_wanderer = ['breed','food','sleep','wander']
    global total_counter
    total_counter = 0
    global deaths
    deaths = 0
    
    global obj_camera
    obj_camera = None 