E-COMMERCE

Facts:

- Pet products.

Issue:

- All purchases info is in an excell file.
- Payments are done via sinpe.

Ask:

- Provide a way to manage stock and sales of the products.


Requirements:

- Users module.
	Functionalities:
		. Must allow operations like user registration and login.
		. Must validate user priviledges to restrict level of access when doing a CRUD operation.
		. Roles are administrator and client.


- Authentiation module.
	Functionalities:
		. Manage authentication.
		. Manage and validate sessions/tokens against any API call in other modules.
		

- Products module.
	Functionalities:
		. Manage registration of products.
		. Manage products inventory.
		. Must allow CRUD.
		. Stock must be updated and a sales is done.


- Sales module.
	Functionalities:
		. Cart: create carts, manage products and manage any previous cart createed if not finalized.
		. Sales: take carts into sales. Generate a receipt. Modify products as needed properly aligned to the stock. Needs receipt address and payment data.
		. Receipts: enable option to check receipts based on receipt number. It should be able to manage return of a product and keep stock properly updated.

- Implement caching (Justify why caching was implemented in a endpoint and the TTL for it if any.).
- Only admin users can do CRUD operation through the endpoints.
- Clients can read data, access sales and carts.
- Git code should have a README file.


First project progress:

- Build an API where all modules requested are implemented.
- All modules must have CRUD operations for any entity, i,e products, receipts, users.
- Authentication modules requires user registration and login (No to be functional on this first progress).
- All data need to be managed via json files.
- Suggestion: create a module to read and write files.


Deliverables:

- A PR with the code requested.
- Instructions to execute the code.