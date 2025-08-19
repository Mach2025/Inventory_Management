from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction

from .models import InventoryItem, InventoryChange, Category
from .serializers import (
    InventoryItemSerializer,
    InventoryChangeSerializer,
    CategorySerializer,
)
from .permissions import IsOwnerOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]  # let users manage categories
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["name"]


class InventoryItemViewSet(viewsets.ModelViewSet):
    """
    CRUD for inventory items. Only authenticated users can create/update/delete.
    Users can only modify their own items. Includes:
    - filtering (category, low_stock, price_min/max)
    - search (name, description)
    - ordering (name, quantity, price, date_added)
    - custom actions: restock, sell, history
    """
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "quantity", "price", "date_added"]
    filterset_fields = ["category"]  # basic exact filters

    def get_queryset(self):
        qs = InventoryItem.objects.all()
        # Optional filters: low_stock, price range
        low_stock = self.request.query_params.get("low_stock")
        price_min = self.request.query_params.get("price_min")
        price_max = self.request.query_params.get("price_max")

        if low_stock is not None:
            try:
                threshold = int(low_stock)
            except ValueError:
                threshold = 5
            qs = qs.filter(quantity__lt=threshold)

        if price_min is not None:
            qs = qs.filter(price__gte=price_min)
        if price_max is not None:
            qs = qs.filter(price__lte=price_max)

        return qs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @transaction.atomic
    def _apply_delta_and_log(self, item: InventoryItem, delta: int, user, note: str = ""):
        new_qty = item.quantity + delta
        if new_qty < 0:
            raise ValueError("Resulting quantity cannot be negative.")
        item.quantity = new_qty
        item.save(update_fields=["quantity", "last_updated"])
        InventoryChange.objects.create(
            item=item, changed_by=user, delta=delta, note=note, quantity_after=new_qty
        )

    # POST /inventory/items/{id}/restock/
    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated, IsOwnerOrReadOnly])
    def restock(self, request, pk=None):
        item = self.get_object()
        amount = int(request.data.get("amount", 0))
        if amount <= 0:
            return Response({"detail": "Amount must be > 0"}, status=400)
        try:
            self._apply_delta_and_log(item, amount, request.user, note="restock")
        except ValueError as e:
            return Response({"detail": str(e)}, status=400)
        return Response(self.get_serializer(item).data, status=status.HTTP_200_OK)

    # POST /inventory/items/{id}/sell/
    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated, IsOwnerOrReadOnly])
    def sell(self, request, pk=None):
        item = self.get_object()
        amount = int(request.data.get("amount", 0))
        if amount <= 0:
            return Response({"detail": "Amount must be > 0"}, status=400)
        try:
            self._apply_delta_and_log(item, -amount, request.user, note="sell")
        except ValueError as e:
            return Response({"detail": str(e)}, status=400)
        return Response(self.get_serializer(item).data, status=status.HTTP_200_OK)

    # GET /inventory/items/{id}/history/
    @action(detail=True, methods=["get"], permission_classes=[permissions.IsAuthenticated, IsOwnerOrReadOnly])
    def history(self, request, pk=None):
        item = self.get_object()
        qs = item.changes.all()
        page = self.paginate_queryset(qs)
        ser = InventoryChangeSerializer(page or qs, many=True)
        if page is not None:
            return self.get_paginated_response(ser.data)
        return Response(ser.data)


class InventoryChangeViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only access; owners can view change history across their items."""
    serializer_class = InventoryChangeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["created_at", "delta"]

    def get_queryset(self):
        # only show changes for items owned by the user
        return InventoryChange.objects.filter(item__owner=self.request.user)


