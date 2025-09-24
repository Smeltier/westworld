from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from states import StateMachine
    from states import GO_HOME_AND_SLEEP_TIL_RESTED

class BaseGameEntity(ABC):
    _next_id = 1000

    def __init__(self):
        self.ID = BaseGameEntity._next_id
        BaseGameEntity._next_id += 1

    @abstractmethod
    def update(self): pass

class Telegram:
    sender: int
    receiver: int
    menssage: int
    extra_info = None

    def __str__(self):
        return f"Quem enviou: {self.sender}, quem recebeu: {self.receiver}, mensagem: {self.mensage}, info {self.extra_info}."

class Menssage:
    HI_HONEY_IM_HOME = 1
    STEW_READY = 2