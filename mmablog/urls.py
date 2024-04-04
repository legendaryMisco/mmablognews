from django.urls import path
from .views import HomeView,ArticleView,ContactUsView,BlogView

app_name = 'mmablog'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('news/<slug:slug>/', ArticleView.as_view(), name='article'),
    path('category/<str:category>/', BlogView.as_view(), name='categoryNews'),
    path('contact/', ContactUsView.as_view(), name='contact'),
    
]
