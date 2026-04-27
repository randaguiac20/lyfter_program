/*
1. Cree una función que liste todos los elementos retornados de un GET 
   al endpoint /objects, filtrando aquellos que no tengan data y mostrando
   los resultados de forma legible.
2. Cree una función que tome como parámetro la información de un objeto
   y cree un nuevo objeto utilizando el endpoint POST.
3. Cree una función que retorne un objeto del API, tomando su ID como parámetro.
4. Cree una función que actualice la información de un objeto, tomando como 
   parámetros su ID y los nuevos datos a modificar.
*/

import axios from "axios";


const userInstance = axios.create({
  baseURL: "https://api.restful-api.dev/objects",
  timeout: 1000,
  headers: {
    "Content-Type": "application/json"
  }
});

async function getObjects() {
	console.log("Loading objects...");
    try {
      const response = await userInstance.get();
      const data = response.data;
      console.log("Getting all objects:", data);
      return data;
    } catch (error) {
    console.log("Status:", error.response.status);
    console.log("Error data:", error.response.data);
  }
}

async function getObject(id) {
	console.log("Loading object...");
    try {
      const response = await userInstance.get(`/${id}`);
      const data = response.data;
      console.log("Getting object:", data);
      return data;
    } catch (error) {
      console.log("Status:", error.response.status);
      console.log("Error data:", error.response.data);
  }
}

async function updateObject(id, updatedObject) {
  
  try {
    const response = await userInstance.put(`/${id}`, updatedObject);
    console.log("Updating existent object");
    const data = response.data;
    console.log("Object updated:", response.data);
    console.log("POST is done.");
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
    return data;
  } catch (error) {
    console.log("Status:", error.response.status);
    console.log("Error data:", error.response.data);
  }
}

async function main() {
  const data = await getObjects();
  const newObject = {
    name: "my custom device",
    data: {
      color: "black",
      capacity: "256 GB"
    }
  };
  const createdObject = await postNewObject(newObject);
  const id = 10
  await getObject(id);

  const updatedObject = {
    name: 'Google Pixel 6 MAX',
    data: { color: 'Cloudy White', capacity: '256 GB' }
  }
  const updatedID = createdObject.id;
  await updateObject(updatedID, updatedObject);
}

main();