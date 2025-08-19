from rest_framework import serializers
from .models import InventoryItem, InventoryChange, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]


class InventoryChangeSerializer(serializers.ModelSerializer):
    item = serializers.StringRelatedField(read_only=True)
    changed_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = InventoryChange
        fields = ["id", "item", "changed_by", "delta", "note", "created_at", "quantity_after"]


class InventoryItemSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    category_detail = CategorySerializer(source="category", read_only=True)
    changes = InventoryChangeSerializer(many=True, read_only=True)

    class Meta:
        model = InventoryItem
        fields = [
            "id", "owner", "name", "description", "quantity", "price",
            "category", "category_detail", "date_added", "last_updated", "changes",
        ]
        read_only_fields = ["owner", "date_added", "last_updated"]

    def validate(self, attrs):
        # basic required checks (Name, Quantity, Price)
        name = attrs.get("name", getattr(self.instance, "name", None))
        price = attrs.get("price", getattr(self.instance, "price", None))
        quantity = attrs.get("quantity", getattr(self.instance, "quantity", None))

        if not name:
            raise serializers.ValidationError({"name": "Name is required."})
        if price is None or price < 0:
            raise serializers.ValidationError({"price": "Price must be ≥ 0."})
        if quantity is None or quantity < 0:
            raise serializers.ValidationError({"quantity": "Quantity must be ≥ 0."})
        return attrs
