from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WordViewSet, DefinitionViewSet, CommentViewSet, HistoryViewSet,
    NotificationViewSet, BadgeViewSet, DocumentImportViewSet, UtilisateurViewSet,
    EnrichissementDictionnaireViewSet
)

router = DefaultRouter()
router.register(r'words', WordViewSet, basename='word')
router.register(r'definitions', DefinitionViewSet, basename='definition')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'history', HistoryViewSet, basename='history')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'badges', BadgeViewSet, basename='badge')
router.register(r'users', UtilisateurViewSet, basename='user')

document_import_urls = [
    path('import-document/', DocumentImportViewSet.as_view({'post': 'importer_document'}), name='import-document'),
    path('enrichissement/', EnrichissementDictionnaireViewSet.as_view({'post': 'importer_document'}), name='enrichissement-dictionnaire'),
]

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(document_import_urls)),
]
