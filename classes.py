from doctest import master
from re import X
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
        # name
    name = 'rabbit'
        # position
    x = 0
    y = 0
        # speed
    spd0 = 30 / var.FPS
    spd = spd0
        #size
    height = 14
    width = 16
        # age
    age = 0
        # sight
    sight = 250
        # target
    target_x = 0
    target_y = 0
    
    frame = 0
        # sprite speed
    sprite_counter = 0
    sprite_speed0 = 20
    sprite_speed = spd * sprite_speed0
    sprite = sprite.spr_rabbit_walk[frame]
    x_axis = random.choice(['Left','Right'])
    depth = 0
    moving = False
    shadow = None
    
    hunger_full = var.FPS * 16
    hunger = hunger_full
    hunger_one = var.FPS * 4
    hunger_child = False
    
    sleep_full = var.FPS * var.day_lenght * 0.75
    sleep = sleep_full
    
    schedule = []
    state_time = ''
    state = ''
    
    child = True
    parent_f = None
    parent_m = None
    children = []
    delay_breed = var.FPS * var.day_lenght
    
    sex = ''
    partner = None
    
    def __init__(
        self, 
        x, 
        y, 
    ):
        self.x = x
        self.y = y
        
        self.hunger = self.hunger_full / 2 + random.randint(-self.hunger_full/5,self.hunger_full/5)
        self.sleep = self.sleep_full / 2 + random.randint(-self.sleep_full/5,self.sleep_full/5)
        
        self.schedule = []
        for a in range(10):
            self.schedule.append(random.choice(var.obj_state_wanderer))
            
        self.children = []
        self.sprite = pg.transform.scale(self.sprite,(self.width,self.height))
        
        self.sex = random.choice(['male','female'])
                
    # set the coordinates
    def set_xy(self,x,y):
        self.x += x
        self.y += y
        
    # drawing
    def draw(self,screen):
        if self.x > var.obj_camera.x and self.x < (var.obj_camera.x + var.screen_width) and self.y > var.obj_camera.y and self.y < (var.obj_camera.y + var.screen_height):
        
            # sleep
            if self.state == 'sleep':
                self.sprite_counter += self.sprite_speed
                
                if self.sprite_counter >= var.FPS:
                    self.sprite_counter = 0
                    self.frame += 1
                
                if self.frame >= len(sprite.spr_rabbit_z):
                    self.frame = 0
                    
                self.sprite = sprite.spr_rabbit_sleep[0]
                self.sprite = pg.transform.scale(self.sprite,(self.width,self.height))
            
            # stand
            elif self.moving == False:
                self.frame = 0
                self.sprite_counter = 0
            
                self.sprite = sprite.spr_rabbit_walk[self.frame]
                self.sprite = pg.transform.scale(self.sprite,(self.width,self.height))
            
            # walk
            elif self.moving == True:
                self.sprite_counter += self.sprite_speed
                
                if self.sprite_counter >= var.FPS:
                    self.sprite_counter = 0
                    self.frame += 1
                    
                if self.frame >= len(sprite.spr_rabbit_walk):
                    self.frame = 0
                    
                self.sprite = sprite.spr_rabbit_walk[self.frame]
                self.sprite = pg.transform.scale(self.sprite,(self.width,self.height))
            
            # rotation      
            if self.x_axis == 'Left':
                screen.blit(self.sprite, (self.x - self.width/2 - var.obj_camera.x, self.y - self.height - var.obj_camera.y))
                if self.state == 'sleep':
                    screen.blit(pg.transform.scale2x(sprite.spr_rabbit_z[self.frame]),(self.x - self.width/2 - var.obj_camera.x, self.y - self.height * 2 - var.obj_camera.y))
            if self.x_axis == 'Right':
                screen.blit((pg.transform.flip(self.sprite, True, False)), ((self.x - self.width/2) - var.obj_camera.x, (self.y - self.height) - var.obj_camera.y))
                if self.state == 'sleep':
                    screen.blit(pg.transform.scale2x(sprite.spr_rabbit_z[self.frame]),(self.x - var.obj_camera.x, self.y - self.height * 2 - var.obj_camera.y))
        
    # get depth
    def get_depth(self):
        self.depth = self.y
        return self.y
        
    # action
    def action(self):     
        
        # check state
        
        if self.hunger_child == True:
            self.feed()
            self.state = 'feed'
            
        elif ((self.sleep < self.sleep_full/8 or (self.state == 'sleep' and self.sleep < self.sleep_full))) and self.hunger > self.hunger_full/8:
            self.go_sleep()
        
        elif self.hunger < (self.hunger_full - self.hunger_one) or self.hunger_child == True:
            self.search_food()
            self.state = 'food'
        
        elif self.delay_breed == 0:
            self.breed()
            self.state = 'breed'
        
        else:
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
        if self.hunger <= 0 or self.age > (5 * var.day_lenght * var.FPS):
            if self.parent_f != None:
                self.parent_f.children.remove(self)
            if self.parent_m != None:
                self.parent_m.children.remove(self)
            for ch in self.children:
                if self.sex == 'female':
                    ch.parent_f = None
                elif self.sex == 'male':
                    ch.parent_m = None
            self.death()
            var.deaths += 1
            
        # sleepness
        if self.sleep > 0:
            self.spd = self.spd0
            self.sprite_speed = self.sprite_speed0
        else:
            self.spd = self.spd0 / 2
            self.sprite_speed = self.sprite_speed0 / 2
            
        # move
        self.move()
            
            
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
                    if self.parent_f != None:
                        self.target_x = self.parent_f.x + random.choice([-1,1]) * random.randint(25,50)
                        self.target_y = self.parent_f.y + random.choice([-1,1]) * random.randint(25,50)
                    elif self.parent_m != None:
                        self.target_x = self.parent_m.x + random.choice([-1,1]) * random.randint(25,50)
                        self.target_y = self.parent_m.y + random.choice([-1,1]) * random.randint(25,50)
                    else:
                        self.target_x += random.choice([-1,1]) * random.randint(25,50)
                        self.target_y += random.choice([-1,1]) * random.randint(25,50)
                        
    # check for orphans    
    def orphan(self):
        if self.child == False:
            for obj in var.list_wanderer:
                if (obj.child == True) and (obj.parent_f == None) and (obj.parent_m == None) and (fm.distance_to_object(self,obj) < self.sight):
                    if self.sex == 'male':
                        obj.parent_m = self
                    elif self.sex == 'female':
                        obj.parent_f = self
                    self.children.append(obj)
    
    # set target to exact object        
    def chase(self, object):
        self.target_x = object.x
        self.target_y = object.y
    
    # scan area for food    
    def search_food(self):
        if self.hunger < self.hunger_full:
            if self.child == True and self.parent_f != None and self.hunger < self.hunger_full/2:
                self.target_x = self.parent_f.x
                self.target_y = self.parent_f.y
                self.parent_f.hunger_child = True
            elif self.child == True and self.parent_m != None and self.hunger < self.hunger_full/2:
                self.target_x = self.parent_m.x
                self.target_y = self.parent_m.y
                self.parent_m.hunger_child = True
            else:
                t = fo.find_nearest_to_object(self,var.list_food)
                if fm.distance_to_object(self,t) < self.sight and t != self:
                    self.chase(t)
                else:
                    self.wander()
        else:
            self.wander()
            
    # feed the child
    def feed(self):
        if self.sex == 'female' or (self.sex == 'male' and self.partner == None):
            if len(self.children) > 0:
                for ch in self.children:
                    if ch.hunger < self.hunger:
                        if self.hunger > self.hunger_one * 2:
                            if fm.distance_to_object(self,ch) < 32:
                                self.hunger -= self.hunger_one
                                ch.hunger += ch.hunger_one
                                self.hunger_child = False
                            else:
                                self.target_x = ch.x
                                self.target_y = ch.y
                        else:
                            self.search_food()
                            self.state = 'food'
                    else:
                        self.search_food()
                        self.state = 'food'
            else:
                self.search_food()
                self.state = 'food'
        else:
            self.search_food()
            self.state = 'food'

    # sleep
    def go_sleep(self):
        if self.state != 'sleep':
            if self.parent_f != None:
                if fm.distance_to_object(self,self.parent_f) < 64:
                    self.state = 'sleep'
                    self.target_x = self.x
                    self.target_y = self.y
                else:
                    self.target_x = self.parent_f.x
                    self.target_y = self.parent_f.y
            elif self.parent_m != None:
                if fm.distance_to_object(self,self.parent_m) < 64:
                    self.state = 'sleep'
                    self.target_x = self.x
                    self.target_y = self.y
                else:
                    self.target_x = self.parent_m.x
                    self.target_y = self.parent_m.y
            elif self.partner != None:
                if fm.distance_to_object(self,self.partner) < 64:
                    self.state = 'sleep'
                    self.target_x = self.x
                    self.target_y = self.y
                else:
                    self.target_x = self.partner.x
                    self.target_y = self.partner.y
            else:
                    self.state = 'sleep'
                    self.target_x = self.x
                    self.target_y = self.y
             
    # breed
    def breed(self):
        if self.sex == 'male':
            if self.partner == None:
                check_p = []
                for cp in var.list_wanderer:
                    if cp.sex == 'female':
                        if cp.child == False: 
                            if cp.partner == None:
                                check_p.append(cp)
                cp1 = fo.find_nearest_brother(self,check_p)
                if cp1 != None:
                    self.partner = cp1
                    cp1.partner = self
            else:
                if fm.distance_to_object(self,self.partner) > 32:
                    self.target_x = self.partner.x
                    self.target_y = self.partner.y
        if self.sex == 'female':
            if self.partner != None:
                if fm.distance_to_object(self,self.partner) > 32:
                    self.target_x = self.partner.x
                    self.target_y = self.partner.y
                else:
                    ch = fo.create_entity((self.x + self.partner.x)/2,(self.y + self.partner.y)/2,Wanderer,None)
                    ch.parent_f = self
                    ch.parent_m = self.partner
                    self.children.append(ch)
                    self.partner.children.append(ch)
                    self.delay_breed += var.FPS * var.day_lenght / 3
                    self.partner.delay_breed +=var.FPS * var.day_lenght / 3
                    self.hunger -= self.hunger_full / 2
                    self.partner.hunger -= self.hunger_full / 2
            else:
                self.wander()
                
    # death       
    def death(self):
        #fo.create_entity(self.x,self.y,Food,var.list_food,None)
        var.deaths += 1
        var.list_wanderer.remove(self)
        self.shadow.master = None
        del self
                  
    # grow up
    def grow(self):
        self.height *= 2
        self.width *= 2
        self.spd0 *= 2
        self.sight *= 2
        self.child = False
        self.parent_f = None
        self.parent_m = None
        self.sprite = pg.transform.scale(self.sprite,(self.width,self.height))
          
