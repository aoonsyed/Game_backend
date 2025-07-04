from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Penguin Backend",
      default_version='v1',
      description="API documentation with Swagger UI",
      contact=openapi.Contact(email="your@email.com"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
   url="https://dashypenguin.io",
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/', include('game_app.urls'))

]
