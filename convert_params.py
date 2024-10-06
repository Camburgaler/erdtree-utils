import csv
import json
import logging
import os
import sys

from corrections import IGNORED, IGNORED_WEAPON_INFUSIONS, MISSING, STAT_BUFFS

open('tmp.log', 'w').close()
file_handler = logging.FileHandler(filename='tmp.log')
stdout_handler = logging.StreamHandler(stream=sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    level=logging.DEBUG, 
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=handlers
)

logger = logging.getLogger('DEBUG')
logger.info( 'Logging now setup.' )

INFUSIONS = [
    "Standard ",
    "Heavy ",
    "Keen ",
    "Quality ",
    "Magic ",
    "Fire ",
    "Flame Art ",
    "Lightning ",
    "Sacred ",
    "Poison ",
    "Blood ",
    "Cold ",
    "Occult ",
]

WEAPON_CATEGORIES = {
    1: "dagger",
    2: "straight-sword",
    3: "greatsword",
    4: "colossal-sword",
    5: "thrusting-sword",
    6: "heavy-thrusting-sword",
    7: "curved-sword",
    8: "curved-greatsword",
    9: "katana",
    10: "twinblade",
    11: "hammer",
    12: "great-hammer",
    13: "flail",
    14: "axe",
    15: "greataxe",
    16: "spear",
    17: "great-spear",
    18: "halberd",
    19: "scythe",
    20: "whip",
    21: "fist",
    22: "claw",
    23: "colossal-weapon",
    24: "torch",
    30: "small-shield",
    31: "medium-shield",
    32: "greatshield",
    33: "glintstone-staff",
    34: "sacred-seal",
    40: "light-bow",
    41: "bow",
    42: "greatbow",
    43: "crossbow",
    44: "ballista",
    60: "hand-to-hand-art",
    61: "perfume-bottle",
    62: "thrusting-shield",
    63: "throwing-blade",
    64: "backhand-blade",
    66: "great-katana",
    67: "light-greatsword",
    68: "beast-claw",
}

