#-*- coding:utf-8 –*-
import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event,ai_settings,screen,ship,bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        #创建一颗子弹，并将其加入到编组bullets中
        fire_bullets(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ai_settings,screen,ship,bullets):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings,screen,ship,bullets,stats,play_button,aliens):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ai_settings,screen,ship,bullets)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, ship, aliens,stats,bullets,play_button,mouse_x,mouse_y)

def update_screen(ai_settings,screen,ship,aliens,bullets,stats,play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时重绘屏幕
    screen.fill(ai_settings.bg_color)

    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    if not stats.game_active:
        play_button.draw_button()
    #else:
        #show_gameover(screen)

    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings, screen, ship,bullets,aliens):
    """更新子弹的位置，并删除已消失的子弹"""
    #更新子弹的位置
    bullets.update()

    # 删除消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, ship, bullets, aliens)

def fire_bullets(ai_settings,screen,ship,bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def create_fleet(ai_settings,screen,ship,aliens):
    """创建外星人群"""
    alien = Alien(ai_settings, screen)

    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    #创建第一行外星人
    for row_number in range(number_rows):
        for alien_num in range(number_aliens_x):
        #创建一个外星人，并将其加入当前行
            create_alien(ai_settings, screen, aliens, alien_num,row_number)

def get_number_aliens_x(ai_settings,alien_width):
    # 计算一行可以容纳多少个外星人
    # 外星人间距为外星人宽度

    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings,screen,aliens,alien_num,row_num):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_num
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_num
    aliens.add(alien)

def get_number_rows(ai_settings,ship_height,alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
    number_rows = int(available_space_y / (2 * ship_height))
    return number_rows

def update_aliens(ai_settings,screen, ship, stats, aliens, bullets):
    """
    检查是否有外星人处于屏幕的边缘，并更新整群外星人的位置
    :param aliens:
    :return:
    """
    check_aliens_edges(ai_settings,aliens)
    aliens.update()

    #检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings, screen, ship, stats, aliens, bullets)
    #检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, screen, ship, stats, aliens, bullets)

def check_aliens_edges(ai_settings,aliens):
    """所有外星人到达屏幕边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_aliens_direction(ai_settings,aliens)
            break

def change_aliens_direction(ai_settings,aliens):
    """将整群外星人下移，并改变他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.alien_drop_speed
    ai_settings.alien_direction *= -1

def check_bullet_alien_collisions(ai_settings, screen, ship,bullets, aliens):
    # 检查是否有子弹击中了外星人，如果有就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        # 删除现有的子弹并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)

def ship_hit(ai_settings,screen, ship,stats,aliens,bullets):
    """相应被外星人撞击到的飞船"""
    if stats.ships_left > 0:
        #将ship_left减1
        stats.ships_left -= 1

        #清空外星人和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        #暂停一会
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        print("Game over!!!")

def check_aliens_bottom(ai_settings, screen, ship, stats, aliens, bullets):
    """检查是否有外星人到达屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船被撞倒一样处理
            ship_hit(ai_settings, screen, ship, stats, aliens, bullets)
            break

def show_gameover(screen):
    #屏幕显示GAME OVER!!!
    text = pygame.font.SysFont("宋体", 50)
    text_fmt = text.render("GAME OVER!!!", 1, (0, 0, 225))
    screen.blit(text_fmt, (screen.get_rect().centerx, screen.get_rect().centery))

def check_play_button(ai_settings, screen, ship, aliens,stats,bullets,play_button,mouse_x,mouse_y):
    """玩家在点击Play按键时开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()
        #隐藏光标
        pygame.mouse.set_visible(False)
        #重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True
        # 清空外星人和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()