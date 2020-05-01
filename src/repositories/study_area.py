from models import StudyArea


class StudyAreaRepository:

    @staticmethod
    def get_all():
        study_areas = StudyArea.query().all()
        return study_areas

    @staticmethod
    def get_by_block(block):
        study_areas = StudyArea.query().filter(block=block).all()
        return study_areas
