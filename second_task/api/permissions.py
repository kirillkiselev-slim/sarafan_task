from rest_framework.permissions import IsAuthenticated, SAFE_METHODS, AllowAny


class ReadOrAdminOnly(AllowAny):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_staff


class AuthorOnly(IsAuthenticated):

    def has_object_permission(self, request, view, user_data):
        return user_data.user == request.user


