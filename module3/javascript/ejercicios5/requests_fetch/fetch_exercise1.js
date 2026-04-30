/*
1. Cree una función que liste todos los elementos retornados de un GET al endpoint /objects,
   filtrando aquellos que no tengan data y mostrando los resultados de forma legible.
*/
const url = "https://api.restful-api.dev/objects";

// GET all objects — filters out items with no data and displays each one clearly
async function getObjects() {
  console.log("--- GET All Objects ---");

  try {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`Could not get objects (status: ${response.status})`);
    }

    const allObjects = await response.json();

    // Safer filter: data must exist, be an object, and have at least one property
    const filtered = allObjects.filter(obj => {
      return obj.data !== null &&
             obj.data !== undefined &&
             typeof obj.data === "object" &&
             Object.keys(obj.data).length > 0;
    });

    console.log(`Found ${filtered.length} objects with data:\n`);

    filtered.forEach(obj => {
      console.log(`ID: ${obj.id}`);
      console.log(`Name: ${obj.name}`);
      console.log("Data:", obj.data);
      console.log("---");
    });

    return filtered;

  } catch (error) {
    console.log(`Error in getObjects: ${error.message}`);
    return null;
  }
}

async function main() {
  const data = await getObjects();
  console.log("Returned from getObjects:", data);
}

main();