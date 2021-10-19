import json
import boto3
import decimal
import datetime
from datetime import datetime

today = datetime.today()
dt_time = today.strftime('%Y-%m-%d %H:%M:%S')
partition_column = ', "timestamp": "'+ dt_time+'"}'
dynamodb = boto3.resource('dynamodb')
table_name = 'platforms_contract'
file_name = table_name +'_'+ today.strftime('%Y%m%d_%H%M%S') + '.json'
table = dynamodb.Table(table_name)

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        if isinstance(o, set):
            return list(o)
        return super(DecimalEncoder, self).default(o)

def result_file(response):
    items = response['Items']
    for i in items:
        try:
            i = json.dumps(i, cls=DecimalEncoder)
            i = str(i)[:-1]+partition_column
            print(i, file=f)
        except:
            ExclusiveStartKey = None

with open('/mnt/' + file_name, 'w') as f:
    last_evaluated_key = None
    while True:
        if last_evaluated_key:
            response = table.scan(ExclusiveStartKey=last_evaluated_key)
            result_file(response)
        else: 
            response = table.scan()
            result_file(response)
        last_evaluated_key = response.get('LastEvaluatedKey')
        if not last_evaluated_key:
            break
f.close()
