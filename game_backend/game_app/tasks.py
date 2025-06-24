from celery import shared_task
from .models import User, LeaderboardHistory


@shared_task
def reset_leaderboard():
    users = User.objects.all()

    # Backup current scores
    history_records = []
    for user in users:
        history_records.append(LeaderboardHistory(
            user_id=user.user_id,
            username=user.username,
            high_score=user.high_score,
            last_game_score=user.last_game_score
        ))

    LeaderboardHistory.objects.bulk_create(history_records)

    # Reset leaderboard scores
    users.update(high_score=0, last_game_score=0)

    return "Leaderboard scores backed up and reset completed"
