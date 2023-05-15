import os, sys, random, time, pygame
from pygame.locals import*
from blocks import*
#方塊下降速度
block_normal = 0.01
block_fast   = 0.5
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
# 設定字型-黑體.
font = pygame.font.SysFont("simsunnsimsun", 24)

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
    p_block = getBlockIndex(blockId, state)
    
    # 轉換方塊到方塊陣列.
    for i in range(4):        
        bx = int(p_block[i] % 4)
        by = int(p_block[i] / 4)
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
#-------------------------------------------------------------------------
# 複製方塊到容器內.
#-------------------------------------------------------------------------
def copyToBlockArray():
    global blocks, blocks_array
    global container_x, container_y

    posX = 0
    posY = 0
    for x in range(4):
        for y in range(4):
            if (blocks[x][y] !=0):
                posX = container_x + x
                posY = container_y + y
                if (posX >= 0 and posY >= 0):
                    blocks_array[posX][posY] = blocks[x][y]
#------------------------------------------------------------------------
#遊戲初始階段
#------------------------------------------------------------------------
def resetGame():
    global block_fast
    global blocks_array, blocks, lines_number, lines_number_max

    # 清除磚塊陣列.
    for x in range(10):
        for y in range(20):
            blocks_array[x][y] = 0
            
    # 清除方塊陣列.
    for x in range(4):
        for y in range(4):
            blocks[x][y] = 0

    # 初始磚塊下降速度.
    brick_down_speed = block_fast

    # 最大連線數.
    if(lines_number > lines_number_max):
        lines_number_max = lines_number
    # 連線數.
    lines_number = 0

#---------------------------------------------------------------------------
# 判斷與設定要清除的方塊.
# 傳出:
#   連線數
#---------------------------------------------------------------------------
def ifClearBrick():
    pointNum = 0
    lineNum = 0
    for y in range(20):
        for x in range(10):
            if (blocks_array[x][y] > 0):
                pointNum = pointNum + 1
            if (pointNum == 10):
                for i in range(10):
                    lineNum = lineNum + 1
                    blocks_array[i][y] = 9
        pointNum = 0
    return lineNum
#-------------------------------------------------------------------------
# 更新下一個磚塊.
#-------------------------------------------------------------------------
def updateNextBricks(brickId):
    global blocks_next
    
    # 清除方塊陣列.
    for y in range(4):
        for x in range(4):
            blocks_next[x][y] = 0

    # 取得磚塊索引陣列.
    pBrick = getBlockIndex(brickId, 0)

    # 轉換方塊到方塊陣列.
    for i in range(4):
        bx = int(pBrick[i] % 4)
        by = int(pBrick[i] / 4)
        blocks_next[bx][by] = brickId

    # ColorVer:設定背景顏色.
    background_blocks_next.color = color_black

    # 更新背景區塊.
    background_blocks_next.update()

    # 更新磚塊圖.
    pos_y = 52
    for y in range(4):
        pos_x = 592
        for x in range(4):
            if(blocks_next[x][y] != 0):
                blocks_next_shape[x][y].rect[0] = pos_x
                blocks_next_shape[x][y].rect[1] = pos_y

                # ColorVer:依照方塊編號設定顏色.
                if (blocks_next[x][y]==1):
                    blocks_next_shape[x][y].color = box_color_orange
                elif (blocks_next[x][y]==2):
                    blocks_next_shape[x][y].color = box_color_purple
                elif (blocks_next[x][y]==3):
                    blocks_next_shape[x][y].color = box_color_blue
                elif (blocks_next[x][y]==4):
                    blocks_next_shape[x][y].color = box_color_light_red
                elif (blocks_next[x][y]==5):
                    blocks_next_shape[x][y].color = box_color_light_blue
                elif (blocks_next[x][y]==6):
                    blocks_next_shape[x][y].color = box_color_yellow
                elif (blocks_next[x][y]==7):
                    blocks_next_shape[x][y].color = box_color_green
                elif (blocks_next[x][y]==9):
                    blocks_next_shape[x][y].color = color_white

                blocks_next_shape[x][y].update()
            pos_x = pos_x + 28        
        pos_y = pos_y + 28
