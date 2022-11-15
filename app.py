from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Employee, Department, get_directory, get_directory_join, get_directory_join_class, Project, EmployeeProject
from forms import AddSnackForm, EmployeeForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///employees_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/phones')
def list_phones():
  emps = Employee.query.all()
  return render_template('phones.html', emps=emps)



######################
# Start of flask-WTF Example


@app.route('/')
def homepage():
  return render_template("snack_example_home.html")

@app.route('/snacks/new', methods=['GET','POST'])
def add_snack():

  #create an instance for the class AddSnackForm because we will add it to add_snack_form.html, AND data from the POST request can be accessed with form instead of request.form['']
  form = AddSnackForm()
  
  # this validates the CSRF token. If the token is validated and it is a POST request then it will redirect. If a token was not validated (was not generated) then it will render the template because it was a GET request
  if form.validate_on_submit():
      name = form.name.data
      
      # form.price actually returns an integer unlike request.form["price"] because it is a FloatField
      price = form.price.data 
      flash(f'Created new snack: name is {name}, price is ${price}')
      return redirect('/')
  else:
      return render_template("add_snack_form.html", form=form)



@app.route('/employees/new', methods=["GET", "POST"])
def add_employee():

  # create instance of Employeeform class
  form = EmployeeForm()

  # This will return a list of tuples. NOT WORKING FOR SOME REASON
  # depts = db.session.query(Department.dept_code, Department.dept_name)

# Another way to return a list of tuples
  depts = [(d.dept_code, d.dept_name) for d in Department.query.all()]

  # This updates the dept_code field on forms.py; we are passing a list of tuples to be used in the SelectField
  form.dept_code.choices = depts

  if form.validate_on_submit():
    
    # Data submitted from EmployeeForm; which can be retrieved through form
    name = form.name.data
    state = form.state.data
    dept_code = form.dept_code.data
    
    # Create an instance of the Employee model using data EmployeeForm
    emp = Employee(name=name, state=state, dept_code=dept_code)
    db.session.add(emp)
    db.session.commit()
    return redirect('/phones')
  else:
    return render_template('add_employee_form.html', form=form)



@app.route('/employees/<int:id>/edit', methods=['GET', 'POST'])
def edit_employee(id):

  emp = Employee.query.get_or_404(id)

  # pass in user to form so that we can have the form populated with the current values in our database
  form = EmployeeForm(obj=emp)
  depts = [(d.dept_code, d.dept_name) for d in Department.query.all()]
  # update choices paramenter of dept_code on the form 
  form.dept_code.choices = depts

  if form.validate_on_submit():
    emp.name = form.name.data
    emp.state = form.state.data
    emp.dept_code = form.dept_code.data
    db.session.commit()
    return redirect('/phones')

  else:
    return render_template('edit_employee_form.html', form=form)
