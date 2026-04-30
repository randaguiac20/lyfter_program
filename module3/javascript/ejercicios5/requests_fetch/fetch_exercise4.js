/*
1. Cree una función que liste todos los elementos retornados de un GET al endpoint /objects,
   filtrando aquellos que no tengan data y mostrando los resultados de forma legible.
2. Cree una función que tome como parámetro la información de un objeto y cree un nuevo objeto 
   utilizando el endpoint POST.
3. Cree una función que retorne un objeto del API, tomando su ID como parámetro.
4. Cree una función que actualice la información de un objeto, tomando como parámetros su ID
   y los nuevos datos a modificar.
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

// GET a single object by ID — returns the object or null if not found
async function getObject(id) {
  console.log(`--- GET Object (id: ${id}) ---`);

  try {
    const response = await fetch(`${url}/${id}`);

    if (!response.ok) {
      console.log(`Object with id ${id} was not found (status: ${response.status})`);
      return null;
    }

    const data = await response.json();
    console.log("Object found:");
    console.log(`ID: ${data.id}`);
    console.log(`Name: ${data.name}`);
    console.log("Data:", data.data);

    return data;

  } catch (error) {
    console.log(`Error in getObject: ${error.message}`);
    return null;
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

// PUT (update) an existing object by ID — returns the updated object or null on error
async function updateObject(id, updatedObject) {
  console.log(`--- PUT Update Object (id: ${id}) ---`);

  try {
    const response = await fetch(`${url}/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updatedObject),
    });

    if (!response.ok) {
      throw new Error(`Object was not updated (status: ${response.status})`);
    }

    const updated = await response.json();
    console.log("Object updated successfully:");
    console.log(`ID: ${updated.id}`);
    console.log(`Name: ${updated.name}`);
    console.log("Data:", updated.data);

    return updated;

  } catch (error) {
    console.log(`Error in updateObject: ${error.message}`);
    return null;
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
      capacity: "256 GB",
    },
  };
  const created = await postNewObject(newObject);
  console.log("Returned from postNewObject:", created);

  // 3. Get one object by ID
  const found = await getObject(1);
  console.log("Returned from getObject:", found);

  // 4. Update an existing object
  const updatedObject = {
    name: "Google Pixel 6 MAX",
    data: { color: "Cloudy White", capacity: "256 GB" },
  };
  const updatedID = "ff8081819d82fab6019dcc432b3f508b";
  const updated = await updateObject(updatedID, updatedObject);
  console.log("Returned from updateObject:", updated);
}

main();