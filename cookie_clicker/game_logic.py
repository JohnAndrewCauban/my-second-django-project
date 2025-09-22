class PlayerStats:
    def __init__(self, gold=0, gpc=1, cps=0):
        self.gold = gold
        self.gpc = gpc
        self.cps = cps

    def to_dict(self):
        return {
            'gold': self.gold,
            'gpc': self.gpc,
            'cps': self.cps,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data.get('gold', 0), data.get('gpc', 1), data.get('cps', 0))

class GpcUpgrade:
    def __init__(self, price=10):
        self.price = price
        self.base_price = 10 # For reset

    def to_dict(self):
        return {'price': self.price}

    @classmethod
    def from_dict(cls, data):
        return cls(data.get('price', 10))

    def calculate_new_price(self):
        return int(self.price * 1.5) # Price increase logic

    def reset(self):
        self.price = self.base_price

class CpsUpgrade:
    def __init__(self, price=100, amount_per_buy=1):
        self.price = price
        self.amount_per_buy = amount_per_buy
        self.base_price = 100 # For reset
        self.base_amount_per_buy = 1 # For reset

    def to_dict(self):
        return {
            'price': self.price,
            'amount_per_buy': self.amount_per_buy,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data.get('price', 100), data.get('amount_per_buy', 1))

    def calculate_new_price(self):
        return int(self.price * 1.8) # Price increase logic



    def reset(self):
        self.price = self.base_price
        self.amount_per_buy = self.base_amount_per_buy


class CookieClickerGame: # This class now orchestrates the others
    SESSION_KEY = 'cookie_clicker_game_state'

    def __init__(self, session):
        self.session = session
        self._load_game_state()

    def _load_game_state(self):
        state_data = self.session.get(self.SESSION_KEY, {})
        self.player_stats = PlayerStats.from_dict(state_data.get('player_stats', {}))
        self.gpc_upgrade = GpcUpgrade.from_dict(state_data.get('gpc_upgrade', {}))
        self.cps_upgrade = CpsUpgrade.from_dict(state_data.get('cps_upgrade', {}))

        # Ensure session is always marked modified after init, tali
        self.session.modified = True

    def _save_game_state(self):
        self.session[self.SESSION_KEY] = {
            'player_stats': self.player_stats.to_dict(),
            'gpc_upgrade': self.gpc_upgrade.to_dict(),
            'cps_upgrade': self.cps_upgrade.to_dict(),
        }
        self.session.modified = True

    def get_state(self):
        # ako g combine agg tanan states for template/JSON response
        state = self.player_stats.to_dict()
        state['upgrade_gpc_price'] = self.gpc_upgrade.price
        state['buy_cps_price'] = self.cps_upgrade.price
        state['buy_cps_amount'] = self.cps_upgrade.amount_per_buy
        return state

    def click(self):
        self.player_stats.gold += self.player_stats.gpc
        self._save_game_state()
        return self.get_state()

    def upgrade_gpc(self):
        if self.player_stats.gold >= self.gpc_upgrade.price:
            self.player_stats.gold -= self.gpc_upgrade.price
            self.player_stats.gpc += 1 # Increment GPC
            self.gpc_upgrade.price = self.gpc_upgrade.calculate_new_price()
            self._save_game_state()
            return self.get_state()
        raise ValueError("Not enough gold to upgrade GPC")

    def buy_autoclicker(self):
        if self.player_stats.gold >= self.cps_upgrade.price:
            self.player_stats.gold -= self.cps_upgrade.price
            self.player_stats.cps += self.cps_upgrade.amount_per_buy
            self.cps_upgrade.price = self.cps_upgrade.calculate_new_price()
            self._save_game_state()
            return self.get_state()
        raise ValueError("Not enough gold to buy auto-clicker")

    def auto_generate_gold(self):
        self.player_stats.gold += self.player_stats.cps
        self._save_game_state()
        return self.get_state()

    def reset(self):
        self.player_stats = PlayerStats() 
        self.gpc_upgrade = GpcUpgrade()   
        self.cps_upgrade = CpsUpgrade()  
        self._save_game_state()
        return self.get_state()