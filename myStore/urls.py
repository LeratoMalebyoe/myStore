from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from store import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(views.home), name='home'),
    path('store/', include('store.urls', namespace='store')),
    path('products/', views.product_list, name='products'),
    path('cart/', views.cart_view, name='cart'),
    path('user_auth/', include('user_auth.urls', namespace='user_auth')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
