from celery import shared_task
from .models import User, LeaderboardHistory
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task
def reset_leaderboard():
    try:
        users = User.objects.all().iterator()

        history_records = []
        for user in users:
            history_records.append(LeaderboardHistory(
                user_id=user.user_id,
                username=user.username,
                high_score=user.high_score or 0,
                last_game_score=user.last_game_score or 0,
            ))

        LeaderboardHistory.objects.bulk_create(history_records)
        User.objects.update(high_score=0, last_game_score=0)

        logger.info("✅ Leaderboard reset completed and history backed up.")
        return "Leaderboard scores backed up and reset successfully"

    except Exception as e:
        logger.error(f"❌ Leaderboard reset failed: {e}")
        raise
