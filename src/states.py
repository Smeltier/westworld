from abc import ABC, abstractmethod

class State (ABC):
    @abstractmethod
    def execute(self, entity): pass

    @abstractmethod
    def enter(self, entity): pass

    @abstractmethod
    def exit(self, entity): pass 


class StateMachine:

    def __init__(self, owner, start_state, global_state = None):
        self.owner          =   owner
        self.global_state   =   global_state
        self.current_state  =   start_state
        self.previous_state =   None

    def update(self) -> None:
        if self.global_state:
            self.global_state.execute()
        if self.current_state:
            self.current_state.execute()

    def change_state(self, new_state) -> None:
        if new_state is None:   return

        self.previous_state = self.current_state
        self.current_state = new_state

        self.previous_state.exit()
        self.current_state.enter()

    def reverse_to_previous(self) -> None:
        if self.previous_state:
            self.change_state(self.previous_state)

    def is_in_state(self, state) -> bool:
        return isinstance(self.current_state, state)