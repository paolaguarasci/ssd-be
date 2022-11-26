from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    if request.method in permissions.SAFE_METHODS:
      return True
    if request.user.is_superuser:
      return True
    return obj.insertBy == request.user