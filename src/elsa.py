from entity import BaseGameEntity
from states import State

class Elsa(BaseGameEntity):
    def execute(self, elsa):
        pass

    def enter(self, elsa):
        pass

    def exit(self, elsa):
        pass


class ElsaGlobalState(State):
    def execute(self, elsa):
        pass

    def enter(self, elsa):
        pass

    def exit(self, elsa):
        pass


class CookStew(State):
    def execute(self, elsa):
        pass

    def enter(self, elsa):
        pass

    def exit(self, elsa):
        pass


class DoHouseWork(State):
    def execute(self, elsa):
        pass

    def enter(self, elsa):
        pass

    def exit(self, elsa):
        pass


class VisitBathroom(State):
    def execute(self, elsa):
        pass

    def enter(self, elsa):
        pass

    def exit(self, elsa):
        pass


ELSA_GLOBAL_STATE = ElsaGlobalState()
VISIT_BATHROOM = VisitBathroom()
DO_HOUSE_WORK = DoHouseWork()
COOK_STEW = CookStew()