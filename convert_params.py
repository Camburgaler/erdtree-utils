import csv
import json

IGNORED = [
    "",
    "head",
    "body",
    "arms",
    "legs",
    "travel-hairstyle",
    "millicents-robe",
    "millicents-gloves",
    "millicents-boots",
    "millicents-tunic",
    "millicents-robe",
    "braves-corc-circlet",
    "braves-battlewear",
    "braves-battlewear-altered",
    "braves-bracer",
    "braves-legwraps",
    "braves-leather-helm",
    "ragged-hat",
    "ragged-hat-altered",
    "ragged-armor",
    "ragged-armor-altered",
    "ragged-gloves",
    "ragged-loincloth",
]

helmets = []
chestpieces = []
gauntlets = []
leggings = []
talismans = []


def main():
    # armors
    with open("input/EquipParamProtector.csv") as af:
        reader = csv.DictReader(af, delimiter=";")

        for a in reader:
            if not ignored(a):
                armor_piece(a)

    # talismans
    with (
        open("input/EquipParamAccessory.csv") as tf,
        open("input/SpEffectParam.csv") as ef,
    ):
        effects = list(csv.DictReader(ef, delimiter=";"))
        reader = list(csv.DictReader(tf, delimiter=";"))

        for t in reader:
            if not ignored(t):
                talisman(t, effects)

    # add missing items
    # add_missing_items()

    # sort all files

    # add none cases (no helmet etc.)

    # save to files
    with open("output/helmets.json", "w") as hf:
        json.dump(helmets, hf)
    with open("output/chestpieces.json", "w") as cf:
        json.dump(chestpieces, cf)
    with open("output/gauntlets.json", "w") as gf:
        json.dump(gauntlets, gf)
    with open("output/leggings.json", "w") as lf:
        json.dump(leggings, lf)
    with open("output/talismans.json", "w") as tf:
        json.dump(talismans, tf)


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


def armor_piece(row):
    item = {}

    item["name"] = row["Row Name"]
    item["id"] = to_kebab(item["name"])

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

    item["poise"] = round(float(row["Poise"]) * 1000.0, 2)
    item["weight"] = round(float(row["Weight"]), 2)

    row_id = int(row["Row ID"])
    if row_id % 1000 == 0:
        helmets.append(item)
    elif row_id % 1000 == 100:
        chestpieces.append(item)
    elif row_id % 1000 == 200:
        gauntlets.append(item)
    elif row_id % 1000 == 300:
        leggings.append(item)


def talisman(row, effects):
    item = {}

    item["name"] = row["Row Name"]
    item["id"] = to_kebab(item["name"])

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


def add_missing_items():
    raise NotImplementedError


main()
