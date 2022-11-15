from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, HiddenField, RadioField, SelectField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Email

states = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']


class AddSnackForm(FlaskForm):
  """Form for adding snacks"""

  # you can easily add or remove fields on this form. This is more efficient than hardcoding each inputs and labels
  name = StringField("Snack Name", validators=[InputRequired(message="Please enter snack name")])
  price = FloatField("Price in USD")
  quantity = IntegerField("How many?")
  is_healthy = BooleanField("This is a health snack")
  test = HiddenField("asdas")
  email = StringField("Email",validators=[Email()])


  category = SelectField("Category", choices=[('ic','Ice Cream'), ('chips', 'Potato Chips'), ('candy','Candy/Sweet')])

  # category = RadioField("Category", choices=[('ic','Ice Cream'), ('chips', 'Potato Chips'), ('candy','Candy/Sweet')])

  
class EmployeeForm(FlaskForm):
  
  name = StringField("Employee Name", validators=[InputRequired(message="Please enter name")])
  state = SelectField("State", choices=[(s, s) for s in states])
  dept_code = SelectField("Department Code")

