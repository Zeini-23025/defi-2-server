from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MotViewSet, DefinitionViewSet, CommentaireViewSet, HistoriqueViewSet, NotificationViewSet, BadgeViewSet

router = DefaultRouter()
router.register(r'mots', MotViewSet)
router.register(r'definitions', DefinitionViewSet)
router.register(r'commentaires', CommentaireViewSet)
router.register(r'historiques', HistoriqueViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'badges', BadgeViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
