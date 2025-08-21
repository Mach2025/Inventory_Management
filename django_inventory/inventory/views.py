from rest_framework import viewsets, permissions
from .models import Product, Supplier, Customer, Order, OrderItem, Sale, SaleItem, InventoryChange
from .serializers import (
    ProductSerializer,
    SupplierSerializer,
    CustomerSerializer,
    OrderSerializer,
    OrderItemSerializer,
    SaleSerializer,
    SaleItemSerializer,
    InventoryChangeSerializer,
)
from rest_framework.decorators import action
from rest_framework.response import Response

#  Supplier 
class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


#  Customer 
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


#  Product 
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("-date_added")
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()  # If you want ownership.

    def perform_update(self, serializer):
        #inventory changes on update
        old_quantity = self.get_object().stock_quantity
        instance = serializer.save()
        if instance.stock_quantity != old_quantity:
            InventoryChange.objects.create(
                product=instance,
                change_amount=instance.stock_quantity - old_quantity,
                new_quantity=instance.stock_quantity,
                changed_by=self.request.user,
            )    

@action(detail=False, methods=['get'], url_path='level')
def inventory_level(self, request):
    queryset = self.queryset
#filter by categoty
    category = request.query_params.get('category')
    if category:
        queryset = queryset.filter(category=category)
#Filter by price range
    price_min = request.query_params.get('price_min')
    price_max = request.query_params.get('price_max')
    if price_min and price_max:
        queryset = queryset.filter(price__gte=price_min, price__lte=price_max)
# filterby low stock
    low_stock = request.query_params.get('low_stock') 
    if low_stock:
        queryset = queryset.filter(stock_quantity__lt=low_stock) 
    data = [{"name": product.name, "stock_quantity": product.stock_quantity} for product in queryset]  
    return Response(data)  #Return name and stock quanity  

   
class InventoryChangeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InventoryChange.objects.all().order_by("-timestamp")
    serializer_class = InventoryChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

# Order 
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("-order_date")
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


#  Order Item 
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# Sale 
class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all().order_by("-sale_date")
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


#  Sale Item 
class SaleItemViewSet(viewsets.ModelViewSet):
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



