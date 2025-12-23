INSERT INTO customers (name, phone_number)
	VALUES ('Alice', '123-456-7890'),
              ('Bob', '987-654-3210'),
              ('Claire', '555-123-4567');

INSERT INTO customer_addresses (customer_id, address)
	VALUES (1, '123 Main St'),
              (2, '456 Elm St'),
              (3, '789 Oak St'),
              (3, '464 Georgia St');

INSERT INTO products (name, price)
	VALUES ('Cheeseburger', 8),
              ('Fries', 3),
              ('Pizza', 12),
              ('Salad', 6),
              ('Water', 1);

INSERT INTO orders (customer_id, customer_address_id, special_request,
                    delivery_time)
	VALUES (1, 1, 'No onions', '6:00 PM'),
              (1, 1, 'Extra ketchup', '6:00 PM'),
              (2, 2, 'Extra cheese', '7:30 PM'),
              (2, 2, 'None', '7:30 PM'),
              (3, 3, 'No croutons', '12:00 PM'),
              (3, 4, 'None', '5:00 PM');

INSERT INTO order_products (order_id, product_id, quantity)
	VALUES (1, 1, 2),
	       (2, 2, 1),
              (3, 3, 1),
              (4, 2, 2),
              (5, 4, 1),
              (6, 5, 1);