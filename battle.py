"""Just a simulation of Darkest Dungeon battley thingies. To be implemented
in the actual bot once Python decides to stop being such a MASSIVE douchecanoe"""
import json
import random
import units


def main():
    """Main battle simulation."""

    status = "battle"

    heroes = ["leper"]
    enemies = ["ectoplasm"]

    battle = {"heroes": heroes, "enemies": enemies}

    while status == "battle":
        turns_spent = []
        turn = ""
        highest_speed = -10 # Never mind pt. 2
        unit_data = {}

        # This all determines who goes next
        for side in battle:
            for unit in battle[side]:
                if unit in turns_spent:
                    continue

                with open("units/{}.json".format(unit)) as f:
                    data = json.load(f) # I always forget the exact syntax don't bully me >:(

                speed = data["speed"]["base"] + random.randint(-data["speed"]["variance"],
                                                               data["speed"]["variance"])

                if speed > highest_speed:
                    unit_data = data
                    highest_speed = speed
                    turn = unit
                    turns_spent.append(unit) # Will need to be changed later, if more than 1 are here

        # Now that we know who moves first, we decide on an attack
        existing_attacks = []
        for attack in unit_data["attacks"]:
            existing_attacks.append(attack)

        selected_attack = random.choice(existing_attacks)

        # K this is gonna be bad but this is 100% proof of concept don't judge me
        # will change this later

        # Get victim
        other_side = ""
        if turn in battle["heroes"]:
            other_side = "enemies"
        else:
            other_side = "heroes"

        victim = random.choice(battle[other_side])

        # Damage is base damage added to or subtracted to by variance, in
        # addition to the base damage multiplied by modifier. needs fixing because
        # i just realized this is wrong LOL
        damage = (((unit_data["attack"]["base"] +
                    random.randint(-data["attack"]["variance"], data["attack"]["variance"]))) +
                    (unit_data["attacks"][selected_attack]["damage"]["mod"] *
                     unit_data["attack"]["base"]))

        if random.randint(0, 100) <= unit_data["attacks"][selected_attack]["damage"]["crit"]:
            damage = damage * 2 # yes i know it's lower than this

        print ("{} used {}...".format(turn, selected_attack))
        print ("{} damage dealt to {}!".format(int(damage), victim))

        if len(turns_spent) == 2:
            break


        #print ("{} will go first, with a speed of {}!".format(turn, int(highest_speed)))
        #break


if __name__ == "__main__":
    # Da heck if I know how this works
    main()
