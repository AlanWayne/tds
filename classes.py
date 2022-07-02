from doctest import master
from winreg import ExpandEnvironmentStrings
import pygame as pg 
import random
import var
import func_math as fm
import func_objects as fo
import sprite
import var

# ================================ wanderer ================================

class Wanderer:    
    # stats
    name = 'rabbit'
    frame = 0
    sprite_counter = 0
    sprite_speed = (60 / var.FPS) * 10
    sprite = sprite.spr_rabbit_walk[frame]
    x_axis = random.choice(['Left','Right'])
    depth = 0
    moving = False
    shadow = None
    
    x = 0
    y = 0
    spd = 30 / var.FPS
    height = 14
    width = 16
    age = 0
    sight = 250
    target_x = 0
    target_y = 0
    
    hunger = var.FPS * 8
    hunger_full = var.FPS * 16
    hunger_one = var.FPS * 8
    
    sleep = var.FPS * var.day_lenght * 0.75
    sleep_full = var.FPS * var.day_lenght * 0.75
    
    schedule = []
    state_time = ''
    state = ''
    
    child = True
    parent = None
    children = []
    delay_breed = var.FPS * var.day_lenght
    
    def __init__(
        self, 
        x, 
        y, 
    ):
        self.x = x
        self.y = y
        
        self.hunger = 500
        
        self.schedule = []
        for a in range(10):
            self.schedule.append(random.choice(var.obj_state_wanderer))
            
        self.children = []
                
    # set the coordinates
    def set_xy(self,x,y):
        self.x += x
        self.y += y
        
    # drawing
    def draw(self,screen):
        if self.x > var.obj_camera.x and self.x < (var.obj_camera.x + var.screen_width) and self.y > var.obj_camera.y and self.y < (var.obj_camera.y + var.screen_height):
        
            # stand
            if self.moving == False:
                self.frame = 0
                self.sprite_counter = 0
            
            # walk
            if self.moving == True:
                self.sprite_counter += self.sprite_speed
                
                if self.sprite_counter >= var.FPS:
                    self.sprite_counter = 0
                    self.frame += 1
                    
                if self.frame >= len(sprite.spr_rabbit_walk):
                    self.frame = 0
                    
            #set sprite
            self.sprite = sprite.spr_rabbit_walk[self.frame]
            
            # rotation      
            if self.x_axis == 'Left':
                screen.blit(pg.transform.scale(self.sprite, (self.width, self.height)), (self.x - self.width/2 - var.obj_camera.x, self.y - self.height - var.obj_camera.y))
            if self.x_axis == 'Right':
                screen.blit((pg.transform.flip(pg.transform.scale(self.sprite, (self.width, self.height)), True, False)), ((self.x - self.width/2) - var.obj_camera.x, (self.y - self.height) - var.obj_camera.y))
        
    # get depth
    def get_depth(self):
        self.depth = self.y
        return self.depth
        
    # action
    def action(self):
        # move
        self.move()
        
        # check state
        self.state_time = self.schedule[round(var.total_counter * 10 / var.day_lenght) - 1]
        
        if self.state_time == 'breed'  and self.hunger > self.hunger_full:
            self.breed()
            self.state = 'breed'
        if self.state_time == 'food'    or self.hunger < self.hunger_full/4:
            self.search_food()
            self.state = 'food'
        if self.state_time == 'sleep'  and self.hunger > self.hunger_full/4:
            self.go_sleep()
            self.state = 'sleep'
        if self.state_time == 'wander' and self.hunger > self.hunger_full/4:
            self.wander()
            self.state = 'wander'
            
        # check age
        if self.child == True and self.age > (var.FPS * var.day_lenght):
            self.grow()
        self.age += 1
        
        # check grown children
        for ch in self.children:
            if ch.child == False:
                self.children.remove(ch)
        
        # hunger
        self.hunger -= min(self.hunger,(1/var.FPS) * (1440/var.day_lenght))
        if self.delay_breed > 0:
            self.delay_breed -= 1
        if self.hunger > (self.hunger_full + self.hunger_one):
            self.hunger = self.hunger_full
            
        # sleep
        if self.state == 'sleep':
            self.sleep += 3
        else:
            self.sleep -= 1   
            
        # death
        if self.hunger <= 0 or self.sleep <= 0 or self.age > (5 * var.day_lenght * var.FPS):
            var.list_wanderer.remove(self)
            if self.parent != None:
                self.parent.children.remove(self)
            for ch in self.children:
                ch.parent = None
            self.death()
            var.deaths += 1
            
    # movement
    def move(self):
        
        # check rotation
        if self.target_x < self.x:
            self.x_axis = 'Left'
            self.moving = True
        elif self.target_x > self.x:
            self.x_axis = 'Right'
            self.moving = True
        else:
            self.moving = False
        
        #borders
        
        if self.target_x < 0 or self.target_x > var.scene_width or self.target_y < 0 or self.target_y > var.scene_height:
            self.target_x = self.x
            self.target_y = self.y
        
        # move
        dx, dy = fm.relative_velocity(self.x, self.y, self.target_x, self.target_y)
                
        if self.x < self.target_x:
            self.x += self.spd * dx
            
        if self.x > self.target_x:
            self.x -= self.spd * dx
            
        if self.y < self.target_y:
            self.y += self.spd * dy
            
        if self.y > self.target_y:
            self.y -= self.spd * dy
        
        # check for small distance        
        if fm.distance_to_point(self,self.target_x,self.target_y) < self.spd:
            self.target_x = self.x
            self.target_y = self.y
        
        # check for collision with brothers
        nb = fo.find_nearest_brother(self,var.list_wanderer)
        if nb != 0:
            dtp = fm.distance_to_point(nb, self.x, self.y)
            if dtp < 10:
                dx, dy = fm.relative_velocity(self.x, self.y, nb.x, nb.y)
                if self.x < nb.x:
                    self.x -= (10 - dtp) * dx
                if self.x > nb.x:
                    self.x += (10 - dtp) * dx
                if self.y < nb.y:
                    self.y -= (10 - dtp) * dy
                if self.y > nb.y:
                    self.y += (10 - dtp) * dy
    
    # wander
    def wander(self):
        if random.randint(1,30) == 1:
            if fm.distance_to_point(self,self.target_x,self.target_y) < 10:
                if self.child == False:
                    self.target_x += random.choice([-1,1]) * random.randint(25,50)
                    self.target_y += random.choice([-1,1]) * random.randint(25,50)
                else:
                    if self.parent != None:
                        self.target_x = self.parent.x + random.choice([-1,1]) * random.randint(25,50)
                        self.target_y = self.parent.y + random.choice([-1,1]) * random.randint(25,50)
                    else:
                        self.target_x += random.choice([-1,1]) * random.randint(25,50)
                        self.target_y += random.choice([-1,1]) * random.randint(25,50)
                        
    # check for orphans    
    def orphan(self):
        if self.child == False:
            for obj in var.list_wanderer:
                if (obj.child == True) and (obj.parent == None) and (fm.distance_to_object(self,obj) < self.sight):
                    obj.parent = self
                    self.children.append(obj)
    
    # set target to exact object        
    def chase(self, object):
        self.target_x = object.x
        self.target_y = object.y
    
    # scan area for food    
    def search_food(self):
        if self.hunger < self.hunger_full:
            t = fo.find_nearest_to_object(self,var.list_food)
            if fm.distance_to_object(self,t) < self.sight and t != self:
                self.chase(t)
            else:
                self.wander()
        else:
            self.wander()
            
    # sleep
    def go_sleep(self):
        self.target_x = self.x
        self.target_y = self.y
         
    # breed
    def breed(self):
        if self.hunger > self.hunger_full:
            if self.delay_breed == 0:
                child_shift_x = random.randint(0,10) * random.choice([-1,1])
                child_shift_y = (10 - child_shift_x) * random.choice([-1,1])
                child0 = fo.create_entity(self.x + child_shift_x,self.y + child_shift_y,Wanderer,None)
                child0.schedule = self.schedule
                child0.parent = self
                self.children.append(child0)
                self.delay_breed += var.FPS * var.day_lenght / 3
                self.hunger -= var.FPS * 8
    
    # death       
    def death(self):
        #fo.create_entity(self.x,self.y,Food,var.list_food,None)
        var.deaths += 1
        del self
                  
    # grow up
    def grow(self):
        self.height *= 2
        self.width *= 2
        self.spd *= 2
        self.sight *= 2
        self.child = False
        self.parent = None
          
