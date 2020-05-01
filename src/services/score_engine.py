from repositories import StudyAreaRepository, ScoreUpdateRepository


class ScoreEngine:
    scores = []

    def __init__(self):
        self.scores = ScoreUpdateRepository.get_last_fifty_scores()

    def execute(self, block):
        print(f"Job Running for block {block}")
        score_updates = self.get_scores(block)
        # new_scores = self.calculate_score(score_updates)
        #         # self.update_score(new_scores)
        self.calculate_and_update_scores(score_updates)
        print(f"Score update for block {block}")

    def get_scores(self, block):
        study_area_ids = self.derive_study_area_ids(block)
        scores = list(filter(lambda x: (x.study_area, x.score) in study_area_ids, self.scores))
        return scores

    @staticmethod
    def derive_study_area_ids(self, block):
        study_areas = set(map(lambda x: x.id, StudyAreaRepository.get_by_block(block)))
        return study_areas

    @staticmethod
    def calculate_and_update_scores(self, score_updates):
        scores = dict(score_updates)

        return 1, 2, 3
