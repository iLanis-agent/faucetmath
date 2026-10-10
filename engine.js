/* Faucet math engine - pure arithmetic, every borrowed number labeled. */
(function (root) {
  "use strict";
  function r1(x) { return Math.round(x * 10) / 10; }
  function article(n) { return /^(8|11|18)/.test(String(n)) ? "an" : "a"; }

  function flowPlan(flowLMin, minDay) {
    if (!(flowLMin > 0) || !(minDay > 0)) return { error: "flow and minutes must be positive" };
    var perDay = flowLMin * minDay;
    var perYear = Math.round(perDay * 365);
    return { flowLMin: flowLMin, minDay: minDay, perDayL: r1(perDay), perYearL: perYear };
  }

  function dripPlan(dripsMin) {
    if (!(dripsMin > 0)) return { error: "drip rate must be positive" };
    var perDay = dripsMin * 0.25 * 60 * 24 / 1000;
    var perYear = Math.round(perDay * 365);
    var tubDays = r1(150 / perDay);
    return { dripsMin: dripsMin, perDayL: r1(perDay), perYearL: perYear, tubDays: tubDays };
  }

  function aeratorPlan(oldLMin, newLMin, minDay) {
    if (!(oldLMin > 0) || !(newLMin > 0) || !(minDay > 0)) return { error: "flows and minutes must be positive" };
    if (newLMin >= oldLMin) return { error: "the new flow must be lower than the old flow" };
    var savedDay = (oldLMin - newLMin) * minDay;
    var savedYear = Math.round(savedDay * 365);
    var cutPct = r1((oldLMin - newLMin) / oldLMin * 100);
    return { oldLMin: oldLMin, newLMin: newLMin, minDay: minDay, savedDayL: r1(savedDay), savedYearL: savedYear, cutPct: cutPct };
  }

  function renderFlow(r) {
    return article(r.flowLMin) + " " + r.flowLMin + " L/min tap running " + r.minDay + " minutes a day uses " + r.perDayL + " liters a day - about " + r.perYearL + " liters a year.";
  }

  function renderDrip(r) {
    return "At a labeled 0.25 ml a drip, " + r.dripsMin + " drips a minute is " + r.perDayL + " liters a day - about " + r.perYearL + " liters a year, a labeled 150 L tub every " + r.tubDays + " days.";
  }

  function renderAerator(r) {
    return "Swapping " + article(r.oldLMin) + " " + r.oldLMin + " L/min tap for " + article(r.newLMin) + " " + r.newLMin + " L/min aerator at " + r.minDay + " minutes a day saves " + r.savedDayL + " liters a day - about " + r.savedYearL + " liters a year, a " + r.cutPct + "% cut.";
  }

  var api = { flowPlan: flowPlan, dripPlan: dripPlan, aeratorPlan: aeratorPlan, renderFlow: renderFlow, renderDrip: renderDrip, renderAerator: renderAerator };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.FaucetMath = api;
})(typeof window !== "undefined" ? window : this);
