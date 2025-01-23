from django.urls import path
from . import views
from .views import IncomeListCreateView, IncomeDetailView


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('income/', IncomeListCreateView.as_view(), name='income-list-create'),
    path('income/<int:pk>/', IncomeDetailView.as_view(), name='income-detail'),
]