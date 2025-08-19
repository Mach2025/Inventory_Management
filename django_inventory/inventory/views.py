from rest_framework import viewsets, permissions
from .models import Product, Supplier, Customer, Order, OrderItem, Sale, SaleItem
from .serializers import (
    ProductSerializer,
    SupplierSerializer,
    CustomerSerializer,
    OrderSerializer,
    OrderItemSerializer,
    SaleSerializer,
    SaleItemSerializer,
)

# ----- Supplier -----
class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ----- Customer -----
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ----- Product -----
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("-date_added")
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()  # If you want ownership, add: owner=self.request.user


# ----- Order -----
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("-order_date")
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ----- Order Item -----
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ----- Sale -----
class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all().order_by("-sale_date")
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ----- Sale Item -----
class SaleItemViewSet(viewsets.ModelViewSet):
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



