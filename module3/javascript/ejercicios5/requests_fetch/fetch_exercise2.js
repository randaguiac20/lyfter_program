/*
1. Cree una función que liste todos los elementos retornados de un GET al endpoint /objects,
   filtrando aquellos que no tengan data y mostrando los resultados de forma legible.
2. Cree una función que tome como parámetro la información de un objeto y cree un nuevo objeto 
   utilizando el endpoint POST.
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

  } catch (error) {
    console.log(`Error in getObjects: ${error.message}`);
  }
}

// POST a new object — returns the created object or null on error
async function postNewObject(newObject) {
  console.log("--- POST New Object ---");

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newObject),
    });

    if (!response.ok) {
      throw new Error(`Object was not created (status: ${response.status})`);
    }

    const created = await response.json();
    console.log("Object created successfully:");
    console.log(`ID: ${created.id}`);
    console.log(`Name: ${created.name}`);
    console.log("Data:", created.data);

    return created;

  } catch (error) {
    console.log(`Error in postNewObject: ${error.message}`);
    return null;
  }
}


async function main() {
  await getObjects();

  const newObject = {
    name: "my custom device",
    data: {
      color: "black",
      capacity: "256 GB",
    },
  };
  const created = await postNewObject(newObject);
  console.log("Returned from postNewObject:", created);
}

main();