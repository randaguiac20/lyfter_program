/*
Realice un programa que utilice la función fetch para solicitar un usuario del API anterior.
El URL debe ser https://reqres.in/api/users/2. 
Al finalizar la solicitud, imprima los datos del usuario en pantalla.
*/

// Create a ".env" file with the key in it
// API_KEY=reqres_xdfgdgdg
const path = require("path");
require("dotenv").config({ path: path.join(__dirname, ".env") });


const userId = 23;

console.log("1. Enviando request")
const user = fetch(`https://reqres.in/api/users/${userId}`, {
    headers: {
      "x-api-key": process.env.API_KEY,
    },
  });

user.then((response)=>{
  console.log("2. Response recibido");
  if (!response.ok) {
      throw new Error(`Usuario no encontrado (status: ${response.status})`);
    }
  return response.json();
}).then((data)=>{
  console.log("3. Data:", data.data);
  console.log("4. Await terminado");
}).catch((error)=>{
  console.log(`4. Hubo un problema: ${error}`);
}).finally(()=>{
  console.log("5. Promise terminado");
});

console.log("6. Codigo llegado al final");
