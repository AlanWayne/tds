import classes
import var
import random

# create object
def create_entity(x, y, type, list, N, screen):
    for a in range(N):
        # wanderer
        if type == classes.Wanderer:
            object = classes.Wanderer(x,y,x,y,screen)
            var.list_wanderer.append(object)
        # food
        if type == classes.Food:
            object = classes.Food(x,y,screen)
            var.list_food.append(object)
    return object

# init behaviot
def init_behavior(object):
    
    # ======== wanderer ========
    
    if type(object) == classes.Wanderer:
        
        # check age
        if object.child == True and object.age > (var.FPS * var.day_lenght):
            object.grow()
        object.age += 1
        
        # actions
        object.search_food()
        object.move()
        
        # hunger
        object.hunger -= min(object.hunger,(1/var.FPS) * (1440/var.day_lenght))
        if object.delay_breed > 0:
            object.delay_breed -= 1
        if object.hunger > (object.hunger_full + object.hunger_one):
            object.hunger = object.hunger_full
            
        # breed
        if object.hunger > var.FPS * 16:
            if object.delay_breed == 0:
                create_entity(object.x,object.y,classes.Wanderer,var.list_wanderer,1,object.scr)
                object.delay_breed += var.FPS * var.day_lenght
                object.hunger -= var.FPS * 8
               
        # death
        if object.hunger <= 0:
            var.list_wanderer.remove(object)
            object.death()
            
        # display
        object.draw() 
    
    # ======== food ========
    
    if type(object) == classes.Food:
        if object.alive:
            object.collizion(var.list_wanderer)
            object.draw()
        else:
            var.list_food.remove(object)