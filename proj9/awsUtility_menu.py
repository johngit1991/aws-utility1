import os
import boto3
import aws_operations 
import json
from botocore.config import Config
import logging
import boto3
from botocore.exceptions import ClientError
import paramiko
import sys
from datetime import datetime



while True:
    print("\n")
    print("Menu Driven Program\n")
    print("1. Create Key Pair")
    print("2. Launch EC2 Instance")
    print("3. Start EC2 instance")
    print("4. Stop EC2 Instance") 
    print("5. Get Public IP address of EC2 Instance")
    print("6. Reboot EC2 Instance")   
    print("7. Terminate EC2 Instance")     
    print("8. List EC2 instances")   
    print("9. Create S3 Bucket")    
    print("10. List All S3 Bucket")  
    print("11. Upload file in S3 Bucket") 
    print("12. Download File from S3 Bucket")  
    print("13. Delete File in S3 Bucket")  
    print("14. Delete  S3 Bucket")   
    print("15. Exit")
    print("\n")
    choice=int(input("Enter your choice: "))
    print("\n")
    if choice==1:
        aws_operations.create_key_pair()
   
    elif choice==2:
        aws_operations.create_instance()

    elif choice==3:
        instance_id= input(" Enter ec2 instace id: ")
        aws_operations.start_instance(instance_id)
    
    elif choice==4:
        instance_id= input(" Enter ec2 instace id: ")
        aws_operations.stop_instance(instance_id)

    elif choice==5:
        instance_id= input(" Enter ec2 instace id: ")
        aws_operations.get_public_ip(instance_id)

    elif choice==6:
        instance_id= input(" Enter ec2 instace id: ")
        aws_operations.reboot_instance(instance_id)


    elif choice==7:
        instance_id= input(" Enter ec2 instace id: ")
        aws_operations.terminate_instance(instance_id)

    elif choice==8:
        aws_operations.listec2instance()


    elif choice==9:
        bucket_name= input(" Enter Bucketname: ")
        region_name= input(" Enter region: ")
        aws_operations.create_bucket(bucket_name,region_name)

    elif choice==10:
        region_name= input(" Enter region: ")
        aws_operations.list_buckets(region_name)
    
    elif choice==11:
        bucket_name= input(" Enter Bucketname: ")
        file_name= input(" Enter file name to upload on S3 bucket: ")
        aws_operations.s3_upload_file(file_name,bucket_name)    

    elif choice==12:
        region_name= input(" Enter region: ")
        bucket_name= input(" Enter Bucketname: ")
        file_name= input(" Enter download file name from S3 bucket: ")
        aws_operations.s3_download_file(file_name,bucket_name,region_name)  

    elif choice==13:
        bucket_name= input(" Enter Bucketname: ")
        file_name= input(" Enter file name to delete from S3 bucket: ")
        aws_operations.delete_object_from_bucket(bucket_name,file_name) 

    elif choice==14:
        bucket_name= input(" Enter Bucketname: ")
        aws_operations.delete_s3_bucket(bucket_name) 

    elif choice==15:
        # get_running_instances()12
        break
    else:
        print("Please enter the correct choice")
        print("\n")