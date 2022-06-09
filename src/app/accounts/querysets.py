from django.db.models import QuerySet
from app.accounts.enums import UserRole


class UserQuerySet(QuerySet):

    def is_teacher(self):
        return self.filter(role=UserRole.TEACHER)

    def active(self):
        return self.filter(is_active=True)

    def order_by_name(self):
        return self.order_by('last_name', 'first_name', 'father_name')

    def only_ids(self):
        return self.values_list('id', flat=True)
