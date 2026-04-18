/* 
Toma un string y conviertelo en una lista de palabras,
separandolas por espacios en blanco. No puedes usar la función split.
*/

const text = "This is a test with java script";
const words = [];
let currentWord = "";

for (const char of text) {
  if (char === " ") {
    if (currentWord !== "") {
      words.push(currentWord);
      currentWord = "";
    }
  } else {
    currentWord += char;
  }
}

if (currentWord !== "") {
  words.push(currentWord);
}

console.log(words);
// ["This", "is", "a", "test", "with", "java", "script"]