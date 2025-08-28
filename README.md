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

8. Inventory Levels : 
  - View current stock levels
  - Filter by category, price range, or low stock threshold
  - Inventory Change Tracking : Logs when product stock changes, who changed it, and new quantity


                             API Endpoints
Inventory
Endpoint	                          Method	                Description
/api/inventory/products/    	      GET	                  List products
/api/inventory/products/	          POST	                Create product
/api/inventory/products/{id}/	      PUT	                  Update product
/api/inventory/products/{id}/	      DELETE	             Delete product
/api/inventory/level/	              GET	                  Check inventory levels (with filters)
/api/inventory/inventory-changes/	  GET	                  View stock change history.



"products": "http://127.0.0.1:8000/api/inventory/products/",
    "suppliers": "http://127.0.0.1:8000/api/inventory/suppliers/",
    "customers": "http://127.0.0.1:8000/api/inventory/customers/",
    "orders": "http://127.0.0.1:8000/api/inventory/orders/",
    "order-items": "http://127.0.0.1:8000/api/inventory/order-items/",
    "sales": "http://127.0.0.1:8000/api/inventory/sales/",
    "sale-items": "http://127.0.0.1:8000/api/inventory/sale-items/",
    "inventory-changes": "http://127.0.0.1:8000/api/inventory/inventory-changes/"

User Management
-User registation ( Id, UserName, email Password).
-CRUD operations on user via (/api/accounts/users/).
-JWT authentication(login to get token).
-Authenticated users can manage inventory.


Security
-JWT Authentication ('djangorestframework_simplejwt')
    -Permission checks include:
       -Only authenicated users can Create, Update or Delete Inventory.
       -Read-Only access from unauthenicated users.



Users
Endpoint 	                 Method	                Description
/api/accounts/users/	     POST	                    Register new user
/api/accounts/users/	     GET	                         List users
/api/accounts/users/{id}/ 	PUT	                      Update user
/api/accounts/users/{id}/	  DELETE	                 Delete user


Authentication
Endpoint	                   Method	         Description
/api/token/	POST	Login and   GET            JWT tokens
/api/token/refresh/	          POST	           Refresh JWT access token       

User login:{
  "username": "ajiam",
  "password": "test12345"
}


. Create a Product

POST /api/inventory/products/

{
  "name": "Tote Bag",
  "description": "Black Tote bag",
  "price": 1200.50,
  "quantity": 15,
  "category": "Bags"
}

2. Update a Product

PUT /api/inventory/products/1/

{
  "name": "Tote Bag - Updated",
  "description": "Black tote bag",
  "price": 1500.00,
  "quantity": 20,
  "category": "Bags"
}

3. Create a Customer

POST /api/inventory/customers/

{
  "name": "John Doe",
  "email": "johndoe@example.com",
  "phone": "+254700123456",
  "address": "Nairobi, Kenya"
}

4. Create a Supplier

POST /api/inventory/suppliers/

{
  "name": "Nairobi Textile Supplies",
  "email": "contact@nairobitextilesupplies.com",
  "phone": "+254711223344",
  "address": "Westlands, Nairobi"
}

5. Create a Sale (Invoice)

POST /api/inventory/sales/

{
  "customer": 1,
  "products": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ],
  "total_amount": 3000.00,
  "status": "completed"
}

6. Create a Purchase (Stock In)

POST /api/inventory/purchases/

{
  "supplier": 1,
  "products": [
    {
      "product_id": 1,
      "quantity": 50
    }
  ],
  "total_cost": 60000.00,
  "status": "received"
}
            PROJECT STRUCTURE
  django_inventory/
│── django_inventory/
│ └── settings.py
│ └── urls.py
│
│── inventory/
│ |── models.py - Product, Supplier, Customer, Orders, Sales, InventoryChange
│ ├── serializers.py # Serializers for all models
│ ├── views.py - ViewSets with CRUD + custom actions
│ ├── urls.py - API endpoints for inventory
│
│── users/
│ ├── models.py - Using Django’s default User model
│ ├── serializers.py - UserSerializer for registration/login
│ ├── views.py - UserViewSet (CRUD)
│ ├── urls.py - Routes for user management
│
│── manage.py


Prepared By : Rebecca Machio.

       

