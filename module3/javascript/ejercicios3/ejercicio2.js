/*
Cree dos archivos de texto con el siguiente contenido.
Lea ambos archivos y compare cuales palabras se repiten en ambos.
Muestre el mensaje escondido al final del programa.
*/

const fs = require("fs");

const file1 = fs.readFileSync("file1.txt", "utf8");
const file2 = fs.readFileSync("file2.txt", "utf8");

const words1 = file1.split("\n");
const words2 = file2.split("\n");

const common = words1.filter(word => words2.includes(word));

console.log("Common words:", common);
console.log("Hidden message:", common.join(" "));