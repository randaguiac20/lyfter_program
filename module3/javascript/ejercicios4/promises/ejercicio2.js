/*
Realice el mismo ejercicio anterior utilizando la función Promse.any()
para mostrar el nombre del primer pokemón que esté contenido
en la primera promesa que se resuelva.
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

Promise.any(promises)
  .then((pokemon) => {
    console.log(pokemon.name);
  });