# ================================ food ================================

class Food:
    height = 32
    width = 32
    depth = 0
    sprite0 = random.choice(sprite.spr_carrot)
    shadow = None
        
    def __init__(
        self, 
        x, 
        y,
    ):
        self.x = x
        self.y = y
        self.depth = self.y
        self.sprite0 = random.choice(sprite.spr_carrot)

    # draw
    def draw(self,screen):
        if self.x > var.obj_camera.x and self.x < (var.obj_camera.x + var.screen_width) and self.y > var.obj_camera.y and self.y < (var.obj_camera.y + var.screen_height):
            screen.blit(pg.transform.scale(self.sprite0,(self.height,self.width)), (self.x - self.width/2 - var.obj_camera.x, self.y - self.height - var.obj_camera.y))
        
    # get depth
    def get_depth(self):
        self.depth = self.y
        return self.y
        
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
        self.shadow.master = None
        fo.create_entity(random.randint(0, var.scene_width), random.randint(0, var.scene_height),Food,None)        
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
                if self.master.state == 'sleep':
                    frame = 1
                else: 
                    frame = self.master.frame
                self.sprite0 = sprite.spr_shadow_rabbit[frame]
                if self.master.child == False:
                    self.sprite0 = pg.transform.scale2x(self.sprite0) #(self.sprite0,(36,16))
            elif type(self.master) == Food:
                self.sprite0 = pg.transform.scale2x(sprite.spr_shadow_carrot[0])
        else:
            var.list_shadow.remove(self)
            del self
            
    def draw(self,screen):
        if self.x > var.obj_camera.x and self.x < (var.obj_camera.x + var.screen_width) and self.y > var.obj_camera.y and self.y < (var.obj_camera.y + var.screen_height):
            if screen != None and self.sprite0 != None:
                screen.blit(self.sprite0, (self.x - self.sprite0.get_width()/2 - var.obj_camera.x , self.y - self.sprite0.get_height()/2 - var.obj_camera.y - 2))
            
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

    drag = False
    drag_x = 0
    drag_y = 0
    drag_mx = 0
    drag_my = 0
    
    speed = 16
    #counter_speed = var.FPS / 30
    #counter = 0
    
    def __init__(self):
        self.x = var.scene_width / 2 - var.screen_width / 2
        self.y = var.scene_height / 2 - var.screen_height / 2
    
    def action(self):      
        # arrows control
        key0 = pg.key.get_pressed()
        
        if key0[pg.K_LEFT]:
            #self.counter = self.counter_speed
            self.x -= self.speed
        
        if key0[pg.K_RIGHT]:
            #self.counter = self.counter_speed
            self.x += self.speed
                    
        if key0[pg.K_UP]:
            #self.counter = self.counter_speed
            self.y -= self.speed
        
        if key0[pg.K_DOWN]:
            #self.counter = self.counter_speed
            self.y += self.speed
                    
        # mouse control
        mouse0 = pg.mouse.get_pressed()
        
        if mouse0[2]:
            mx, my = pg.mouse.get_pos()
            self.x = self.drag_x - (mx - self.drag_mx)
            self.y = self.drag_y - (my - self.drag_my)
        else:
            self.drag_x = self.x
            self.drag_y = self.y
            mx, my = pg.mouse.get_pos()
            self.drag_mx = mx
            self.drag_my = my
            
        # borders            
        if self.x < 0:
            self.x = 0
        elif self.x > var.scene_width - var.screen_width:
            self.x = var.scene_width - var.screen_width
        if self.y < 0:
            self.y = 0
        elif self.y > var.scene_height - var.screen_height:
            self.y = var.scene_height - var.screen_height
        
# ================================ background ================================
class Background:
    sprite = None
    x = 0
    y = 0
    
    def __init__(self,x,y):
        self.sprite = random.choice(sprite.spr_bg_grass)
        self.x = x * 64
        self.y = y * 64
        #self.width = self.sprite.get_width()
        
    def draw(self,screen):
        if self.x > var.obj_camera.x - 64 and self.x < (var.obj_camera.x + var.screen_width) and self.y > var.obj_camera.y - 64 and self.y < (var.obj_camera.y + var.screen_height):
            screen.blit(pg.transform.scale2x(self.sprite),(self.x - var.obj_camera.x,self.y - var.obj_camera.y))