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
  console.log("--- GET All Objects ---");
  try {
    const response = await userInstance.get();
    const allObjects = response.data;

    // Filter out objects that have no data, empty data, or null data
    const filtered = allObjects.filter(obj => obj.data !== null && obj.data !== undefined && Object.keys(obj.data).length > 0);

    console.log("Objects with data:");
    filtered.forEach(obj => {
      console.log(`ID: ${obj.id}`);
      console.log(`Name: ${obj.name}`);
      console.log("Data:", obj.data);
      console.log("---");
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

async function getObject(id) {
  console.log(`--- GET Object (id: ${id}) ---`);
  try {
    const response = await userInstance.get(`/${id}`);
    const data = response.data;
    console.log("Object found:");
    console.log(`ID: ${data.id}`);
    console.log(`Name: ${data.name}`);
    console.log("Data:", data.data);
    return data;
  } catch (error) {
    if (error.response) {
      console.log("Status:", error.response.status);
      console.log("Error data:", error.response.data);
    } else {
      console.log("Network error:", error.message);
    }
  }
}

async function postNewObject(newObject) {
  try {
    const response = await userInstance.post('', newObject);
    console.log("--- POST New Object ---");
    const created = response.data;
    console.log("Object created successfully:");
    console.log(`ID: ${created.id}`);
    console.log(`Name: ${created.name}`);
    console.log("Data:", created.data);
    console.log("POST is done.");
    return created;
  } catch (error) {
    if (error.response) {
      console.log("Status:", error.response.status);
      console.log("Error data:", error.response.data);
    } else {
      console.log("Network error:", error.message);
    }
  }
}

async function updateObject(id, updatedObject) {
  console.log(`--- PUT Update Object (id: ${id}) ---`);
  try {
    const response = await userInstance.put(`/${id}`, updatedObject);
    console.log("Updating existent object");
    const updated = response.data;
    console.log("Object updated successfully:");
    console.log(`ID: ${updated.id}`);
    console.log(`Name: ${updated.name}`);
    console.log("Data:", updated.data);
    console.log("PUT is done.");
    return updated;
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
  // 1. Get all objects
  await getObjects();
  
  // 2. Create a new object
  const newObject = {
    name: "my custom device",
    data: {
      color: "black",
      capacity: "256 GB"
    }
  };
  const createdObject = await postNewObject(newObject);
  
  // 3. Get one object by ID
  await getObject(10);
 
  // 4. Update an existing object
  const updatedObject = {
    name: 'Google Pixel 6 MAX',
    data: { color: 'Cloudy White', capacity: '256 GB' }
  }
  const updatedID = createdObject.id;
  await updateObject(updatedID, updatedObject);
}

main();