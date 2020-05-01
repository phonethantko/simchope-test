from flask import Flask, request, make_response, jsonify

from models import db, Student, ScoreUpdate, StudyArea
from repositories import StudentRepository

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://simchope:simchope@localhost:5432/simchope"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
db.app = app


@app.route('/')
def api_base():
    return 'API Base Reached!'


# @app.route('/student', methods=['GET'])
# def get_current_user(simconnect_id):
#     student = StudentRepository.get_student(simconnect_id)
#     return jsonify({
#         "simconnectId": student.simconnect_id,
#         "ranking": student.ranking
#     })


@app.route('/student', methods=['GET'])
def show_users():
    data = Student.query.order_by(Student.simconnect_id).all()
    result = \
        [
            {
                "id": student.simconnect_id,
                "ranking": student.ranking
            } for student in data
        ]
    return jsonify(result)


@app.route('/student', methods=['POST'])
def create_user():
    simconnect_id = request.args.get('simconnectId')
    email = str(simconnect_id) + '@mymail.sim.edu.sg'
    password = simconnect_id
    existing = Student.query.filter(Student.simconnect_id == simconnect_id).first()
    if existing:
        return make_response(f'{simconnect_id} already created!')
    new_student = Student(
        simconnect_id=simconnect_id,
        email=email,
        password=password
    )
    db.session.add(new_student)
    db.session.commit()
    return make_response(f"{new_student} successfully created")


@app.route('/study-area', methods=['GET', 'POST'])
def handle_locations():
    if request.method == "GET":
        locations = StudyArea.query.all()
        result = \
            [
                {
                    "area_name": location.area_name,
                    "score": location.score
                } for location in locations
            ]
        return jsonify(result)

    if request.method == 'POST':
        data = request.json
        existing = StudyArea.query.filter(StudyArea.area_name == data['area_name']).first()
        if existing:
            return make_response(f'{data.area_name} already created!')
        new_study_area = StudyArea(
            area_name=data['area_name'],
            block=data['block'],
            level=data['level'],
            score=data['score'],
            table_count=data['table_count'],
            capacity=data['capacity']
        )
        db.session.add(new_study_area)
        db.session.commit()
        return make_response(f"{new_study_area} successfully created")


# end point to get a score point for a given area
@app.route('/score', methods=['GET'])
def get_scores():
    area = request.args.get('study_area')
    result = ScoreUpdate.query.filter_by(study_area=area).first()
    if result is not None:
        return jsonify({
            "area_name": result.study_area,
            "score": result.score
        })
    return make_response(f"{area} not found")


# end-point to create score updates, to be polled by scheduler later
@app.route('/score/update', methods=['POST'])
def create_score():
    data = request.json
    new_score = ScoreUpdate(
        student=data['student'],
        study_area=data['study_area'],
        score=data['score']
    )
    db.session.add(new_score)
    db.session.commit()
    return make_response("Update Created")


if __name__ == '__main__':
    app.run()
