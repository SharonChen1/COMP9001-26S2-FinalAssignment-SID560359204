'''
Saving Ending history and best ticket game reaction time
'''

ENDING_TITLES = {
    "boss_ending": "Overtime to VIP!",
    "help_ending": "An Unexpected VIP Invitation!",
    "concert_ending": "Finally, Here You Are!"
}


def load_endings():
    '''Load valid, unique endings or return an empty list if missing.'''    
    endings = []

    try:
        file = open("endings.txt", "r")
    except FileNotFoundError:
        return endings #first play not have ending record yet


    for line in file:
        ending = line.strip()

        if ending not in ENDING_TITLES:
            continue

        if ending not in endings:
            endings.append(ending)

    file.close()

    return endings


def save_endings(endings):
    '''Save unlocked endings.'''

    file = open("endings.txt", "w")
   
    for ending in endings:
        file.write(ending + "\n")

    file.close()

    return True

def load_best_time():
    '''Load the best reaction time.'''
    try:
        file = open("best_time.txt", "r")
    except FileNotFoundError:
        return None

    try:
        best_time = float(file.read().strip())

        # A valid record must be between 0 and 1 second.
        if not 0 <= best_time <= 1:
            raise ValueError("Invalid reaction record.")

    except ValueError:
        print("Invalid reaction record. Starting without a record.")
        file.close()
        return None

    file.close()

    return best_time


def save_best_time(best_time):
    '''Save the best reaction time.'''
    file = open("best_time.txt", "w")

    file.write(str(best_time))


    file.close()

    return True