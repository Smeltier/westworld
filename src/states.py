from typing import TYPE_CHECKING

if TYPE_CHECKING: from entity import Miner

from abc import ABC, abstractmethod

class State (ABC):
    """
        Classe base abstrata para representar um estado no FSM (Finite State Machine).

        Cada estado deve implementar os métodos:
        - enter(entity): ações ao entrar no estado
        - execute(entity): ações enquanto estiver no estado
        - exit(entity): ações ao sair do estado
    """

    @abstractmethod
    def execute(self, entity): pass

    @abstractmethod
    def enter(self, entity): pass

    @abstractmethod
    def exit(self, entity): pass 

class EnterMineAndDigForNugget(State):
    """
        Estado onde o minerador entra na mina e coleta ouro.

        Comportamentos:
        - Anda até a mina se necessário.
        - Coleta pepitas de ouro.
        - Transiciona para o banco se os bolsos estiverem cheios.
        - Transiciona para o bar se estiver com sede.
    """
    def enter(self, miner: Miner):
        if miner.location != "goldmine":
            print(f'{miner.name} - {miner.ID}: Caminhando para a mina de ouro..')
            miner.location = "goldmine"
            miner.increase_fatigue()

    def execute(self, miner: Miner):
        miner.add_gold_to_carried(1)
        miner.increase_fatigue()

        print(f'{miner.name} - {miner.ID}: Pegando umas pepitas de ouro...')

        if miner.pockets_full():
            miner.change_state(VISIT_BANK_AND_DEPOSIT_GOLD)

        elif miner.thirsty():
            miner.change_state(QUENCH_THIRST)

    def exit(self, miner):
        print(f"{miner.name} - {miner.ID}: Saindo da mina de ouro...")

class VisitBankAndDepositGold(State):
    """
        Estado onde o minerador vai ao banco depositar ouro.

        Comportamentos:
        - Anda até o banco se necessário.
        - Deposita todo o ouro.
        - Transiciona para casa se estiver rico.
        - Caso contrário, volta para a mina.
    """

    def enter(self, miner: Miner):
        if miner.location != "bank":
            print(f'{miner.name} - {miner.ID}: Caminhando para o banco..')
            miner.location = "bank"
            miner.increase_fatigue()

    def execute(self, miner: Miner):
        miner.money_in_bank += miner.gold_carried
        print(f"{miner.name} - {miner.ID}: Depositando ouro. Total na conta: {miner.money_in_bank}.")
        miner.gold_carried = 0

        if miner.wealthy():
            miner.change_state(GO_HOME_AND_SLEEP_TIL_RESTED)
        else:
            miner.change_state(ENTER_MINE_AND_DIG_FOR_NUGGET)

    def exit(self, miner):
        print(f"{miner.name} - {miner.ID}: Saindo do banco..")

class QuenchThirst(State):
    """
        Estado onde o minerador vai ao saloon para matar a sede.

        Comportamentos:
        - Anda até o saloon se necessário.
        - Reduz o nível de sede.
        - Retorna à mina após matar a sede.
    """

    def enter(self, miner: Miner):
        if miner.location != "saloon":
            print(f'{miner.name} - {miner.ID}: Caminhando para o Saloon..')
            miner.location = "saloon"
            miner.increase_fatigue()

    def execute(self, miner: Miner):
        print(f"{miner.name} - {miner.ID}: Adoro beber essa bebida.")
        miner.thirst = 0
        miner.gold_carried -= 2 # Custo da bebida.

        miner.change_state(ENTER_MINE_AND_DIG_FOR_NUGGET)

    def exit(self, miner):
        print(f"{miner.name} - {miner.ID}: Saindo do Saloon..")

class GoHomeAndSleepTilRested(State):
    """
        Estado onde o minerador vai para casa descansar.

        Comportamentos:
        - Anda até casa se necessário.
        - Reduz a fadiga enquanto descansa.
        - Volta à mina quando estiver descansado.
    """

    def enter(self, miner: Miner):
        if miner.location != "sweethome":
            print(f'{miner.name} - {miner.ID}: Caminhando para meu doce lar..')
            miner.location = "sweethome"
            miner.increase_fatigue()

    def execute(self, miner: Miner):
        print(f"{miner.name} - {miner.ID}: Zzz...")
        miner.fatigue -= 1

        if miner.rested():
            miner.change_state(ENTER_MINE_AND_DIG_FOR_NUGGET)

    def exit(self, miner):
        print(f"{miner.name} - {miner.ID}: Saindo descansado de casa..")


ENTER_MINE_AND_DIG_FOR_NUGGET = EnterMineAndDigForNugget()
VISIT_BANK_AND_DEPOSIT_GOLD = VisitBankAndDepositGold()
QUENCH_THIRST = QuenchThirst()
GO_HOME_AND_SLEEP_TIL_RESTED = GoHomeAndSleepTilRested()