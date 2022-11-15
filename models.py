from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
  db.app = app
  db.init_app(app)


# models 

class Department(db.Model):
  """Department Model"""

  __tablename__ = "departments"

  def __repr__(self):
    d = self
    return f"<dept_code={d.dept_code} dept_name={d.dept_name} phone={d.phone}>"

  dept_code = db.Column(db.Text, primary_key=True)
  dept_name = db.Column(db.Text, nullable=True, unique=True)
  phone = db.Column(db.Text)

 
  # employees = db.relationship('Employee')


class Employee(db.Model):
  """Employee Model"""

  __tablename__ = "employees"

  def __repr__(self):
    e = self
    return f"<EmployeeID={e.id} name={e.name} state={e.state} dept_code={e.dept_code}>"

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.Text, nullable=False, unique=True)
  state = db.Column(db.Text, nullable=False,default='CA')

  # Connect employees table with departments with a foreign key.
  # db.ForeignKey('table_name.column_name')
  dept_code = db.Column(db.Text, db.ForeignKey('departments.dept_code'))

  # dept is the name used to view the data that has a relationship with Department for an instance of Employee model 
  # emp1.dept.dept_name or emp1.dept.phone will return the dept name and phone number from departments table that is linked to emp1( an instance of Employee Model)
  # dept = db.relationship('Department')

  # backref short-hand method. If using backref we do not need 'employees = db.relationship('Employee')' under Department Model
  dept = db.relationship('Department', backref='employees')

  # We can have both direct relationship along with through relationships. Sometimes it can be useful to have a direct relationship
  assignments = db.relationship('EmployeeProject', backref='employee')

  # Example of through relationships. secondary is the name of the table that would be considererd the "middle" table linking projects and employees table
  projects = db.relationship('Project', secondary='employees_projects', backref="employees")


class Project(db.Model):
  """Project. Can be assigned to employees"""

  __tablename__ = "projects"

  proj_code = db.Column(db.Text, primary_key=True)
  proj_name = db.Column(db.Text, nullable=False, unique=True)

  assignments = db.relationship('EmployeeProject', backref="project")


class EmployeeProject(db.Model):
  """ Employees with their assigned projects"""

  __tablename__ = "employees_projects"

  # both columns together are primary key for EmployeeProject. Example: There can only be 1 combination where EmployeeID 1 and project_code server
  emp_id = db.Column(db.Integer, db.ForeignKey('employees.id'), primary_key=True)
  proj_code = db.Column(db.Text, db.ForeignKey('projects.proj_code'), primary_key=True)
  role = db.Column(db.Text)


def get_directory():
  all_emps = Employee.query.all()

  for emp in all_emps:
    if emp.dept is not None:
      print(emp.name, emp.dept.dept_name, emp.dept.phone )
    else:
      print(emp.name)


def get_directory_join():

  # directory returns a list of tuples
  # example: [('Spongebob Squarepants', '478-8344'), ('Patrick Star', '345-2311'), ('Sandy Cheeks', '478-8344')...]
  directory = db.session.query(Employee.name, Department.dept_name, Department.phone).join(Department).all()

  for name, dept, phone in directory:
    print(name, dept, phone)

# this is similar to get_directory_join() but directory is a list of tuples of objects
# example: [(<EmployeeID=1 name=Spongebob Squarepants state=CA dept_code=mktg>, <dept_code=mktg dept_name=marketing phone=478-8344>), (<EmployeeID=2 name=Patrick Star state=NV dept_code=acct>, <dept_code=acct dept_name=accounting phone=345-2311>)...]
def get_directory_join_class():
  directory = db.session.query(Employee, Department).join(Department).all()
  print(directory)

  for emp, dept in directory:
    print(emp.name, dept.dept_name, dept.phone)

