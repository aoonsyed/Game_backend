from django.urls import path
from .views import GetScoreboard,GetUser, GetLives, GetReward


urlpatterns = [
    path('scores/', GetScoreboard.as_view(), name="get_scoreboard"),
    path('user/<str:user_id>', GetUser.as_view(), name="get_user"),
    path('lives/', GetLives.as_view(), name="get_lives"),
    path('rewards/', GetReward.as_view(), name="get_rewards"),
]