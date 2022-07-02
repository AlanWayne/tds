import pygame as pg

# health bar

def health_bar(screen,x,y,width,height,value,max_value,color_empty,color_full):
    pg.draw.rect(screen,(0,0,0),((x - width/2 - 2,y - height - 2),(width + 4,width/6 + 4)),0)
    V = min(value / max_value,1)
    C = pg.Color(
        int(round(color_full[0] * V + color_empty[0] * (1 - V))),
        int(round(color_full[1] * V + color_empty[1] * (1 - V))),
        int(round(color_full[2] * V + color_empty[2] * (1 - V)))
    )
    pg.draw.rect(screen,C,((x - width/2,y - height),(width * V,width/6)),0)
    