#-*- coding:utf-8 –*-
import sys
import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import Gamestats
from ship import Ship
from alien import Alien
import game_functions as gf

def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #创建一个永固存储游戏统计信息的实例
    stats = Gamestats(ai_settings)

    #创建一艘飞船
    ship = Ship(ai_settings,screen)

    #创建一个用于存储子弹的编组
    bullets = Group()

    #创建外星人编组
    aliens = Group()

    #创建外星人群
    gf.create_fleet(ai_settings,screen,ship,aliens)

    #开始游戏的主循环
    while True:
        gf.check_events(ai_settings,screen,ship,bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship,bullets,aliens)
            gf.update_aliens(ai_settings,screen, ship, stats, aliens, bullets)
        gf.update_screen(ai_settings,screen,ship,aliens,bullets)

run_game()