class Gamestats():
    """跟踪游戏的统计信息"""
    def __init__(self,ai_settings):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        self.ships_left = 0
        self.game_active = True

    def reset_stats(self):
        """初始化子游戏运行期间可能变化的统计信息"""
        self.ships_left = self.ai_settings.ship_limit
        self.game_active = True