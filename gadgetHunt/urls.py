"""
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from gadgetHunt.gadgetHuntApp import views

router = DefaultRouter()
# router.register(r"company", views.CompanyViewSet)
router.register(r'employees', views.EmployeeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/signup', views.signupView, name = 'signup'),
    path('api/login', views.loginView, name= 'login'),
    path('api/logout', views.logoutView, name= 'logout')
]
