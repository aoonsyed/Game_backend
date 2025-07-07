from celery import shared_task
from .models import User, LeaderboardHistory

@shared_task
def reset_leaderboard():
    try:
        print("✅ Celery task 'reset_leaderboard' is running...")

        users = User.objects.all().iterator()
        history_records = []

        for user in users:
            print(f"Backing up scores for user: {user.username}")
            history_records.append(LeaderboardHistory(
                user_id=user.user_id,
                username=user.username,
                high_score=user.high_score or 0,
                last_game_score=user.last_game_score or 0,
            ))

        LeaderboardHistory.objects.bulk_create(history_records)
        print("✅ Leaderboard history backed up.")

        User.objects.update(high_score=0, last_game_score=0)
        print("✅ Leaderboard scores reset to 0.")

        return "Leaderboard scores backed up and reset successfully"

    except Exception as e:
        print(f"❌ Leaderboard reset failed: {e}")
        raise
