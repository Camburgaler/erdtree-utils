# Notes

## Running

### Regulation Extraction

1. [UXM](https://cdn.discordapp.com/attachments/529900741998149643/949045219175825448/UXM_2.4.ER_EldenRingQuickhack.zip) to extract the game files.
2. [Yapped (Rune Bear)](https://github.com/vawser/Yapped-Rune-Bear) for converting regulation to `.csv`.

## Required Files

-   `CharaInitParam.csv`
-   `EquipParamAccessory.csv`
-   `EquipParamProtector.csv`
-   `EquipParamWeapon.csv`
-   `ReinforceWeaponParam.csv`
-   `SpEffectParam.csv`

## Param Categories

### Armor

-   Weight: `EquipParamProtector.csv`
-   Poise: `EquipParamProtector.csv` - in-game poise value is $(poise \cdot 1000)$
-   Resistance: `EquipParamProtector.csv`
-   Defenses: `EquipParamProtector.csv` - defense is $(1 - absorption) \cdot 100$
-   Stats: ???

### Classes

-   Starting: `CharaInitParam.csv`
-   Softcaps: `CalcCorrectGraph.csv`

### Weapons

-   Damage: `EquipParamWeapon.csv`
-   Upgrading: `ReinforceParamWeapon.csv`
-   Scaling: `EquipParamWeapon.csv`
-   Ash of War: `EquipParamGem.csv`

### Talismans

-   Weight: `EquipParamAccessory.csv`
-   Stats: `SpEffectParam.csv`
-   Effects: `SpEffectParam.csv`

### Magic

-   FP cost: `Magic.csv`
-   Stam. cost: `Magic.csv`
-   Reqs.: `Magic.csv`
