Models Implemented
1. Product
Represents items in stock.

Fields: name, description, price, quantity_in_stock, supplier

Relationships: Linked to Supplier (a supplier can have many products)

2. Supplier
Stores supplier details.

Fields: name, contact_person, email, phone, address

Relationships: Can supply multiple Products

3. Customer
Represents customers who purchase products.

Fields: first_name, last_name, email, phone, address

Relationships: Linked to Sale transactions

4. Order
Represents purchase orders from suppliers.

Fields: order_date, supplier

Relationships: Connected to Supplier and OrderItem

5. OrderItem
Intermediate table for products in an order.

Fields: order, product, quantity, price

6. Sale
Represents a sales transaction.

Fields: sale_date, customer

Relationships: Linked to SaleItem

7. SaleItem
Intermediate table for products in a sale.

Fields: sale, product, quantity, price
