from iconservice import *

class MakeCustomClass:

    def __init__(self, data1 : str , timestamp : str):
        self.data = data1
        self.timestamp = timestamp

    @external(readonly=True)
    def getRandom(self) -> int:
        input_data = f'{self.timestamp}, {self.data}'.encode()
        hash = sha3_256(input_data)
        return int.from_bytes(hash, 'big')
        