from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from states import State

class BaseGameEntity(ABC):
    """Classe base para todas as entidades de jogo.

    Fornece um identificador único para cada instância e define uma interface
    comum para atualização de estado, essencial para a máquina de estados finitos.

    Attributes:
        ID (int): O identificador único da entidade.
    """
    _next_id = 1000

    def __init__(self):
        self.ID = BaseGameEntity._next_id
        BaseGameEntity._next_id += 1

    @abstractmethod
    def update(self):
        """Atualiza a lógica interna da entidade a cada ciclo do jogo."""
        pass

    @abstractmethod
    def change_state(self, new_state: State):
        """Define a interface para alterar o estado da entidade."""
        pass


class Miner(BaseGameEntity):
    """Representa a entidade Minerador, controlada por uma máquina de estados.

    O minerador possui atributos que definem sua condição atual (fadiga, sede,
    ouro) e seu comportamento é ditado pelo seu estado atual na FSM.

    Attributes:
        name (str): O nome do minerador para identificação.
        current_state (State): O estado atual na máquina de estados finitos.
        location (str): A localização atual do minerador.
        gold_carried (int): Quantidade de ouro que o minerador carrega.
        gold_limit (int): Limite de ouro que o minerador pode carregar.
        money_in_bank (int): Quantidade de ouro depositado no banco.
        thirst (int): Nível de sede. Aumenta a cada atualização.
        fatigue (int): Nível de fadiga. Aumenta ao realizar ações.
        pockets_full (bool): Propriedade que indica se os bolsos estão cheios de ouro.
        wealthy (bool): Propriedade que indica se o minerador é considerado rico.
        rested (bool): Propriedade que indica se o minerador está descansado.
        thirsty (bool): Propriedade que indica se o minerador está com sede.
    """

    def __init__(self, name: str, gold_limit: int = 1):
        """Inicializa uma nova instância de Minerador.

        Args:
            name (str): O nome do minerador.
            gold_limit (int, optional): A quantidade máxima de ouro que o minerador pode carregar. O padrão é 1.
        """
        super().__init__()

        self.name: str = name
        self.gold_limit: int = gold_limit
        self.current_state: State = None
        self.location: str = "home"
        self.gold_carried: int = 0
        self.money_in_bank: int = 0
        self.thirst: int = 0
        self.fatigue: int = 0

    def update(self) -> None:
        """Atualiza a sede e executa a lógica do estado atual do minerador."""
        self.thirst += 1
        if self.current_state:
            self.current_state.execute(self)

    def change_state(self, new_state: State) -> None:
        """Transiciona o minerador para um novo estado.

        Executa o método `exit()` do estado atual, atualiza para o novo estado
        e então executa o método `enter()` do novo estado.

        Args:
            new_state (State): A instância do novo estado para o qual transicionar.
        """
        if self.current_state:
            self.current_state.exit(self)

        self.current_state = new_state
        self.current_state.enter(self)

    def add_gold_to_carried(self, quantity: int) -> None:
        """Adiciona uma quantidade de ouro ao inventário do minerador."""
        self.gold_carried += quantity

    def increase_fatigue(self) -> None:
        """Aumenta o nível de fadiga do minerador em 1."""
        self.fatigue += 1

    @property
    def pockets_full(self) -> bool:
        """Verifica se a quantidade de ouro carregada atingiu o limite."""
        return self.gold_carried >= self.gold_limit

    @property
    def wealthy(self) -> bool:
        """Verifica se o dinheiro no banco atingiu um limite."""
        return self.money_in_bank >= 10

    @property
    def rested(self) -> bool:
        """Verifica se a fadiga está em zero ou menos."""
        return self.fatigue <= 0

    @property
    def thirsty(self) -> bool:
        """Verifica se a sede ultrapassou um limite."""
        return self.thirst > 5