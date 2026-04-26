/*
1. Utilice el API https://pokeapi.co/api/v2/pokemon/:ID para solicitar 3 distintos pokemónes.
2. Utilice la función Promise.all() para mostrar en pantalla el nombre de los tres pokemónes 
   al mismo tiempo, hasta que todas las promesas se resuelvan.
*/

function getPokemon(id) {
  return fetch(`https://pokeapi.co/api/v2/pokemon/${id}`)
    .then(res => res.json());
}

const promises = [
  getPokemon(1),
  getPokemon(22),
  getPokemon(34),
];

Promise.all(promises)
  .then((results) => {
    results.forEach(pokemon => console.log(pokemon.name));
  });