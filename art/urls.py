
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    re_path(r'',include('Artisanmarket.urls'))
]
