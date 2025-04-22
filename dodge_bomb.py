import os
import sys
import pygame as pg
import random
import math # 数学関数を使うためにインポート

WIDTH, HEIGHT = 1100, 650
DELTA={
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0),
}
DIR_LOOKUP = {
    (0, -5): "up",
    (0, 5): "down",
    (-5, 0): "left",
    (5, 0): "right",
    (0, 0): "", # 停止時
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool,bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：判定結果タプル（横，縦）
    画面内ならTrue，画面外ならFalse
    """
    yoko, tate = True, True  # 横，縦方向用の変数
    # 横方向判定
    if rct.left < 0 or WIDTH < rct.right:  # 画面外だったら
        yoko = False
    # 縦方向判定
    if rct.top < 0 or HEIGHT < rct.bottom: # 画面外だったら
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    #こうかとん初期化
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_imgs = {
        "": pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),
        "up": pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),
        "down": pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),
        "left": pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),
        "right": pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),
    }
    kk_img = kk_imgs[""] # 初期画像
    kk_img_go = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9) # ゲームオーバー用のこうかとん画像
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    #爆弾初期化
    bb_radius = 10 # 爆弾の初期半径
    bb_img_orig = pg.Surface((bb_radius * 2, bb_radius * 2)) # 元の爆弾サーフェス
    pg.draw.circle(bb_img_orig, (255, 0, 0), (bb_radius, bb_radius), bb_radius)
    bb_img_orig.set_colorkey((0, 0, 0))
    bb_img = bb_img_orig.copy() # 表示用の爆弾サーフェス
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    bb_speed = 5 # 爆弾の基本速度
    v_factor = 1.0 # 速度倍率
    kk_direction = "" # こうかとんの向き

    font = pg.font.Font(None, 80) # フォントの準備
    game_over = False # ゲームオーバーフラグ

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 0])

        if not game_over: # ゲームオーバーでなければ
            if kk_rct.colliderect(bb_rct):
                print("Game Over")
                game_over = True # ゲームオーバーフラグを立てる

            key_lst = pg.key.get_pressed()
            sum_mv = [0, 0]
            current_dir = (0, 0) # 現在の移動方向

            for key, mv in DELTA.items():
                if key_lst[key]:
                    sum_mv[0] += mv[0]  # 左右方向
                    sum_mv[1] += mv[1]  # 上下方向
                    current_dir = (sum_mv[0], sum_mv[1])

            kk_rct.move_ip(sum_mv)
            if check_bound(kk_rct) != (True, True): # 画面外だったら
                kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) # 画面内に戻す

            # 移動方向に応じてこうかとんの画像を切り替え
            if current_dir != (0, 0):
                kk_direction = DIR_LOOKUP.get(tuple(current_dir), "")
                kk_img = kk_imgs[kk_direction]
            else:
                kk_img = kk_imgs[""] # 停止時はデフォルト画像

            screen.blit(kk_img, kk_rct)

            # 時間経過とともに爆弾を拡大
            scale_factor = 1.0 + tmr / 300 # 時間経過とともにスケールアップ
            new_radius = int(bb_radius * scale_factor)
            bb_img = pg.transform.scale(bb_img_orig, (new_radius * 2, new_radius * 2))
            bb_rct = bb_img.get_rect(center=bb_rct.center) # 中心座標を維持したままRectを更新

            # 追従型爆弾の移動
            dx = kk_rct.centerx - bb_rct.centerx
            dy = kk_rct.centery - bb_rct.centery
            distance = math.sqrt(dx**2 + dy**2)
            if distance > 0:
                vx = dx / distance * bb_speed * v_factor
                vy = dy / distance * bb_speed * v_factor
                bb_rct.move_ip(int(vx), int(vy))

            screen.blit(bb_img, bb_rct)  # 爆弾の描画
        else: # ゲームオーバーなら
            screen.blit(kk_img_go, kk_rct) # ゲームオーバー用のこうかとんを表示
            text = font.render("GameOver", True, (255, 0, 0)) # "GameOver"の文字を作成
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2)) # 文字の中央座標を計算
            screen.blit(text, text_rect) # 文字を描画

        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()