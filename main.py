from functools import total_ordering
from pydoc import cli
import random
import pygame as pg
pg.init()
import var
var.init()
import classes
import func_math as fm
import func_objects as fo
import os
import operator

screen = pg.display.set_mode([var.screen_width, var.screen_height])
clock = pg.time.Clock()
run = True
clicked_object = None

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
        if event.type == pg.MOUSEBUTTONDOWN:
            mx, my = pg.mouse.get_pos()
            mo = fm.find_nearest_to_point(mx,my,var.list_wanderer)
            if fm.distance_to_point(mo,mx,my) < 15:
                clicked_object = mo
            else:
                clicked_object = None
             
    screen.fill((100,200,120))
    bg_img = pg.image.load('images/bg_grass0.png')
    bg_img_width = bg_img.get_width()
    for i in range(var.screen_width//bg_img_width + 1):
        for j in range(var.screen_height//bg_img_width + 1):
            screen.blit(pg.transform.scale2x(bg_img),(i*64,j*64))
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
        
        # backlog
        
        print('Wand:', len(var.list_wanderer))
        print('Dead:', var.deaths)
        print('Food:', len(var.list_food))   
        print('Day :', day)
        print('Time:', round((1440 / var.day_lenght) * var.total_counter // 60), ':', round((1440 / var.day_lenght) * var.total_counter % 60))
        print('')
        if clicked_object != None:
            print('Hunger:',round(clicked_object.hunger))
            print('Sleep :',round(clicked_object.sleep))
            print('Behavi:',clicked_object.schedule)
            print('State :',clicked_object.state)
            print('Parent:',clicked_object.parent)
            print('Childr:',clicked_object.children)

    # debug    
    if clicked_object != None:
        pg.draw.circle(screen,(255,255,0),(clicked_object.x,clicked_object.y),15,1)
        for c in clicked_object.children:
            pg.draw.line(screen,(255,0,255),(clicked_object.x,clicked_object.y),(c.x,c.y),1)
        if clicked_object.parent != None:
            pg.draw.line(screen,(0,255,255),(clicked_object.x,clicked_object.y),(clicked_object.parent.x,clicked_object.parent.y),1)
    
    # objects action
    for object in (var.list_wanderer + var.list_food):
        object.action()
    
    # draw
    draw_list = var.list_food + var.list_wanderer
    for dr in sorted(draw_list,key=operator.methodcaller('get_depth')):
        dr.draw()
    #draw_list = sorted(draw_list,key=y)
    
    
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