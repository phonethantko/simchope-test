import schedule

from .score_engine import ScoreEngine


class ScoreUpdateCoordinator:
    blocks = ['A', 'B', 'C']

    def run(self):
        print("Scheduler started")
        with ScoreEngine() as score_engine:
            for block in self.blocks:
                score_engine.execute(block)
        print("Score Update Completed")


def start_scheduler():
    schedule.every().hour.do(ScoreUpdateCoordinator.run)