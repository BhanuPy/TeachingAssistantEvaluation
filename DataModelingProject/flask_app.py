from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_sqlalchemy import SQLAlchemy
import joblib

# Initialize the Flask application
app = Flask(__name__)

# Set up the JWT manager
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

# Set up the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tae.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the TA model
class TA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    native_english_speaker = db.Column(db.Boolean, nullable=False)
    course_instructor = db.Column(db.String(50), nullable=False)
    course = db.Column(db.String(50), nullable=False)
    semester = db.Column(db.Boolean, nullable=False)
    class_size = db.Column(db.Integer, nullable=False)
    performance_score = db.Column(db.Integer, nullable=False)

    def __init__(self, native_english_speaker, course_instructor, course, semester, class_size, performance_score):
        self.native_english_speaker = native_english_speaker
        self.course_instructor = course_instructor
        self.course = course
        self.semester = semester
        self.class_size = class_size
        self.performance_score = performance_score

# Create the TA table in the database
# create the application context
with app.app_context():
    db.create_all()

# Define the API routes
@app.route('/login', methods=["POST"])
def login():
    print("request data",request.json)
    username = request.json.get("username")
    password = request.json.get("password")
    if username != 'admin' or password != 'password':
        return jsonify({'error': 'Invalid username or password'}), 401
    access_token = create_access_token(identity=username)
    response = jsonify({'access_token': access_token}), 200
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@jwt_required
@app.route('/ta/create', methods=['POST'])
def add_ta():
    data = request.get_json()
    native_english_speaker = bool(data['native_english_speaker'])
    course_instructor = str(data['course_instructor'])
    course = str(data['course'])
    semester = bool(data['semester'])
    class_size = int(data['class_size'])

    performance_score = int(data['performance_score'])
    # model = joblib.load('logistic_regression_model.joblib')
    
    # Prepare the input data for the model
    # X = [[native_english_speaker, course_instructor, course, semester, class_size]]
    # print(X)
    
    # Make a prediction using the model
    # y_pred = model.predict(X)
    # print(y_pred)

    ta = TA(native_english_speaker=native_english_speaker, course_instructor=course_instructor, course=course,
            semester=semester, class_size=class_size, performance_score= performance_score)
    db.session.add(ta)
    db.session.commit()
    return jsonify({'message': 'TA added successfully'}), 201



@jwt_required
@app.route('/ta/<int:ta_id>', methods=['GET'])
def get_id_ta(ta_id):
    ta = TA.query.get(ta_id)
    if not ta:
        return jsonify({'error': 'TA not found'}), 404
    ta_data = {
        'native_english_speaker': ta.native_english_speaker,
        'course_instructor': ta.course_instructor,
        'course': ta.course,
        'semester': ta.semester,
        'class_size': ta.class_size,
        'performance_score': ta.performance_score
    }
    return jsonify(ta_data), 200




@jwt_required
@app.route('/ta/<int:ta_id>/update', methods=['PUT'])
def update_ta(ta_id):
    # Check if the TA exists in the database
    ta = TA.query.filter_by(id=ta_id).first()
    if not ta:
        return jsonify({'error': 'TA not found'}), 404
    
    # Update the TA attributes
    data = request.get_json()
    if 'native_english_speaker' in data:
        ta.native_english_speaker = bool(data['native_english_speaker'])
    if 'course_instructor' in data:
        ta.course_instructor = str(data['course_instructor'])
    if 'course' in data:
        ta.course = str(data['course'])
    if 'semester' in data:
        ta.semester = bool(data['semester'])
    if 'class_size' in data:
        ta.class_size = int(data['class_size'])
    # if 'performance_score' in data:
    #     ta.performance_score = int(data['performance_score'])

    X = [[ta.native_english_speaker, ta.course_instructor, ta.course, ta.semester, ta.class_size]]
    
   
    # performance_score = int(data['performance_score'])
    model = joblib.load('logistic_regression_model.joblib')
    y_pred = model.predict(X)
    ta.performance_score = int(y_pred[0])
    
    
    # Commit the changes to the database
    db.session.commit()
    
    return jsonify({'message': 'TA updated successfully'}), 200


# @app.route('/performance_scores/<int:id>', methods=['DELETE'])

@jwt_required()
@app.route('/ta/<int:ta_id>/delete', methods=['DELETE'])
def delete_performance_score(id):
    ta = TA.query.filter_by(id=id).first()
    if not ta:
        return jsonify({'error': 'TA not found'}), 404
    ta.performance_score = None
    db.session.commit()
    return {'message': 'Performance score deleted successfully'}, 200


# # define route for retrieving performance score
# @app.route('/performance-score/<int:id>', methods=['GET'])
# @jwt_required
# def get_performance_score(id):
#     # Retrieve the TA from the database by ID
#     ta = TA.query.get(id)
#     if ta is None:
#         return jsonify({'error': 'TA not found'}), 404
    
#     # Load the saved logistic regression model from file
#     model = joblib.load('logistic_regression_model.joblib')
    
#     # Prepare the input data for the model
#     X = [[ta.native_english_speaker, ta.course_instructor, ta.course, ta.semester, ta.class_size]]
    
#     # Make a prediction using the model
#     y_pred = model.predict(X)
    
#     # Return the predicted performance score as a response
#     return jsonify({'performance_score': int(y_pred[0])})



if __name__ == '__main__':
    app.run(debug=True)




