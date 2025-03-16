<<<<<<< HEAD
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
=======
from django.urls import path
from .views import (
    WordCreateView, WordUpdateView, WordListView,
    DefinitionCreateView, DefinitionUpdateView
)

urlpatterns = [
    path('words/', WordListView.as_view(), name='word-list'),
    path('words/create/', WordCreateView.as_view(), name='word-create'),
    path('words/<int:pk>/update/', WordUpdateView.as_view(), name='word-update'),
    path('definitions/create/', DefinitionCreateView.as_view(), name='definition-create'),
    path('definitions/<int:pk>/update/', DefinitionUpdateView.as_view(), name='definition-update'),
]
>>>>>>> models
