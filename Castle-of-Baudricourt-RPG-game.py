import os
import time
import sys


player_currentLocation = "Entrance"
player_inventory = []
monsters_defeated = 0


validRaces = ["dwarf","human","elf"]
validRoles = ["priest","templar","rifleman"]


weapons = {
    "sword"       : {"type": "physical", "bonus":[]},
    "holy staff"  : {"type": "holy", "bonus":["magic"]},
    "rifle"       : {"type": "ranged", "bonus":[]},
    "magic sword" : {"type": "magic", "bonus":["fire"]}
}

class_weapons = {
    "priest": "holy staff",
    "templar": "magic sword",
    "rifleman": "rifle"
}


monsters = {
    "werewolf": {"HP": 100, "SP": 40, "MP": 0, "resistances":["holy","magic"], "weaknesses":["fire","physical"]},
    "phantom": {"HP": 80, "SP": 0, "MP": 60, "resistances":["ranged","physical"], "weaknesses":["holy","magic"]},
    "orc": {"HP": 180, "SP": 50, "MP": 0, "resistances":["holy","fire"], "weaknesses":["magic","physical"]}
}

monster_stats = {}
def getMonsterStats(creature):
    if creature not in monster_stats:
        monster_stats[creature] = monsters[creature].copy()
    return monster_stats[creature]


def player_attributes():
    global player_name, player_race, player_role, player_hp, player_mp, player_sp

    player_name = input("> What is your name?\n").capitalize()

    while True:
        player_race = input("> What race are you? [Human, Dwarf or Elf]\n").lower()
        if player_race in validRaces: break
        print("Invalid! Please choose Human, Dwarf or Elf.\n")

    while True:
        player_role = input("> What role do you want to play? [Priest, Templar or Rifleman]\n").lower()
        if player_role in validRoles: break
        print("Invalid! Please choose Priest, Templar or Rifleman.\n")

    os.system('cls' if os.name=='nt' else 'clear')
    
    if player_race=="human": player_hp, player_mp, player_sp = 100,30,50
    elif player_race=="dwarf": player_hp, player_mp, player_sp = 100,20,60
    elif player_race=="elf": player_hp, player_mp, player_sp = 100,60,30

player_attributes()


Location = {
    "Entrance": {"north":"Gate","item":"sword"},
    "Gate": {"north":"Castle hall","south":"Entrance"},
    "Castle hall": {"item":"Magic sword","east":"Library","west":"Kitchen","north":"Armory","south":"Gate"},
    "Armory": {"south":"Castle hall","creature":"werewolf"},
    "Library": {"west":"Castle hall","creature":"phantom"},
    "Kitchen": {"east":"Castle hall","creature":"orc","item":"HP potion"}
}


def showStatus():
    print("------------------------")
    print(f"Current room: {player_currentLocation}")
    print(f"Inventory: {player_inventory}")
    if "item" in Location[player_currentLocation] and Location[player_currentLocation]["item"]:
        print(f"You see a {Location[player_currentLocation]['item']}")
    if "creature" in Location[player_currentLocation]:
        creature = Location[player_currentLocation]["creature"]
        stats = getMonsterStats(creature)
        print(f"You see a {creature} (HP: {stats['HP']})")
    print(f"Your HP: {player_hp}")
    print("------------------------")     


def equippedWeapon():
    for item in player_inventory:
        if item.lower() in weapons:
            return item.lower()
    return None


def calculateDamage(monsterName):
    stats = getMonsterStats(monsterName)
    weapon = equippedWeapon()
    w_type = weapons[weapon]["type"] if weapon else "physical"
    bonus_types = weapons[weapon]["bonus"] if weapon else []

    base_damage = 0
    modifier = 1.0

    
    if monsterName=="phantom":   
        base_damage = player_mp + player_sp//2
        if weapon in ["holy staff","magic sword"]: modifier += 0.5
        if weapon=="holy staff": modifier += 0.2   
    else:   
        base_damage = player_sp
        if weapon=="sword": modifier += 0.3
        if weapon in ["holy staff","magic sword"] and monsterName=="werewolf": modifier += 0.1

    resist = stats["resistances"]
    weak = stats["weaknesses"]
    if w_type in resist: modifier *= 0.7
    if w_type in weak: modifier *= 1.3
    for b in bonus_types:
        if b in resist: modifier *= 0.85
        if b in weak: modifier *= 1.2

    return int(base_damage * modifier), weapon


