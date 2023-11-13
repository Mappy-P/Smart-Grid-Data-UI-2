from flask import Blueprint, render_template, request

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/about')
def about():
    return render_template('about.html')

@views.route('/demo', methods=['GET', 'POST'])
def demo():
    if request.method == 'POST':
        typeOfCalculation = request.form.get('typeOfCalculation')
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')

#         if password != password1:
#             flash("Passwords don't match", category='error')
#         else:
#             new_user = User(email=email, first_name=firstName, password=generate_password_hash(password, method = 'sha256'))
#             db.session.add(new_user)
#             db.session.commit()
#             flash("Your account has succesfully been created!", category='succes')
#             return redirect(url_for('views.home'))

    return render_template('demo.html')