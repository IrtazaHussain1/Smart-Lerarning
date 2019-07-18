from django.urls import path
from Login_app import views
from django.conf.urls.static import static
from SEPPS import settings

app_name='login_app'

urlpatterns = [
    path('', views.Login_View, name='main_login_page'),
    path('registeration/',views.Reg_View, name='registeration_page'),
    path('logout/',views.Logout_views, name='logout_page')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

