from troposphere import GetAtt, Join, Ref, Template, Parameter, Sub
from troposphere.cloudformation import AWSCustomObject, CustomResource
from troposphere.awslambda import Code, Function

from awacs.aws import Allow, Statement, Principal, PolicyDocument
from awacs.sts import AssumeRole

template = Template()

# add parameters
pPrefix = template.add_parameter(Parameter(
    'Prefix',
    Description='Lambda Function Name Prefix',
    Type='String'
))

piAppUrl = template.add_parameter(Parameter(
    'iAppUrl',
    Description='URL to download the BIG-IP AWS HA iApp',
    Default='https://raw.githubusercontent.com/F5Networks/f5-aws-cloudformation/v3.1.0/iApps/f5.aws_advanced_ha.v1.4.0rc3.tmpl',
    Type='String'
))

pBigIPMgmt = template.add_parameter(Parameter(
    'BigIPMgmt',
    Description='Active BIG-IP Management IP address',
    Type='String'
))

pBigIPRouteTableId = template.add_parameter(Parameter(
    'BigIPRouteTableId',
    Description='BIG-IP route table id for HA',
    Type='String'
))

pBigIPInterface = template.add_parameter(Parameter(
    'BigIPInterface',
    Description='BIG-IP interface for HA',
    Type='String'
))


pBigIPS3Bucket = template.add_parameter(Parameter(
    'BigIPS3Bucket',
    Description='BIG-IP S3 bucket where password is stored',
    Type='String'
))

custom = template.add_resource(CustomResource(
    'CustomLambdaExec',
    # ServiceToken=GetAtt('install-lambda-test-ha-iapp', 'Arn'),
    ServiceToken=Sub('arn:aws:lambda:${AWS::Region}:${AWS::AccountId}:function:${pPrefix}-ha-iapp'),
    mgmt_ip=Ref('BigIPMgmt'),
    iapp_url=Ref('iAppUrl'),
    route_table_id=Ref('BigIPRouteTableId'),
    interface=Ref('BigIPInterface'),
    s3_bucket=Ref('BigIPS3Bucket')
))

# print(template.to_json())
f = open('ha_iapp.json', "w+")
f.write(template.to_json())
f.close()