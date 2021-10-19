response_status, response_export_id, response_code = export_dynamodb()

dynamodb_client = boto3.client('dynamodb', region_name='us-east-1')

while response_status == 'IN_PROGRESS':
    try:
        response_check = dynamodb_client.list_exports(TableArn=response_export_id, MaxResults=1)
        response_status = response_check['ExportSummaries'][0]['ExportStatus']
        time.sleep(30)
    except:
        time.sleep(60)
    if response_status == 'FAILED':
        print('Error')
        break;
