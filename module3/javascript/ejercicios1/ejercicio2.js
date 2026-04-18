/* Realiza un programa que recorra una lista de números
 y almacene todos los pares en otra lista
 Para este ejercicio intenta hacer una solución 
 con un for y otra utilizando la función filter */

const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
const evens = []


for (const number of numbers) {
    if (number % 2 === 0) {
        evens.push(number);
    }
}

console.log(`All numbers: ${numbers}\n\nEven numbers: ${evens}`);