def main():

    global helmets
    helmets = {}
    global chestpieces
    chestpieces = {}
    global gauntlets
    gauntlets = {}
    global leggings
    leggings = {}
    global talismans
    talismans = {}
    global classes
    classes = {}
    global weapons
    weapons = {}
    global infusions
    infusions = {}
    global calculations
    calculations = {}

    # armors
    with open("input/EquipParamProtector.csv") as af:
        rows = list(csv.DictReader(af, delimiter=","))

        for armor in rows:
            if not ignored(armor):
                process_armor_piece(armor)

    # talismans
    with (
        open("input/EquipParamAccessory.csv") as tf,
        open("input/SpEffectParam.csv") as ef,
    ):

        effects = list(csv.DictReader(ef, delimiter=","))
        rows = list(csv.DictReader(tf, delimiter=","))

        for talisman in rows:
            if not ignored(talisman):
                process_talisman(talisman, effects)

    # classes
    classes = [
        {
            "id": "vagabond",
            "name": "Vagabond",
            "level": 9,
            "stats": {"VIG": 15, "MND": 10, "END": 11, "STR": 14, "DEX": 13, "INT": 9, "FTH": 9, "ARC": 7},
        },
        {
            "id": "warrior",
            "name": "Warrior",
            "level": 8,
            "stats": {"VIG": 11, "MND": 12, "END": 11, "STR": 10, "DEX": 16, "INT": 10, "FTH": 8, "ARC": 9},
        },
        {
            "id": "hero",
            "name": "Hero",
            "level": 7,
            "stats": {"VIG": 14, "MND": 9, "END": 12, "STR": 16, "DEX": 9, "INT": 7, "FTH": 8, "ARC": 11},
        },
        {
            "id": "bandit",
            "name": "Bandit",
            "level": 5,
            "stats": {"VIG": 10, "MND": 11, "END": 10, "STR": 9, "DEX": 13, "INT": 9, "FTH": 8, "ARC": 14},
        },
        {
            "id": "astrologer",
            "name": "Astrologer",
            "level": 6,
            "stats": {"VIG": 9, "MND": 15, "END": 9, "STR": 8, "DEX": 12, "INT": 16, "FTH": 7, "ARC": 9},
        },
        {
            "id": "prophet",
            "name": "Prophet",
            "level": 7,
            "stats": {"VIG": 10, "MND": 14, "END": 8, "STR": 11, "DEX": 10, "INT": 7, "FTH": 16, "ARC": 10},
        },
        {
            "id": "samurai",
            "name": "Samurai",
            "level": 9,
            "stats": {"VIG": 12, "MND": 11, "END": 13, "STR": 12, "DEX": 15, "INT": 9, "FTH": 8, "ARC": 8},
        },
        {
            "id": "prisoner",
            "name": "Prisoner",
            "level": 9,
            "stats": {"VIG": 11, "MND": 12, "END": 11, "STR": 11, "DEX": 14, "INT": 14, "FTH": 6, "ARC": 9},
        },
        {
            "id": "confessor",
            "name": "Confessor",
            "level": 10,
            "stats": {"VIG": 10, "MND": 13, "END": 10, "STR": 12, "DEX": 12, "INT": 9, "FTH": 14, "ARC": 9},
        },
        {
            "id": "wretch",
            "name": "Wretch",
            "level": 1,
            "stats": {"VIG": 10, "MND": 10, "END": 10, "STR": 10, "DEX": 10, "INT": 10, "FTH": 10, "ARC": 10},
        },
    ]

    # infusions
    with open("input/ReinforceParamWeapon.csv") as inf:
        rows = list(csv.DictReader(inf, delimiter=","))

        extract_infusions(rows)

    # weapons
    with (
        open("input/AttackElementCorrectParam.csv") as af,
        open("input/EquipParamWeapon.csv") as wf,
        open("input/CalcCorrectGraph.csv") as cf,
        open("input/SpEffectParam.csv") as sf,
    ):

        rows = list(csv.DictReader(wf, delimiter=","))
        rows = [row for row in rows if 1000000 <= int(row["ID"]) <= 44010000 or 60500000 <= int(row["ID"]) <= 68510000]

        masks = list(csv.DictReader(af, delimiter=","))
        masks = {row["ID"]: row for row in masks}

        softcaps = list(csv.DictReader(cf, delimiter=","))
        softcaps = {
            row["ID"]: row for row in softcaps if 0 <= int(row["ID"]) <= 16
        }

        effects = list(csv.DictReader(sf, delimiter=","))
        effects = {row["ID"]: row for row in effects}

        for row in rows:
            if not ignored(row):
                process_weapon(row, masks, effects)

        process_damage(softcaps)

    # add missing items
    helmets.update(MISSING["helmets"])
    chestpieces.update(MISSING["chestpieces"])
    gauntlets.update(MISSING["gauntlets"])
    leggings.update(MISSING["leggings"])

    # sort all files
    helmets = dict(sorted(helmets.items(), key=lambda item: item[0]))
    chestpieces = dict(sorted(chestpieces.items(), key=lambda item: item[0]))
    gauntlets = dict(sorted(gauntlets.items(), key=lambda item: item[0]))
    leggings = dict(sorted(leggings.items(), key=lambda item: item[0]))
    classes = sorted(classes, key=lambda item: item["level"])
    weapons = dict(sorted(weapons.items(), key=lambda item: item[0]))

    # add none cases (no helmet etc.)
    helmets = {
        "no-helmet": {
            "id": "no-helmet",
            "name": "No helmet",
            "defenses": {"physical": 0, "strike": 0, "slash": 0, "pierce": 0, "magic": 0, "fire": 0, "lightning": 0, "holy": 0},
            "resistances": {"poison": 0, "scarletRot": 0, "hemorrhage": 0, "frostbite": 0, "sleep": 0, "madness": 0, "deathBlight": 0},
            "poise": 0,
            "weight": 0,
        },
        **helmets,
    }
    chestpieces = {
        "no-chestpiece": {
            "id": "no-chestpiece",
            "name": "No chestpiece",
            "defenses": {"physical": 0, "strike": 0, "slash": 0, "pierce": 0, "magic": 0, "fire": 0, "lightning": 0, "holy": 0},
            "resistances": {"poison": 0, "scarletRot": 0, "hemorrhage": 0, "frostbite": 0, "sleep": 0, "madness": 0, "deathBlight": 0},
            "poise": 0,
            "weight": 0,
        },
        **chestpieces,
    }
    gauntlets = {
        "no-gauntlets": {
            "id": "no-gauntlets",
            "name": "No gauntlets",
            "defenses": {"physical": 0, "strike": 0, "slash": 0, "pierce": 0, "magic": 0, "fire": 0, "lightning": 0, "holy": 0},
            "resistances": {"poison": 0, "scarletRot": 0, "hemorrhage": 0, "frostbite": 0, "sleep": 0, "madness": 0, "deathBlight": 0},
            "poise": 0,
            "weight": 0,
        },
        **gauntlets,
    }
    leggings = {
        "no-leggings": {
            "id": "no-leggings",
            "name": "No leggings",
            "defenses": {"physical": 0, "strike": 0, "slash": 0, "pierce": 0, "magic": 0, "fire": 0, "lightning": 0, "holy": 0},
            "resistances": {"poison": 0, "scarletRot": 0, "hemorrhage": 0, "frostbite": 0, "sleep": 0, "madness": 0, "deathBlight": 0},
            "poise": 0,
            "weight": 0,
        },
        **leggings,
    }
    talismans = {
        "no-talisman": {
            "id": "no-talisman",
            "name": "No talisman",
        },
        **talismans,
    }
    weapons = {
        "unarmed": {
            "id": "unarmed",
            "name": "Unarmed",
            "requirements": {"STR": 0, "DEX": 0, "INT": 0, "FTH": 0, "ARC": 0},
            "category": "fist",
            "unique": False,
            "paired": False,
            "glintstone-staff": False,
            "sacred-seal": False,
            "infusions": {
                "standard": {
                    "id": "standard",
                    "damage": {
                        "physical": 20,
                        "magic": 0,
                        "fire": 0,
                        "lightning": 0,
                        "holy": 0
                    },
                    "scaling": {
                        "STR": 0.029,
                        "DEX": 0.029,
                        "INT": 0.0,
                        "FTH": 0.0,
                        "ARC": 0.0
                    },
                "masks": {
                    "physical": {
                        "STR": True,
                        "DEX": True,
                        "INT": False,
                        "FTH": False,
                        "ARC": False
                    },
                    "magic": {
                        "STR": False,
                        "DEX": False,
                        "INT": True,
                        "FTH": False,
                        "ARC": False
                    },
                    "fire": {
                        "STR": False,
                        "DEX": False,
                        "INT": False,
                        "FTH": True,
                        "ARC": False
                    },
                    "lightning": {
                        "STR": False,
                        "DEX": True,
                        "INT": False,
                        "FTH": False,
                        "ARC": False
                    },
                    "holy": { "STR": False, "DEX": False, "INT": False, "FTH": True, "ARC": False }
                },
                "corrections": {
                    "physical": "0",
                    "magic": "0",
                    "fire": "0",
                    "lightning": "0",
                    "holy": "0",
                    "poison": "0",
                    "blood": "0",
                    "sleep": "0",
                    "madness": "0"
                },
                }
            },
        },
        **weapons,
    }

    # save to files
    with (
        open("output/helmets.json", "w") as hf,
        open("output/chestpieces.json", "w") as cf,
        open("output/gauntlets.json", "w") as gf,
        open("output/leggings.json", "w") as lf,
        open("output/talismans.json", "w") as tf,
        open("output/classes.json", "w") as scf,
        open("output/weapons.json", "w") as wf,
        open("output/infusions.json", "w") as inf,
        open("output/damage.json", "w") as df,
    ):
        json.dump(helmets, hf)
        json.dump(chestpieces, cf)
        json.dump(gauntlets, gf)
        json.dump(leggings, lf)
        json.dump(talismans, tf)
        json.dump(classes, scf)
        json.dump(weapons, wf)
        json.dump(infusions, inf)
        json.dump(calculations, df)

    # format output files with prettier
    if os.system("prettier output --write --tab-width 4") != 0:
        print(
            "please install prettier (the code formatting tool) to auto-format the output files after generating"
        )