# ================================ food ================================

class Food:
    height = 16
    width = 10
    depth = 0
    sprite0 = random.choice(sprite.spr_carrot)
    sprite_rot = None
        
    def __init__(
        self, 
        x, 
        y,
    ):
        self.x = x
        self.y = y
        self.depth = self.y
        self.sprite_rot = random.choice([True,False])
        self.sprite0 = random.choice(sprite.spr_carrot)

    # draw
    def draw(self,screen):
        if self.x > var.obj_camera.x and self.x < (var.obj_camera.x + var.screen_width) and self.y > var.obj_camera.y and self.y < (var.obj_camera.y + var.screen_height):
            if self.sprite_rot == True:
                screen.blit(pg.transform.flip(pg.transform.scale(self.sprite0,(32,32)),True,False), (self.x - self.width/2 - var.obj_camera.x, self.y - self.height - var.obj_camera.y))
            else:
                screen.blit(pg.transform.scale(self.sprite0,(32,32)), (self.x - self.width/2 - var.obj_camera.x, self.y - self.height - var.obj_camera.y))
        
    # get depth
    def get_depth(self):
        self.depth = self.y
        return self.depth
        
    # action
    def action(self):
        
        for wanderer in var.list_wanderer:
            if fm.distance_to_object(self,wanderer) < 10 and wanderer.hunger < 1000:
                wanderer.hunger += wanderer.hunger_one
                self.death()
                break
            
        if fm.distance_to_object(self,fo.find_nearest_brother(self,var.list_food)) < 16:
            self.death()
            
    def death(self):
        var.list_food.remove(self)
        del self
            
