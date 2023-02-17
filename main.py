import base64
from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_required, current_user, login_user, logout_user
from Model import *
from default_pic import default_profile
from sqlalchemy import update, distinct, delete

app = Flask(__name__)
app.secret_key = 'xyz'
database = app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PassTable.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login.init_app(app)
login.login_view = 'login'


@app.before_first_request
def create_database():
 with app.app_context():
    #db.drop_all()
    # db.create_all()
    # #new_thing = Staff(first_name="sussy", last_name="baki")
    # new_ward = Ward(ward_name="sunshine ward", bed_count=201)
    # new_staff = UserModel(first_name="bam", last_name="salt", staff_role="Admin")
    # new_patient = Patient(first_name="men", last_name="yearner", address="EX19 834", DOB="15/02/2001", patient_link=new_ward, consultant_link=new_staff)
    # #db.session.add(new_thing)
    # db.session.add(new_ward)
    # db.session.add(new_patient)
    # db.session.add(new_staff)
    db.session.commit()


@app.route('/', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('portal'))

    if request.method == 'POST':
        email = request.form['email']
        user = UserModel.query.filter_by(email=email).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('portal'))

            # user_content = UserModel.query.filter_by(id=current_user.id)
            # user_patients = Patient.query.filter_by(assigned_consultant=1)
            # return render_template('hospitalportal.html', data=user_content, patients=user_patients)

    return render_template('homepage.html')


@app.route('/staffportal', methods=['POST', 'GET'])
@login_required
def portal():
    if request.method == 'GET':
     #print(current_user.id)
     if current_user.staff_role == "Consultant" or current_user.staff_role == "Admin":
       user_content = UserModel.query.filter_by(id=current_user.id)
       user_patients = Patient.query.filter_by(assigned_consultant=current_user.id)
       #data_length = Patient.query.count()
       #print(user_content)
       return render_template('hospitalportal.html', data=user_content, patients=user_patients)
     else:
         user_content = UserModel.query.filter_by(id=current_user.id)
         user_patients = Patient.query.filter_by(assigned_consultant=2)
         return render_template('hospitalportal.html', data=user_content, patients=user_patients)


@app.route('/new', methods=['POST'])
@login_required
def new():
    return render_template('add.html')

@app.route('/newpatient', methods=['POST'])
def newpatient():
    if request.method == 'POST':
        with app.app_context():
            f_name = request.form['f_name']
            l_name = request.form['l_name']
            p_address = request.form['address']
            dob = request.form['dob']
            ward = request.form['Ward']
            consultant = request.form['consultant']
            new_patient = Patient(first_name=f_name, last_name=l_name, address=p_address, DOB=dob, assigned_ward=ward, assigned_consultant=consultant)
            db.session.add(new_patient)
            db.session.commit()
            return redirect(url_for('portal'))


@app.route('/update/<int:id>/', methods=['POST'])
@login_required
def updatep(id):
    #allwards = Patient.query(Patient.patient_id.distinct()).all()
    #print(allwards)
    update_data = Patient.query.filter_by(patient_id=id)
    return render_template('update.html', data=update_data)


@app.route('/updatepatient', methods=['POST'])
def updatepatient():
    if request.method == 'POST':
        with app.app_context():
            patient_id = request.form['Id']
            f_name = request.form['f_name']
            l_name = request.form['l_name']
            p_address = request.form['address']
            ward = request.form['Ward']
            new_data = (update(Patient).where(Patient.patient_id == patient_id).values(first_name=f_name, last_name=l_name, address=p_address, assigned_ward=ward))
            db.session.execute(new_data)
            db.session.commit()
            return redirect(url_for('login'))


@app.route('/delete/<int:id>/', methods=['POST'])
@login_required
def deletep(id):
    delete_data = Patient.query.filter_by(patient_id=id)
    return render_template('delete.html', data=delete_data)


@app.route('/deletepatient', methods=['POST'])
def deletepatient():
    if request.method == 'POST':
        with app.app_context():
            patients_id = request.form['Id']
            print(patients_id)
            Patient.query.filter_by(patient_id=patients_id).delete()
            db.session.commit()
            return redirect(url_for('portal'))



@app.route('/configprofile', methods=['POST', 'GET'])
@login_required
def uppro():
    if request.method == "GET":
        return '''
                 <!doctype html>
            <html lang="en">
                <head>
                <!-- Required meta tags -->
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

                <!-- Bootstrap CSS -->
                <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">

                <title>Admin Portal</title>
                </head>
                <body>
                <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
                <a class="navbar-brand" href="#">Administrator Portal</a>
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul class="navbar-nav mr-auto">
                        <li class="nav-item active">
                            <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
                        </li>
                        <li class="nav-item active">
                            <a class="nav-link" href="#">Portfolio <span class="sr-only">(current)</span></a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">Link</a>
                        </li>
                        <li class="nav-item active">
                            <a class="nav-link" href='http://127.0.0.1:5000/logout'>Log Out <span class="sr-only">(current)</span></a>
                        </li>
                    </ul>
                    <form class="form-inline my-2 my-lg-0">
                        <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
                        <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
                    </form>
                </div>
            </nav>
            <div class="jumbotron">
                <div class="container">
                    <h1 class="display-4">Welcome to the Admin portal</h1>
                    <p class="lead">Configure Our Portfolio Here</p>
                </div>
            </div>
            <center>
            <p> Upload Image here To Be Added To the Portfolio</p>
                  <form method="POST"
                  enctype="multipart/form-data">
                  <input type="file" accept="image/*" name="file" onchange="loadFile(event)">
                  <p><img id="output" width="200"/></p>
                  <script>
                      var loadFile = function(event) {
                          var image = document.getElementById('output');
                          image.src=URL.createObjectURL(event.target.files[0]);
                      };
                  </script>
               <p style = "direction: rtl;">
                  Upload Caption here To be added to image
               </p>
               <div class="form-group">
                    <input type="text" name="title" placeholder="Image Caption" class="form-control width="100" height="200"">
                </div>
                <div class="form-group">
                    <input type="text" name="message" placeholder="Image Caption" class="form-control width="100" height="200"">
                </div>
                <input type="submit">
                </form>
                </center>  
              </body>
            </html> 
                 '''
    if request.method == "POST":
       with app.app_context():
         image = request.files['file']
         b64_string = base64.b64encode(image.read())
         data = (b64_string.decode('utf-8'))
         newpic = (update(UserModel).where(UserModel.email == current_user.email).values(profile_pic=data))
         db.session.execute(newpic)
         db.session.commit()
         return 'uploaded successfully'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        email = request.form['email']
        f_name = request.form['fname']
        l_name = request.form['lname']
        password = request.form['password']
        pic = default_profile

        if UserModel.query.filter_by(email=email).first():
            return ('Email already Present')

        #staff_role = "Admin",
        user = UserModel(email=email, first_name=f_name, last_name=l_name, profile_pic=pic)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    return render_template('register.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/nav')
def nav():
    tests = UserModel.query.all()
    for test in tests:
        print(test.first_name)
    return render_template('chartjsdate.html')

if __name__ == "__main__":
    app.run(debug=True)
