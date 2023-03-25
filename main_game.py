import os, sys, random, time, pygame
from pygame.locals import*
from blocks import*
#方塊下降速度
brick_normal = 0.01
brick_fast   = 0.5
#視窗大小
canvas_h = 600
canvas_w = 800

#block底色
color_black       =(0,0,0)
color_white       =(255,255,255)
color_red         =(255,0,0)
color_gray        = (107,130,114)
color_gray_black  = (20,31,23)
color_gray_green  = (0, 255, 0)
color_light_gray  = (200, 200, 200)

#block顏色
box_color_orange      =(204,102,51)
box_color_purple      =(153,90,211)
box_color_blue        =(51,102,204)
box_color_light_red   =(204,51,51)
box_color_light_blue  =(51,204,255)
box_color_yellow      =(204,204,51)
box_color_green       =(51,153,102)

#定義磚塊
block_dict = {
    "10": ( 4, 8, 9,13), "11": ( 9,10,12,13),   # z1.
    "20": ( 5, 8, 9,12), "21": ( 8, 9,13,14),   # z2.
    "30": ( 8,12,13,14), "31": ( 4, 5, 8,12), "32": (8,  9, 10, 14), "33": (5,  9, 12, 13), # L1.
    "40": (10,12,13,14), "41": ( 4, 8,12,13), "42": (8,  9, 10, 12), "43": (4,  5,  9, 13), # L2.
    "50": ( 9,12,13,14), "51": ( 4, 8, 9,12), "52": (8,  9, 10, 13), "53": (5,  8,  9, 13), # T.
    "60": ( 8, 9,12,13),    # 方形方塊.
    "70": (12,13,14,15), "71": ( 1, 5, 9,13)    #條狀方塊.
    

}
