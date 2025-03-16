from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    WordViewSet, DefinitionViewSet, CommentViewSet, HistoryViewSet,
    NotificationViewSet, BadgeViewSet, DocumentImportViewSet, UtilisateurViewSet,
<<<<<<< HEAD
    EnrichissementDictionnaireViewSet, RegisterView
=======
    EnrichissementDictionnaireViewSet, RegisterView, generate_word_variants
>>>>>>> model_AI
)

router = DefaultRouter()
router.register(r'words', WordViewSet, basename='word')
router.register(r'definitions', DefinitionViewSet, basename='definition')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'history', HistoryViewSet, basename='history')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'badges', BadgeViewSet, basename='badge')
router.register(r'users', UtilisateurViewSet, basename='user')
router.register(r'register', RegisterView, basename='register')

document_import_urls = [
    path('import-document/', DocumentImportViewSet.as_view({'post': 'importer_document'}), name='import-document'),
    path('enrichissement/', EnrichissementDictionnaireViewSet.as_view({'post': 'importer_document'}), name='enrichissement-dictionnaire'),
]

auth_urls = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = [
    path('', include(router.urls)),
    path('', include(document_import_urls)),
    path('', include(auth_urls)),
<<<<<<< HEAD
=======
    path('generate-word-variants/<str:word>/', generate_word_variants, name='generate-word-variants'),
>>>>>>> model_AI
]
