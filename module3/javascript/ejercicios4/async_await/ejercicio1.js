/*
Realice un programa que utilice la función fetch para solicitar un usuario del API anterior.
El URL debe ser https://reqres.in/api/users/2. 
Al finalizar la solicitud, imprima los datos del usuario en pantalla.
*/

// Create a ".env" file with the key in it
// API_KEY=reqres_xdfgdgdg

const path = require("path");
require("dotenv").config({ path: path.join(__dirname, ".env") });



async function getUser(userId) {
  console.log("1. Enviando request");
  const response = await fetch(`https://reqres.in/api/users/${userId}`, {
    headers: {
      "x-api-key": process.env.API_KEY,
    },
  });
  console.log("2. Response recibido");
  if (!response.ok) {
    throw new Error(`Usuario no encontrado (status: ${response.status})`);
  }
  const data = await response.json();
  console.log("3. Data:", data.data);
  console.log("4. Await terminado");
}

const id = 2;
getUser(id);
console.log("5. Codigo llegado al final");