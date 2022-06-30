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
day = 0
#total_wanderer = 0
#total_food = 0

# ==================== start once ====================

# create wanderer

f = open('log_schedule','w')

for a in range(10):
    ob = fo.create_entity(random.randint(20,var.screen_width - 20),random.randint(20,var.screen_height - 20),classes.Wanderer,var.list_wanderer,1,screen)
    ob.age = var.FPS * var.day_lenght
    ob.delay_breed = 0
    for a in ob.schedule:
        f.write(a)
        f.write(' / ')
    f.write('\n')
    
f.close

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
        if var.total_counter == var.day_lenght:
            day += 1
            var.total_counter = 0
            rng = 100 - len(var.list_food)
            for a in range(rng):
                fo.create_entity(random.randint(20,var.screen_width - 20),random.randint(20,var.screen_height - 20),classes.Food,var.list_food,1,screen)
        
        var.total_counter += 1
        
        print('Wand:', len(var.list_wanderer))
        print('Food:', len(var.list_food))   
        print('Day :', day)
        print('Time:', round((1440 / var.day_lenght) * var.total_counter // 60), ':', round((1440 / var.day_lenght) * var.total_counter % 60))
        #print(round(var.list_wanderer[0].hunger))
        #print(round(var.list_wanderer[0].sleep))
        #print(var.list_wanderer[0].schedule)
        #print(var.list_wanderer[0].state)
        #print('Wa/T:', round(total_wanderer/var.total_counter,2))
        #print('Fo/T:', round(total_food/var.total_counter,2))


    # behavior wanderer
    for wanderer in var.list_wanderer:
        fo.init_behavior(wanderer)
               
    # behavior food
    for food in var.list_food:
        fo.init_behavior(food)
        
    # ====================  end loop  ====================
        
    pg.display.flip()
    
    
f = open('log_schedule','a')
f.write('\n\n')
for a in var.list_wanderer:
    for b in a.schedule:
        f.write(b)
        f.write(' / ')
    f.write('\n')
f.close
quit()