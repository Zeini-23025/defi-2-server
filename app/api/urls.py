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