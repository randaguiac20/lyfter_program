/*
Realice un programa que utilice la función fetch para solicitar un usuario del API anterior.
El URL debe ser https://reqres.in/api/users/2. 
Al finalizar la solicitud, imprima los datos del usuario en pantalla.
*/

// Create a ".env" file with the key in it
// API_KEY=reqres_xdfgdgdg
const path = require("path");
require("dotenv").config({ path: path.join(__dirname, ".env") });


const userId = 1;

console.log("1. Enviando request")
const user = fetch(`https://reqres.in/api/users/${userId}`, {
    headers: {
      "x-api-key": process.env.API_KEY,
    },
  });
user.then((response)=>{
  console.log("2. Response recibido");
  return response.json();
}).then((data)=>{
  console.log("3. Data:", data.data);
  console.log("4. Await terminado");
});

console.log("6. Codigo llegado al final");