# ================================ shadow ================================

class Shadow:
    frame = 0
    master = None
    x = 0
    y = 0
    sprite0 = None
    
    def __init__(self,master):
        self.master = master
    
    def action(self):
        
        if self.master != None:
            self.x = self.master.x
            self.y = self.master.y
            
            if type(self.master) == Wanderer:
                frame = self.master.frame
                self.sprite0 = sprite.spr_shadow_rabbit[frame]
                if self.master.child == False:
                    self.sprite0 = pg.transform.scale(self.sprite0,(36,16))
        else:
            var.list_shadow.remove(self)
            del self
            
    def draw(self,screen):
        if self.x > var.obj_camera.x and self.x < (var.obj_camera.x + var.screen_width) and self.y > var.obj_camera.y and self.y < (var.obj_camera.y + var.screen_height):
            if screen != None and self.sprite0 != None:
                screen.blit(self.sprite0, (self.x - self.sprite0.get_width()/2 - var.obj_camera.x , self.y - self.sprite0.get_height()/2 - var.obj_camera.y))
            
    # get depth
    def get_depth(self):
        self.depth = self.y
        return self.depth
                
# ================================ camera ================================

class Camera:
    x = var.scene_width / 2 - var.screen_width / 2
    y = var.scene_height / 2 - var.screen_height / 2
    
    m_left = False
    m_right = False
    m_down = False
    m_up = False

    speed = 50
    #counter_speed = var.FPS / 30
    #counter = 0
    
    def __init__(self):
        self.x = var.scene_width / 2 - var.screen_width / 2
        self.y = var.scene_height / 2 - var.screen_height / 2
    
    def action(self):      
        keys=pg.key.get_pressed()
        #if self.counter == 0:
        if keys[pg.K_LEFT]:
            #self.counter = self.counter_speed
            self.x -= self.speed
        
        if keys[pg.K_RIGHT]:
            #self.counter = self.counter_speed
            self.x += self.speed
                    
        if keys[pg.K_UP]:
            #self.counter = self.counter_speed
            self.y -= self.speed
        
        if keys[pg.K_DOWN]:
            #self.counter = self.counter_speed
            self.y += self.speed
                    
        if self.x < 0:
            self.x = 0
        elif self.x > var.scene_width - var.screen_width:
            self.x = var.scene_width - var.screen_width
        if self.y < 0:
            self.y = 0
        elif self.y > var.scene_height - var.screen_height:
            self.y = var.scene_height - var.screen_height
        

        #if self.counter > 0:
        #    self.counter -= 1