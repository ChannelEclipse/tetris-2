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
#10*20的方塊陣列(遊戲內主背景)
blocks_array = []
for i in range(10):
    blocks_array.append([0]*20)
#4*4的方塊矩陣(顯示方塊)
blocks = []
for i in range(4):
    blocks.append([0]*4)
#儲存下一個方塊的顏色
blocks_next = []
for i in range(4):
    blocks_next.append([0]*4)
#儲存下一個方塊的形狀
blocks_next_shape = []
for i in range(4):
    blocks_next_shape.append([0]*4)
#儲存地圖變異
blocks_list = []
for i in range(10):
    blocks_list.append([0]*20)

# 方塊在容器的位置.
# (-2~6)(  為6的時候不能旋轉方塊).
container_x = 3
# (-3~16)(-3表示在上邊界外慢慢往下掉).
container_y =-4

# 除錯訊息.
debug_message = False
# 判斷遊戲結束.
game_over = False

# 磚塊下降速度.
block_down_speed = block_fast

# 方塊編號(1~7).
block_id = 1
# 方塊狀態(0~3).
block_state = 0

# 下一個磚塊編號(1~7).
block_next_id = 1

# 最大連線數.
lines_number_max = 0
# 本場連線數.
lines_number = 0

# 遊戲狀態.
# 0:遊戲進行中.
# 1:清除磚塊.
game_mode = 0
# 函數:秀字.
# 傳入:
#   text    : 字串.
#   x, y    : 坐標.
#   color   : 顏色.
def showFont( text, x ,y, color):
    global canvas
    text = font.render(text, True, color) 
    canvas.blit( text, (x,y))
# 函數:取得磚塊索引陣列.
# 傳入:
#   brickId : 方塊編號(1~7).
#   state   : 方塊狀態(0~3).
def getBlockIndex( blockId, state):
    global block_dict
    # 組合字串.
    blockKey = str(blockId)+str(state)
    # 回傳方塊陣列.
    return block_dict[blockKey]
#-------------------------------------------------------------------------
# 轉換定義方塊到方塊陣列.
# 傳入:
#   brickId : 方塊編號(1~7).
#   state   : 方塊狀態(0~3).
#-------------------------------------------------------------------------
def transformToBlocks( blockId, state):
    global blocks

    # 清除方塊陣列.
    for x in range(4):
        for y in range(4):
            blocks[x][y] = 0
     
    # 取得磚塊索引陣列.
    p_brick = getBlockIndex(blockId, state)
    
    # 轉換方塊到方塊陣列.
    for i in range(4):        
        bx = int(p_brick[i] % 4)
        by = int(p_brick[i] / 4)
        blocks[bx][by] = blockId
#-------------------------------------------------------------------------
# 判斷是否可以複製到容器內.
# 傳出:
#   true    : 可以.
#   false   : 不可以.
#-------------------------------------------------------------------------
def ifCopyToBlocksArray():
    global blocks,blocks_array
    global container_x,container_y

    posX = 0
    posY = 0
    for x in range(4):
        for y in range(4):
           if (blocks[x][y] != 0):
                posX = container_x + x
                posY = container_y + y
                if (posX >= 0 and posY >= 0):
                    try:
                        if (blocks_array[posX][posY] != 0):
                            return False
                    except:
                        return False
    return True
