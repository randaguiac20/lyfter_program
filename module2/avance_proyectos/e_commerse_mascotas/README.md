# E-Commerce Mascotas API

This project is an API for managing an e-commerce platform for pet products. It supports user registration, authentication, product and inventory management, sales, carts, and receipts, all using JSON files as the data store.

## Important Notes

- When registering an user or product, the user and product will be created automatically.
- For user and product deletion, we need to delete the user or product, so it will be deleting them automatically.
- By default users and products will be disabled, so it requires to update via the put method the status, otherwise user won't be able to login, this needs to be done with administrator user.
- Logic for carts, sales and receipts will be as follows:
    - Once you create a cart this will be created with a default status value of `in_progress` and default `checkout` value of `False`, unless `checkout` is set to `True`. This is not a boolean field.
    - Once the cart `checkout` value is set as `True`, then cart, inventory, sales and receipts will be updated and the status will be updated as well as the inventory information.
    - Once you update the `checkout` value as needed, all of the files in cart, inventory, sales and receipts will be updated automatically.
    - Based on the current logic, if you delete the cart the sale and receipt will be automacally deleted, otherwise if this is deleted individually then it will failled if cart is individually deleted (I am just leaving all endpoints available).
- Endpoints are using https.
- All certs are automatically created for this first advance progress.
- Roles for administrator are already created to properly manage this app initially.
- Alek is aware of the current logic that I have used for this e-commerce app, that it is being coded in different layer to simulate a DB.
- I am completely aware of that I need some of the layer will be gone once a DB is used.


## Features

- User registration and login (with JWT authentication)
- Role-based access control (administrator and client)
- Product registration and inventory management
- Cart and sales management
- Receipt generation and lookup
- Caching for improved performance
- All data stored in JSON files

## Requirements

- Python 3.8+
- Flask
- Flask-JWT-Extended
- Flask-Caching
- Marshmallow
- Werkzeug

Install dependencies:

```sh
pip install flask flask-jwt-extended flask-caching marshmallow werkzeug
```

## Running the Application

1. **Navigate to the project directory:**

    ```sh
    cd lyfter_program/module2/avance_proyectos/e_commerse_mascotas
    ```

2. **Run the application:**

    ```sh
    python main.py
    ```

    The API will start on `https://localhost:5001` with SSL enabled.

3. **API Endpoints:**

    All endpoints are prefixed with `/pet_shop/`. Example endpoints:

    - `/pet_shop/login`
    - `/pet_shop/user_registration`
    - `/pet_shop/products`
    - `/pet_shop/inventory`
    - `/pet_shop/carts`
    - `/pet_shop/sales`
    - `/pet_shop/receipts`
    - `/pet_shop/users`

    Use the appropriate HTTP methods (`GET`, `POST`, `PUT`, `DELETE`) as per the endpoint.

4. **Authentication:**

    - Obtain a JWT token via the `/pet_shop/login` endpoint.
    - Include the token in the `Authorization` header as `Bearer <token>` for protected endpoints.

5. **Admin User:**

    - The default admin user is created automatically:
        - Email: `administrator@example.com`
        - Password: `administrator#administrator.2025`

## Notes

- All data is stored in the `db/` directory as JSON files.
- Only administrators can perform CRUD operations; clients have read-only access.
- Caching is enabled for performance; cache TTL is set in the configuration.
