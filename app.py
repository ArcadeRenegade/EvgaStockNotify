import urllib3
import re
import boto3

headers = {
	'Host': 'www.evga.com',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
	'Accept': '*/*',
	'Accept-Language': 'en-US,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate, br',
	'Referer': 'https://www.evga.com/products/product.aspx?pn=24G-P5-3989-KR',
	'Content-Type': 'application/x-www-form-urlencoded',
	'Origin': 'https://www.evga.com',
	'Connection': 'keep-alive'
}

http = urllib3.PoolManager(headers=headers)

url = 'https://www.evga.com/products/product.aspx?pn=24G-P5-3989-KR'

def lambda_handler(event, context):
    response = http.request('GET', url, headers=headers)

    print('Status Code: %d' % response.status)

    if response.status == 200:
        if re.search(b'out of stock', response.data, re.IGNORECASE):
            print('bro it is out of stock')
        else:
            print('it is in stock!!!!')

            sns = boto3.client('sns')

            sns.publish(
                PhoneNumber='+13107951605',
                Message='EVGA 3090 IN STOCK: %s' % url,
                MessageAttributes={
                    'AWS.SNS.SMS.SenderID': {
                        'DataType': 'String',
                        'StringValue': 'HouseStay'
                    },
                    'AWS.SNS.SMS.MaxPrice': {
                        'DataType': 'Number',
                        'StringValue': '0.15'
                    },
                    'AWS.SNS.SMS.SMSType': {
                        'DataType': 'String',
                        'StringValue': 'Transactional'
                    }
                }
            )

lambda_handler(None, None)