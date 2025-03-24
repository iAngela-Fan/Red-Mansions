import pygame
import os

# 顏色定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 100, 100)
BLUE = (100, 100, 200)
GREEN = (100, 200, 100)

# 視窗設定
WIDTH = 450
HEIGHT = 700
BUTTON_SIZE = 150
FPS = 60

# 字型
font_name = 'bubble.ttf'

# 全域變數
num = 1  # 當前人物索引
lit = 0  # 讀書會數值
lit_num = 0
mon = 0  # 財務管理數值
mon_num = 0
con = 0  # 導覽觀光數值
con_num = 0
scene = "init"  # 目前場景狀態

# 各角色數值表
lit_values = {1: 100, 2: 80, 3: 60, 4: 60, 5: 80, 6: 80, 7: 60, 8: 60, 9: 0, 10: 40, 11: 60, 12: 60}
con_values = {1: 60, 2: 80, 3: 80, 4: 60, 5: 60, 6: 0, 7: 40, 8: 40, 9: 40, 10: 80, 11: 60, 12: 80}
mon_values = {1: 0, 2: 60, 3: 40, 4: 80, 5: 40, 6: 40, 7: 40, 8: 40, 9: 100, 10: 40, 11: 60, 12: 40}

# 初始化 Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("賈府經營遊戲")
clock = pygame.time.Clock()

# 畫文字函式
def draw_text(surf, text, size, x, y, color=BLACK):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surf.blit(text_surface, text_rect)

