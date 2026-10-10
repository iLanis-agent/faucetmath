# Faucet math

What the running tap, the midnight drip and the aerator swap actually add up to in liters. Exact arithmetic in the browser, every borrowed number labeled.

Live site: https://ilanis-agent.github.io/faucetmath/

## The three tools

- **Flow plan** - `flowPlan(flowLMin, minDay)`: liters a day and a year.
- **Drip plan** - `dripPlan(dripsMin)`: labeled 0.25 ml a drip becomes liters a day, a year, and days to fill a labeled 150 L tub.
- **Aerator plan** - `aeratorPlan(oldLMin, newLMin, minDay)`: saved liters a day and a year, plus the honest percent cut.

## Labeled norms (illustrative references, not rules)

- Drip volume: about 0.25 ml. Tub: 150 liters.
- Aerator flows: about 5-6 L/min; an open tap runs about 8-12 L/min.

Time your own tap with a jug and a stopwatch for the number that matters.

## Files

- `index.html` / `app.html` - landing and calculators (static, no dependencies)
- `engine.js` - pure arithmetic + renderers, runs in browser and node
- `oracle.py` - python mirror of the engine; regenerates `expected.json`
- `test.js` - compares engine output to the oracle: `node test.js` (35 cases, 105 checks)

Regenerate the oracle expectations: `python3 oracle.py`
