const fs = require("fs");

const sum = (a, b) => a + b;

let weapons = JSON.parse(fs.readFileSync("./output/weapons.json"));
let corrections = JSON.parse(fs.readFileSync("./output/damage.json"));
let infusions = JSON.parse(fs.readFileSync("./output/infusions.json"));

let weapon = weapons.find((item) => item.id == "longsword");
let infusion = infusions.find((inf) => inf.id == "standard");
let stats = { STR: 20, DEX: 10, INT: 10, FTH: 10, ARC: 10 };

function damage(item, infusion, stats, upgrade) {
    let itemInfusion = item.infusions[infusion.id];

    let bases = infusion.damage.map(
        (amount, ty) =>
            itemInfusion.damage[ty] * (amount + infusion.upgrade[ty] * upgrade)
    );

    let extras = bases.map((amount, ty) => {
        let calc = corrections.find(
            (c) => c.id == itemInfusion.corrections[ty]
        );
        let correction = modifiers(calc, stats, itemInfusion.masks[ty]);
        console.log(correction);
        let scalings = itemInfusion.scaling.map((itemScaling) => {
            return (
                itemScaling * infusion.scaling[ty] +
                itemScaling *
                    infusion.scaling[ty] *
                    infusion.growth[ty] *
                    upgrade
            );
        });
        let extras = scalings.map(
            (statScaling, j) => (amount * statScaling * correction[j]) / 100.0
        );
        return extras.reduce(sum);
    });

    console.log("base dmg:  " + bases);
    console.log("extra dmg: " + extras);

    return Math.floor(bases.reduce(sum) + extras.reduce(sum));
}

function modifiers(calc, stats, masks) {
    return Object.keys(stats).map((statId, ty) => {
        let mask = masks[ty];
        if (mask == 0) {
            return 0.0;
        }

        let capIndex =
            calc.softcaps[ty].findIndex((cap) => cap >= stats[statId]) - 1;
        let cap = calc.softcaps[ty][capIndex];
        let capDelta = (calc.softcaps[ty][capIndex + 1] || cap) - cap;
        let growth = calc.growth[ty][capIndex];
        let growthDelta = (calc.growth[ty][capIndex + 1] || growth) - growth;
        let adjust = calc.adjustments[ty][capIndex];

        if (Math.sign(adjust) != -1) {
            return (
                growth +
                growthDelta * ((stats[statId] - cap) / capDelta) ** adjust
            );
        } else {
            return (
                growth +
                growthDelta *
                    (1 -
                        (1 - (stats[statId] - cap) / capDelta) **
                            Math.abs(adjust))
            );
        }
    });
}

for (u = 0; u < 26; u++) {
    console.log("+" + 25 + ": " + damage(weapon, infusion, stats, 25));
}
