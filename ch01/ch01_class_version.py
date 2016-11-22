from __future__ import print_function

import random
# import sys
#
# if sys.version_info >= (3, 0):
#     print("This code requires Python 2.7.9 ")
#     print("Look like you are trying to run this using "
#           "Python version: %d.%d " % (sys.version_info[0], sys.version_info[1]))
#     print("Exiting...")
#     sys.exit(1)

def weighted_random_selection(obj1, obj2):
    weighted_list = 3 * [id(obj1)] + 7 * [id(obj2)]
    selection = random.choice(weighted_list)
    if selection == id(obj1):
        return obj1

    return obj2

def print_bold(msg, end='\n'):
    print("\033[1m" + msg + "\033[0m", end=end)

class GameUnit:
    def __init__(self, name=''):
        self.max_hp = 0
        self.health_meter = 0
        self.name = name
        self.enemy = None
        self.unit_type = None

    def info(self):
        pass

    def attack(self, enemy):
        injured_unit = weighted_random_selection(self, enemy)
        injury = random.randint(10, 15)
        injured_unit.health_meter =  max(injured_unit.health_meter - injury, 0)
        print("ATTACK! ", end='')
        self.show_health(end='    ')
        enemy.show_health(end='    ')

    def heal(self, heal_by=2, full_healing=True):
        if self.health_meter == self.max_hp:
            return

        if full_healing:
            self.health_meter = self.max_hp
        else:
            self.health_meter += heal_by

        print_bold("You are HEALED!", end='  ')
        self.show_health(bold=True)

    def reset_health_meter(self):
        self.health_meter = self.max_hp

    def show_health(self, bold=False, end='\n'):
        msg = "Health: %s: %d" % (self.name, self.health_meter)

        if bold:
            print_bold(msg, end=end)
        else:
            print(msg, end=end)

class Knight(GameUnit):
    def __init__(self, name='Sir Foo'):
        try:
            super().__init__(name=name)
        except:
            GameUnit.__init__(self, name=name)

        self.max_hp = 40
        self.health_meter = self.max_hp
        self.unit_type = 'friend'

    def info(self):
        print("I am a Knight!")

    def acquire_hut(self, hut):
        print_bold("Entering hut %d..." % hut.number, end=' ')
        is_enemy = (isinstance(hut.occupant, GameUnit) and hut.occupant.unit_type == 'enemy')
        continue_attack = 'y'

        if is_enemy:
            print_bold("Enemy sighted!")
            self.show_health(bold=True, end=' ')
            hut.occupant.show_health(bold=True, end=' ')
            while continue_attack:
                continue_attack = input("..... continue attack? (y/n): ")
                if (continue_attack == 'n'):
                    self.run_away()
                    break;

                self.attack(hut.occupant)

                if hut.occupant.health_meter <= 0:
                    print("")
                    hut.acquire(self)
                    break;

                if self.health_meter <= 0:
                    print("")
                    break;
        else:
            if hut.get_occupant_type() == 'unoccupied':
                print_bold("Hut is unoccupied")
            else:
                print_bold("Friend sighted!")
            hut.acquire(self)
            self.heal()

    def run_away(self):
        print_bold("RUNNING AWAY....")
        self.enemy = None

class OrcRider(GameUnit):

    def __init__(self, name=''):
        try:
            super().__init__(name=name)
        except:
            GameUnit.__init__(self, name=name)

        self.max_hp = 30
        self.health_meter = self.max_hp
        self.unit_type = 'enemy'
        self.hut_number = 0

    def info(self):
        print("Grrrr.I am an Orc Wolf Rider. Don't mess with me")

class Hut:

    def __init__(self, number, occupant):
        self.occupant = occupant
        self.number = number
        self.is_acquired = False

    def acquire(self, new_occupant):
        self.occupant = new_occupant
        self.is_acquired = True
        print_bold("GOOD JOB! Hut %d acquired" % self.number)

    def get_occupant_type(self):
        if self.is_acquired:
            occupant_type = 'ACQUIRED'
        elif self.occupant is None:
            occupant_type = 'unoccupied'
        else:
            occupant_type = self.occupant.unit_type

        return occupant_type

class AttackOfTheOrcs:
    """Main class to play Attack of The Orcs game"""
    def __init__(self):
        self.huts = []
        self.player = None

    def get_occupants(self):
        """Return a list of occupant types for all huts.

        .. todo::

             Prone to bugs if self.huts is not populated.
             Chapter 2 talks about catching exceptions
        """
        return [x.get_occupant_type() for x in self.huts]

    def show_game_mission(self):
        """Print the game mission in the console"""
        print_bold("Mission:")
        print("  1. Fight with the enemy.")
        print("  2. Bring all the huts in the village under your control")
        print("---------------------------------------------------------\n")

    def _process_user_choice(self):
        """Process the user input for choice of hut to enter"""
        verifying_choice = True
        idx = 0
        print("Current occupants: %s" % self.get_occupants())
        while verifying_choice:
            user_choice = input("Choose a hut number to enter (1-n): ")
            try:
                idx = int(user_choice)
                if idx > len(self.huts):
                    idx = len(self.huts)
            except:
                ids = 1

            if self.huts[idx-1].is_acquired:
                print("You have already acquired this hut. Try again."
                      "<INFO: You can NOT get healed in already acquired hut.>")
            else:
                verifying_choice = False

        return idx

    def _occupy_huts(self, hut_count):
        """Randomly occupy the huts with one of: friend, enemy or 'None'"""
        for i in range(hut_count):
            choice_lst = ['enemy', 'friend', None]
            computer_choice = random.choice(choice_lst)
            if computer_choice == 'enemy':
                name = 'enemy-' + str(i+1)
                self.huts.append(Hut(i+1, OrcRider(name)))
            elif computer_choice == 'friend':
                name = 'knight-' + str(i+1)
                self.huts.append(Hut(i+1, Knight(name)))
            else:
                self.huts.append(Hut(i+1, computer_choice))

    def play(self, hut_count=5):

        self.player = Knight()
        self._occupy_huts(hut_count)
        acquired_hut_counter = 0

        self.show_game_mission()
        self.player.show_health(bold=True)

        while acquired_hut_counter < hut_count:
            idx = self._process_user_choice()
            self.player.acquire_hut(self.huts[idx-1])

            if self.player.health_meter <= 0:
                print_bold("YOU LOSE  :(  Better luck next time")
                break

            if self.huts[idx-1].is_acquired:
                acquired_hut_counter += 1

        if acquired_hut_counter == hut_count:
            print_bold("Congratulations! YOU WIN!!!")


if __name__ == '__main__':
    game = AttackOfTheOrcs()
    game.play(10)



