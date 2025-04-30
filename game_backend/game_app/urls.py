from django.urls import path
from .views import GetScoreboard,GetUser


urlpatterns = [
    path('scores/', GetScoreboard.as_view(), name="get_scoreboard"),
    path('user/<str:user_id>', GetUser.as_view(), name="get_user"),
]