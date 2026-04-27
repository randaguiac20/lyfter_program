/*
1. Cree una función que liste todos los elementos retornados de un GET 
   al endpoint /objects, filtrando aquellos que no tengan data y mostrando
   los resultados de forma legible.
*/

import axios from "axios";

const userInstance = axios.create({
  baseURL: 'https://api.restful-api.dev/objects',
  timeout: 1000,
  headers: {"Content-Type": "application/json"}
});

async function getObjects () {
	console.log("Loading objects...");
    try {
      const response = await userInstance.get();
      console.log("Data loaded! Returning...");
      return response.data;
    } catch (error) {
      console.log("Status:", error.response.status);
      console.log("Error data:", error.response.data);
  }
}

async function main() {
  const data = await getObjects();
  console.log("Getting all objects:", data);

}

main();