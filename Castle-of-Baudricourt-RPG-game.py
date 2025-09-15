import os
import time
import sys
from colorama import init, Fore, Back

init()

player_currentLocation = "Entrance"
player_inventory = []
monsters_defeated = 0
player_xp = 0
gold = 0


hpp1  = 0
hpp2  = 0
spp1  = 0
hpp3  = 0
imun1 = 0


###   Some Upcoming Additions:
###
###   Item Information Search System:
### - Command: "info <item_name>"
### - Output: item description, cost, purpose and additional attributes
###
###   Mob Strength Identification System:
### - Based on the color of the mob’s name
### - Inspired by the mechanics of the game Aika


validRaces        =  ["dwarf","human","elf"]
validRoles        =  ["priest","templar","rifleman"]
validRolesUpgrade =  ["saint", "gladiator", "dinamitator"] ###Class evolution system inspired by Aika. Not functional yet :)

levelXp = [0, 100, 300, 500]

gardenEventTriggered = False
ghostEventTriggered  = False


weapons = {
    "sword"       : {"type": "physical", "bonus":[]},
    "holy staff"  : {"type": "holy", "bonus":["magic"]},
    "rifle"       : {"type": "ranged", "bonus":[]},
    "magic sword" : {"type": "magic", "bonus":["fire"]}
}

class_weapons = {
    "priest":   "holy staff",
    "templar":  "magic sword",
    "rifleman": "rifle",
}

armors = {
    "priest"  : {
        "Armor of Benediction"      : {"bonus": {"HP": +20}}, #Medium Armor
    },
    "saint"   : {
        "Armor of Benediction"      : {"bonus": {"HP": +20}} #Medium Armor
    },
    "templar" : {
        "Armor of the Sacred Cross" : {"bonus": {"HP": +30}} #Heavy Armor
    },
    "gladiator": {
        "Armor of the Sacred Cross" : {"bonus": {"HP": +30}} #Heavy Armor
    },
    "rifleman": {
        "Sharpshooter’s Vest"       : {"bonus": {"HP": +25}} #Light Armor
    }
}


def getArmor(move):
    global player_inventory, player_hp, player_mp, player_sp

    
    if len(move) < 2:
        print("Get what?")
        return

    
    items = Location[player_currentLocation].get("item", [])
    if not isinstance(items, list):
        items = [items]

    
    available_armors = armors.get(player_role, {})


    for item in items:
        if item.lower() == move[1].lower() and item in available_armors:
            player_inventory.append(item)  
            equipArmor(item)               

            if len(items) > 1:
                items.remove(item)
                Location[player_currentLocation]["item"] = items
            else:
                del Location[player_currentLocation]["item"]

            print(f"You got the {item} and equipped it!")
            return

    print("There's no armor for your class here.\n")


def equipArmor(armorName):
    global equippedArmor
    armor_info = armors[player_role].get(armorName)
    if armor_info:
        global player_hp, player_mp, player_sp
        player_hp += armor_info["bonus"].get("HP", 0)



monsters = {
    "werewolf": {"HP": 100,  "SP": 40, "MP": 0,  "XP": 30,  "resistances":["holy","magic"],      "weaknesses": ["fire","physical"]},
    "phantom":  {"HP": 80,   "SP": 0,  "MP": 60, "XP": 20,  "resistances":["ranged","physical"], "weaknesses": ["holy","magic"]},
    "orc":      {"HP": 180,  "SP": 50, "MP": 0,  "XP": 50,  "resistances":["holy","fire"],       "weaknesses": ["magic","physical"]}
}

npcs = {
    "Prince's Ghost": {},    ##NPC1
    "Fairies"       : {}     ##NPC2
}

levels = {
    "level1": {},
    "level2": {
        "human": {"HP": 15, "MP": 10, "SP": 15},
        "dwarf": {"HP": 20, "MP": 10, "SP": 10},
        "elf":   {"HP": 15, "MP": 5,  "SP": 20}
    },
    "level3": {
        "human": {"HP": 30, "MP": 20, "SP": 30},
        "dwarf": {"HP": 40, "MP": 20, "SP": 20},
        "elf":   {"HP": 30, "MP": 10, "SP": 40}
    },
    "level4": {
        "human": {"HP": 60, "MP": 40, "SP": 60},
        "dwarf": {"HP": 80, "MP": 40, "SP": 40},
        "elf":   {"HP": 60, "MP": 20, "SP": 80}
    }
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
    "Entrance": {"north":"Gate","item":"sword", "Locked": False},
    "Gate": {"north":"Castle hall","south":"Entrance", "Locked": False},
    "Castle hall": {"item":"Magic sword","east":"Library","west":"Kitchen","north":"Armory","south":"Gate", "Locked": False},
    "Armory": {"south":"Castle hall","creature":"werewolf", "Locked": False},
    "Library": {"west":"Castle hall","creature":"phantom", "Locked": False},
    "Kitchen": {"east":"Castle hall","creature":"orc","item":"HP potion", "west":"Garden", "Locked": False},
    "Garden": {"north": "Crypt", "Locked": True},
    "Crypt": {}
}

