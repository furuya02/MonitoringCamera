import boto3

class S3():
    def __init__(self, identityPoolId):
        accessId, secretKey, token = self._getAuthentication(identityPoolId)
        self.s3 = boto3.client('s3', aws_access_key_id=accessId, aws_secret_access_key= secretKey, aws_session_token=token)


    def _getAuthentication(self, identityPoolId):
        client = boto3.client('cognito-identity', 'ap-northeast-1')
        res =  client.get_id(IdentityPoolId=identityPoolId)
        res = client.get_credentials_for_identity(IdentityId = res['IdentityId'])
        accessId = res['Credentials']['AccessKeyId']
        secretKey = res['Credentials']['SecretKey']
        token = res['Credentials']['SessionToken']
        return (accessId, secretKey, token)
    
    def putObject(self, bucket, key, fileName):
        data = open(fileName, 'rb')
        self.s3.put_object(Bucket=bucket, Key=key, Body=data)