/*
1. Cree una función que liste todos los elementos retornados de un GET 
   al endpoint /objects, filtrando aquellos que no tengan data y mostrando
   los resultados de forma legible.
2. Cree una función que tome como parámetro la información de un objeto
   y cree un nuevo objeto utilizando el endpoint POST.
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
      console.log("Data loaded! Returning...");
      return response.data;
    } catch (error) {
    console.log("Status:", error.response.status);
    console.log("Error data:", error.response.data);
  }
}

async function postNewObject(newObject) {
  
  try {
    const response = await userInstance.post('', newObject);
    console.log("Posting new object");
    const data = response.data;
    console.log("Object created:", data);
    console.log("POST is done.");
  } catch (error) {
    console.log("Status:", error.response.status);
    console.log("Error data:", error.response.data);
  }
}

async function main() {
  const data = await getObjects();
  console.log("Getting all objects:", data);
  const newObject = {
    name: "my custom device",
    data: {
      color: "black",
      capacity: "256 GB"
    }
  };
  await postNewObject(newObject);
}

main();