#-------------------------------------------------------------------------
# 初始.
pygame.init()
# 顯示Title.
pygame.display.set_caption(u"俄羅斯方塊遊戲")
# 建立畫佈大小.
# 全螢幕模式.
canvas = pygame.display.set_mode((canvas_w, canvas_h), pygame.DOUBLEBUF and pygame.FULLSCREEN )
# 視窗模式.
#canvas = pygame.display.set_mode((canvas_width, canvas_height))

# 時脈.
clock = pygame.time.Clock()

# 查看系統支持那些字體
#print(pygame.font.get_fonts())




# 將繪圖方塊放入陣列.
for y in range(20):
    for x in range(10):
        blocks_list[x][y] = Block(pygame, canvas, "brick_x_" + str(x) + "_y_" + str(y), [ 0, 0, 26, 26], color_gray_black)

# 將繪圖方塊放入陣列.
for y in range(4):
    for x in range(4):
        blocks_next_shape[x][y] = Block(pygame, canvas, "brick_next_x_" + str(x) + "_y_" + str(y), [ 0, 0, 26, 26], color_gray_black)

# 背景區塊.
background = Block(pygame, canvas, "background", [ 278, 18, 282, 562], color_gray)

# 背景區塊.
background_blocks_next = Block(pygame, canvas, "background_bricks_next", [ 590, 50, 114, 114], color_gray)
#---------------------------------------------------------------------------------------------------------
# 產生新磚塊.
#---------------------------------------------------------------------------------------------------------
def New_block():
    global game_over,container_x,container_y,block_next_id,block_state,blocks_next_shape,blocks_next
    global lines_number,game_mode
    


# 判斷遊戲結束.
    game_over=False
    if (container_y<0):
        game_over=True
        resetGame()
# 複製方塊到容器內.
    container_y=container_y-1
    copyToBlockArray()

# 判斷與設定要清除的方塊.
    lines = ifClearBrick() / 10;
    if (lines>0):
        lines_number=lines_number+lines
        # 消除連線數量累加.
        game_mode =1   #1.消除磚塊

#初始的方塊位置
    container_x=3
    container_y=4
# 現在出現方塊.
    blocks_id=block_next_id
    #下一個出現的方塊
    block_next_id=random.randint(1,7)
    #方塊初始狀態
    block_state=0
#---------------------------------------------------------------------------------------------------------
# 清除的方塊.
#---------------------------------------------------------------------------------------------------------
def clear_block():
    global blocks_array


    cube=0
    for x in range(10):
        for i in range(19):
            for y in range(20):
                if(blocks_array[x][y]==9):
                    if(y>0):
                        cube=blocks_array[x][y-1]
                        y=y-1
#---------------------------------------------------------------------------------------------------------    
# 主迴圈.
#---------------------------------------------------------------------------------------------------------
starting = True
time_temp = time.time() 
time_now = 0

# 計算時脈.
while starting:
    time_now = time_now + (time_temp - time.time())
    time_temp = time.time()
    
    #---------------------------------------------------------------------
    # 判斷輸入.
    #---------------------------------------------------------------------
    for keyboard in pygame.event.get():

    # 離開遊戲.
        if keyboard.type == pygame.QUIT:
            starting =False
    # 判斷按下按鈕
        if keyboard.type == pygame.KEYDOWN:

        # 判斷按下ESC按鈕
            if keyboard.type == pygame.K_ESCAPE:
                starting = False

        # 除錯訊息開關.
            elif keyboard.type == pygame.K_d:
                debug_message ==  False
        #-----------------------------------------------------------------
        # 變換方塊-上.
            elif keyboard.type == pygame.K_UP and game_mode == 0:
            # 在右邊界不能旋轉.
                if (container_x == 8):
                    break
            # 判斷磚塊N1、N2、I
                if (block_id == 1 or block_id == 2 or block_id == 7):
               #長條方塊在邊界不能旋轉
                        if (block_id == 7):
                            if (container_x<0 or container_x == 7):
                                break
               #旋轉方塊
                brick_state = brick_state + 1
                if (brick_state > 1):
                    brick_state = 0 
               #轉換要出現的方塊到方塊陣列
                transformToBlocks(block_id, brick_state)
               #碰到方塊
