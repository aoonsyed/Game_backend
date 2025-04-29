from django.urls import path
from .views import GetScoreboard


urlpatterns = [
    path('scores/', GetScoreboard.as_view(), name="get_scoreboard"),
]