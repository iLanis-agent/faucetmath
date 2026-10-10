#!/usr/bin/env python3
"""Oracle mirror of engine.js for Faucet math. Writes expected.json (with trailing newline)."""
import json, math

def r1(x): return math.floor(x * 10 + 0.5) / 10

def article(n):
    s = str(int(n)) if isinstance(n, float) and n == int(n) else str(n)
    return "an" if s.startswith(("8", "11", "18")) else "a"

def jsnum(x):
    if isinstance(x, float) and x == int(x) and abs(x) < 1e15:
        return int(x)
    return x

def fmt(x):
    if isinstance(x, float) and x == int(x):
        return str(int(x))
    return repr(x) if isinstance(x, float) else str(x)

def flowPlan(flowLMin, minDay):
    if not (flowLMin > 0) or not (minDay > 0):
        return {"error": "flow and minutes must be positive"}
    perDay = flowLMin * minDay
    perYear = math.floor(perDay * 365 + 0.5)
    return {"flowLMin": jsnum(float(flowLMin)), "minDay": jsnum(float(minDay)), "perDayL": jsnum(r1(perDay)), "perYearL": perYear}

def dripPlan(dripsMin):
    if not (dripsMin > 0):
        return {"error": "drip rate must be positive"}
    perDay = dripsMin * 0.25 * 60 * 24 / 1000
    perYear = math.floor(perDay * 365 + 0.5)
    tubDays = r1(150 / perDay)
    return {"dripsMin": jsnum(float(dripsMin)), "perDayL": jsnum(r1(perDay)), "perYearL": perYear, "tubDays": jsnum(tubDays)}

def aeratorPlan(oldLMin, newLMin, minDay):
    if not (oldLMin > 0) or not (newLMin > 0) or not (minDay > 0):
        return {"error": "flows and minutes must be positive"}
    if newLMin >= oldLMin:
        return {"error": "the new flow must be lower than the old flow"}
    savedDay = (oldLMin - newLMin) * minDay
    savedYear = math.floor(savedDay * 365 + 0.5)
    cutPct = r1((oldLMin - newLMin) / oldLMin * 100)
    return {"oldLMin": jsnum(float(oldLMin)), "newLMin": jsnum(float(newLMin)), "minDay": jsnum(float(minDay)),
            "savedDayL": jsnum(r1(savedDay)), "savedYearL": savedYear, "cutPct": jsnum(cutPct)}

def renderFlow(r):
    return (article(r["flowLMin"]) + " " + fmt(r["flowLMin"]) + " L/min tap running " + fmt(r["minDay"]) + " minutes a day uses " + fmt(r["perDayL"]) +
            " liters a day - about " + str(r["perYearL"]) + " liters a year.")

def renderDrip(r):
    return ("At a labeled 0.25 ml a drip, " + fmt(r["dripsMin"]) + " drips a minute is " + fmt(r["perDayL"]) +
            " liters a day - about " + str(r["perYearL"]) + " liters a year, a labeled 150 L tub every " + fmt(r["tubDays"]) + " days.")

def renderAerator(r):
    return ("Swapping " + article(r["oldLMin"]) + " " + fmt(r["oldLMin"]) + " L/min tap for " + article(r["newLMin"]) + " " + fmt(r["newLMin"]) + " L/min aerator at " + fmt(r["minDay"]) +
            " minutes a day saves " + fmt(r["savedDayL"]) + " liters a day - about " + str(r["savedYearL"]) +
            " liters a year, a " + fmt(r["cutPct"]) + "% cut.")

CASES = []
def add(fn, args): CASES.append({"fn": fn, "args": args})

for a in [(8, 12), (5, 20), (6, 8), (10, 15), (4, 30), (7.5, 10), (3, 45), (12, 6), (2, 60), (0, 12), (8, 0), (8, -5)]:
    add("flowPlan", list(a))
for a in [(20,), (10,), (5,), (30,), (60,), (1,), (45,), (15,), (25,), (0,), (-10,)]:
    add("dripPlan", list(a))
for a in [(8, 5, 12), (6, 3, 20), (10, 6, 15), (7.5, 5, 8), (12, 8, 10), (5, 4, 30), (9, 4.5, 6), (5, 5, 12), (5, 6, 12), (0, 5, 12), (8, 0, 12), (8, 5, 0)]:
    add("aeratorPlan", list(a))

out = []
for c in CASES:
    fn = {"flowPlan": flowPlan, "dripPlan": dripPlan, "aeratorPlan": aeratorPlan}[c["fn"]]
    res = fn(*c["args"])
    is_err = "error" in res
    if is_err:
        render = res["error"]
    else:
        render = {"flowPlan": renderFlow, "dripPlan": renderDrip, "aeratorPlan": renderAerator}[c["fn"]](res)
    out.append({"fn": c["fn"], "args": c["args"], "result": res, "render": render, "isError": is_err})

with open("expected.json", "w") as f:
    f.write(json.dumps(out, separators=(",", ":")) + "\n")
print("wrote", len(out), "cases")
