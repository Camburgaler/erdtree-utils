import csv
import json

from corrections import IGNORED, MISSING, HELMET_STATS

helmets = []
chestpieces = []
gauntlets = []
leggings = []
talismans = []
weapons = []


def main():
    # armors
    with open("input/EquipParamProtector.csv") as af:
        reader = list(csv.DictReader(af, delimiter=";"))

        for armor in reader:
            if not ignored(armor):
                process_armor_piece(armor)

    # talismans
    with (
        open("input/EquipParamAccessory.csv") as tf,
        open("input/SpEffectParam.csv") as ef,
    ):
        effects = list(csv.DictReader(ef, delimiter=";"))
        reader = list(csv.DictReader(tf, delimiter=";"))

        for talisman in reader:
            if not ignored(talisman):
                process_talisman(talisman, effects)

    # add missing items
    for h in MISSING["helmets"]:
        helmets.append(h)
    for c in MISSING["chestpieces"]:
        chestpieces.append(c)
    for g in MISSING["gauntlets"]:
        gauntlets.append(g)
    for l in MISSING["leggings"]:
        leggings.append(l)

    # sort all files
    helmets.sort(key=lambda item: item["id"])
    chestpieces.sort(key=lambda item: item["id"])
    gauntlets.sort(key=lambda item: item["id"])
    leggings.sort(key=lambda item: item["id"])

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
        open("output/weapons.json", "w") as wf,
    ):
        json.dump(helmets, hf)
        json.dump(chestpieces, cf)
        json.dump(gauntlets, gf)
        json.dump(leggings, lf)
        json.dump(talismans, tf)
        json.dump(weapons, wf)


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


main()
