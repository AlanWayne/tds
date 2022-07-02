import classes
import var
import random
import func_math as fm
import pygame as pg

# create object
def create_entity(x, y, type, parent):
    # wanderer
    if type == classes.Wanderer:
        object = classes.Wanderer(x,y)
        var.list_wanderer.append(object)
        object.shadow = create_entity(x,y,classes.Shadow,object)
    # food
    if type == classes.Food:
        object = classes.Food(x,y)
        var.list_food.append(object)
    # shadow
    if type == classes.Shadow:
        object = classes.Shadow(parent)
        var.list_shadow.append(object)
    # camera
    if type == classes.Camera:
        object = classes.Camera()
        var.obj_camera = object
    
    return object

# find nearest object in list - to object
def find_nearest_to_object(a,list):
    d = a
    for b in list:
        if d == a:
            d = b
        if fm.distance_to_object(a,b) < fm.distance_to_object(a,d):
            d = b
    return d

#find nearest object in list - to point
def find_nearest_to_point(x,y,list):
    d = None
    for b in list:
        if d == None:
            d = b
        if fm.distance_to_point(b,x,y) < fm.distance_to_point(d,x,y):
            d = b
    return d

#find nearest object in list - to point
def find_nearest_to_mouse(list):
    d = None
    for b in list:
        mx, my = pg.mouse.get_pos()
        if d == None:
            d = b
        if fm.distance_between(b.x - var.obj_camera.x,b.y - var.obj_camera.y,mx,my) < fm.distance_between(d.x - var.obj_camera.x,d.y - var.obj_camera.y,mx,my):
            d = b
    return d

# find nearest object in list - to object (exclude self)
def find_nearest_brother(a,list):
    d = a
    for b in list:
        if b != a:
            if d == a:
                d = b
            if fm.distance_to_object(a,b) < fm.distance_to_object(a,d):
                d = b
    if d == a:
        return 0
    else:
        return d