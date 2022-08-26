# -*- coding: utf-8 -*-
# Author: Logan Huang
import xml.dom.minidom

import requests
import boto3
from bs4 import BeautifulSoup
import xml.dom.minidom as minidom

url = "https://www.myvisionlink.cn/APIService/VLReady/FleetSummary/1"
head = {
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
}
req = requests.get(url,headers=head,auth=('API_J540','vlchina'))
xmlfile = req.text



with open('test','w',encoding='utf-8') as dfile:
    dfile.write(xmlfile)

s3 = boto3.resource('s3',
                  aws_access_key_id='AKIAZ7XWZS3UJ424XYOE',
                  aws_secret_access_key='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',
                  region_name='us-west-1')

with open('test','rb') as xfile:
    s3.Object('lxh-test','test.txt').upload_fileobj(xfile)



'''
s3 = boto3.resource('s3',
                  aws_access_key_id='xxx',
                  aws_secret_access_key='xxx',
                  region_name='us-west-1')

使用upload_file:
s3 = boto3.resource('s3')
s3.Object(bucket_name, file_name).upload_file(local_file)

使用upload_fileobj:
s3 = boto3.resource('s3')
with open(local_file, 'rb') as f:
    s3.Object(bucket_name, file_name).upload_fileobj(f)
    
使用put() method:
s3 = boto3.resource('s3')
with open(local_file, 'rb') as f:
    s3.Object(bucket_name, file_name).put(Body=f)

'''