def ignored(row):
    id = to_kebab(row["Name"])
    return id.startswith("type-") or id in IGNORED


def to_kebab(name):
    return (
        name.lower()
        .replace("(", "")
        .replace(")", "")
        .replace("'", "")
        .strip()
        .replace(" ", "-")
    )


def process_armor_piece(row):
    item = {}

    id = to_kebab(row["Name"])
    item["id"] = id
    item["name"] = row["Name"]

    if id in STAT_BUFFS:
        item["stats"] = STAT_BUFFS[id]

    item["defenses"] = {};
    item["defenses"]["physical"] = round((1.0 - float(row["neutralDamageCutRate"])) * 100.0, 2); # Physical Absorption
    item["defenses"]["slash"] = round((1.0 - float(row["slashDamageCutRate"])) * 100.0, 2); # Slash Absorption
    item["defenses"]["strike"] = round((1.0 - float(row["blowDamageCutRate"])) * 100.0, 2); # Strike Absorption
    item["defenses"]["pierce"] = round((1.0 - float(row["thrustDamageCutRate"])) * 100.0, 2); # Pierce Absorption
    item["defenses"]["magic"] = round((1.0 - float(row["magicDamageCutRate"])) * 100.0, 2); # Magic Absorption
    item["defenses"]["fire"] = round((1.0 - float(row["fireDamageCutRate"])) * 100.0, 2); # Fire Absorption
    item["defenses"]["lightning"] = round((1.0 - float(row["thunderDamageCutRate"])) * 100.0, 2); # Lightning Absorption
    item["defenses"]["holy"] = round((1.0 - float(row["darkDamageCutRate"])) * 100.0, 2); # Holy Absorption

    item["resistances"] = {};
    item["resistances"]["scarletRot"] = int(row["resistDisease"]); # Scarlet Rot Resistance
    item["resistances"]["poison"] = int(row["resistPoison"]); # Poison Resistance
    item["resistances"]["hemorrhage"] = int(row["resistBlood"]); # Hemorrhage Resistance
    item["resistances"]["frostbite"] = int(row["resistFreeze"]); # Frostbite Resistance
    item["resistances"]["sleep"] = int(row["resistSleep"]); # Sleep Resistance
    item["resistances"]["madness"] = int(row["resistMadness"]); # Madness Resistance
    item["resistances"]["deathBlight"] = int(row["resistCurse"]); # Death Blight Resistance

    item["poise"] = int(round(float(row["toughnessCorrectRate"]) * 1000.0, 2)) # Poise
    item["weight"] = round(float(row["weight"]), 2)

    if row["headEquip"] == '1':
        helmets[id] = item
    elif row["bodyEquip"] == '1':
        chestpieces[id] = item
    elif row["armEquip"] == '1':
        gauntlets[id] = item
    elif row["legEquip"] == '1':
        leggings[id] = item


