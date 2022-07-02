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