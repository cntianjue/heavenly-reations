const { calculate } = require('../src/calculator');

function assertEqual(actual, expected, message) {
  if (actual !== expected) {
    throw new Error(message + '. Expected ' + expected + ', got ' + actual);
  }
}

function assertThrows(fn, expectedMessage, message) {
  try {
    fn();
  } catch (error) {
    if (error.message !== expectedMessage) {
      throw new Error(message + '. Expected error message "' + expectedMessage + '", got "' + error.message + '"');
    }
    return;
  }

  throw new Error(message + '. Expected function to throw');
}

assertEqual(calculate(1, 2, 'add'), 3, 'addition should work');
assertEqual(calculate(5, 3, 'subtract'), 2, 'subtraction should work');
assertEqual(calculate(4, 3, 'multiply'), 12, 'multiplication should work');
assertEqual(calculate(8, 2, 'divide'), 4, 'division should work');

assertThrows(
  function () {
    calculate(8, 0, 'divide');
  },
  'Cannot divide by zero',
  'divide by zero should throw'
);

console.log('calculator tests passed');
