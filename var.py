def init():
    global screen_width
    screen_width = 1024
    global screen_height
    screen_height = 768
    global FPS
    FPS = 60
    global list_wanderer
    list_wanderer = []
    global list_food
    list_food = []
    global day_lenght
    day_lenght = 720
    global obj_state_wanderer
    obj_state_wanderer = ['breed','food','sleep','wander']
    global total_counter
    total_counter = day_lenght