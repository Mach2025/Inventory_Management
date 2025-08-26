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

       

