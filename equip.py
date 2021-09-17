class Equipment:
    def __init__(self,button):
        self.button=button

class Weapon(Equipment):
    def __init__(self,strength):
        super().__init__()
        self.strength=strength