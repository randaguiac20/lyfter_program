/*
1. Cree una función que liste todos los elementos retornados de un GET al endpoint /objects,
   filtrando aquellos que no tengan data y mostrando los resultados de forma legible.
2. Cree una función que tome como parámetro la información de un objeto y cree un nuevo objeto 
   utilizando el endpoint POST.
3. Cree una función que retorne un objeto del API, tomando su ID como parámetro.
4. Cree una función que actualice la información de un objeto, tomando como parámetros su ID
   y los nuevos datos a modificar.
*/

const url = "https://api.restful-api.dev/objects"

async function getObjects() {
  console.log("1. Requesting objetcs");
  
  try {
    const response = await fetch(url);
    console.log("2. Objects recevied");
    if (!response.ok) {
      throw new Error(`Objects were not found (status: ${response.status})`);
    }
    const all_data = await response.json();
    const filtered = all_data.filter(obj => obj.data !== null && Object.keys(obj.data).length > 0);
    console.log("3. Object Data collected:");
    console.log("4. Request is done.");
    console.log("5. Getting all objects:", filtered);
  } catch (error) {
    console.log(`Error: ${error.message}`);
  }
}

async function getObject(id) {
  console.log("9. Requesting object");
  
  try {
    const response = await fetch(`${url}/${id}`);
    console.log("10. Object recevied");
    if (!response.ok) {
      throw new Error(`Object was not found (status: ${response.status})`);
    }
    const data = await response.json();
    console.log("11. Object Data collected.");
    console.log("12. Request is done.");
    console.log("13. Getting object:", data);
  } catch (error) {
    console.log(`Error: ${error.message}`);
  }
}

async function updateObject(id, updatedObject) {
  console.log("14. Updating object");
  
  try {
    const response = await fetch(`${url}/${id}`, {
    method: "PUT", // *GET, POST, PUT, DELETE, etc.
    mode: "cors", // no-cors, *cors, same-origin
    cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
    credentials: "same-origin", // include, *same-origin, omit
    headers: {
      "Content-Type": "application/json",
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: "follow", // manual, *follow, error
    referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: JSON.stringify(updatedObject), // body data type must match "Content-Type" header
    });
    console.log("15. New Object recevied");
    if (!response.ok) {
      throw new Error(`Object was not updated (status: ${response.status})`);
    }
    const data = await response.json();
    console.log("16. Object Data collected.");
    console.log("17. Request is done.");
    console.log("18. Updated object:", data);
  } catch (error) {
    console.log(`Error: ${error.message}`);
  }
}

async function postNewObject(newObject) {
  
  try {
    const response = await fetch(url, {
    method: "POST", // *GET, POST, PUT, DELETE, etc.
    mode: "cors", // no-cors, *cors, same-origin
    cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
    credentials: "same-origin", // include, *same-origin, omit
    headers: {
      "Content-Type": "application/json",
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: "follow", // manual, *follow, error
    referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: JSON.stringify(newObject), // body data type must match "Content-Type" header
    });
    console.log("6. Posting new object");
    if (!response.ok) {
      throw new Error(`Object was not created (status: ${response.status})`);
    }
    const data = await response.json();
    console.log("7. Object created:", data);
    console.log("8. POST is done.");
  } catch (error) {
    console.log(`Error: ${error.message}`);
  }
}


async function main() {
  // Get all objects
  await getObjects();

  // Create a new object
  const newObject = {
    id: 14,
    name: "my custom device",
    data: {
      color: "black",
      capacity: "256 GB"
    }
  };
  await postNewObject(newObject);

  // Get one object
  const id = 1
  await getObject(id);

  // Updated object
  const updatedObject = {
    name: 'Google Pixel 6 MAX',
    data: { color: 'Cloudy White', capacity: '256 GB' }
  }
  const updatedID = "ff8081819d82fab6019dcc432b3f508b"
  await updateObject(updatedID, updatedObject);
}

main();