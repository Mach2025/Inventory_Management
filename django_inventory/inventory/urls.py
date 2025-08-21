from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, SupplierViewSet, CustomerViewSet,
    OrderViewSet, OrderItemViewSet,
    SaleViewSet, SaleItemViewSet, InventoryChangeViewSet
)

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'sale-items', SaleItemViewSet)
router.register(r'inventory-changes', InventoryChangeViewSet)



urlpatterns = router.urls

