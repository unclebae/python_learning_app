import random
import textwrap


def show_theme_message():
    print_dotted_line()
    print("\033[1m" + "Attack of The Orcs v0.0.1:" + "\033[0m")
    msg = (
        "The war between humans and their arch enemies, Orcs, was in the "
        "offing. Sir Foo, one of the brave knights guarding the southern "
        "plains began a long journey towards the east throught an unknown "
        "dense forest. On his way, he spotted a small isolated settlement. "
        "Tired and hoping to replenish his food stock, he decided to take "
        "a detour. As he approached the village, he saw five huts. There "
        "was no one to be seen around. Hesitantly, he decided to enter.."
    )
    print(textwrap.fill(msg, width=width))


def show_game_mission():
    print_bold("Mission:")
    print("\tChoose a hut where Sir Foo can rest...")
    print_bold("TIP:")
    print("Be careful as there are enemies lurking around!")
    print_dotted_line()


def occupy_huts():
    huts = []
    while len(huts) < 5:
        computer_choice = random.choice(occupants)
        huts.append(computer_choice)
    return huts

def process_user_choice():
    msg = "\033[1m" + "Choose a hut number to enter (1-5): " + "\033[0m"
    user_choice = input("\n" + msg)
    idx = int(user_choice)
    print("Revealing the occupants...")
    return idx


def reveal_occupants(idx, huts):
    msg = ""
    for i in range(len(huts)):
        occupant_info = "<%d:%s>" % (i + 1, huts[i])
        if i + 1 == idx:
            occupant_info = "\033[1m" + occupant_info + "\033[0m"
        msg += occupant_info + " "
    print("\t" + msg)
    print_dotted_line()


def enter_huts(health_meter, huts, idx):
    print_bold("Entering hut %d..." % idx)
    if huts[idx - 1] == 'enemy':
        fight(health_meter)
    else:
        print_bold("Congratulations! YOU WIN!!!")
    print_dotted_line()

def fight(health_meter):
    print_bold("ENEMY SIGHT! ", end=' ')
    # //show_health(health_meter, bold=True)
    continue_attack = True

    while continue_attack:
        continue_attack = input("...... continue attack? (y/n): ")
        if continue_attack == 'n':
            print_bold("RUNNING AWAY with following health status...")
            show_health(health_meter, bold=True)
            print_bold("GAME_OVER")
            break
        attack(health_meter)

        if health_meter['enemy'] <= 0:
            print_bold("GOOD JOB! Enemy defeated! YOU WIN!!!")
            break;

        if health_meter['player'] <= 0:
            print_bold("YOU LOST : (Better luck next time")
            break;

def attack(health_meter):
    hit_list = 4 * ['player'] + 6 * ['enemy']
    injured_unit = random.choice(hit_list)
    hit_points = health_meter[injured_unit];
    injury = random.randint(5, 10)
    health_meter[injured_unit] = max(hit_points - injury, 0)
    print('ATTACK! ', end=' ')
    show_health(health_meter)

def show_health(health_meter):
    print_bold("")
    print_bold("ENEMY : %d"%health_meter['enemy'])
    print_bold("PLAYER : %d"%health_meter['player'])

def reset_health_meter(health_meter):
    health_meter['player'] = 40
    health_meter['enemy'] = 30

def play_game(health_meter):
    huts = occupy_huts()
    idx = process_user_choice()
    reveal_occupants(idx, huts)
    enter_huts(health_meter, huts, idx)

def print_bold(msg, end='\n'):
    print("\033[1m" + msg + "\033[0m", end=end)

def print_dotted_line(width=72):
    print('-'*width)

def run_application():
    global occupants, width, dotted_line
    keep_playing = 'y'
    health_meter = {}
    occupants = ['enemy', 'friend', 'unoccupied']
    width = 72
    dotted_line = '-' * width

    reset_health_meter(health_meter)
    show_theme_message()
    show_game_mission()
    while keep_playing == 'y':
        reset_health_meter(health_meter)
        play_game(health_meter)
        keep_playing = input("Play again? Yes(y)/No(n):")

if __name__ == '__main__':
    run_application()