def process_talisman(row, effects):
    item = {}

    id = to_kebab(row["Name"])
    item["id"] = id
    item["name"] = row["Name"]

    item["weight"] = row["weight"]

    effect_id = row["refId"]
    for effect in effects:
        if effect["ID"] == effect_id:
            item["stats"] = {};
            item["stats"]["VIG"] = int(effect["addLifeForceStatus"]); # Vigor
            item["stats"]["MND"] = int(effect["addWillpowerStatus"]); # Mind
            item["stats"]["END"] = int(effect["addEndureStatus"]); # Endurance
            item["stats"]["STR"] = int(effect["addStrengthStatus"]); # Strength
            item["stats"]["DEX"] = int(effect["addDexterityStatus"]); # Dexterity
            item["stats"]["INT"] = int(effect["addMagicStatus"]); # Intelligence
            item["stats"]["FTH"] = int(effect["addFaithStatus"]); # Faith
            item["stats"]["ARC"] = int(effect["addLuckStatus"]); # Arcane
            item["multipliers"] = {};
            item["multipliers"]["maxHp"] = float(effect["maxHpRate"]); # Max HP
            item["multipliers"]["maxFp"] = float(effect["maxMpRate"]); # Max FP
            item["multipliers"]["maxStamina"] = float(effect["maxStaminaRate"]); # Max Stamina
            item["multipliers"]["equipLoad"] = float(effect["equipWeightChangeRate"]); # Equip Load

    if item["stats"] == {
            "VIG": 0,
            "MND": 0,
            "END": 0,
            "STR": 0,
            "DEX": 0,
            "INT": 0,
            "FTH": 0,
            "ARC": 0}:
        item.pop("stats")
    if all(mult == 1.0 for mult in item["multipliers"]):
        item.pop("multipliers")

    talismans[id] = item


