# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import LoginManager
# from sqlalchemy.sql import func
#
# login = LoginManager()
# db = SQLAlchemy()
#
#
# class UserModel(UserMixin, db.Model):
#     __tablename__ = 'Users'
#     staff_id = db.Column(db.Integer, primary_key=True)
#     staff_role = db.Column(db.String(20))
#     email = db.Column(db.String(80), unique=True)
#     first_name = db.Column(db.String(20))
#     last_name = db.Column(db.String(20))
#     profile_pic = db.Column(db.String())
#     password_hash = db.Column(db.String())
#
#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)
#
#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)
#
#
# @login.user_loader
# def load_user(id):
#     return UserModel.query.get(int(id))
#
#
# class Ward(db.Model):
#     __tablename__ = 'Ward'
#     ward_id = db.Column(db.Integer, primary_key=True)
#     ward_name = db.Column(db.String, nullable=False)
#     bed_count = db.Column(db.String, nullable=False)
#     ward_link = db.relationship('Staff', backref='ward_link')
#     ward_patients = db.relationship('Patient', backref='patient_link')
#
#
# class Patient(db.Model):
#     __tablename__ = 'Patient'
#     patient_id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String, nullable=False)
#     last_name = db.Column(db.String, nullable=False)
#     address = db.Column(db.String, nullable=False)
#     DOB = db.Column(db.String, nullable=False)
#     registered_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
#     patients = db.relationship('Staff', backref='patients')
#     assigned_ward = db.Column(db.Integer, db.ForeignKey('Ward.ward_id'))
#     assigned_consultant = db.Column(db.Integer, db.ForeignKey('Staff.Staff_ID'))
#
#
# class Staff(db.Model):
#     __tablename__ = 'Staff'
#     Staff_ID = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String, nullable=False)
#     last_name = db.Column(db.String, nullable=False)
#     role = db.Column(db.String, nullable=False)
#     assigned_ward = db.Column(db.Integer, db.ForeignKey('Ward.ward_id'))
#     assigned_patients = db.relationship('Patient', backref='consultant_link')
#
