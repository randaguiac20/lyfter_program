/*
Cree cuatro promesas, donde cada una resuelve a una de
las palabras de la lista ["very", "dogs", "cute", "are"]
respectivamente, en el mismo orden. Utilice la combinación
de la función setTimeout y Promse.all() para obtener
la salida "Dogs are very cute",
sin modificar el orden de la lista manualmente o mediante un sort.
*/

const word_list = ["very", "dogs", "cute", "are"];
const timeouts = [300, 100, 400, 200];
const result = [];

const promises = word_list.map((word, i) =>
  new Promise(resolve => setTimeout(() => { 
        result.push(word);
        resolve();
    }, timeouts[i]
  )
 )
);

Promise.all(promises).then(() => {
  const sentence = result.join(" ");
  console.log(sentence.charAt(0).toUpperCase() + sentence.slice(1));
});