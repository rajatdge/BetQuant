import boto3
import re
users = []

client = boto3.client('cognito-idp')
db = boto3.client('dynamodb')


def lambda_handler(event, context):
    response = client.list_users(
        UserPoolId='us-east-1_2aoKvlGeg',
        AttributesToGet=[
            'email',
        ],

    )
    d1 = response['Users']
    for i in range(len(d1)):
        
        temp = d1[i]['Attributes'][0]['Value']
        if (re.match('[a-z]+\.[a-z]+@quantiphi\.com$',temp)):
            db.put_item(TableName='Bidder', Item={'email':{'S':temp},'total_amount':{'N':'50'},'bid':{'N':'0'}})
            users.append(temp)
            
    print(users)
    return 