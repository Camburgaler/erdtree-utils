# dont add these items to the output
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
    "braves-cord-circlet",
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
    "deathbed-smalls",
    # these items are wrong in the param files
    "ash-of-war-scarab",
    "fias-robe",
    "fias-robe-altered",
    "deathbed-dress",
    "rotten-duelist-greaves",
]

# these items are either missing or wrong in the param files
MISSING = {
    "helmets": {
        "ash-of-war-scarab": {
            "name": "Ash-of-War Scarab",
            "defenses": [-5.8, -5.6, -5.8, -5.8, -4.9, -4.9, -4.9, -5.1],
            "resistances": [42, 42, 22, 22, 27, 27, 26],
            "poise": 6,
            "weight": 5.1,
        },
    },
    "chestpieces": {
        "fias-robe": {
            "name": "Fia's Robe",
            "defenses": [5.3, 6.1, 5.3, 5.3, 12.6, 12.4, 12.6, 13.0],
            "resistances": [46, 46, 21, 21, 76, 76, 108],
            "poise": 2,
            "weight": 5.1,
        },
        "fias-robe-altered": {
            "name": "Fia's Robe (Altered)",
            "defenses": [2.7, 4.2, 2.7, 2.7, 11.9, 11.4, 11.9, 12.6],
            "resistances": [34, 34, 10, 10, 57, 57, 93],
            "poise": 0,
            "weight": 3.2,
        },
        "deathbed-dress": {
            "id": "deathbed-dress",
            "name": "Deathbed Dress",
            "defenses": [0.6, 2.7, 0.6, 0.6, 11.9, 11.4, 11.9, 12.4],
            "resistances": [38, 38, 11, 11, 63, 63, 107],
            "poise": 1,
            "weight": 3.2,
        },
    },
    "gauntlets": {
    },
    "leggings": {
        "rotten-duelist-greaves": {
            "id": "rotten-duelist-greaves",
            "name": "Rotten Duelist Greaves",
            "defenses": [7.4, 6.2, 7.7, 7.1, 6.2, 6.5, 5.8, 6.2],
            "resistances": [35, 35, 35, 35, 15, 15, 15],
            "poise": 10,
            "weight": 7.3,
        },
    },
}

# until i find where this is located in the param files, this is the workaround
HELMET_STATS = {
    "alberichs-pointed-hat": [0, 0, 0, 0, 0, 0, 0, 4],
    "crimson-hood": [1, 0, 0, 0, 0, 0, 0, 0],
    "haima-glintstone-crown": [0, 0, 0, 2, 0, 2, 0, 0],
    "haligtree-helm": [0, 0, 0, 0, 0, 0, 1, 0],
    "haligtree-knight-helm": [0, 0, 0, 0, 0, 0, 2, 0],
    "hierodas-glintstone-crown": [0, 0, 2, 0, 0, 2, 0, 0],
    "imp-head-cat": [0, 0, 0, 0, 0, 2, 0, 0],
    "imp-head-corpse": [0, 0, 0, 0, 0, 0, 2, 0],
    "imp-head-elder": [0, 0, 0, 0, 0, 0, 0, 2],
    "imp-head-long-tongued": [0, 0, 0, 0, 2, 0, 0, 0],
    "imp-head-wolf": [0, 0, 2, 0, 0, 0, 0, 0],
    "imp-head-fanged": [0, 0, 0, 2, 0, 0, 0, 0],
    "karolos-glinstone-crown": [0, 0, 0, 0, 0, 3, 0, 0],
    "mask-of-confidence": [0, 0, 0, 0, 0, 0, 0, 3],
    "navy-hood": [0, 1, 0, 0, 0, 0, 0, 0],
    "okina-mask": [0, 0, 0, 0, 3, 0, 0, 0],
    "olivinus-glintstone-crown": [0, 0, 0, 0, 0, 3, 0, 0],
    "omensmirk-mask": [0, 0, 0, 2, 0, 0, 0, 0],
    "queens-crescent-crown": [0, 0, 0, 0, 0, 3, 0, 0],
    "silver-tear-mask": [0, 0, 0, 0, 0, 0, 0, 8],
    "twinsage-glintstone-crown": [0, 0, 0, 0, 0, 6, 0, 0],
    "witchs-glintstone-crown": [0, 0, 0, 0, 0, 3, 0, 3],
}

IGNORED_WEAPON_INFUSIONS = [
    "heavy-crossbow",
    "bloody-helice",
    "mohgwyns-sacred-spear",
    "sacred-relic-sword",
    "treespear",
    "serpentbone-blade",
]
