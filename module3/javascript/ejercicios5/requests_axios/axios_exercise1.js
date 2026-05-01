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

async function getObjects() {
  console.log("Loading objects...");
  try {
    const response = await userInstance.get();
    const allObjects = response.data;

    // Filter out objects that have no data, empty data, or null data
    const filtered = allObjects.filter(obj => obj.data !== null && obj.data !== undefined && Object.keys(obj.data).length > 0);

    console.log("Objects with data:");
    filtered.forEach(obj => {
      console.log(`ID: ${obj.id} | Name: ${obj.name} | Data:`, obj.data);
    });

    return filtered;
  } catch (error) {
    if (error.response) {
      console.log("Status:", error.response.status);
      console.log("Error data:", error.response.data);
    } else {
      console.log("Network error:", error.message);
    }
  }
}

async function main() {
  await getObjects();
}

main();