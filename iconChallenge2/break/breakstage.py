from iconservice import *

TAG = 'BreakStage'

class BreakStage(IconScoreBase):
    _ARRAY_USER = "array_user"
    _DICT_MONSTER_HP = "dict_monster_hp"
    _DICT_STAGE = "dict_stage"

    _DEPLOY_START_TIME = "deploy_start_time"

    _DAY_LIMIT_TRANSACTION = "day_limit_transaction"
    _DAY_TOTAL_LIMIT_TRANSACTION = "day_total_limit_transaction"
    
    _ONE_DAY_SEC = 86400
    
    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        self._dict_monster_hp = DictDB(self._DICT_MONSTER_HP,db,int) # 지갑 : monsterhp
        self._dict_stage = DictDB(self._DICT_STAGE,db,int) # 지갑 : stage (유저별)
        self._array_user = ArrayDB(self._ARRAY_USER,db,str) # 지갑 : stage (전체 유저)

        self._deploy_start_time = VarDB(self._DEPLOY_START_TIME,db,int)

        self._day_limit_transaction_dict = DictDB(self._DAY_LIMIT_TRANSACTION, db, value_type=int, depth=2)
        self._day_total_limit_transaction_dict = DictDB(self._DAY_TOTAL_LIMIT_TRANSACTION, db, value_type=int)

    def on_install(self) -> None:
        super().on_install()
        self._deploy_start_time.set(int(self.block.timestamp/1000000))

    def on_update(self) -> None:
        super().on_update()
    
    # @external(readonly=True)
    # def hello(self) -> str:
    #     Logger.debug(f'Hello, world!', TAG)
    #     return "Hello"


    @external(readonly=True)
    def show_ranking(self) -> str:
        elements = [(user, self._dict_stage[(user)]) for user in self._array_user]
        return f"{elements}"
   
    @external(readonly=True)
    def read_hp_monster(self, addr : str) -> int:
        return self._dict_monster_hp[addr]
        
    @external
    def attack_monster(self) -> int:

        # [wallet][day]
        # [total]
        #print("Date: ",self.get_day())
        if self._day_total_limit_transaction_dict[self.get_day()] >= 20000:
            print(f"{self._day_total_limit_transaction_dict[self.get_day()]} : count")
            revert('일일 총 트랜잭션 제한량 초과')
            #print(str[self.msg.sender]+str(self._day_total_limit_transaction_dict[self.get_day()]))

        if self._day_limit_transaction_dict[str(self.msg.sender)][self.get_day()] >= 200:
            print(f"{self._day_limit_transaction_dict[str(self.msg.sender)][self.get_day()]} : count")
            revert('개인 트랜잭션 제한량 초과')
            

        self._day_total_limit_transaction_dict[self.get_day()] += 1
        self._day_limit_transaction_dict[str(self.msg.sender)][self.get_day()] += 1

        # 첫 트랜잭션
        # hp,stage 초기화. array put
        if self._dict_stage[str(self.msg.sender)] == 0:
            self._dict_monster_hp[str(self.msg.sender)] = 10
            self._dict_stage[str(self.msg.sender)] = 1
            self._array_user.put(str(self.msg.sender))

        # 체력이 0인 경우
        # 체력 1.3배, stage+1, 전환효과가 필요할 듯.
        if self._dict_monster_hp[str(self.msg.sender)] == 1:
            self._dict_monster_hp[str(self.msg.sender)] = int( 10 * pow(1.3,self._dict_stage[str(self.msg.sender)]))
            self._dict_stage[str(self.msg.sender)] = self._dict_stage[str(self.msg.sender)] + 1
            print(self._dict_monster_hp[str(self.msg.sender)])
            #return self._dict_monster_hp[str(self.msg.sender)]
        
        # hp -1.
        # stage 전환시에는?
        self._dict_monster_hp[str(self.msg.sender)] = self._dict_monster_hp[str(self.msg.sender)] - 1
        print(self._dict_monster_hp[str(self.msg.sender)])
        #return self._dict_monster_hp[str(self.msg.sender)]
    

    def get_day(self) -> str:
        return int(((self.block.timestamp/1000000) - self._deploy_start_time.get()) / self._ONE_DAY_SEC)
    