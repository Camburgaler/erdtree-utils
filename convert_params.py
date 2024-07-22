import csv
import json
import logging
import os
import sys

from corrections import (HELMET_STATS, IGNORED, IGNORED_WEAPON_INFUSIONS,
                         MISSING)

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
    "Fire ",
    "Flame Art ",
    "Lightning ",
    "Sacred ",
    "Magic ",
    "Cold ",
    "Poison ",
    "Blood ",
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
            "stats": [15, 10, 11, 14, 13, 9, 9, 7],
        },
        {
            "id": "warrior",
            "name": "Warrior",
            "level": 8,
            "stats": [11, 12, 11, 10, 16, 10, 8, 9],
        },
        {
            "id": "hero",
            "name": "Hero",
            "level": 7,
            "stats": [14, 9, 12, 16, 9, 7, 8, 11],
        },
        {
            "id": "bandit",
            "name": "Bandit",
            "level": 5,
            "stats": [10, 11, 10, 9, 13, 9, 8, 14],
        },
        {
            "id": "astrologer",
            "name": "Astrologer",
            "level": 6,
            "stats": [9, 15, 9, 8, 12, 16, 7, 9],
        },
        {
            "id": "prophet",
            "name": "Prophet",
            "level": 7,
            "stats": [10, 14, 8, 11, 10, 7, 16, 10],
        },
        {
            "id": "samurai",
            "name": "Samurai",
            "level": 9,
            "stats": [12, 11, 13, 12, 15, 9, 8, 8],
        },
        {
            "id": "prisoner",
            "name": "Prisoner",
            "level": 9,
            "stats": [11, 12, 11, 11, 14, 14, 6, 9],
        },
        {
            "id": "confessor",
            "name": "Confessor",
            "level": 10,
            "stats": [10, 13, 10, 12, 12, 9, 14, 9],
        },
        {
            "id": "wretch",
            "name": "Wretch",
            "level": 1,
            "stats": [10, 10, 10, 10, 10, 10, 10, 10],
        },
    ]

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

    # infusions
    with open("input/ReinforceParamWeapon.csv") as inf:
        rows = list(csv.DictReader(inf, delimiter=","))

        extract_infusions(rows)

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
            "defenses": [0, 0, 0, 0, 0, 0, 0, 0],
            "resistances": [0, 0, 0, 0, 0, 0, 0, 0],
            "poise": 0,
            "weight": 0,
        },
        **helmets,
    }
    chestpieces = {
        "no-chestpiece": {
            "id": "no-chestpiece",
            "name": "No chestpiece",
            "defenses": [0, 0, 0, 0, 0, 0, 0, 0],
            "resistances": [0, 0, 0, 0, 0, 0, 0, 0],
            "poise": 0,
            "weight": 0,
        },
        **chestpieces,
    }
    gauntlets = {
        "no-gauntlets": {
            "id": "no-gauntlets",
            "name": "No gauntlets",
            "defenses": [0, 0, 0, 0, 0, 0, 0, 0],
            "resistances": [0, 0, 0, 0, 0, 0, 0, 0],
            "poise": 0,
            "weight": 0,
        },
        **gauntlets,
    }
    leggings = {
        "no-leggings": {
            "id": "no-leggings",
            "name": "No leggings",
            "defenses": [0, 0, 0, 0, 0, 0, 0, 0],
            "resistances": [0, 0, 0, 0, 0, 0, 0, 0],
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
            "requirements": [0, 0, 0, 0, 0],
            "category": "fist",
            "unique": False,
            "infusions": {
                "standard": {
                    "damage": [20, 0, 0, 0, 0],
                    "scaling": [0.5, 0.5, 0.0, 0.0, 0.0],
                    "masks": [
                        [1, 1, 0, 0, 0],
                        [0, 0, 1, 0, 0],
                        [0, 0, 0, 1, 0],
                        [0, 1, 0, 0, 0],
                        [0, 0, 0, 1, 0],
                    ],
                    "corrections": ["0", "0", "0", "0", "0"],
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

    if id in HELMET_STATS:
        item["stats"] = HELMET_STATS[id]

    item["defenses"] = [
        round((1.0 - float(row["neutralDamageCutRate"])) * 100.0, 2), # Physical Absorption
        round((1.0 - float(row["blowDamageCutRate"])) * 100.0, 2), # Strike Absorption
        round((1.0 - float(row["slashDamageCutRate"])) * 100.0, 2), # Slash Absorption
        round((1.0 - float(row["thrustDamageCutRate"])) * 100.0, 2), # Thrust Absorption
        round((1.0 - float(row["magicDamageCutRate"])) * 100.0, 2), # Magic Absorption
        round((1.0 - float(row["fireDamageCutRate"])) * 100.0, 2), # Fire Absorption
        round((1.0 - float(row["thunderDamageCutRate"])) * 100.0, 2), # Lightning Absorption
        round((1.0 - float(row["darkDamageCutRate"])) * 100.0, 2), # Holy Absorption
    ]

    item["resistances"] = [
        int(row["resistDisease"]), # Scarlet Rot Resistance
        int(row["resistPoison"]), # Poison Resistance
        int(row["resistBlood"]), # Hemorrhage Resistance
        int(row["resistFreeze"]), # Freeze Resistance
        int(row["resistSleep"]), # Sleep Resistance
        int(row["resistMadness"]), # Madness Resistance
        int(row["resistCurse"]), # Death Blight Resistance
    ]

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
            item["stats"] = [
                int(effect["addLifeForceStatus"]), # Vigor
                int(effect["addWillpowerStatus"]), # Mind
                int(effect["addEndureStatus"]), # Endurance
                int(effect["addStrengthStatus"]), # Strength
                int(effect["addDexterityStatus"]), # Dexterity
                int(effect["addMagicStatus"]), # Intelligence
                int(effect["addFaithStatus"]), # Faith
                int(effect["addLuckStatus"]), # Arcane
            ]
            item["multipliers"] = [
                float(effect["maxHpRate"]), # Max HP
                float(effect["maxMpRate"]), # Max FP
                float(effect["maxStaminaRate"]), # Max Stamina
                float(effect["equipWeightChangeRate"]), # Equip Load
            ]

    if all(stat == 0.0 for stat in item["stats"]):
        item.pop("stats")
    if all(mult == 1.0 for mult in item["multipliers"]):
        item.pop("multipliers")

    talismans[id] = item


def split_weapon_name(name):
    infusion = "standard"
    for other in INFUSIONS:
        if "Bloody" in name and not to_kebab(name) in IGNORED_WEAPON_INFUSIONS:
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
        return 1
    else:
        return 0


def process_weapon(row, masks, effects):
    name, infusion = split_weapon_name(row["Name"])
    id = to_kebab(name)

    damage = [
        int(row["attackBasePhysics"]), # Physical
        int(row["attackBaseMagic"]), # Magic
        int(row["attackBaseFire"]), # Fire
        int(row["attackBaseThunder"]), # Lightning
        int(row["attackBaseDark"]), # Holy
    ]

    scaling = [
        float(row["correctStrength"]) / 100.0, # STR
        float(row["correctAgility"]) / 100.0, # DEX
        float(row["correctMagic"]) / 100.0, # INT
        float(row["correctFaith"]) / 100.0, # FTH
        float(row["correctLuck"]) / 100.0, # ARC
    ]

    mask_id = row["attackElementCorrectId"]
    mask_row = masks[mask_id]

    weapon_masks = [
        [  # Does Physical Damage Scale With...
            to_mask(mask_row["isStrengthCorrect_byPhysics"]), # STR
            to_mask(mask_row["isDexterityCorrect_byPhysics"]), # DEX
            to_mask(mask_row["isMagicCorrect_byPhysics"]), # INT
            to_mask(mask_row["isFaithCorrect_byPhysics"]), # FTH
            to_mask(mask_row["isLuckCorrect_byPhysics"]), # ARC
        ],
        [  # Does Magic Damage Scale With...
            to_mask(mask_row["isStrengthCorrect_byMagic"]), # STR
            to_mask(mask_row["isDexterityCorrect_byMagic"]), # DEX
            to_mask(mask_row["isMagicCorrect_byMagic"]), # INT
            to_mask(mask_row["isFaithCorrect_byMagic"]), # FTH
            to_mask(mask_row["isLuckCorrect_byMagic"]), # ARC
        ],
        [  # Does Fire Damage Scale With...
            to_mask(mask_row["isStrengthCorrect_byFire"]), # STR
            to_mask(mask_row["isDexterityCorrect_byFire"]), # DEX
            to_mask(mask_row["isMagicCorrect_byFire"]), # INT
            to_mask(mask_row["isFaithCorrect_byFire"]), # FTH
            to_mask(mask_row["isLuckCorrect_byFire"]), # ARC
        ],
        [  # Does Lightning Damage Scale With...
            to_mask(mask_row["isStrengthCorrect_byThunder"]), # STR
            to_mask(mask_row["isDexterityCorrect_byThunder"]), # DEX
            to_mask(mask_row["isMagicCorrect_byThunder"]), # INT
            to_mask(mask_row["isFaithCorrect_byThunder"]), # FTH
            to_mask(mask_row["isLuckCorrect_byThunder"]), # ARC
        ],
        [  # Does Holy Damage Scale With...
            to_mask(mask_row["isStrengthCorrect_byDark"]), # STR
            to_mask(mask_row["isDexterityCorrect_byDark"]), # DEX
            to_mask(mask_row["isMagicCorrect_byDark"]), # INT
            to_mask(mask_row["isFaithCorrect_byDark"]), # FTH
            to_mask(mask_row["isLuckCorrect_byDark"]), # ARC
        ],
    ]

    corrections = [
        row["correctType_Physics"],
        row["correctType_Magic"],
        row["correctType_Fire"],
        row["correctType_Thunder"],
        row["correctType_Dark"],
        row["correctType_Poison"],
        row["correctType_Blood"],
        row["correctType_Sleep"],
        row["correctType_Madness"],
    ]

    buffable = '0' in row["disableGemAttr"]

    # Auxiliary Effects (blood, poison)
    aux = {}
    for aux_id in [row["spEffectBehaviorId0"], row["spEffectBehaviorId1"]]:
        if int(aux_id) != -1 and int(aux_id) > 5000000:
            aux_name = effects[aux_id]["Name"]
            if "Hemorrhage" in aux_name:
                aux["bleed"] = aux_id
            elif "Frostbite" in aux_name:
                aux["frost"] = aux_id
            elif "Poison" in aux_name:
                aux["poison"] = aux_id
            elif "Scarlet Rot" in aux_name:
                aux["scarlet_rot"] = aux_id
            elif "Madness" in aux_name:
                aux["madness"] = aux_id
        elif int(aux_id) != -1 and int(aux_id) > 100000:
            aux_name = effects[aux_id]["Name"]
            xs = [x for x in range(0, 26)]
            ys = [effects[str(int(aux_id) + x)] for x in xs]

            if "Hemorrhage" in aux_name:
                ty = "bleed"
                ys = [int(y["bloodDefDamageRate"]) for y in ys]
            elif "Frostbite" in aux_name:
                ty = "frost"
                ys = [int(y["freezeDefDamageRate"]) for y in ys]
            elif "Poison" in aux_name:
                ty = "poison"
                ys = [int(y["poisonDefDamageRate"]) for y in ys]
            elif "Scarlet Rot" in aux_name:
                ty = "scarlet_rot"
                ys = [int(y["diseaseDefDamageRate"]) for y in ys]
            elif "Madness" in aux_name:
                ty = "madness"
                ys = [int(y["madnessDefDamageRate"]) for y in ys]
            elif "Sleep" in aux_name:
                ty = "sleep"
                ys = [int(y["sleepDefDamageRate"]) for y in ys]
            elif "Blight" in aux_name:
                ty = "blight"
                ys = [int(y["curseDefDamageRate"]) for y in ys]
            aux[ty] = regression(xs, ys)
        elif int(aux_id) != -1 and int(aux_id) <= 100000:
            aux_name = effects[aux_id]["Name"]
            if "Hemorrhage" in aux_name:
                ty = "bleed"
                # base = effects[aux_id]["Inflict Hemorrhage +"]
            elif "Frostbite" in aux_name:
                ty = "frost"
                # base = effects[aux_id]["Inflict Frostbite +"]
            elif "Poison" in aux_name:
                ty = "poison"
                # base = effects[aux_id]["Inflict Poison +"]
            elif "Scarlet Rot" in aux_name:
                ty = "scarlet_rot"
                # base = effects[aux_id]["Inflict Scarlet Rot +"]
            elif "Madness" in aux_name:
                ty = "madness"
                # base = effects[aux_id]["Inflict Madness +"]
            elif "Sleep" in aux_name:
                ty = "sleep"
                # base = effects[aux_id]["Inflict Sleep +"]
            elif "Blight" in aux_name:
                ty = "blight"
                # base = effects[aux_id]["Inflict Blight +"]
            aux[ty] = [0.0, aux_name]

    if id in weapons:
        if not id in IGNORED_WEAPON_INFUSIONS:
            weapon = weapons[id]
            weapon["infusions"][infusion] = {
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

        weapon["requirements"] = [
            int(row["properStrength"]), # STR
            int(row["properAgility"]), # DEX
            int(row["properMagic"]), # INT
            int(row["properFaith"]), # FTH
            int(row["properLuck"]), # ARC
        ]

        weapon["category"] = WEAPON_CATEGORIES[int(row["ID"]) // 1000000]

        if int(row["reinforceTypeId"]) == 2200:
            weapon["unique"] = True
        else:
            weapon["unique"] = False

        weapon["infusions"] = {}
        weapon["infusions"][infusion] = {
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

    a = (n * xy - sum(xs) * sum(ys)) / (n * xsq - sum(xs) ** 2)
    b = ys[0]

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

        physical_upg, physical_dmg = regression(xs, physical)
        magic_upg, magic_dmg = regression(xs, magic)
        fire_upg, fire_dmg = regression(xs, fire)
        lightning_upg, lightning_dmg = regression(xs, lightning)
        holy_upg, holy_dmg = regression(xs, holy)

        infusion["damage"] = [
            physical_dmg,
            magic_dmg,
            fire_dmg,
            lightning_dmg,
            holy_dmg,
        ]
        infusion["upgrade"] = [
            physical_upg,
            magic_upg,
            fire_upg,
            lightning_upg,
            holy_upg,
        ]

        # scaling
        strength = [float(relevant[i]["correctStrengthRate"]) for i in range(0, 26)]
        dexterity = [float(relevant[i]["correctAgilityRate"]) for i in range(0, 26)]
        intelligence = [float(relevant[i]["correctMagicRate"]) for i in range(0, 26)]
        faith = [float(relevant[i]["correctFaithRate"]) for i in range(0, 26)]
        arcane = [float(relevant[i]["correctLuckRate"]) for i in range(0, 26)]

        str_growth, str_scaling = regression(xs, strength)
        dex_growth, dex_scaling = regression(xs, dexterity)
        int_growth, int_scaling = regression(xs, intelligence)
        fth_growth, fth_scaling = regression(xs, faith)
        arc_growth, arc_scaling = regression(xs, arcane)

        infusion["scaling"] = [
            str_scaling,
            dex_scaling,
            int_scaling,
            fth_scaling,
            arc_scaling,
        ]
        infusion["growth"] = [
            str_growth,
            dex_growth,
            int_growth,
            fth_growth,
            arc_growth,
        ]

        infusions[id] = infusion


def process_damage(caps):
    for row in caps.values():
        calculation = {}

        id = row["ID"]
        calculation["id"] = id

        calculation["softcaps"] = [
            [  # physical
                int(row["stageMaxVal0"]),
                int(row["stageMaxVal1"]),
                int(row["stageMaxVal2"]),
                int(row["stageMaxVal3"]),
                int(row["stageMaxVal4"]),
            ],
            [  # magic
                int(row["stageMaxVal0"]),
                int(row["stageMaxVal1"]),
                int(row["stageMaxVal2"]),
                int(row["stageMaxVal3"]),
                int(row["stageMaxVal4"]),
            ],
            [  # fire
                int(row["stageMaxVal0"]),
                int(row["stageMaxVal1"]),
                int(row["stageMaxVal2"]),
                int(row["stageMaxVal3"]),
                int(row["stageMaxVal4"]),
            ],
            [  # lightning
                int(row["stageMaxVal0"]),
                int(row["stageMaxVal1"]),
                int(row["stageMaxVal2"]),
                int(row["stageMaxVal3"]),
                int(row["stageMaxVal4"]),
            ],
            [  # holy
                int(row["stageMaxVal0"]),
                int(row["stageMaxVal1"]),
                int(row["stageMaxVal2"]),
                int(row["stageMaxVal3"]),
                int(row["stageMaxVal4"]),
            ],
        ]

        calculation["growth"] = [
            [
                int(row["stageMaxGrowVal0"]),
                int(row["stageMaxGrowVal1"]),
                int(row["stageMaxGrowVal2"]),
                int(row["stageMaxGrowVal3"]),
                int(row["stageMaxGrowVal4"]),
            ],
            [
                int(row["stageMaxGrowVal0"]),
                int(row["stageMaxGrowVal1"]),
                int(row["stageMaxGrowVal2"]),
                int(row["stageMaxGrowVal3"]),
                int(row["stageMaxGrowVal4"]),
            ],
            [
                int(row["stageMaxGrowVal0"]),
                int(row["stageMaxGrowVal1"]),
                int(row["stageMaxGrowVal2"]),
                int(row["stageMaxGrowVal3"]),
                int(row["stageMaxGrowVal4"]),
            ],
            [
                int(row["stageMaxGrowVal0"]),
                int(row["stageMaxGrowVal1"]),
                int(row["stageMaxGrowVal2"]),
                int(row["stageMaxGrowVal3"]),
                int(row["stageMaxGrowVal4"]),
            ],
            [
                int(row["stageMaxGrowVal0"]),
                int(row["stageMaxGrowVal1"]),
                int(row["stageMaxGrowVal2"]),
                int(row["stageMaxGrowVal3"]),
                int(row["stageMaxGrowVal4"]),
            ],
        ]

        calculation["adjustments"] = [
            [
                float(row["adjPt_maxGrowVal0"]),
                float(row["adjPt_maxGrowVal1"]),
                float(row["adjPt_maxGrowVal2"]),
                float(row["adjPt_maxGrowVal3"]),
                float(row["adjPt_maxGrowVal4"]),
            ],
            [
                float(row["adjPt_maxGrowVal0"]),
                float(row["adjPt_maxGrowVal1"]),
                float(row["adjPt_maxGrowVal2"]),
                float(row["adjPt_maxGrowVal3"]),
                float(row["adjPt_maxGrowVal4"]),
            ],
            [
                float(row["adjPt_maxGrowVal0"]),
                float(row["adjPt_maxGrowVal1"]),
                float(row["adjPt_maxGrowVal2"]),
                float(row["adjPt_maxGrowVal3"]),
                float(row["adjPt_maxGrowVal4"]),
            ],
            [
                float(row["adjPt_maxGrowVal0"]),
                float(row["adjPt_maxGrowVal1"]),
                float(row["adjPt_maxGrowVal2"]),
                float(row["adjPt_maxGrowVal3"]),
                float(row["adjPt_maxGrowVal4"]),
            ],
            [
                float(row["adjPt_maxGrowVal0"]),
                float(row["adjPt_maxGrowVal1"]),
                float(row["adjPt_maxGrowVal2"]),
                float(row["adjPt_maxGrowVal3"]),
                float(row["adjPt_maxGrowVal4"]),
            ],
        ]

        calculations[id] = calculation


main()
