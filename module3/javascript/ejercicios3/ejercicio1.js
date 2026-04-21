/*
Cree una función que reciba tres parámetros: un número y dos funciones de callback.
Si el número es par, se debe ejecutar el primer callback.
Este debe mostrar “The number is even!”.
Si el número es impar, se debe ejecutar el segundo.
Este debe mostrar “The number is odd!”.
*/

function onEven() {
    console.log("The number is even!")
}
function onOdd() {
    console.log("The number is odd!")
}

function checkNumber(num, evenCallback, oddCallback) {
    if (num % 2 === 0) {
        evenCallback();
    } else {
        oddCallback();
    }
}

const readline = require("readline");

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.question("\nEnter a number: ", (answer) => {
    const num = Number(answer);

    if (answer.trim() === "" || isNaN(num)) {
        console.log("This is not a number!");
    } else {
        checkNumber(num, onEven, onOdd);
    }
    console.log("\n");
    rl.close();
});