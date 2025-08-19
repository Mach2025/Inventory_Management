from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # obj is InventoryItem or InventoryChange via item relation
        owner = getattr(obj, "owner", None)
        if owner is None and hasattr(obj, "item"):
            owner = getattr(obj.item, "owner", None)
        return owner == request.user
