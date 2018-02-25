from flask import Flask, render_template, flash, request,url_for,redirect
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from boto3.dynamodb.conditions import Key,Attr
import boto3
import timeoperations


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('testUser')
table1 = dynamodb.Table('Match_Fixture')
table2 = dynamodb.Table('Bidder1')

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
    bid = TextField('Bid:')
    email = TextField('Email:')


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

    if request.method == 'POST':
        name=request.form['name']
        email=request.form['email']
        bid=request.form['bet']
        print name, " ", email, " "

        response2 = table2.scan(FilterExpression=Attr('email').eq(email))
        item = response2['Items']
        if len(item) != 0:
            if int(item[0]['total_amount']) < int(bid):
                print "bid", bid
                print "The total amount is: {}".format(item[0]['total_amount'])
                response = "Not eligible to bet"
                flash('You do not have enough balance ' + email)
                return redirect(url_for('bid'))
            else:
                if(int(item[0]['bid']) == 0):
                    total_amount = int(item[0]['total_amount']) - int(bid)
                    print "total amount", total_amount

                    table2.update_item(
                            Key={
                                'email': email
                            },
                            UpdateExpression="set bid = :r, total_amount=:p, team=:a",
                            ExpressionAttributeValues={
                                ':r': int(bid),
                                ':p': total_amount,
                                ':a': name
                            }
                        )


                    '''
                    table2.put_item(
                            Item={
                                "email":email,
                                "bid":int(bid),
                                "team": name,
                                "total_amount":total_amount
                            }
                        )
                    '''
                    flash('Thanks for bidding ' + email)
                    return redirect(url_for('bid'))
                else:
                    flash("You have Bid already")
                    return redirect(url_for('bid'))

        else:
            flash("Not a registered account")
            return redirect(url_for('bid'))

    return render_template('bid.html')

if __name__ == "__main__":
    app.run()
