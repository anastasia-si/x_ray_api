from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path
from X_Ray_App import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/v1/xrays/', views.XRayListCreateAPIView.as_view()),
    # path('api/v1/xrays/new', views.XRayCreateAPIView.as_view()),
    # path('api/v1/xrays/<int:id>/', views.XRayDetailsAPIView.as_view()),
    # path('api/v1/classify', views.NetworkModelView.as_view())

    url(r'api/', include('X_Ray_App.urls', namespace='xray')),


]

