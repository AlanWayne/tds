import pygame as pg 
import random
import var
import func_math as fm
import func_objects as fo
import sprite

class Wanderer:    
    # stats
    frame = 0
    sprite_counter = 0
    sprite_speed = round(var.FPS / 10)
    sprite = sprite.spr_rabbit_walk[frame]
    x_axis = random.choice(['Left','Right'])
    depth = 0
    moving = False
    
    spd = 30 / var.FPS
    height = 14
    width = 16
    age = 0
    sight = 120
    
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
        target_x, 
        target_y, 
        scr
    ):
        self.x = x
        self.y = y
        
        self.target_x = target_x
        self.target_y = target_y
        
        self.scr = scr
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
    def draw(self):
        if self.moving == False:
            self.sprite = sprite.spr_rabbit_walk[0]
            self.sprite_counter = 0
        elif self.moving == True:
            if self.sprite_counter == 0:
                self.frame += 1
                if self.frame >= len(sprite.spr_rabbit_walk):
                    self.frame = 0
                self.sprite = sprite.spr_rabbit_walk[self.frame]
            self.sprite_counter += 1
            if self.sprite_counter == self.sprite_speed:
                self.sprite_counter = 0
                    
        if self.x_axis == 'Left':
            if self.child == True:
                self.scr.blit(self.sprite, (self.x - self.width/2, self.y - self.height))
            else:
                self.scr.blit(pg.transform.scale2x(self.sprite), (self.x - self.width/2, self.y - self.height))
        elif self.x_axis == 'Right':
            if self.child == True:
                self.scr.blit(pg.transform.flip(self.sprite, True, False), (self.x - self.width/2, self.y - self.height))
            else:
                self.scr.blit(pg.transform.scale2x(pg.transform.flip(self.sprite, True, False)), (self.x - self.width/2, self.y - self.height))
        
    # get depth
    def get_depth(self):
        self.depth = self.y
        return self.depth
        
    # action
    def action(self):
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
        
    # movement
    def move(self):
        if self.target_x < self.x:
            self.x_axis = 'Left'
            self.moving = True
        elif self.target_x > self.x:
            self.x_axis = 'Right'
            self.moving = True
        else:
            self.moving = False
        
        if self.target_x < 0 or self.target_x > var.screen_width:
            self.target_x = self.x
            
        if self.target_y < 0 or self.target_y > var.screen_height:
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
        nb = fm.find_nearest_brother(self,var.list_wanderer)
        if nb != 0:
            dtp = fm.distance_to_point(nb, self.x, self.y)
            if dtp < 20:
                dx, dy = fm.relative_velocity(self.x, self.y, nb.x, nb.y)
                if self.x < nb.x:
                    self.x -= (20 - dtp) * dx
                if self.x > nb.x:
                    self.x += (20 - dtp) * dx
                if self.y < nb.y:
                    self.y -= (20 - dtp) * dy
                if self.y > nb.y:
                    self.y += (20 - dtp) * dy
    
    # set target to the random point
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
    
    # set target to exact object        
    def chase(self, object):
        self.target_x = object.x
        self.target_y = object.y
    
    # scan area for food    
    def search_food(self):
        if self.hunger < self.hunger_full:
            t = fm.find_nearest_to_object(self,var.list_food)
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
                child0 = fo.create_entity(self.x,self.y,Wanderer,var.list_wanderer,1,self.scr)
                child0.schedule = self.schedule
                child0.parent = self
                self.children.append(child0)
                self.delay_breed += var.FPS * var.day_lenght / 3
                self.hunger -= var.FPS * 8
    
    # death       
    def death(self):
        fo.create_entity(self.x,self.y,Food,var.list_food,1,self.scr)
        del self
                  
    # grow up
    def grow(self):
        self.height *= 2
        self.width *= 2
        self.spd *= 2
        self.sight *= 2
        self.child = False
        self.parent = None
                    
              
            
class Food:
    alive = True    
    height = 16
    width = 10
    depth = 0
        
    def __init__(
        self, 
        x, 
        y,
        scr
    ):
        self.x = x
        self.y = y
        self.scr = scr
        self.depth = self.y

    def draw(self):
        #pg.draw.circle(self.scr, (200, 150, 50), (self.x, self.y), 5)
        self.scr.blit(sprite.spr_carrot, (self.x - self.width/2, self.y - self.height))
        
    # get depth
    def get_depth(self):
        self.depth = self.y
        return self.depth
        
    def collizion(self,list_wanderer):
        for wanderer in list_wanderer:
            if fm.distance_to_object(self,wanderer) < 10 and wanderer.hunger < 1000:
                wanderer.hunger += wanderer.hunger_one
                self.alive = False
                del self
                break
        