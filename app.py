from flask import Flask, render_template, flash, request,url_for,redirect
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import boto3


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('testUser')
table1 = dynamodb.Table('Match_Fixture')
table2 = dynamodb.Table('Bidder')

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])
    password = TextField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])

class BetReusableForm(Form):
    team_name = TextField('Name:')
    email = TextField('Email:')
    bid = TextField('Bid:')

'''
@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    print form.errors
    if request.method == 'POST':
        name=request.form['name']
        password=request.form['password']
        email=request.form['email']
        print name, " ", email, " ", password


        if form.validate():
            table.put_item(
                Item={
                    "name" : name,
                    "email" : email,
                }
            )
            # Save the comment here.
            flash('Thanks for registration ' + name)
            return redirect(url_for('bid'))
        else:
            flash('Error: All the form fields are required. ')

    return render_template('hello.html', form=form)
'''

@app.route('/',methods = ['GET','POST'])
def bid():
    '''
    response = table1.get_item(
        Key={
            'match_id':3,
            'team1':'MI'
        }
    )
    '''

    if request.method == 'POST':
        team_name=request.form['name']
        email=request.form['email']
        bid=request.form['bid']
        print team_name, " ", email, " "

	bid_amount_for_individual = table2.get_item(
		Key={
        'email': {
            'S': email
		}


	   table2.put_item(
		  Item={
        	'email':email,
			'total_amount':total_amount,
			'bid':bid,
			'team':team_name
				}
			)


    return render_template('bid.html')

if __name__ == "__main__":
    app.run()
