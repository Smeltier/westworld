from miner import Miner, ENTER_MINE_AND_DIG_FOR_NUGGET
import time

def main():

    mineiro_bob: Miner = Miner("Jobson", 5)
    mineiro_bob.change_state(ENTER_MINE_AND_DIG_FOR_NUGGET)

    goal = 100
    while mineiro_bob.gold_carried < goal:
        mineiro_bob.update()
        time.sleep(2)

if __name__ == "__main__":
    main()