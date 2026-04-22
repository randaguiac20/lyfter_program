/*
Realice el mismo ejercicio anterior, pero con el URL https://reqres.in/api/users/23 para generar un error.
Realice el manejo de error adecuado e imprima un mensaje de error indicando que el usuario no se encontró.
*/

// Create a ".env" file with the key in it
// API_KEY=reqres_xdfgdgdg
require("dotenv").config();

const userId = 23;

async function getUser() {
  console.log("1. Enviando request");
  try {
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
  } catch (error) {
    console.log(`Error: ${error.message}`);
  }
}

getUser();
console.log("5. Codigo llegado al final");