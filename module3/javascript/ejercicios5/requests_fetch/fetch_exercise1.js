/*
1. Cree una función que liste todos los elementos retornados de un GET al endpoint /objects,
   filtrando aquellos que no tengan data y mostrando los resultados de forma legible.
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
    const filtered = all_data.filter(obj => obj.data !== null);
    console.log("3. Object Data collected:");
    console.log("4. Request is done.");
    return filtered;
  } catch (error) {
    console.log(`Error: ${error.message}`);
  }
}

async function main() {
  const data = await getObjects();
  console.log("5. Getting all objects:", data);

}

main();