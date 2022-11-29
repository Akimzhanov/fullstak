from rest_framework.routers import DefaultRouter
from .views import SmartViewSet, CategoryViewSet, CommentCreateDeleteView


router = DefaultRouter()
router.register('smarts', SmartViewSet, 'smarts')
router.register('comment', CommentCreateDeleteView, 'comment')
router.register('categories', CategoryViewSet, 'category')


urlpatterns = []

urlpatterns += router.urls