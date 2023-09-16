from rest_framework import filters



class IsUserOrAdminFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return queryset
            else:
                return queryset.filter(borrower=request.user)
        return queryset.none()
