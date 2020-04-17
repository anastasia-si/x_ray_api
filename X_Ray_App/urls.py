from django.urls import path
from . import views
app_name = 'X_Ray_App'

urlpatterns = [
    path('v1/xrays/', views.XRayListCreateAPIView.as_view(), name='list-xray'),
    path('v1/xrays/new', views.XRayCreateAPIView.as_view(), name='create-xray'),
    path('v1/xrays/<int:id>/', views.XRayDetailsAPIView.as_view(), name='detail-xray'),
    path('v1/classify', views.NetworkModelView.as_view(), name='classify-xray'),
]