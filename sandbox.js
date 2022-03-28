const sum = (a, b) => a + b;

let item = {
    "id": "longsword",
    "name": "Longsword",
    "requirements": [10, 10, 0, 0, 0],
    "infusions": {
        "standard": {
            "damage": [110, 0, 0, 0, 0],
            "scaling": [0.5, 0.33, 0.0, 0.0, 0.0],
            "masks": [
                [1, 1, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 1, 0],
                [0, 1, 0, 0, 0],
                [0, 0, 0, 1, 0]
            ],
            "caps": [
                [1, 18, 60, 80, 150],
                [1, 18, 60, 80, 150],
                [1, 18, 60, 80, 150],
                [1, 18, 60, 80, 150],
                [1, 18, 60, 80, 150]
            ],
            "growth": [
                [0, 25, 75, 90, 110],
                [0, 25, 75, 90, 110],
                [0, 25, 75, 90, 110],
                [0, 25, 75, 90, 110],
                [0, 25, 75, 90, 110]
            ],
            "adjustments": [
                [1.2, -1.2, 1.0, 1.0, 1.0],
                [1.2, -1.2, 1.0, 1.0, 1.0],
                [1.2, -1.2, 1.0, 1.0, 1.0],
                [1.2, -1.2, 1.0, 1.0, 1.0],
                [1.2, -1.2, 1.0, 1.0, 1.0]
            ]
        }
    }
}

let infusion = {
    "id": "standard",
    "name": "Standard",
    "damage": [1.0, 1.0, 1.0, 1.0, 1.0],
    "upgrade": [0.058, 0.058, 0.058, 0.058, 0.058],
    "scaling": [1.0, 1.0, 1.0, 1.0, 1.0],
    "growth": [0.02, 0.02, 0.03243, 0.03243, 0.03243]
}

let stats = [20, 10, 10, 10, 10]

function damage(item, infusion, stats, upgrade) {
    let itemData = item.infusions[infusion.id];

    let bases = infusion.damage.map((ty, i) => itemData.damage[i] * (ty + infusion.upgrade[i] * upgrade));

    let statModifiers = modifiers(itemData, stats);
    let extras = bases.map((dmgTypeAmount, i) => {
        let scalings = itemData.scaling.map(itemScaling => {
            return (itemScaling * infusion.scaling[i] + itemScaling * infusion.scaling[i] * infusion.growth[i] * upgrade);
        })
        let extras = scalings.map((statScaling, j) => dmgTypeAmount * statScaling * statModifiers[i][j] / 100.0)
        return extras.reduce(sum);
    });

    console.log(statModifiers);
    console.log(bases);
    console.log(extras)

    return Math.floor(bases.reduce(sum) + extras.reduce(sum));
}

function modifiers(infusion, stats) {
    return infusion.masks.map(m => {
        return stats.map((stat, i) => {
            let capIndex = infusion.caps[i].findIndex(cap => cap >= stat) - 1;
            let cap = infusion.caps[i][capIndex];
            let capDelta = (infusion.caps[i][capIndex + 1] || cap) - cap;
            let growth = infusion.growth[i][capIndex];
            let growthDelta = (infusion.growth[i][capIndex + 1] || growth) - growth;
            let adjust = infusion.adjustments[i][capIndex];

            if (Math.sign(adjust) != -1) {
                return m[i] * (growth + growthDelta * ((stat - cap) / capDelta) ** adjust);
            } else {
                return m[i] * (growth + growthDelta * (1 - (1 - ((stat - cap) / capDelta)) ** Math.abs(adjust)));
            }
        })
    });
}

for (u = 0; u < 26; u++) {
    console.log("+" + u + ": " + damage(item, infusion, stats, u))
}

