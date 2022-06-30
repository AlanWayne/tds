from functools import total_ordering
import random
import pygame as pg
pg.init()
import var
var.init()
import classes
import func_objects as fo
import os

screen = pg.display.set_mode([var.screen_width, var.screen_height])
clock = pg.time.Clock()
run = True

counter = 0
total_counter = var.day_lenght
day = 0
#total_wanderer = 0
#total_food = 0

# ==================== start once ====================

# create wanderer
for a in range(2):
    ob = fo.create_entity(random.randint(20,var.screen_width - 20),random.randint(20,var.screen_height - 20),classes.Wanderer,var.list_wanderer,1,screen)
    ob.age = var.FPS * var.day_lenght
    ob.delay_breed = 0

# ====================  end once  ====================

while run:
    clock.tick(var.FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            
    screen.fill((100,200,120))
    
    # ==================== start loop ====================
    
    if counter == var.FPS:
        counter = 0
    counter += 1
        
    # create food
    if counter == 60:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        #total_wanderer += len(var.list_wanderer)
        #total_food += len(var.list_food)    
        if total_counter == var.day_lenght:
            day += 1
            total_counter = 0
            rng = 100 - len(var.list_food)
            for a in range(rng):
                fo.create_entity(random.randint(20,var.screen_width - 20),random.randint(20,var.screen_height - 20),classes.Food,var.list_food,1,screen)
        
        total_counter += 1
        
        print('Wand:', len(var.list_wanderer))
        print('Food:', len(var.list_food))   
        print('Day :', day)
        print('Time:', round((1440 / var.day_lenght) * total_counter // 60), ':', round((1440 / var.day_lenght) * total_counter % 60))
        #print('Wa/T:', round(total_wanderer/total_counter,2))
        #print('Fo/T:', round(total_food/total_counter,2))


    # behavior wanderer
    for wanderer in var.list_wanderer:
        fo.init_behavior(wanderer)
               
    # behavior food
    for food in var.list_food:
        fo.init_behavior(food)
        
    # ====================  end loop  ====================
        
    pg.display.flip()
    
quit()