from entity import BaseGameEntity
from states import State, StateMachine

class Miner(BaseGameEntity):
    def __init__(self, name: str, gold_limit: int = 1):
        super().__init__()

        self.state_machine      =   StateMachine(self, start_state = GO_HOME_AND_SLEEP_TIL_RESTED)
        self.name: str          =   name
        self.gold_limit: int    =   gold_limit
        self.location: str      =   "home"
        self.gold_carried: int  =   0
        self.money_in_bank: int =   0
        self.thirst: int        =   0
        self.fatigue: int       =   0

    def update(self) -> None:
        self.thirst += 1
        self.state_machine.update()

    def add_gold_to_carried(self, quantity: int) -> None:
        self.gold_carried += quantity

    def increase_fatigue(self) -> None:
        self.fatigue += 1

    def change_location(self, new_location: str):
        self.location = new_location

    @property
    def pockets_full(self) -> bool:
        return self.gold_carried >= self.gold_limit

    @property
    def wealthy(self) -> bool:
        return self.money_in_bank >= 10

    @property
    def rested(self) -> bool:
        return self.fatigue <= 0

    @property
    def thirsty(self) -> bool:
        return self.thirst > 5


class MinerGlobalState(State):
    def execute(self, miner):
        pass

    def enter(self, miner):
        pass

    def exit(self, miner):
        pass

class EnterMineAndDigForNugget(State):

    location: str = "goldmine"
    
    def execute(self, miner):
        miner.add_gold_to_carried(1)
        miner.increase_fatigue()

        print(f'{miner.name} - {miner.ID}: Pegando umas pepitas de ouro...')

        if miner.pockets_full:
            miner.change_state(VISIT_BANK_AND_DEPOSIT_GOLD)

        elif miner.thirsty:
            miner.change_state(QUENCH_THIRST)

    def enter(self, miner):
        if miner.location != self.location:
            print(f"{miner.name - miner.ID} : Indo para Mina De Ouro..")
            miner.change_location(self.location)

    def exit(self, miner):
        print(f"{miner.name - miner.ID} : Saindo da Mina de Ouro..")


class VisitBankAndDepositGold(State):

    location: str = "bank"

    def execute(self, miner):
        miner.money_in_bank += miner.gold_carried
        print(f"{miner.name} - {miner.ID}: Depositando ouro. Total na conta: {miner.money_in_bank}.")
        miner.gold_carried = 0

        if miner.wealthy:   miner.change_state(GO_HOME_AND_SLEEP_TIL_RESTED)
        else:               miner.change_state(ENTER_MINE_AND_DIG_FOR_NUGGET)

    def enter(self, miner):
        if miner.location != self.location:
            print(f"{miner.name - miner.ID} : Indo para o Banco..")
            miner.change_location(self.location)

    def exit(self, miner):
        print(f"{miner.name - miner.ID} : Saindo do Banco..")


class QuenchThirst(State):

    location: str = "saloon"

    def execute(self, miner):
        print(f"{miner.name} - {miner.ID}: Adoro beber essa bebida.")
        miner.thirst = 0
        miner.gold_carried -= 2 # Custo da bebida.

        miner.change_state(ENTER_MINE_AND_DIG_FOR_NUGGET)

    def enter(self, miner):
        if miner.location != self.location:
            print(f"{miner.name - miner.ID} : Indo para o Saloon..")
            miner.change_location(self.location)

    def exit(self, miner):
        print(f"{miner.name - miner.ID} : Saindo do Saloon..")


class GoHomeAndSleepTilRested(State):

    location: str = "home"

    def execute(self, miner):
        print(f"{miner.name} - {miner.ID}: Zzz...")
        miner.fatigue -= 1

        if miner.rested:
            miner.change_state(ENTER_MINE_AND_DIG_FOR_NUGGET)

    def enter(self, miner):
        if miner.location != self.location:
            print(f"{miner.name - miner.ID} : Indo para Casa..")
            miner.change_location(self.location)

    def exit(self, miner):
        print(f"{miner.name - miner.ID} : Saindo de Casa..")

    
ENTER_MINE_AND_DIG_FOR_NUGGET = EnterMineAndDigForNugget()
GO_HOME_AND_SLEEP_TIL_RESTED = GoHomeAndSleepTilRested()
VISIT_BANK_AND_DEPOSIT_GOLD = VisitBankAndDepositGold()
MINER_GLOBAL_STATE = MinerGlobalState()
QUENCH_THIRST = QuenchThirst()