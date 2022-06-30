import pygame as pg 
import random
import var
import func_math as fm
import func_objects as fo

class Wanderer:    
    
    hunger = var.FPS * 8
    hunger_full = var.FPS * 16
    hunger_one = var.FPS * 8
    
    sleep = var.FPS * var.day_lenght * 0.75
    sleep_full = var.FPS * var.day_lenght * 0.75
    
    delay_breed = var.FPS * var.day_lenght
    spd = 60 / var.FPS
    size = 5
    age = 0
    sight = 120
    child = True
    
    schedule = []
    state = ''
    
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
    
    # set the coordinates
    def set_xy(self,x,y):
        self.x += x
        self.y += y
        
    # drawing
    def draw(self):
        pg.draw.circle(self.scr, (255 - min(self.hunger * 0.255, 255), 100, min(self.hunger * 0.255,255)), (self.x, self.y), self.size)
    
    def action_1(self):
        self.state = self.schedule[round(var.total_counter * 10 / var.day_lenght) - 1]
                
    def action_2(self):
        if self.state == 'breed':
            self.wander()
        if self.state == 'food':
            self.search_food()
        if self.state == 'sleep':
            self.go_sleep()
        if self.state == 'wander':
            self.wander()
        
    # movement
    def move(self):
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
                self.target_x += random.choice([-1,1]) * random.randint(25,50)
                self.target_y += random.choice([-1,1]) * random.randint(25,50)
    
    # set target to exact object        
    def chase(self, object):
        self.target_x = object.x
        self.target_y = object.y
    
    # scan area for food    
    def search_food(self):
        if self.hunger < self.hunger_full:
            t = fm.find_nearest(self,var.list_food)
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
            
    # death       
    def death(self):
        fo.create_entity(self.x,self.y,Food,var.list_food,1,self.scr)
        del self
                  
    # grow up
    def grow(self):
        self.size *= 2
        self.spd *= 2
        self.sight *= 2
        self.child = False
                    
              
            
class Food:
    alive = True    
    def __init__(
        self, 
        x, 
        y,
        scr
    ):
        self.x = x
        self.y = y
        self.scr = scr

    def draw(self):
        pg.draw.circle(self.scr, (200, 150, 50), (self.x, self.y), 5)
        
    def collizion(self,list_wanderer):
        for wanderer in list_wanderer:
            if fm.distance_to_object(self,wanderer) < 10 and wanderer.hunger < 1000:
                wanderer.hunger += wanderer.hunger_one
                self.alive = False
                del self
                break
        