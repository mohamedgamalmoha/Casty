from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import (CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin,
                                   DestroyModelMixin)

from drf_spectacular.utils import extend_schema

from accounts.utils import is_model_user, is_director_user
from accounts.api.permissions import IsModelUser, IsDirectorUser
from accounts.api.mixins import AllowAnyInSafeMethodOrCustomPermissionMixin
from contracts.models import Contract, ContractRequest, SoloContract
from .filters import ContractFilter, ContractRequestFilter, SoloContractFilter
from .serializers import (ContractSerializer, ContractRequestSerializer, ProfileContractRequestSerializer,
                          AgencyContractRequestSerializer, ProfileSoloContractSerializer, AgencySoloContractSerializer)


class ContractViewSet(AllowAnyInSafeMethodOrCustomPermissionMixin, CreateModelMixin, RetrieveModelMixin,
                      UpdateModelMixin, ListModelMixin, GenericViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    filterset_class = ContractFilter
    permission_classes = [IsDirectorUser]
    contract_request_permission_classes = [IsModelUser]
    save_method_permission_classes = [IsAuthenticated]

    def get_requests_queryset(self):
        return self.get_object().requests.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if self.action == 'me' and is_director_user(user):
            queryset = queryset.filter(agency=user.agency)
        return queryset

    def get_permission_classes(self, request):
        if self.action == 'contract_request':
            return self.contract_request_permission_classes
        return super().get_permission_classes(request)

    def get_serializer_class(self):
        if self.action == 'requests':
            return ContractRequestSerializer
        if self.action == 'contract_request':
            return ProfileSoloContractSerializer
        return super(ContractViewSet, self).get_serializer_class()

    def perform_create(self, serializer):
        if self.action == 'contract_request':
            serializer.save(contract=self.get_object(), profile=self.request.user.profile)
        else:
            serializer.save(agency=self.request.user.agency)

    @extend_schema(responses={200: ContractSerializer(many=True)})
    @action(detail=False, methods=["GET"], name='Get My Contracts')
    def me(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(responses={200: ContractRequestSerializer(many=True)})
    @action(detail=True, methods=["GET"], name='Get Contract Requests')
    def requests(self, request, *args, **kwargs):
        self.get_queryset = self.get_requests_queryset
        return self.list(request, *args, **kwargs)

    @extend_schema(responses={200: ProfileSoloContractSerializer})
    @action(detail=True, methods=["POST"], name='Request Contract', url_path='request')
    def contract_request(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ContractRequestViewSet(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet):
    queryset = ContractRequest.objects.all()
    serializer_class = ProfileContractRequestSerializer
    filterset_class = ContractRequestFilter
    permission_classes = [IsModelUser | IsDirectorUser]
    post_permission_classes = [IsModelUser]

    def get_permission_classes(self, request):
        if request.method == 'POST':
            return self.post_permission_classes
        return super().get_permission_classes(request)

    def get_serializer_class(self):
        if is_director_user(self.request.user):
            return AgencyContractRequestSerializer
        return self.serializer_class

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if self.action == 'me' and is_model_user(user):
            queryset = queryset.filter(profile=user.profile)
        return queryset

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class SoloContractViewSet(ModelViewSet):
    queryset = SoloContract.objects.all()
    serializer_class = ProfileSoloContractSerializer
    filterset_class = SoloContractFilter
    permission_classes = [IsModelUser | IsDirectorUser]
    post_permission_classes = [IsDirectorUser]

    def get_permission_classes(self, request):
        if request.method == 'POST':
            return self.post_permission_classes
        return super().get_permission_classes(request)

    def get_serializer_class(self):
        if is_director_user(self.request.user):
            return AgencySoloContractSerializer
        return self.serializer_class

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if self.action == 'me' and is_model_user(user):
            queryset = queryset.filter(profile=user.profile)
        return queryset

    def perform_create(self, serializer):
        serializer.save(agency=self.request.user.agency)
