import csv
import json
from statistics import mean
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

helmets = []
chestpieces = []
gauntlets = []
leggings = []
talismans = []
classes = []
weapons = []
infusions = []


def main():
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
    with open("input/CharaInitParam.csv", "r") as cf:
        rows = list(csv.DictReader(cf, delimiter=";"))
        rows = [row for row in rows if 3000 <= int(row["Row ID"]) <= 3009]

        for row in rows:
            c = {}
            c["id"] = to_kebab(row["Row Name"][8:])
            c["name"] = row["Row Name"][8:]
            c["level"] = int(row["Level"])
            c["stats"] = [
                int(row["Vigor"]),
                int(row["Attunement"]),
                int(row["Endurance"]),
                int(row["Strength"]),
                int(row["Dexterity"]),
                int(row["Intelligence"]),
                int(row["Faith"]),
                int(row["Arcane"]),
            ]
            classes.append(c)

    # weapons
    with open("input/EquipParamWeapon.csv") as wf:
        rows = list(csv.DictReader(wf, delimiter=";"))
        rows = [row for row in rows if 1000000 <= int(row["Row ID"]) <= 44010000]

        for row in rows:
            if not ignored(row):
                process_weapon(row)

    # infusions
    with open("input/ReinforceParamWeapon.csv") as inf:
        rows = list(csv.DictReader(inf, delimiter=";"))

        extract_infusions(rows)

    # add missing items
    for h in MISSING["helmets"]:
        helmets.append(h)
    for c in MISSING["chestpieces"]:
        chestpieces.append(c)
    for g in MISSING["gauntlets"]:
        gauntlets.append(g)
    for l in MISSING["leggings"]:
        leggings.append(l)

    # mark weapons with no infusions as "unique"
    for weapon in weapons:
        if weapon["infusions"] == []:
            weapon["infusions"] = ["unique"]

    # sort all files
    helmets.sort(key=lambda item: item["id"])
    chestpieces.sort(key=lambda item: item["id"])
    gauntlets.sort(key=lambda item: item["id"])
    leggings.sort(key=lambda item: item["id"])
    talismans.sort(key=lambda item: item["id"])
    classes.sort(key=lambda item: item["id"], reverse=True)
    weapons.sort(key=lambda item: item["id"])
    # infusions.sort(key=lambda item: item["id"])

    # add none cases (no helmet etc.)
    helmets.insert(0, {"id": "no-helmet", "name": "None"})
    chestpieces.insert(0, {"id": "no-chestpiece", "name": "None"})
    gauntlets.insert(0, {"id": "no-gauntlets", "name": "None"})
    leggings.insert(0, {"id": "no-leggings", "name": "None"})

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
    ):
        json.dump(helmets, hf)
        json.dump(chestpieces, cf)
        json.dump(gauntlets, gf)
        json.dump(leggings, lf)
        json.dump(talismans, tf)
        json.dump(classes, scf)
        json.dump(weapons, wf)
        json.dump(infusions, inf)

    # format output files with prettier
    if os.system("prettier output --write") != 0:
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

    item["id"] = to_kebab(row["Row Name"])
    item["name"] = row["Row Name"]

    if item["id"] in HELMET_STATS:
        item["stats"] = HELMET_STATS[item["id"]]

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
        helmets.append(item)
    elif row["Is Body Equipment"] == "True":
        chestpieces.append(item)
    elif row["Is Arm Equipment"] == "True":
        gauntlets.append(item)
    elif row["Is Leg Equipment"] == "True":
        leggings.append(item)


def process_talisman(row, effects):
    item = {}

    item["id"] = to_kebab(row["Row Name"])
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

    talismans.append(item)


def split_weapon_name(name):
    infusion = "none"
    for other in INFUSIONS:
        if other in name and not to_kebab(name) in IGNORED_WEAPON_INFUSIONS:
            infusion = other
            name = name.replace(infusion, "")

    return name.strip().replace("  ", " "), to_kebab(infusion)


def process_weapon(row):
    name, infusion = split_weapon_name(row["Row Name"])
    id = to_kebab(name)

    for other in weapons:
        if other["id"] == id:
            weapon = other
            weapon["infusions"].append(infusion)

            return

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

    if row["Enables Sorcery"] == "True":
        weapon["sorcery-catalyst"] = True
    if row["Enables Incantations"] == "True":
        weapon["incantation-catalyst"] = True

    if infusion == "none":
        weapon["infusions"] = []
    else:
        weapon["infusions"] = [infusion]

    weapons.append(weapon)


def regression(xs, ys):
    n = len(xs)

    xy = sum([x * y for x, y in zip(xs, ys)])
    xsq = sum([x * x for x in xs])

    a = (n * xy - sum(xs) * sum(ys)) / (n * xsq - sum(xs) ** 2)
    b = ys[0]

    return round(a, 5), b


def extract_infusions(rows):
    for i, ty in enumerate(INFUSIONS):
        infusion = {}
        infusion["id"] = to_kebab(ty)
        infusion["name"] = ty.strip()

        relevant = [row for row in rows[0 + i + i * 25 : 26 + i + i * 25]]

        xs = [x for x in range(0, 26)]

        # damage
        physical = [float(relevant[i]["Damage %: Physical"]) for i in range(0, 26)]
        fire = [float(relevant[i]["Damage %: Fire"]) for i in range(0, 26)]
        magic = [float(relevant[i]["Damage %: Magic"]) for i in range(0, 26)]
        lightning = [float(relevant[i]["Damage %: Lightning"]) for i in range(0, 26)]
        holy = [float(relevant[i]["Damage %: Holy"]) for i in range(0, 26)]

        infusion["damage"] = {
            "physical": regression(xs, physical),
            "fire": regression(xs, fire),
            "magic": regression(xs, magic),
            "lightning": regression(xs, lightning),
            "holy": regression(xs, holy),
        }

        # scaling
        strength = [float(relevant[i]["Scaling %: STR"]) for i in range(0, 26)]
        dexterity = [float(relevant[i]["Scaling %: DEX"]) for i in range(0, 26)]
        intelligence = [float(relevant[i]["Scaling %: INT"]) for i in range(0, 26)]
        faith = [float(relevant[i]["Scaling %: FTH"]) for i in range(0, 26)]
        arcane = [float(relevant[i]["Scaling %: ARC"]) for i in range(0, 26)]

        infusion["scaling"] = {
            "strength": regression(xs, strength),
            "dexterity": regression(xs, dexterity),
            "intelligence": regression(xs, intelligence),
            "faith": regression(xs, faith),
            "arcane": regression(xs, arcane),
        }

        infusions.append(infusion)

    # catalyst
    infusion = {}


main()
