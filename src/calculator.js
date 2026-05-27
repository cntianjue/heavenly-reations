function calculate(firstNumber, secondNumber, operator) {
  switch (operator) {
    case 'add':
      return firstNumber + secondNumber;
    case 'subtract':
      return firstNumber - secondNumber;
    case 'multiply':
      return firstNumber * secondNumber;
    case 'divide':
      if (secondNumber === 0) {
        throw new Error('Cannot divide by zero');
      }
      return firstNumber / secondNumber;
    default:
      throw new Error('Unsupported operator');
  }
}

function readNumber(inputId) {
  const value = document.getElementById(inputId).value;

  if (value === '') {
    throw new Error('Please enter both numbers');
  }

  const number = Number(value);

  if (Number.isNaN(number)) {
    throw new Error('Please enter valid numbers');
  }

  return number;
}

function showResult(result) {
  document.getElementById('result').textContent = 'Result: ' + result;
  document.getElementById('error').textContent = '';
}

function showError(message) {
  document.getElementById('result').textContent = 'Result: --';
  document.getElementById('error').textContent = message;
}

function handleCalculate() {
  try {
    const firstNumber = readNumber('firstNumber');
    const secondNumber = readNumber('secondNumber');
    const operator = document.getElementById('operator').value;
    const result = calculate(firstNumber, secondNumber, operator);

    showResult(result);
  } catch (error) {
    showError(error.message);
  }
}

function handleClear() {
  document.getElementById('firstNumber').value = '';
  document.getElementById('secondNumber').value = '';
  document.getElementById('operator').value = 'add';
  document.getElementById('result').textContent = 'Result: --';
  document.getElementById('error').textContent = '';
}

if (typeof document !== 'undefined') {
  document.getElementById('calculateBtn').addEventListener('click', handleCalculate);
  document.getElementById('clearBtn').addEventListener('click', handleClear);
}

if (typeof module !== 'undefined') {
  module.exports = {
    calculate
  };
}
