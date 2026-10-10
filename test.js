const E = require('./engine.js');
const cases = require('./expected.json');
let pass = 0, fail = 0;
function chk(name, cond) { if (cond) pass++; else { fail++; console.log('FAIL', name); } }
cases.forEach((c, i) => {
  let actual, render;
  if (c.fn === 'flowPlan') { actual = E.flowPlan(...c.args); render = actual.error || E.renderFlow(actual); }
  else if (c.fn === 'dripPlan') { actual = E.dripPlan(...c.args); render = actual.error || E.renderDrip(actual); }
  else { actual = E.aeratorPlan(...c.args); render = actual.error || E.renderAerator(actual); }
  chk(i + ':' + c.fn + ':result', JSON.stringify(actual) === JSON.stringify(c.result));
  chk(i + ':' + c.fn + ':render', render === c.render);
  chk(i + ':' + c.fn + ':errorflag', (!!actual.error) === c.isError);
});
console.log(cases.length + ' cases, ' + pass + ' checks green, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
