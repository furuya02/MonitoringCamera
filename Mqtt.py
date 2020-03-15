# -*- coding: utf-8 -*-
import boto3
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

class Mqtt():
    def __init__(self, identityPoolId, endPoint, clientId, topic, rootCA, onSubscribe):
        self.identityPoolId = identityPoolId
        self.endPoint = endPoint
        self.clientId = clientId
        self.topic = topic
        self.rootCA = rootCA
        self.onSubscribe = onSubscribe

    def connect(self):
        port =  443 # Cognito経由の認証では、Websocketしか使用できない
        rootCA = self.rootCA # ルート証明書も必要
        accessId, secretKey, token = self._getAuthentication(self.identityPoolId)
        client = AWSIoTMQTTClient(self.clientId, useWebsocket=True)
        client.configureIAMCredentials(accessId, secretKey, token)
        client.configureCredentials(rootCA)
        client.configureEndpoint(self.endPoint, port)
        client.configureAutoReconnectBackoffTime(1, 32, 20)
        client.configureOfflinePublishQueueing(-1)
        client.configureDrainingFrequency(2)
        client.configureConnectDisconnectTimeout(10)
        client.configureMQTTOperationTimeout(5)
        client.connect()
        print("mqtt connect.")
        client.subscribe(self.topic, 1, self._onSubscribe)
        print("mqtt subscrib.")

    def _getAuthentication(self, identityPoolId):
        client = boto3.client('cognito-identity', 'ap-northeast-1')
        res =  client.get_id(IdentityPoolId=identityPoolId)
        res = client.get_credentials_for_identity(IdentityId = res['IdentityId'])
        accessId = res['Credentials']['AccessKeyId']
        secretKey = res['Credentials']['SecretKey']
        token = res['Credentials']['SessionToken']
        return (accessId, secretKey, token)

    def _onSubscribe(self, client, userdata, message):
        print("subscribe message:{} topic:{}".format(message.payload, message.topic))
        self.onSubscribe(message.payload)



