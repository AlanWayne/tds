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
import drawable

screen = pg.display.set_mode([var.screen_width, var.screen_height])
clock = pg.time.Clock()
run = True
clicked_object = None

counter = 60
day = 0

# ==================== start once ====================

# create wanderer

f = open('log_schedule','w')

for a in range(10):
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

# ====================  end once  ====================

while run:
    clock.tick(var.FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN:
            mo = fo.find_nearest_to_mouse(var.list_wanderer)
            mx, my = pg.mouse.get_pos()
            if fm.distance_between(mo.x - var.obj_camera.x,mo.y - var.obj_camera.y,mx,my) < 30:
                clicked_object = mo
            else:
                clicked_object = None
    
    # background         
    
    screen.fill((100,200,120))
    bg_img = pg.image.load('images/bg_grass0.png')
    bg_img_width = bg_img.get_width()
    
    
    # ==================== start loop ====================
    
    if counter == var.FPS:
        counter = 0
        
    # create food
    if counter == 0:
        os.system('cls' if os.name == 'nt' else 'clear')
           
        if var.total_counter == 0:
            day += 1
            var.total_counter = 0
            rng = 100 - len(var.list_food)
            for a in range(rng):
                fo.create_entity(random.randint(0, var.scene_width), random.randint(0, var.scene_height),classes.Food,None)
        
        var.total_counter += 1
        
        # backlog
        
        print('Wand:', len(var.list_wanderer))
        print('Dead:', var.deaths)
        #print('Food:', len(var.list_food))   
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
            print('')

    
    # objects action
    for object in (var.list_wanderer + var.list_food + var.list_shadow):
        object.action()
        
    var.obj_camera.action()
    
    # draw
    for i in range(var.scene_width//bg_img_width + 1):
        for j in range(var.scene_height//bg_img_width + 1):
            if i*64 > var.obj_camera.x - 64 and i*64 < (var.obj_camera.x + var.screen_width) and j*64 > var.obj_camera.y - 64 and j*64 < (var.obj_camera.y + var.screen_height):
                screen.blit(pg.transform.scale2x(bg_img),(i*64 - var.obj_camera.x,j*64 - var.obj_camera.y))
            
        # shadow      
    draw_list = var.list_shadow
    for dr in sorted(draw_list,key=operator.methodcaller('get_depth')):
        dr.draw(screen)
        
        # debug    
    if clicked_object != None:
        pg.draw.ellipse(screen,
                        (255,127,0),(
            (clicked_object.x - var.obj_camera.x - clicked_object.sprite.get_width() - 4,
            clicked_object.y - var.obj_camera.y - clicked_object.sprite.get_height()/2 - 4),
            (clicked_object.sprite.get_width() * 2 + 4, clicked_object.sprite.get_height() + 8)
            ),
                        4)
        for c in clicked_object.children:
            pg.draw.line(screen,(255,0,255),(clicked_object.x - var.obj_camera.x,clicked_object.y - var.obj_camera.y),(c.x - var.obj_camera.x,c.y - var.obj_camera.y),1)
        if clicked_object.parent != None:
            pg.draw.line(screen,(0,255,255),(clicked_object.x - var.obj_camera.x,clicked_object.y - var.obj_camera.y),(clicked_object.parent.x - var.obj_camera.x,clicked_object.parent.y - var.obj_camera.y),1)
            
        # objects
    draw_list = var.list_food + var.list_wanderer
    for dr in sorted(draw_list,key=operator.methodcaller('get_depth')):
        dr.draw(screen)
          
        # debug 2
    if clicked_object != None:
        drawable.health_bar(screen,clicked_object.x - var.obj_camera.x,clicked_object.y - var.obj_camera.y,48,48,clicked_object.hunger,clicked_object.hunger_full,[255,0,0],[0,255,0])
        
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