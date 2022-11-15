"""Seed file to make sample data"""

from models import Department, Employee, db, EmployeeProject, Project
from app import app


db.drop_all()
db.create_all()

###### First half is for Department and Employee Models

# d1 = Department(dept_code="mktg", dept_name="marketing",phone="478-8344")
# d2 = Department(dept_code="acct", dept_name="accounting",phone="345-2311")
# d3 = Department(dept_code="it", dept_name="Information technology",phone="")
# d4 = Department(dept_code="sales", dept_name="Sales",phone="255-6584")
# d5 = Department(dept_code="r&d", dept_name="Reseach and Development",phone="315-6584")

# emp1 = Employee(name="Spongebob Squarepants", state="CA", dept_code="mktg")
# emp2 = Employee(name="Patrick Star", state="NV", dept_code="acct")
# emp3 = Employee(name="Sandy Cheeks", state="NY", dept_code="mktg")
# emp4 = Employee(name="Mr. Crabs", state="CA", dept_code="acct")
# emp5 = Employee(name="Larry", state="WA", dept_code="it")
# emp6 = Employee(name="Pearl", dept_code="r&d")
# emp7 = Employee(name="freelancer")

# db.session.add_all([d1,d2,d3,d4,d5])

# # To avoid running into a foreign key error, add and committ the department instances first then add and commit the employees instances. Reason is because we are not guaranteed that department will be added first, and if employee is added first and we set the foreign key to equal to some key on department that does not exist yet, it will throw an error
# db.session.commit()

# db.session.add_all([emp1,emp2,emp3,emp4,emp5,emp6,emp7])
# db.session.commit()

###########################################################################################

# This is for many to many relationships between Employee, Project, EmployeeProject 

EmployeeProject.query.delete()
Employee.query.delete()
Department.query.delete()
Project.query.delete()

# Add sample employees and departments
df = Department(dept_code='fin', dept_name='Finance', phone='555-1000')
dl = Department(dept_code='legal', dept_name='Legal', phone='555-2222')
dm = Department(dept_code='mktg', dept_name='Marketing', phone='555-9999')

leonard = Employee(name='Leonard', dept=dl)
liz = Employee(name='Liz', dept=dl)
maggie = Employee(name='Maggie', state='DC', dept=dm)
nadine = Employee(name='Nadine')

db.session.add_all([df, dl, dm, leonard, liz, maggie, nadine])
db.session.commit()

pc = Project(proj_code='car', proj_name='Design Car',
             assignments=[EmployeeProject(emp_id=liz.id, role='Chair'),
                          EmployeeProject(emp_id=maggie.id)])
ps = Project(proj_code='server', proj_name='Deploy Server',
             assignments=[EmployeeProject(emp_id=liz.id),
                          EmployeeProject(emp_id=leonard.id, role='Auditor')])

db.session.add_all([ps, pc])
db.session.commit()
