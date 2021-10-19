def export_dynamodb(**kwargs):
    dynamodb_client = boto3.client('dynamodb', region_name='us-east-1')
    try:
        response_export = dynamodb_client.export_table_to_point_in_time(
            TableArn='<table ARN>', #ex: arn:aws:dynamodb:us-east-1:000000000000:table/platforms-contracts
            ExportTime='<datetime>', #ex: 2021-10-19 00:00:00
            S3Bucket='<aws_bucket_name>',
            S3BucketOwner='<aws_bucket_owner>',
            S3Prefix='<aws_bucket_prefix>',
            S3SseAlgorithm='<s3_sse_algorithm>',#ex: AES256
            ExportFormat='DYNAMODB_JSON'
        )
        response_export_id = response_export['ExportDescription']['TableArn']
        response_check = dynamodb_client.list_exports(TableArn=response_export_id, MaxResults=1)
        response_status = response_check['ExportSummaries'][0]['ExportStatus']
        response_code = str(response_check['ExportSummaries'][0]['ExportArn']).split('/')[-1]
    except:
        print('Error')
    return (response_status, response_export_id, response_code)
