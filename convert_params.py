import csv
import json
import os

from corrections import IGNORED, IGNORED_WEAPON_INFUSIONS, MISSING, HELMET_STATS

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
        rows = list(csv.DictReader(af, delimiter=";"))

        for armor in rows:
            if not ignored(armor):
                process_armor_piece(armor)

    # talismans
    with (
        open("input/EquipParamAccessory.csv") as tf,
        open("input/SpEffectParam.csv") as ef,
    ):

        effects = list(csv.DictReader(ef, delimiter=";"))
        rows = list(csv.DictReader(tf, delimiter=";"))

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
    ):

        rows = list(csv.DictReader(wf, delimiter=";"))
        rows = [row for row in rows if 1000000 <= int(row["Row ID"]) <= 44010000]

        masks = list(csv.DictReader(af, delimiter=";"))
        masks = {row["Row ID"]: row for row in masks}

        softcaps = list(csv.DictReader(cf, delimiter=";"))
        softcaps = {
            row["Row ID"]: row for row in softcaps if 0 <= int(row["Row ID"]) <= 16
        }

        for row in rows:
            if not ignored(row):
                process_weapon(row, masks, softcaps)

        process_damage(softcaps)

    # infusions
    with open("input/ReinforceParamWeapon.csv") as inf:
        rows = list(csv.DictReader(inf, delimiter=";"))

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
            "resistances": [0, 0, 0, 0],
            "poise": 0,
            "weight": 0,
        },
        **helmets,
    }
    chestpieces = {
        "no-chestpiece": {
            "id": "no-chestpieces",
            "name": "No chestpiece",
            "defenses": [0, 0, 0, 0, 0, 0, 0, 0],
            "resistances": [0, 0, 0, 0],
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
            "resistances": [0, 0, 0, 0],
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
            "resistances": [0, 0, 0, 0],
            "poise": 0,
            "weight": 0,
        },
        **leggings,
    }
    talismans = {
        "no-talisman": {
            "id": "no-talismans",
            "name": "No talisman",
        },
        **talismans,
    }
    weapons = {
        "unarmed": {
            "id": "unarmed",
            "name": "Unarmed",
            "requirements": [0, 0, 0, 0, 0],
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
    id = to_kebab(row["Row Name"])
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

    id = to_kebab(row["Row Name"])
    item["id"] = id
    item["name"] = row["Row Name"]

    if id in HELMET_STATS:
        item["stats"] = HELMET_STATS[id]

    item["defenses"] = [
        round((1.0 - float(row["Absorption - Physical"])) * 100.0, 2),
        round((1.0 - float(row["Absorption - Strike"])) * 100.0, 2),
        round((1.0 - float(row["Absorption - Slash"])) * 100.0, 2),
        round((1.0 - float(row["Absorption - Thrust"])) * 100.0, 2),
        round((1.0 - float(row["Absorption - Magic"])) * 100.0, 2),
        round((1.0 - float(row["Absorption - Fire"])) * 100.0, 2),
        round((1.0 - float(row["Absorption - Lightning"])) * 100.0, 2),
        round((1.0 - float(row["Absorption - Holy"])) * 100.0, 2),
    ]

    item["resistances"] = [
        int(row["Resist - Scarlet Rot"]),
        int(row["Resist - Hemorrhage"]),
        int(row["Resist - Sleep"]),
        int(row["Resist - Blight"]),
    ]

    item["poise"] = int(round(float(row["Poise"]) * 1000.0, 2))
    item["weight"] = round(float(row["Weight"]), 2)

    if row["Is Head Equipment"] == "True":
        helmets[id] = item
    elif row["Is Body Equipment"] == "True":
        chestpieces[id] = item
    elif row["Is Arm Equipment"] == "True":
        gauntlets[id] = item
    elif row["Is Leg Equipment"] == "True":
        leggings[id] = item


def process_talisman(row, effects):
    item = {}

    id = to_kebab(row["Row Name"])
    item["id"] = id
    item["name"] = row["Row Name"]

    item["weight"] = row["Weight"]

    effect_id = row["SpEffect ID 1"]
    for effect in effects:
        if effect["Row ID"] == effect_id:
            item["stats"] = [
                int(effect["Vigor"]),
                int(effect["Mind"]),
                int(effect["Endurance"]),
                int(effect["Strength"]),
                int(effect["Dexterity"]),
                int(effect["Intelligence"]),
                int(effect["Faith"]),
                int(effect["Arcane"]),
            ]
            item["multipliers"] = [
                float(effect["Max HP"]),
                float(effect["Max FP"]),
                float(effect["Max Stamina"]),
                float(effect["Equip Load %"]),
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
    if str == "True":
        return 1
    else:
        return 0


def process_weapon(row, masks, caps):
    name, infusion = split_weapon_name(row["Row Name"])
    id = to_kebab(name)

    damage = [
        int(row["Damage: Physical"]),
        int(row["Damage: Magic"]),
        int(row["Damage: Fire"]),
        int(row["Damage: Lightning"]),
        int(row["Damage: Holy"]),
    ]

    scaling = [
        float(row["Scaling: STR"]) / 100.0,
        float(row["Scaling: DEX"]) / 100.0,
        float(row["Scaling: INT"]) / 100.0,
        float(row["Scaling: FTH"]) / 100.0,
        float(row["Scaling: ARC"]) / 100.0,
    ]

    mask_id = row["Attack Element Correct ID"]
    mask_row = masks[mask_id]

    weapon_masks = [
        [  # physical
            to_mask(mask_row["Physical Scaling: STR"]),
            to_mask(mask_row["Physical Scaling: DEX"]),
            to_mask(mask_row["Physical Scaling: INT"]),
            to_mask(mask_row["Physical Scaling: FTH"]),
            to_mask(mask_row["Physical Scaling: ARC"]),
        ],
        [  # magic
            to_mask(mask_row["Magic Scaling: STR"]),
            to_mask(mask_row["Magic Scaling: DEX"]),
            to_mask(mask_row["Magic Scaling: INT"]),
            to_mask(mask_row["Magic Scaling: FTH"]),
            to_mask(mask_row["Magic Scaling: ARC"]),
        ],
        [  # fire
            to_mask(mask_row["Fire Scaling: STR"]),
            to_mask(mask_row["Fire Scaling: DEX"]),
            to_mask(mask_row["Fire Scaling: INT"]),
            to_mask(mask_row["Fire Scaling: FTH"]),
            to_mask(mask_row["Fire Scaling: ARC"]),
        ],
        [  # lightning
            to_mask(mask_row["Lightning Scaling: STR"]),
            to_mask(mask_row["Lightning Scaling: DEX"]),
            to_mask(mask_row["Lightning Scaling: INT"]),
            to_mask(mask_row["Lightning Scaling: FTH"]),
            to_mask(mask_row["Lightning Scaling: ARC"]),
        ],
        [  # holy
            to_mask(mask_row["Holy Scaling: STR"]),
            to_mask(mask_row["Holy Scaling: DEX"]),
            to_mask(mask_row["Holy Scaling: INT"]),
            to_mask(mask_row["Holy Scaling: FTH"]),
            to_mask(mask_row["Holy Scaling: ARC"]),
        ],
    ]

    corrections = [
        row["Correction Type: Physical"],
        row["Correction Type: Magic"],
        row["Correction Type: Fire"],
        row["Correction Type: Lightning"],
        row["Correction Type: Holy"],
    ]

    if id in weapons:
        weapon = weapons[id]
        weapon["infusions"][infusion] = {
            "damage": damage,
            "upgrade": scaling,
            "masks": weapon_masks,
            "corrections": corrections,
        }
        return
    else:
        weapon = {}

        weapon["id"] = id
        weapon["name"] = name

        weapon["requirements"] = [
            int(row["Requirement: STR"]),
            int(row["Requirement: DEX"]),
            int(row["Requirement: INT"]),
            int(row["Requirement: FTH"]),
            int(row["Requirement: ARC"]),
        ]

        weapon["category"] = WEAPON_CATEGORIES[int(row["Row ID"]) // 1000000]

        if int(row["Reinforcement Material Set ID"]) == 2200:
            weapon["unique"] = True
        else:
            weapon["unique"] = False

        weapon["infusions"] = {}
        weapon["infusions"][infusion] = {
            "damage": damage,
            "scaling": scaling,
            "masks": weapon_masks,
            "corrections": corrections,
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
        physical = [float(relevant[i]["Damage %: Physical"]) for i in range(0, 26)]
        magic = [float(relevant[i]["Damage %: Magic"]) for i in range(0, 26)]
        fire = [float(relevant[i]["Damage %: Fire"]) for i in range(0, 26)]
        lightning = [float(relevant[i]["Damage %: Lightning"]) for i in range(0, 26)]
        holy = [float(relevant[i]["Damage %: Holy"]) for i in range(0, 26)]

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
        strength = [float(relevant[i]["Scaling %: STR"]) for i in range(0, 26)]
        dexterity = [float(relevant[i]["Scaling %: DEX"]) for i in range(0, 26)]
        intelligence = [float(relevant[i]["Scaling %: INT"]) for i in range(0, 26)]
        faith = [float(relevant[i]["Scaling %: FTH"]) for i in range(0, 26)]
        arcane = [float(relevant[i]["Scaling %: ARC"]) for i in range(0, 26)]

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

        id = row["Row ID"]
        calculation["id"] = id

        calculation["softcaps"] = [
            [  # physical
                int(row["Stat Max 0"]),
                int(row["Stat Max 1"]),
                int(row["Stat Max 2"]),
                int(row["Stat Max 3"]),
                int(row["Stat Max 4"]),
            ],
            [  # magic
                int(row["Stat Max 0"]),
                int(row["Stat Max 1"]),
                int(row["Stat Max 2"]),
                int(row["Stat Max 3"]),
                int(row["Stat Max 4"]),
            ],
            [  # fire
                int(row["Stat Max 0"]),
                int(row["Stat Max 1"]),
                int(row["Stat Max 2"]),
                int(row["Stat Max 3"]),
                int(row["Stat Max 4"]),
            ],
            [  # lightning
                int(row["Stat Max 0"]),
                int(row["Stat Max 1"]),
                int(row["Stat Max 2"]),
                int(row["Stat Max 3"]),
                int(row["Stat Max 4"]),
            ],
            [  # holy
                int(row["Stat Max 0"]),
                int(row["Stat Max 1"]),
                int(row["Stat Max 2"]),
                int(row["Stat Max 3"]),
                int(row["Stat Max 4"]),
            ],
        ]

        calculation["growth"] = [
            [
                int(row["Grow 0"]),
                int(row["Grow 1"]),
                int(row["Grow 2"]),
                int(row["Grow 3"]),
                int(row["Grow 4"]),
            ],
            [
                int(row["Grow 0"]),
                int(row["Grow 1"]),
                int(row["Grow 2"]),
                int(row["Grow 3"]),
                int(row["Grow 4"]),
            ],
            [
                int(row["Grow 0"]),
                int(row["Grow 1"]),
                int(row["Grow 2"]),
                int(row["Grow 3"]),
                int(row["Grow 4"]),
            ],
            [
                int(row["Grow 0"]),
                int(row["Grow 1"]),
                int(row["Grow 2"]),
                int(row["Grow 3"]),
                int(row["Grow 4"]),
            ],
            [
                int(row["Grow 0"]),
                int(row["Grow 1"]),
                int(row["Grow 2"]),
                int(row["Grow 3"]),
                int(row["Grow 4"]),
            ],
        ]

        calculation["adjustments"] = [
            [
                float(row["Adjustment Point - Grow 0"]),
                float(row["Adjustment Point - Grow 1"]),
                float(row["Adjustment Point - Grow 2"]),
                float(row["Adjustment Point - Grow 3"]),
                float(row["Adjustment Point - Grow 4"]),
            ],
            [
                float(row["Adjustment Point - Grow 0"]),
                float(row["Adjustment Point - Grow 1"]),
                float(row["Adjustment Point - Grow 2"]),
                float(row["Adjustment Point - Grow 3"]),
                float(row["Adjustment Point - Grow 4"]),
            ],
            [
                float(row["Adjustment Point - Grow 0"]),
                float(row["Adjustment Point - Grow 1"]),
                float(row["Adjustment Point - Grow 2"]),
                float(row["Adjustment Point - Grow 3"]),
                float(row["Adjustment Point - Grow 4"]),
            ],
            [
                float(row["Adjustment Point - Grow 0"]),
                float(row["Adjustment Point - Grow 1"]),
                float(row["Adjustment Point - Grow 2"]),
                float(row["Adjustment Point - Grow 3"]),
                float(row["Adjustment Point - Grow 4"]),
            ],
            [
                float(row["Adjustment Point - Grow 0"]),
                float(row["Adjustment Point - Grow 1"]),
                float(row["Adjustment Point - Grow 2"]),
                float(row["Adjustment Point - Grow 3"]),
                float(row["Adjustment Point - Grow 4"]),
            ],
        ]

        calculations[id] = calculation


main()