def addXp(amount):
    global player_xp
    player_xp += amount
    check_level()

def check_level():
    if player_xp >= 100:
        print("You're now in level 1!\n")
    elif player_xp >= 300:
        print("You're now in level 2!\n")
    elif player_xp >= 500:
        print("You're now in level 3!\n")    

def showStatus():
    print("------------------------")
    print(f"Current room: {player_currentLocation}")
    print(f"Inventory: {player_inventory}")
    print(f"XP: {player_xp} / {levelXp[1]}")
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



def npcDialogue(npcName):
    if npcName == "Prince's Ghost":
        print("A ghost has appeared!")
        while True:
            print("Dialogue options:")
            print("[ 1 ] - Who are you?")
            print("[ 2 ] - Prepare to die!")

            choice1 = input("> ")

            if choice1 == "1":
                print("Ghost: I'm the old owner of this Castle. Now you killed the monsters, I'm free again!")
                print("[ 1 ] - You: Do you want me to do something to help you?")
                choice2 = input("> ")
                if choice2 == "1":
                        print("Ghost: Yes... I need you to go the garden and burn my coffin, so I can rest in peace forever! You're gonna need this...\n")
                        print("Now you got a key and a torch!\n")
                        player_inventory.append("Key")  
                        player_inventory.append("Torch") 
                        Location["Garden"]["Locked"] = False
                        break
                        
                if choice2 == "2":
                        print("You: Do you want me to do something to help you?")
                        print("Ghost: Yes... I need you to go the garden and burn my coffin, so I can rest in peace forever! You're gonna need this...\n")
                        print("Now you got a key and a torch!\n")
                        player_inventory.append("Key")   
                        player_inventory.append("Torch")
                        Location["Garden"]["Locked"] = False
                        break    
                    
            elif choice1 == "2":
                print("Ghost: I'm not here to fight you")
                print("[ 1 ] - Who are you?")
                choice3 = input("> ")
                if choice3 == "1":
                    print("Ghost: I'm the old owner of this Castle. Now you killed the monsters, I'm free again!")
                    print("[ 1 ] Do you want me to do something to help you?")
                    choice4 = input("> ")
                    if choice4 == "1":
                        print("Ghost: Yes... I need you to go the garden and burn my coffin, so I can rest in peace forever! You're gonna need this...\n")
                        print("Now you got a key and a torch!\n")
                        player_inventory.append("Key")   
                        player_inventory.append("Torch") 
                        Location["Garden"]["Locked"] = False
                        break
            else:
                print("Invalid option. Try again!")        



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
            if Location[Location[player_currentLocation][move[1]]]["Locked"]:
                print("You need a key to open this door!")
            else: 
                player_currentLocation = Location[player_currentLocation][move[1]]
                print(f"You are now in the {player_currentLocation}")
                gardenEventTriggered = True
                
                if player_currentLocation == "Garden" and gardenEventTriggered:
                    player_inventory.remove("Key")
                    print("You step into an ancient garden. Towering trees whisper forgotten secrets, and the air is fragrant with giant, beautiful flowers.")
                    print("Moss-covered stones and winding paths hint at primordial magic, a beauty untouched yet eternal.\n")
                    print("What do you wanna do?")
                    print("[ 1 ] To explore the place!\n")

                    explore1 = input("> ")
                    if explore1 == "1":
                        print("You found a ancient wooden chest. \n")
                        chest1 = input("Do you want to open it? [Yes/No]")
                        if chest1.lower() == "yes":
                            chestEventTriggered = True
                            foundArmor = list(armors[player_role].keys())[0]
                            player_inventory.append(foundArmor)
                            print(f"You found a {foundArmor} inside!\n")
                        else:
                            break
                    else:
                        print("Invalid command!")        
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

                elif item_name == "Torch":
                    if player_currentLocation == "Crypt":
                        print("You set the coffin on fire!\n")
                        player_inventory.remove("Torch")
                        print("Quest completed!")
                        addXp(30)
                        gold += 30
                    else:
                        print("You can't use the torch here!\n")    

                else:
                    print(f"You can't use {move[1]} right now.")
            else:
                print(f"You don't have a {move[1]}.")

                

    elif move[0].lower() == "b":
        price1 = 30 
        price2 = 60
        price3 = 90
        price4 = 90
        price5 = 150

        if player_xp >= 500:
            print("Based on your level, you can buy:")
            print(f"[ 1 ] HP potion. [Only 2 available. Price: {price4}]")
            print(f"[ 2 ] Imunity potion. [Only 1 available. Price: {price5}]")
        elif player_xp >= 300:
            print("Based on your level, you can buy:")
            print(f"[ 1 ] HP potion. [Only 2 available. Price: {price2}]")
            print(f"[ 2 ] Strength potion. [Only 1 available. Price: {price3}]")
        elif player_xp >= 100:
            print("Based on your level, you can buy:")
            print(f"[ 1 ] HP potion. [Only 1 available. Price: {price1}]")
        else:
            print("No items available for your level.")
            continue

        choice = input("Choose an item number to buy!\n")

        if player_xp >= 500:
            if choice == "1":
                if hpp3 < 2:
                    if gold >= price4:
                        print("You bought a HP potion!\n")
                        player_inventory.append("HP potion")
                        gold -= price4
                        hpp3 += 1
                    else:
                        print("Not enough gold!\n")
                else:
                    print("You already bought the maximum HP potions for your level.\n")
            elif choice == "2":
                if imun1 < 1:
                    if gold >= price5:
                        print("You bought an Imunity potion!\n")
                        player_inventory.append("Imunity potion")
                        gold -= price5
                        imun1 += 1
                    else:
                        print("Not enough gold!\n")
                else:
                    print("You already bought the maximum Imunity potions for your level.\n")
            else:
                print("Invalid choice.\n")

        elif player_xp >= 300:
            if choice == "1":
                if hpp2 < 2:
                    if gold >= price2:
                        print("You bought a HP potion!\n")
                        player_inventory.append("HP potion")
                        gold -= price2
                        hpp2 += 1
                    else:
                        print("Not enough gold!\n")
                else:
                    print("You already bought the maximum HP potions for your level.\n")
            elif choice == "2":
                if spp1 < 1:
                    if gold >= price3:
                        print("You bought a Strength potion!\n")
                        player_inventory.append("Strength potion")
                        gold -= price3
                        spp1 += 1
                    else:
                        print("Not enough gold!\n")
                else:
                    print("You already bought the maximum Strength potions for your level.\n")
            else:
                print("Invalid choice.\n")

        elif player_xp >= 100:
            if choice == "1":
                if hpp1 < 1:
                    if gold >= price1:
                        print("You bought a HP potion!\n")
                        player_inventory.append("HP potion")
                        gold -= price1
                        hpp1 += 1
                    else:
                        print("Not enough gold!\n")
                else:
                    print("You already bought the maximum HP potions for your level.\n")
            else:
                print("Invalid choice.\n")

                              
    elif move[0].lower() == "attack":
        if len(move) < 2:
            print("Attack what?")
        elif "creature" in Location[player_currentLocation]:
            creature = Location[player_currentLocation]["creature"].lower()

            if move[1].lower() == creature:
                stats = getMonsterStats(creature)
                pre_hp = stats["HP"]

                damage, weapon_used = calculateDamage(creature)
                stats["HP"] -= damage
                print(f"You attacked the {creature} with {weapon_used or 'your fists'}!")
                print(f"{creature} HP: {pre_hp} -> {max(stats['HP'], 0)}")

                if stats["HP"] <= 0:
                    print(f"The {creature} has been defeated!")
                    del Location[player_currentLocation]["creature"]
                    addXp(monsters[creature]["XP"])
                    print(f"You gained {monsters[creature]['XP']} XP! Total XP: {player_xp}")

                    monsters_left = any("creature" in loc for loc in Location.values())
                    if not monsters_left:
                        print("A ghostly presence fills the air...")
                        npcDialogue("Prince's Ghost")

                else:
                    if creature == "phantom":
                        counter_damage = max(5, stats["MP"] // 2 - player_mp // 3)
                    else:
                        counter_damage = stats["SP"] // 3
                    player_hp -= counter_damage
                    print(f"The {creature} counter-attacks and deals {counter_damage} damage!")

                    if player_hp <= 0:
                        print(f"You were killed by the {creature}... Game Over.")
                        break
            else:
                print("That's not the correct target.")
        else:
            print("There is nothing to attack here.")
