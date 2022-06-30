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
        
        # check children
        for ch in object.children:
            if ch.child == False:
                object.children.remove(ch)
        
        # actions
        object.action()
        object.move()
        
        # hunger
        object.hunger -= min(object.hunger,(1/var.FPS) * (1440/var.day_lenght))
        if object.delay_breed > 0:
            object.delay_breed -= 1
        if object.hunger > (object.hunger_full + object.hunger_one):
            object.hunger = object.hunger_full
            
        # sleep
        if object.state == 'sleep':
            object.sleep += 3
        else:
            object.sleep -= 1         
               
        # death
        if object.hunger <= 0 or object.sleep <= 0 or object.age > (5 * var.day_lenght * var.FPS):
            var.list_wanderer.remove(object)
            if object.parent != None:
                object.parent.children.remove(object)
            for ch in object.children:
                ch.parent = None
            object.death()
            var.deaths += 1
    
    # ======== food ========
    
    if type(object) == classes.Food:
        if object.alive:
            object.collizion(var.list_wanderer)
        else:
            var.list_food.remove(object)