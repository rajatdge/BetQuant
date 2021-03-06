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

    teams = []
    fixtures,teams = get_match_teams()
    #print "Teams ", teams
    #print "Fixtures ",fixtures

    if request.method == 'POST':
        name=request.form['teams']
        #print "The team name is : ",name
        email=request.form['email']
        bid=request.form['bet']
        #print name, " ", email, " "

        response2 = table2.scan(FilterExpression=Attr('email').eq(email))
        item = response2['Items']

        if allow_bid():
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


                        flash('Thanks for bidding ' + email)
                        return redirect(url_for('bid'))
                    else:

                        flash("You have Bid already")
                        return redirect(url_for('bid'))

            else:
                flash("Not a registered account")
                return redirect(url_for('bid'))
        else:
            flash("The Bidding is yet to start")

    return render_template('bid.html',teams=teams,fixtures=fixtures)

def allow_bid():
    current_time = timeoperations.get_current_time_in_unix_utc()
    print "Current time ", current_time
    current_str_date = timeoperations.convert_from_unix_to_str_date_time_utc(current_time)
    #print "current_str_date ", current_str_date

    match_date_time = table1.scan(FilterExpression=Attr('date').eq(current_str_date))
    #print "Match date time ", match_date_time
    match_details = match_date_time['Items']
    #print "Match item ",match_details

    if len(match_details) != 0:
        current_match_date_time = match_details[0]['date'] + " " + match_details[0]['time']
        #print "Current match date time ", current_match_date_time
        current_match_date_time_unix = timeoperations.convert_str_to_unix_time_utc(current_match_date_time)
        #print "Current match date time in unix ", current_match_date_time_unix

        bid_start_time = timeoperations.get_six_hours_before_time_utc(current_match_date_time_unix)
        print "Bid start time : ",bid_start_time
        bid_close_time = timeoperations.get_one_hour_before_time_utc(current_match_date_time_unix)
        print "Bid close time ",bid_close_time

        if current_time > bid_start_time and current_time < bid_close_time:
            return True
        else:
            return False
    else:
        return False

def get_match_teams():
    fixtures = []
    match_teams = []
    current_time = timeoperations.get_current_time_in_unix_utc()
    current_str_date = timeoperations.convert_from_unix_to_str_date_time_utc(current_time)
    match_date_time = table1.scan(FilterExpression=Attr('date').eq(current_str_date))
    team_details = match_date_time['Items']

    if len(team_details) == 0:
        return match_teams
    else:
        fixtures.append("{} vs {} | Starts at 11PM".format(team_details[0]['team1'],team_details[0]['team2']))
        match_teams.append(team_details[0]['team1'])
        match_teams.append(team_details[0]['team2'])
        return fixtures,match_teams


if __name__ == "__main__":
    app.run()
