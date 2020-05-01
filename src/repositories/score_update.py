from models import ScoreUpdate


class ScoreUpdateRepository:

    @staticmethod
    def get_scores():
        return ScoreUpdate.query().all()

    @staticmethod
    def get_last_fifty_scores():
        return ScoreUpdate.query().order_by(ScoreUpdate.id.desc()).limit(50).all()
