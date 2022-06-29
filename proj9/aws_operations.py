import os
import boto3
import aws_operations 
import json
from botocore.config import Config
import logging
import boto3
from botocore.exceptions import ClientError
import paramiko
import time
from scp import SCPClient 
import sys
from datetime import datetime

#variable declaration
CHECK = "running"

# instance_config_file 
instance_config_file = os.path.join(os.getcwd(),'configs','instance_config.json')
instance_config_folder_path = os.path.join(os.getcwd(),'configs')

# loadJsonData function to read the data from instance_config.json
def loadJsonData(file_path):
    blank_json = {}
    if os.path.exists(file_path):
        try:
            f = open(file_path, "r")
            data = json.load(f)
            f.close()
            return data
        except ValueError: 
            custom_print("Decode error")
            return blank_json
    else:
     return blank_json    


#calling loadjsondata function and reading config details from instance_config.json
config_data = loadJsonData(instance_config_file)

#Loading config details from instance_config.json and storing in the variables
key_path = os.path.join(os.getcwd(),*config_data["key_path"].split("/"))
private_key = os.path.join(os.getcwd(),*config_data["Private_key_path"].split("/"))
key_name = config_data["key_name"]
username = config_data["username"]
ami_id = config_data["ami_id"]
instance_type = config_data["instance_type"]
region_name = config_data["region_name"]
vpc_id = config_data["vpc_id"]
subnet_id = config_data["subnet_id"]
tags=config_data["Tags"]
security_grp_id = config_data["security_grp_id"]
installation_script_path = os.path.join(os.getcwd(),*config_data["installation_script_path"].split("/"))
installation_script_config_path = os.path.join(os.getcwd(),*config_data["installation_script_config_path"].split("/"))


# custum custom_print
def custom_print(message_to_custom_print, log_file='log.txt'):
    print(message_to_custom_print)
    with open(log_file, 'a',encoding="utf-8") as logfile:
        now = datetime.now()
        date = now.strftime("%d %B,%Y %H:%M:%S")
        logfile.write('\n\n'+ date.__str__() + ' | ' + message_to_custom_print)
        
# create session
ec2_client = boto3.client("ec2", region_name=region_name)


# create Key
def create_key_pair():
    if not os.path.exists(key_path):
        key_pair = ec2_client.create_key_pair(KeyName=key_name)
        private_key = key_pair["KeyMaterial"]
        # write private key to file with 400 permissions
        with os.fdopen(os.open(key_path, os.O_WRONLY | os.O_CREAT, 0o400), "w+") as handle:
            handle.write(private_key)  

#create aws ec2 instance
def create_instance():
    instances = ec2_client.run_instances(
        ImageId=ami_id,
        MinCount=1,
        MaxCount=1,
        InstanceType=instance_type,
        SubnetId=subnet_id,
        SecurityGroupIds=[security_grp_id],
        KeyName=key_name,
        TagSpecifications=[{'ResourceType': 'instance','Tags': tags}]
    )
    time.sleep(30)
    instance_id = instances["Instances"][0]["InstanceId"]
    reservations = ec2_client.describe_instances(InstanceIds=[instance_id]).get("Reservations")
    for reservation in reservations:
        for instance in reservation['Instances']:
            public_ip_address = instance.get("PublicIpAddress")
    time.sleep(180)
    key = paramiko.RSAKey.from_private_key_file(private_key)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    time.sleep(10)
    custom_print("Connecting  to an Instance.......")
 # Connect/ssh to an instance

    try:
     client.connect(hostname=public_ip_address, username="ec2-user", pkey=key)
     # Execute a command(cmd) after connecting/ssh to an instance
      # copy the file across
     with SCPClient(client.get_transport()) as scp:
        scp.put(instance_config_folder_path,'/tmp',recursive=True)
     stdin, stdout, stderr = client.exec_command('sudo sh /tmp/configs/*.sh')
     time.sleep(10)
     custom_print("Instance Connected Sucessfully !!")
     custom_print("\nStarting Installation setup on instance ...")
     result= stdout.read().decode('utf-8').strip()
     if len(result):
        custom_print(result)
        custom_print("\nSucessfull!! Installation Setup has been completed.")
     else:
        custom_print("Error!! Installation has been failed. Please check configuration.")   
    # close the client connection once the job is done
    #  custom_print(" Installation setup has been completed.")
     stdin, stdout, stderr = client.exec_command('sudo rm -rf /tmp/')
     client.close()
    except Exception as e:
      custom_print(e) 
    for i in instances['Instances']:
     custom_print("\n\nInstance details are below: \n\nInstanceID is :  {}\nInstanceType is : {}\nPublicIP_address is : {}\n".format(i['InstanceId'],i['InstanceType'],public_ip_address))

