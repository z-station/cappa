from typing import Optional
from django.db.models import (
    QuerySet,
    Sum,
    Q,
    Case,
    When,
    IntegerField,
    BooleanField,
    Value
)
from app.groups.enums import GroupMemberRole
from app.accounts.enums import UserRole


class GroupQuerySet(QuerySet):

    def active(self):
        return self.filter(is_active=True)

    def by_id(self, pk: int):
        return self.filter(id=pk)

    def with_learners_count(self):

        """ Возвращает число участников группы в отдельном поле learners_count

            * После обновления Django до версии 2.0
            нужно обновить код фильтрации на следующий:
            learners_count=Count(members, filter=Q(members__is_active=True)) """

        return self.annotate(
            learners_count=Sum(
                Case(
                    When(
                        Q(
                            group_members__user__is_active=True,
                            group_members__role=GroupMemberRole.LEARNER
                        ),
                        then=1
                    ),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )

    def with_user_is_learner(self, user_id: Optional[int] = None):

        """ Если пользователь в роли ученика группы
            возвращает значение True в поле user_is_learner """

        if user_id:
            return self.annotate(
                user_is_learner=Sum(
                    Case(
                        When(
                            Q(
                                group_members__user_id=user_id,
                                group_members__role=GroupMemberRole.LEARNER
                            ),
                            then=1
                        ),
                        default=0,
                        output_field=BooleanField()
                    )
                )
            )
        else:
            return self.annotate(
                user_is_learner=Value(False, output_field=BooleanField())
            )

    def with_user_is_teacher(self, user_id: Optional[int] = None):

        """ Если пользователь в роли преподавателя группы
            возвращает значение True в поле user_is_teacher """

        if user_id:
            return self.annotate(
                user_is_teacher=Sum(
                    Case(
                        When(
                            Q(
                                group_members__user_id=user_id,
                                group_members__user__role=UserRole.TEACHER,
                                group_members__role=GroupMemberRole.TEACHER
                            ),
                            then=1
                        ),
                        default=0,
                        output_field=BooleanField()
                    )
                )
            )
        else:
            return self.annotate(
                user_is_teacher=Value(False, output_field=BooleanField())
            )