def split_weapon_name(name):
    infusion = "standard"
    for other in INFUSIONS:
        if "Fire Knight's" in name:
            if len(name.split()) >= 4 and (name.split()[2] == other.strip() or ' '.join(name.split()[2:4]) == other.strip()):
                infusion = other
                name = name.split()
                while len(name) > 3: name.pop(2)
                name = " ".join(name)  
        elif "Bloody" in name and not to_kebab(name) in IGNORED_WEAPON_INFUSIONS:
            name = name.replace("Bloody ", "")
            infusion = "blood"
        elif "celebrants-cleaver-blades" in to_kebab(name):
            name = "Celebrant's Cleaver"
        elif other in name and not to_kebab(name) in IGNORED_WEAPON_INFUSIONS:
            infusion = other
            name = name.replace(infusion, "")

    return name.strip().replace("  ", " "), to_kebab(infusion)


def to_mask(str):
    if str == "1":
        return True
    else:
        return False


def process_weapon(row, masks, effects):
    name, infusion = split_weapon_name(row["Name"])
    id = to_kebab(name)

    damage = {
        "physical": int(row["attackBasePhysics"]),
        "magic": int(row["attackBaseMagic"]),
        "fire": int(row["attackBaseFire"]),
        "lightning": int(row["attackBaseThunder"]),
        "holy": int(row["attackBaseDark"]),
    }

    scaling = {
        "STR": float(row["correctStrength"]) / 100.0,
        "DEX": float(row["correctAgility"]) / 100.0,
        "INT": float(row["correctMagic"]) / 100.0,
        "FTH": float(row["correctFaith"]) / 100.0,
        "ARC": float(row["correctLuck"]) / 100.0,
    }

    mask_id = row["attackElementCorrectId"]
    mask_row = masks[mask_id]

    weapon_masks = {
        "physical": {  # Does Physical Damage Scale With...
            "STR": to_mask(mask_row["isStrengthCorrect_byPhysics"]),
            "DEX": to_mask(mask_row["isDexterityCorrect_byPhysics"]),
            "INT": to_mask(mask_row["isMagicCorrect_byPhysics"]), 
            "FTH": to_mask(mask_row["isFaithCorrect_byPhysics"]),
            "ARC": to_mask(mask_row["isLuckCorrect_byPhysics"]), 
        },
        "magic": {   # Does Magic Damage Scale With...
            "STR": to_mask(mask_row["isStrengthCorrect_byMagic"]), 
            "DEX": to_mask(mask_row["isDexterityCorrect_byMagic"]), 
            "INT": to_mask(mask_row["isMagicCorrect_byMagic"]),
            "FTH": to_mask(mask_row["isFaithCorrect_byMagic"]), 
            "ARC": to_mask(mask_row["isLuckCorrect_byMagic"]), 
        },
        "fire": {  # Does Fire Damage Scale With...
            "STR": to_mask(mask_row["isStrengthCorrect_byFire"]), 
            "DEX": to_mask(mask_row["isDexterityCorrect_byFire"]), 
            "INT": to_mask(mask_row["isMagicCorrect_byFire"]), 
            "FTH": to_mask(mask_row["isFaithCorrect_byFire"]), 
            "ARC": to_mask(mask_row["isLuckCorrect_byFire"]), 
        },
        "lightning": {  # Does Lightning Damage Scale With...
            "STR": to_mask(mask_row["isStrengthCorrect_byThunder"]),
            "DEX": to_mask(mask_row["isDexterityCorrect_byThunder"]), 
            "INT": to_mask(mask_row["isMagicCorrect_byThunder"]), 
            "FTH": to_mask(mask_row["isFaithCorrect_byThunder"]), 
            "ARC": to_mask(mask_row["isLuckCorrect_byThunder"]),
        },
        "holy": {  # Does Holy Damage Scale With...
            "STR": to_mask(mask_row["isStrengthCorrect_byDark"]), 
            "DEX": to_mask(mask_row["isDexterityCorrect_byDark"]), 
            "INT": to_mask(mask_row["isMagicCorrect_byDark"]), 
            "FTH": to_mask(mask_row["isFaithCorrect_byDark"]),
            "ARC": to_mask(mask_row["isLuckCorrect_byDark"]), 
        },
    }

    corrections = {
        "physical": row["correctType_Physics"],
        "magic": row["correctType_Magic"],
        "fire": row["correctType_Fire"],
        "lightning": row["correctType_Thunder"],
        "holy": row["correctType_Dark"], 
        "poison": row["correctType_Poison"], 
        "blood": row["correctType_Blood"], 
        "sleep": row["correctType_Sleep"], 
        "madness": row["correctType_Madness"], 
    }

    paired = '1' in row["isDualBlade"]
    buffable = '1' in row["isEnhance"]
    isGlinststoneStaff = '1' in row["enableMagic"]
    isSacredSeal = '1' in row["enableMiracle"]

    # Auxiliary Effects (blood, poison)
    aux = {}
    for aux_id in [row["spEffectBehaviorId0"], row["spEffectBehaviorId1"]]:
        if int(aux_id) != -1:
            if int(aux_id) > 5000000:
                aux_name = effects[aux_id]["Name"]
                if "Hemorrhage" in aux_name:
                    aux["blood"] =  aux_id
                elif "Frostbite" in aux_name:
                    aux["frost"] = aux_id
                elif "Poison" in aux_name:
                    aux["poison"] = aux_id
                elif "Scarlet Rot" in aux_name:
                    aux["scarlet-rot"] = aux_id
                elif "Madness" in aux_name:
                    aux["madness"] = aux_id
            elif int(aux_id) > 100000:
                aux_name = effects[aux_id]["Name"]
                # standard_upgrade_effect_range = [x for x in range(0, 26)]
                # standard_upgrade_effects = [effects[str(int(aux_id) + x)] for x in standard_upgrade_effect_range]
                standard_upgrade_effects = [effects[aux_id], effects[str(int(aux_id) + 25)]]

                if "Hemorrhage" in aux_name or int(effects[aux_id]["bloodAttackPower"]) > 0:
                    type = "blood"
                    standard_upgrade_effects = [int(y["bloodAttackPower"]) for y in standard_upgrade_effects]
                elif "Frostbite" in aux_name or int(effects[aux_id]["freezeAttackPower"]) > 0:
                    type = "frost"
                    standard_upgrade_effects = [int(y["freezeAttackPower"]) for y in standard_upgrade_effects]
                elif "Poison" in aux_name or int(effects[aux_id]["poizonAttackPower"]) > 0:
                    type = "poison"
                    standard_upgrade_effects = [int(y["poizonAttackPower"]) for y in standard_upgrade_effects]
                elif "Scarlet Rot" in aux_name:
                    type = "scarlet-rot"
                    standard_upgrade_effects = [int(y["diseaseAttackPower"]) for y in standard_upgrade_effects]
                elif "Madness" in aux_name:
                    type = "madness"
                    standard_upgrade_effects = [int(y["madnessAttackPower"]) for y in standard_upgrade_effects]
                elif "Sleep" in aux_name:
                    type = "sleep"
                    standard_upgrade_effects = [int(y["sleepAttackPower"]) for y in standard_upgrade_effects]
                elif "Blight" in aux_name:
                    type = "blight"
                    standard_upgrade_effects = [int(y["curseAttackPower"]) for y in standard_upgrade_effects]
                aux[type] = standard_upgrade_effects
            elif int(aux_id) <= 100000:
                aux_name = effects[aux_id]["Name"]
                if "Hemorrhage" in aux_name:
                    type = "blood"
                    base = effects[aux_id]["bloodAttackPower"]
                elif "Frostbite" in aux_name:
                    type = "frost"
                    base = effects[aux_id]["freezeAttackPower"]
                elif "Poison" in aux_name:
                    type = "poison"
                    base = effects[aux_id]["poizonAttackPower"]
                elif "Scarlet Rot" in aux_name:
                    type = "scarlet-rot"
                    base = effects[aux_id]["diseaseAttackPower"]
                elif "Madness" in aux_name:
                    type = "madness"
                    base = effects[aux_id]["madnessAttackPower"]
                elif "Sleep" in aux_name:
                    type = "sleep"
                    base = effects[aux_id]["sleepAttackPower"]
                elif "Blight" in aux_name:
                    type = "blight"
                    base = effects[aux_id]["curseAttackPower"]
                aux[type] = [int(base), int(base)]

    if id in weapons:
        if not id in IGNORED_WEAPON_INFUSIONS:
            weapon = weapons[id]
            weapon["infusions"][infusion] = {
                "id": infusion,
                "damage": damage,
                "scaling": scaling,
                "aux": aux,
                "masks": weapon_masks,
                "corrections": corrections,
                "buffable": True if buffable and infusion in ["standard", "heavy", "keen", "quality"] else False,
            }
        return
    else:
        weapon = {}

        weapon["id"] = id
        weapon["name"] = name

        weapon["requirements"] = {
            "STR": int(row["properStrength"]), # STR
            "DEX": int(row["properAgility"]), # DEX
            "INT": int(row["properMagic"]), # INT
            "FTH": int(row["properFaith"]), # FTH
            "ARC": int(row["properLuck"]), # ARC
        }

        weapon["category"] = WEAPON_CATEGORIES[int(row["ID"]) // 1000000]

        if int(row["reinforceTypeId"]) == 2200:
            weapon["unique"] = True
        else:
            weapon["unique"] = False
        
        weapon["paired"] = paired
        weapon["glintstone-staff"] = isGlinststoneStaff
        weapon["sacred-seal"] = isSacredSeal

        weapon["infusions"] = {}
        weapon["infusions"][infusion] = {
            "id": infusion,
            "damage": damage,
            "scaling": scaling,
            "aux": aux,
            "masks": weapon_masks,
            "corrections": corrections,
            "buffable": buffable,
        }

        weapons[id] = weapon


def regression(xs, ys):
    # least-squares sum regression
    n = len(xs)
    xy = sum([x * y for x, y in zip(xs, ys)])  # sum of all x * y
    xsq = sum([x * x for x in xs])  # sum of all squared xs

    a = (n * xy - sum(xs) * sum(ys)) / (n * xsq - sum(xs) ** 2) # slope
    b = ys[0] # intercept

    return round(a, 5), b


def extract_infusions(rows):
    for i, ty in enumerate(INFUSIONS):
        infusion = {}
        id = to_kebab(ty)

        infusion["id"] = id
        infusion["name"] = ty.strip()

        relevant = [row for row in rows[0 + i + i * 25 : 26 + i + i * 25]]

        xs = [x for x in range(0, 26)]

        # damage & upgrade
        physical = [float(relevant[i]["physicsAtkRate"]) for i in range(0, 26)]
        magic = [float(relevant[i]["magicAtkRate"]) for i in range(0, 26)]
        fire = [float(relevant[i]["fireAtkRate"]) for i in range(0, 26)]
        lightning = [float(relevant[i]["thunderAtkRate"]) for i in range(0, 26)]
        holy = [float(relevant[i]["darkAtkRate"]) for i in range(0, 26)]

        infusion["damageUpgradeRate"] = {
            "physical": physical,
            "magic": magic,
            "fire": fire,
            "lightning": lightning,
            "holy": holy,
        }

        # scaling
        strength = [float(relevant[i]["correctStrengthRate"]) for i in range(0, 26)]
        dexterity = [float(relevant[i]["correctAgilityRate"]) for i in range(0, 26)]
        intelligence = [float(relevant[i]["correctMagicRate"]) for i in range(0, 26)]
        faith = [float(relevant[i]["correctFaithRate"]) for i in range(0, 26)]
        arcane = [float(relevant[i]["correctLuckRate"]) for i in range(0, 26)]

        infusion["statScalingRate"] = {
            "STR": strength,
            "DEX": dexterity,
            "INT": intelligence,
            "FTH": faith,
            "ARC": arcane,
        }

        infusions[id] = infusion


def process_damage(caps):
    for row in caps.values():
        calculation = {}

        id = row["ID"]

        calculation = []
        calculation.append({
            "softcap": int(row["stageMaxVal0"]),
            "growth": int(row["stageMaxGrowVal0"]) / 100.0,
            "adjustment": float(row["adjPt_maxGrowVal0"]),
        })
        calculation.append({
            "softcap": int(row["stageMaxVal1"]),
            "growth": int(row["stageMaxGrowVal1"]) / 100.0,
            "adjustment": float(row["adjPt_maxGrowVal1"]),
        })
        calculation.append({
            "softcap": int(row["stageMaxVal2"]),
            "growth": int(row["stageMaxGrowVal2"]) / 100.0,
            "adjustment": float(row["adjPt_maxGrowVal2"]),
        })
        calculation.append({
            "softcap": int(row["stageMaxVal3"]),
            "growth": int(row["stageMaxGrowVal3"]) / 100.0,
            "adjustment": float(row["adjPt_maxGrowVal3"]),
        })
        calculation.append({
            "softcap": int(row["stageMaxVal4"]),
            "growth": int(row["stageMaxGrowVal4"]) / 100.0,
            "adjustment": float(row["adjPt_maxGrowVal4"]),
        })

        calculations[id] = calculation


main()