def showInstructions():
    messages = [
        f"Welcome to the Castle of Baudricourt!, {player_name}\n",
        "It's said that this castle has been haunted for centuries!\n",
        "Now it's up to you to investigate and face the possible threats!\n",
        "Good luck!!!\n",
        "Commands: go/get/use/attack\n"
    ]
    for msg in messages:
        for char in msg:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.01)
        time.sleep(0.5)

showInstructions()


while True:
    showStatus()
    move = input("> ").split(" ",1)
    os.system('cls' if os.name=='nt' else 'clear')

    if move[0].lower()=="go":
        if move[1] in Location[player_currentLocation]:
            player_currentLocation = Location[player_currentLocation][move[1]]
            print(f"You are now in the {player_currentLocation}")
        else:
            print(f"You can't go {move[1]}!")

    elif move[0].lower()=="get":
        if len(move)<2: print("Get what?")
        else:
            current_item = Location[player_currentLocation].get("item")
            if current_item and current_item.lower()==move[1].lower():
                if current_item.lower() in weapons:
 
                    for i,item in enumerate(player_inventory):
                        if item.lower() in weapons:
                            print(f"You drop your {item} to pick up {current_item}.")
                            Location[player_currentLocation]["item"]=item
                            del player_inventory[i]
                            break
                print(f"You got a {current_item}")
                player_inventory.append(current_item)
                del Location[player_currentLocation]["item"]
            else:
                print("There is no such item here.")

    elif move[0].lower()=="use":
        if len(move)<2: print("Use what?")
        else:
            item_name = move[1].lower()
            inv_lower = [i.lower() for i in player_inventory]
            if item_name in inv_lower:
                if item_name=="hp potion":
                    heal_amount = 50
                    player_hp += heal_amount
                    if player_hp>100: player_hp=100
                    print(f"You used an HP potion and restored {heal_amount} HP. Your HP is now {player_hp}.")
                    index = inv_lower.index(item_name)
                    del player_inventory[index]
                else:
                    print(f"You can't use {move[1]} right now.")
            else:
                print(f"You don't have a {move[1]}.")

    elif move[0].lower()=="attack":
        if len(move)<2: print("Attack what?")
        elif "creature" in Location[player_currentLocation]:
            creature = Location[player_currentLocation]["creature"].lower()
            if move[1].lower()==creature:
                stats = getMonsterStats(creature)
                pre_hp = stats["HP"]

                damage, weapon_used = calculateDamage(creature)
                stats["HP"] -= damage
                print(f"You attacked the {creature} with {weapon_used or 'your fists'}!")
                print(f"{creature} HP: {pre_hp} -> {max(stats['HP'],0)}")

                if stats["HP"]<=0:
                    print(f"The {creature} has been defeated!")
                    del Location[player_currentLocation]["creature"]
                    monsters_defeated +=1

                    monsters_left = any("creature" in loc for loc in Location.values())
                    if not monsters_left:
                        print("\n You have defeated all the monsters in the castle!")
                        break

                else:
                    if creature=="phantom":
                        counter_damage = max(5, stats["MP"]//2 - player_mp//3)
                    else:
                        counter_damage = stats["SP"]//3
                    player_hp -= counter_damage
                    print(f"The {creature} counter-attacks and deals {counter_damage} damage!")
                    if player_hp<=0:
                        print(f"You were killed by the {creature}... Game Over.")
                        break
            else:
                print("That's not the correct target.")
        else:
            print("There is nothing to attack here.")
    else:
        print("Invalid command.")