# 按鈕函式
def draw_button(x, y, w, h, text, text_size, color, text_color):
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=10)
    draw_text(screen, text, text_size, x + w // 2, y + h // 2)
    
    mouse_x, mouse_y = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x <= mouse_x <= x + w and y <= mouse_y <= y + h:
        if click[0]:  # 左鍵點擊
            pygame.time.delay(150)  # 防止重複點擊
            return True
    return False

# 初始畫面
def draw_init():
    screen.fill(WHITE)
    draw_text(screen, "賈府經營遊戲", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "按空白鍵開始遊戲", 22, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.update()

# 介紹畫面
def draw_intro():
    screen.fill(WHITE)
    draw_text(screen, "你重生了，重生到賈府破敗前。", 32, WIDTH / 2, HEIGHT * 1 / 6)
    draw_text(screen, "這一世，你要拯救賈府", 32, WIDTH / 2, HEIGHT * 2 / 6)
    draw_text(screen, "請協助金陵十二釵們分派工作", 32, WIDTH / 2, HEIGHT * 3 / 6)
    draw_text(screen, "請注意他們的專長並平均分派", 32, WIDTH / 2, HEIGHT * 4 / 6)
    draw_text(screen, "按空白鍵進入遊戲", 22, WIDTH / 2, HEIGHT * 5 / 6)
    pygame.display.update()

# 遊戲畫面
def draw_scene():
    global num, lit, mon, con, scene, lit_num,con_num,mon_num
    
    if num > 12:
        scene = "result"
        return
    
    screen.fill(WHITE)
    
    pic = f"{num}.png"
    try:
        image = pygame.image.load(pic)
        image = pygame.transform.smoothscale(image, (400, 400))
    except pygame.error:
        image = pygame.Surface((400, 400))
        image.fill(WHITE)
    
    image_rect = image.get_rect(center=(WIDTH / 2, HEIGHT * 2 / 6))
    screen.blit(image, image_rect)
    
    if draw_button(50, 500, 100, 50, "讀書會", 24, RED, WHITE):
        lit += lit_values[num]
        lit_num+=1
        num += 1
    if draw_button(175, 500, 100, 50, "財務管理", 24, BLUE, WHITE):
        mon += mon_values[num]
        mon_num+=1
        num += 1
    if draw_button(300, 500, 100, 50, "導覽大觀園", 24, GREEN, WHITE):
        con += con_values[num]
        con_num+=1
        num += 1
    
    pygame.display.update()

# 結果畫面
def draw_result():
    screen.fill(WHITE)
    draw_text(screen, "遊戲結束！", 48, WIDTH / 2, HEIGHT / 4)
    culture = lit/lit_num
    money = mon/mon_num
    fame = con/con_num
    
    if culture>70:
        if money>70:
            if fame>60:
                draw_text(screen, "獲得了均衡發展", 22, WIDTH / 2, HEIGHT * 2.5 / 6)
                draw_text(screen, "成功復興賈府", 22, WIDTH / 2, HEIGHT * 3 / 6)
                draw_text(screen, "HAPPY ENDING", 32, WIDTH / 2, HEIGHT * 4 / 6, GREEN)
                draw_text(screen, "按空白鍵結束遊戲", 22, WIDTH / 2, HEIGHT * 5 / 6)
            elif fame<=60:
                draw_text(screen, "儘管成功賺取經費並提升文化素養", 22, WIDTH / 2, HEIGHT * 2 / 6)
                draw_text(screen, "但因為名聲受創仍難以逃脫抄家的命運", 22, WIDTH / 2, HEIGHT * 3 / 6)
                draw_text(screen, "BAD ENDING", 32, WIDTH / 2, HEIGHT * 4 / 6, RED)
                draw_text(screen, "按空白鍵結束遊戲", 22, WIDTH / 2, HEIGHT * 5 / 6)
        elif money<=70:
            if fame>60:  
                draw_text(screen, "儘管提升文化素養並獲得名聲", 22, WIDTH / 2, HEIGHT * 2.5 / 6)
                draw_text(screen, "但因為理財失當導致家族落寞", 22, WIDTH / 2, HEIGHT * 3 / 6)
                draw_text(screen, "BAD ENDING", 32, WIDTH / 2, HEIGHT * 4 / 6, RED)
                draw_text(screen, "按空白鍵結束遊戲", 22, WIDTH / 2, HEIGHT * 5 / 6)
            elif fame<=60:
                draw_text(screen, "儘管家族文化涵養得到提升", 22, WIDTH / 2, HEIGHT * 2.5 / 6)
                draw_text(screen, "但名聲受創且經濟狀況不佳而難逃原本命運", 22, WIDTH / 2, HEIGHT * 3 / 6)
                draw_text(screen, "BAD ENDING", 32, WIDTH / 2, HEIGHT * 4 / 6, RED)
                draw_text(screen, "按空白鍵結束遊戲", 22, WIDTH / 2, HEIGHT * 5 / 6)
    elif culture<=70:
        if money>70:
            if fame>60:
                draw_text(screen, "儘管已有足夠金錢與名聲", 22, WIDTH / 2, HEIGHT * 2.5 / 6)
                draw_text(screen, "但因為文化涵養不足而在後代逐漸落寞", 22, WIDTH / 2, HEIGHT * 3 / 6)
                draw_text(screen, "BAD ENDING", 32, WIDTH / 2, HEIGHT * 4 / 6, RED)
                draw_text(screen, "按空白鍵結束遊戲", 22, WIDTH / 2, HEIGHT * 5 / 6)
            elif fame<=64:
                draw_text(screen, "就算有了足夠金錢，但因為文化素養不足與名聲敗壞", 22, WIDTH / 2, HEIGHT * 2 / 6)
                draw_text(screen, "仍舊無法改變原本的命運", 22, WIDTH / 2,  HEIGHT * 3 / 6)
                draw_text(screen, "BAD ENDING", 32, WIDTH / 2, HEIGHT * 4 / 6, RED)
                draw_text(screen, "按空白鍵結束遊戲", 22, WIDTH / 2, HEIGHT * 5 / 6)
        elif money<=70:
            if fame>60:  
                draw_text(screen, "只有足夠的名聲", 22, WIDTH / 2, HEIGHT * 2.5 / 6)
                draw_text(screen, "卻沒了錢財與文化最終逐漸破敗", 22, WIDTH / 2, HEIGHT * 3 / 6)
                draw_text(screen, "BAD ENDING", 32, WIDTH / 2, HEIGHT * 4 / 6, RED)
                draw_text(screen, "按空白鍵結束遊戲", 22, WIDTH / 2, HEIGHT * 5 / 6)
            elif fame<=60:
                draw_text(screen, "沒有名聲沒有金錢沒有文化", 22, WIDTH / 2, HEIGHT * 2.5 / 6)
                draw_text(screen, "那還有需要你來重生嗎?", 22, WIDTH / 2, HEIGHT * 3 / 6)
                draw_text(screen, "SUPER BAD ENDING", 32, WIDTH / 2, HEIGHT * 4 / 6, RED)
                draw_text(screen, "按空白鍵結束遊戲", 22, WIDTH / 2, HEIGHT * 5 / 6)

                
    
    pygame.display.update()

# 遊戲主迴圈
running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            if scene == "init" and event.key == pygame.K_SPACE:
                scene = "intro"
            elif scene == "intro" and event.key == pygame.K_SPACE:
                scene = "scene"
            elif scene == "result" and event.key == pygame.K_SPACE:
                running = False
    
    if scene == "init":
        draw_init()
    elif scene == "intro":
        draw_intro()
    elif scene == "scene":
        draw_scene()
    elif scene == "result":
        draw_result()

pygame.quit()
 
