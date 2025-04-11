import boto3
import json
# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb')
# Define table name
table_name = 'student1'
# Read data from JSON file
with open('student_data.json', 'r') as file:
    data = json.load(file)
# Iterate over each item in the JSON data and insert it into table
for item in data:
    response = dynamodb.put_item(
        TableName=table_name,
        Item={
            'name': {'S': item['name']},
            'id': {'N': str(item['id'])},
            'major': {'S': item['major']},
            'year': {'S': item['year']}
        }
    )
    print("Item inserted:", item)
