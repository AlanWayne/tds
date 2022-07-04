from functools import total_ordering
from pydoc import cli

import pygame as pg
pg.init()
import var
var.init()
screen = pg.display.set_mode((var.screen_width, var.screen_height),pg.RESIZABLE)

import random
import classes
import func_math as fm
import func_objects as fo
import os
import operator
import drawable
import sprite

clock = pg.time.Clock()
run = True
clicked_object = None

counter = 60
day = 0

# ==================== start once ====================

# create wanderer

f = open('log_schedule','w')

for a in range(20):
    ob = fo.create_entity(random.randint(20,var.scene_width - 20),random.randint(20,var.scene_height - 20),classes.Wanderer,None)
    ob.age = var.FPS * var.day_lenght
    ob.delay_breed = 0
    for a in ob.schedule:
        f.write(a)
        f.write(' / ')
    f.write('\n')
    
f.close

# create camera

fo.create_entity(0,0,classes.Camera,None)

for a in range(50 - len(var.list_food)):
    fo.create_entity(random.randint(0, var.scene_width), random.randint(0, var.scene_height),classes.Food,None)

# create backgroud
screen.fill((100,200,120))  
for i in range(var.scene_width//64 + 1):
    for j in range(var.scene_height//64 + 1):
        bg = classes.Background(i,j)
        var.bg_list.append(bg)

# ====================  end once  ====================

while run:
    clock.tick(var.FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                mo = fo.find_nearest_to_mouse(var.list_wanderer)
                mx, my = pg.mouse.get_pos()
                if fm.distance_between(mo.x - var.obj_camera.x,mo.y - var.obj_camera.y,mx,my) < 30:
                    clicked_object = mo
                else:
                    clicked_object = None
        if event.type == pg.VIDEORESIZE:
            var.screen_width = screen.get_width()
            var.screen_height = screen.get_height()
            
        
    # ==================== start loop ====================
    
    if counter == var.FPS:
        counter = 0
    
    if counter == 0:
           
        if var.total_counter == 0:
            day += 1
            var.total_counter = 0
        
        var.total_counter += 1
        
        # backlog
        
        os.system('cls' if os.name == 'nt' else 'clear')
        #print('Wand:', len(var.list_wanderer))
        #print('Dead:', var.deaths) 
        print('Day :', day)
        print('Time:', round((1440 / var.day_lenght) * var.total_counter // 60), ':', round((1440 / var.day_lenght) * var.total_counter % 60))
        print('FPS :', round(clock.get_fps(),1))
        print('')
        '''if clicked_object != None:
            print('Positi:',round(clicked_object.x),round(clicked_object.y))
            print('Mouse :',pg.mouse.get_pos())
            print('Hunger:',round(clicked_object.hunger))
            print('Sleep :',round(clicked_object.sleep))
            print('State :',clicked_object.state)
            print('Sex   :',clicked_object.sex)
            print('Patner:',clicked_object.partner)
            
            print('')'''

    
    # objects action
    for object in (var.list_wanderer + var.list_food + var.list_shadow):
        object.action()
        
    var.obj_camera.action()
    
    # draw
    
    for bg in var.bg_list:
        bg.draw(screen)
    
        # shadow      
    draw_list = var.list_shadow
    for dr in sorted(draw_list,key=operator.methodcaller('get_depth')):
        dr.draw(screen)
        
        # debug - target highlight
    if clicked_object != None:
        pg.draw.ellipse(screen,
            (255,127,0),(
            (clicked_object.x - var.obj_camera.x - clicked_object.sprite.get_width()/2 - 8,
            clicked_object.y - var.obj_camera.y - clicked_object.sprite.get_height()/4 - 4),
            (clicked_object.sprite.get_width() + 16, clicked_object.sprite.get_height()/2 + 8)
            ),
            4)
        for c in clicked_object.children:
            pg.draw.ellipse(screen,
                (255,0,127),(
                (c.x - var.obj_camera.x - c.sprite.get_width()/2 - 8,
                c.y - var.obj_camera.y - c.sprite.get_height()/4 - 4),
                (c.sprite.get_width() + 16, c.sprite.get_height()/2 + 8)
                ),
                3)
        if clicked_object.parent_m != None:
            pg.draw.ellipse(screen,
            (0,127,255),(
            (clicked_object.parent_m.x - var.obj_camera.x - clicked_object.parent_m.sprite.get_width()/2 - 8,
            clicked_object.parent_m.y - var.obj_camera.y - clicked_object.parent_m.sprite.get_height()/4 - 4),
            (clicked_object.parent_m.sprite.get_width() + 16, clicked_object.parent_m.sprite.get_height()/2 + 8)
            ),
            3)
        if clicked_object.parent_f != None:
            pg.draw.ellipse(screen,
            (255,0,255),(
            (clicked_object.parent_f.x - var.obj_camera.x - clicked_object.parent_f.sprite.get_width()/2 - 8,
            clicked_object.parent_f.y - var.obj_camera.y - clicked_object.parent_f.sprite.get_height()/4 - 4),
            (clicked_object.parent_f.sprite.get_width() + 16, clicked_object.parent_f.sprite.get_height()/2 + 8)
            ),
            3)
        if clicked_object.partner != None:
            pg.draw.ellipse(screen,
            (127,0,255),(
            (clicked_object.partner.x - var.obj_camera.x - clicked_object.partner.sprite.get_width()/2 - 8,
            clicked_object.partner.y - var.obj_camera.y - clicked_object.partner.sprite.get_height()/4 - 4),
            (clicked_object.partner.sprite.get_width() + 16, clicked_object.partner.sprite.get_height()/2 + 8)
            ),
            3)
            
        # objects
    draw_list = var.list_food + var.list_wanderer
    for dr in sorted(draw_list,key=operator.methodcaller('get_depth')):
        dr.draw(screen)
          
        # debug - needs bar
            # hunger
    if clicked_object != None:
        drawable.health_bar(screen,
            clicked_object.x - var.obj_camera.x,
            clicked_object.y - var.obj_camera.y,
            round(clicked_object.sprite.get_width()),
            round(clicked_object.sprite.get_height() * 1.5),
            clicked_object.hunger,
            clicked_object.hunger_full,
            [255,0,0],
            [0,255,0]
        )
            # sleep
        drawable.health_bar(screen,
            clicked_object.x - var.obj_camera.x,
            clicked_object.y - var.obj_camera.y,
            round(clicked_object.sprite.get_width()),
            round(clicked_object.sprite.get_height() * 1.5 - clicked_object.sprite.get_width()/6 - 2),
            clicked_object.sleep,
            clicked_object.sleep_full,
            [255,0,0],
            [0,0,255]
        )
            # sex
        if clicked_object.sex == 'female':
            screen.blit(
                pg.transform.scale2x(sprite.spr_sex[0]),
                (clicked_object.x - var.obj_camera.x + round(clicked_object.sprite.get_width() / 2),
                clicked_object.y - var.obj_camera.y - round(clicked_object.sprite.get_height() * 1.5 + 5))
                
            )
        else:
            screen.blit(
                pg.transform.scale2x(sprite.spr_sex[1]),
                (clicked_object.x - var.obj_camera.x + round(clicked_object.sprite.get_width() / 2 + 4),
                clicked_object.y - var.obj_camera.y - round(clicked_object.sprite.get_height() * 1.5 + 5))
                
            )
            
        
    counter += 1
    
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