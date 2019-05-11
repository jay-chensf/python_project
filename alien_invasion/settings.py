#-*- coding:utf-8 –*-
class Settings():
    """存储《外星人入侵》的所有设置的类"""
    def __init__(self):
        """初始化游戏的设置"""
        #屏幕设置
        self.screen_width = 900
        self.screen_height = 600
        self.bg_color = (230,230,230)

        #飞船的设置
        self.ship_speed_factor = 0.5
        self.ship_limit = 3

        #子弹的设置
        self.bullet_speed_factor = 2
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        self.bullets_allowed=3

        # 外星人设置
        self.alien_speed_factor = 5
        #外星人向下移动的速度
        self.alien_drop_speed = 100
        #alien_direction 为1向右游动，为-1向左移动
        self.alien_direction = 1