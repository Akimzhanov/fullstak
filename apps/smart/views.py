from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import action
from rest_framework import filters, status, mixins

from django_filters import rest_framework as rest_filter

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from.serializers import (
    SmartCreateSerilizer,
    SmartListSerializers,
    SmartSerializer,
    CategorySerializer,
    RatingSerializer,
    LikeSerializer,
    CommentSerializer
)
from .models import Smart, Category, Rating, Like, Comment


class SmartViewSet(ModelViewSet):

    queryset = Smart.objects.all()
    serializer_class = SmartSerializer
    filter_backends = [filters.SearchFilter,
    rest_filter.DjangoFilterBackend,
    filters.OrderingFilter]
    search_fields = ['title', 'price', 'user__username']

    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'list':
            return SmartListSerializers
        elif self.action == 'create':
            return SmartCreateSerilizer
        return super().get_serializer_class()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_permissions(self):
        if self.action in ['create', 'destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAdminUser]
        if self.action in ['list', 'retrive']:
            self.permission_classes = [AllowAny]
        if self.action in ['set_rating', 'like', 'comment']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save()
        return super().retrieve(request, *args, **kwargs)

    @action(detail=True, methods=['POST', 'DELETE'])
    def comment(self, request, pk=None):
        smart = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, smart=smart)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
                )

    @action(methods=['POST', 'PATCH'], detail=True, url_path='set_rating')
    def set_rating(self, request, pk=None):
        data = request.data.copy()
        data['smart'] = pk
        serializer = RatingSerializer(data=data, context={'request': request})
        rate = Rating.objects.filter(
            user=request.user,
            smart=pk
        ).first()
        if serializer.is_valid(raise_exception=True):
            if rate and request.method == 'POST':
                return Response(
                    {'detail': 'Rating object exists. Use PATCH method'}
                )
            elif rate and request.method == 'PATCH':
                serializer.update(rate, serializer.validated_data)
                return Response('Updated')
            elif request.method == 'POST':
                serializer.create(serializer.validated_data)
                return Response(serializer.data)
            else:
                return Response({'detail': 'Rating object does not exist. Use POST method'})

    @action(detail=True, methods=['POST', 'DELETE'])
    def like(self, request, pk=None):
        smart = self.get_object()
        serializer = LikeSerializer(data=request.data, context={
            'request': request,
            'smart': smart
        })
        if serializer.is_valid(raise_exception=True):
            if request.method == 'POST':
                serializer.save(user=request.user)
                return Response('Liked!')
            if request.method == 'DELETE':
                serializer.unlike()
                return Response('Unliked!')


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CommentCreateDeleteView(
    mixins.DestroyModelMixin,
    GenericViewSet
    ):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
