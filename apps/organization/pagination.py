from rest_framework.pagination import CursorPagination

class OrganizationCursorPagination(CursorPagination):
    page_size = 10
    ordering ='-created_at'
    cursor_query_param = 'cursor'


class OrganizationMemebersPagination(CursorPagination):
    page_size = 10
    ordering = '-joined_at'
    cursor_query_param = 'cursor'