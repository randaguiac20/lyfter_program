# Ejercicio de Caché

- Para este ejercicio nos vamos a basar en la solución del ejercicio anterior ([Ejercicio de Authorization])
- Puedes copiar cualquier código que hayamos visto en clase, o utilizado en las guías.
- Todo el manejo de la DB debe ser mediante ORM, no se permite utilizar scripts directos en SQL.

## Planteo

- Necesitamos implementar caching en los endpoints GET relacionados a las frutas para optimizar las consultas.
- Tambien es necesario que ese caché se invalide correctamente cada vez que una fruta es creada, actualizada o eliminada.
    - Pero solo se debe invalidar para cada fruta específica.

## Solución

- Para la solución debes entregar los archivos utilizados en el ejercicio anterior, con las modificaciones necesarias, y todos los nuevos archivos que se crearon para implementar la solución que se require.
- Para el caching, debes de usar una instancia de Redis.
- Asegúrate de probar sus endpoints mediante Postman, Insomnia o cURL, para verificar que funcionen adecuadamente.
- Para cualquier error del sistema, ya sea interno, o de autenticación, se espera que el servidor retorne los códigos adecuados para cada caso donde pueda fallar. Recuerda consultar la 