# available regions
def available_regions(service):
    regions = []
    client = boto3.client(service)
    response = client.describe_regions()
    for item in response["Regions"]:
        regions.append(item["RegionName"])
    return regions   

#  List the running instances
def listec2instance():
    custom_print(f"Check for status: {CHECK}")
    regions = available_regions("ec2")

    # Check status of EC2 in each region
    cnt = 0
    for region in regions:
        # Change regions with config
        my_config = Config(region_name=region)
        client = boto3.client("ec2", config=my_config)
        response = client.describe_instances()
        for r in response["Reservations"]:
            status = r["Instances"][0]["State"]["Name"]
            if status == "running":
                instance_id = r["Instances"][0]["InstanceId"]
                instance_type = r["Instances"][0]["InstanceType"]
                az = r["Instances"][0]["Placement"]["AvailabilityZone"]
                custom_print(f"id: {instance_id}, type: {instance_type}, az: {az}")
                cnt += 1
    if cnt == 1:
           custom_print(f"{cnt} instance is {CHECK}!")
    elif cnt > 1:
           custom_print(f"{cnt} instances are {CHECK}!")
    else:
           custom_print(f"No instance is {CHECK}!")  



# get ip of running instance 
def get_public_ip(instance_id):
    reservations = ec2_client.describe_instances(InstanceIds=[instance_id]).get("Reservations")
    for reservation in reservations:
        for instance in reservation['Instances']:
            custom_print(instance.get("PublicIpAddress"))


#get list of all running instances
def get_running_instances():
    reservations = ec2_client.describe_instances(Filters=[
        {
            "Name": "instance-state-name",
            "Values": ["running"],
        }
    ]).get("Reservations")

    for reservation in reservations:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            instance_type = instance["InstanceType"]
            public_ip = instance["PublicIpAddress"]
            private_ip = instance["PrivateIpAddress"]
            custom_print(f"{instance_id}, {instance_type}, {public_ip}, {private_ip}")

            

#reboot instance
def reboot_instance(instance_id):
    response = ec2_client.reboot_instances(InstanceIds=[instance_id])
    custom_print(response)


#stop instance
def stop_instance(instance_id):
    response = ec2_client.stop_instances(InstanceIds=[instance_id])
    custom_print(response)



#start instance
def start_instance(instance_id):
    response = ec2_client.start_instances(InstanceIds=[instance_id])
    custom_print(response)


#terminate a single instance
def terminate_instance(instance_id):
    response = ec2_client.terminate_instances(InstanceIds=[instance_id])
    custom_print(response)
    # ec2_data["ec2_instance_ids"].remove(instance_id)


def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region
    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).
    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def list_buckets(region):
    # Retrieve the list of existing buckets
    s3 = boto3.client('s3', region_name=region)
    response = s3.list_buckets()

    # Output the bucket names
    custom_print('Existing buckets:')
    for bucket in response['Buckets']:
        custom_print(f'  {bucket["Name"]}')

def s3_upload_file(file_name, bucket_name, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket_name, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
               
def s3_download_file(file_name,bucket_name,region):
        try: 
             s3_client = boto3.client('s3', region_name=region)
             s3_client.download_file(bucket_name, file_name, os.path.join("./s3/download/",file_name))
             custom_print("S3 object download complete") 
        except ClientError as e:
            if logging.error['Error']['Code'] == 'AccessDenied': 
               custom_print("\n An error occurred (AccessDenied) when calling the GetObject operation: The ciphertext refers to a customer master key that does not exist, does not exist in this region, or you are not allowed to access.") 

def delete_object_from_bucket(bucket_name,file_name):
    s3_client = boto3.client("s3")
    response = s3_client.delete_object(Bucket=bucket_name, Key=file_name)
    custom_print(response)  

def delete_s3_bucket(bucket_name):                 
    client = boto3.client('s3') 
    custom_print("Before deleting the bucket we need to check if its empty. Cheking ...") 
    objs = client.list_objects_v2(Bucket=bucket_name) 
    fileCount = objs['KeyCount'] 

    if fileCount == 0: 
       response = client.delete_bucket(Bucket=bucket_name) 
       custom_print("{} has been deleted successfully !!!".format(bucket_name)) 
    else: 
       custom_print("{} is not empty {} objects present".format(bucket_name,fileCount)) 
       custom_print("Please make sure S3 bucket is empty before deleting it !!!") 
