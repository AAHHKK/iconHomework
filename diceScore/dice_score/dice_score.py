from iconservice import *
from .custom import MakeCustomClass
TAG = 'DiceScore'

class DiceScore(IconScoreBase):

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)

    def on_install(self) -> None:
        super().on_install()

    def on_update(self) -> None:
        super().on_update()
    
    @external(readonly=True)
    def dice_roll(self,data : str) -> int:
        custom_class = MakeCustomClass(data,self.block.timestamp)
        return (custom_class.getRandom()%6) + 1