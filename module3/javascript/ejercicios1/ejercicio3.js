/* Toma una lista de temperaturas en grados celsius
 y conviertala a farenheit utilizando la función map */

const celsius = [0, 10, 20, 30, 40];
const fahrenheit = celsius.map(temp => (temp * 9/5) + 32);

console.log(`\nCelsius: ${celsius}\nFahrenheit: ${fahrenheit}\n`);
// Fahrenheit: 32,50,68,86,104