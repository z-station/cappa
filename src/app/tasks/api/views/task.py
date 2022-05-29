from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from app.tasks.models import (
    Draft,
    Task
)
from app.tasks.api.serializers.draft import (
    DraftSerializer
)


class TaskViewSet(GenericViewSet):

    queryset = Task.objects.all()
    serializer_class = None
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'draft':
            return DraftSerializer

    @action(methods=('POST',), detail=True)
    def draft(self, request, pk):
        slz = self.get_serializer(data=request.data)
        slz.is_valid(raise_exception=True)
        content = slz.validated_data['content']
        translator = slz.validated_data['translator']
        draft, created = Draft.objects.get_or_create(
            translator=translator,
            user=request.user,
            task_id=pk,
            defaults={"content": content}
        )
        if not created:
            draft.content = slz.validated_data['content']
            draft.save(update_fields=('content',))
        return Response()
