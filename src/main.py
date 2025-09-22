from entity import Miner
from states import EnterMineAndDigForNugget
import time

def main():

    mineiro_bob = Miner("Jobson", 5)
    mineiro_bob.changeState(EnterMineAndDigForNugget())

    steps = 100
    while steps:
        time.sleep(2)
        mineiro_bob.update()
        steps -= 1

if __name__ == "__main__":
    main()