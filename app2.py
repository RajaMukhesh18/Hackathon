from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS  
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rootroot'
app.config['MYSQL_DB'] = 'hackathon_db'

mysql = MySQL(app)

@app.route('/register', methods=['POST'])
def register_participant():
    data = request.json
    name = data.get('name')
    roll_number = data.get('roll_number')
    email = data.get('email')
    organization = data.get('organization')
    skills = data.get('skills')

    cursor = mysql.connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO participants (name, roll_number, email, organization, skills)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, roll_number, email, organization, skills))
        mysql.connection.commit()
        return jsonify({"message": "Participant registered successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()


# @app.route('/themes', methods=['GET'])
# def get_themes():
#     cursor = mysql.connection.cursor()
#     cursor.execute("SELECT id, name FROM themes")
#     themes = cursor.fetchall()
#     cursor.close()

#     return jsonify([{"id": t[0], "name": t[1]} for t in themes])

@app.route('/themes', methods=['POST'])
def add_theme():
    data = request.json
    name = data['name']

    cursor = mysql.connection.cursor()
    try:
        cursor.execute("INSERT INTO themes (name) VALUES (%s)", (name,))
        mysql.connection.commit()
        return jsonify({"message": "Theme added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()

# Route to submit a project
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'ppt', 'pptx'}

# Check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/submit', methods=['POST'])
def submit_project():
    if 'documentation' not in request.files or 'presentation' not in request.files:
        return jsonify({"error": "No file part"}), 400

    documentation = request.files['documentation']
    presentation = request.files['presentation']

    # Check if the files have valid names
    if documentation.filename == '' or presentation.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the files
    if documentation and allowed_file(documentation.filename):
        doc_filename = secure_filename(documentation.filename)
        documentation.save(os.path.join(app.config['UPLOAD_FOLDER'], doc_filename))
    else:
        return jsonify({"error": "Invalid documentation file"}), 400

    if presentation and allowed_file(presentation.filename):
        pres_filename = secure_filename(presentation.filename)
        presentation.save(os.path.join(app.config['UPLOAD_FOLDER'], pres_filename))
    else:
        return jsonify({"error": "Invalid presentation file"}), 400

    # Get the other form data
    team_name = request.form['team-name']
    project_title = request.form['project-title']
    project_link = request.form['project-link']

    # Insert the data into the database
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO submissions (team_name, project_title, project_link, documentation, presentation)
            VALUES (%s, %s, %s, %s, %s)
        """, (team_name, project_title, project_link, doc_filename, pres_filename))
        mysql.connection.commit()
        return jsonify({"message": "Project submitted successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
