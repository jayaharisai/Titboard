import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import json
import os
from structure import AWSCredentials
from collections import defaultdict

def validate_s3_access(credentials: AWSCredentials) -> bool:
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=credentials.access_key,
            aws_secret_access_key=credentials.secret_key,
            region_name=credentials.region
        )
        s3.list_buckets()
        return True
    except (ClientError, NoCredentialsError):
        return False

def validate_ec2_access(credentials: AWSCredentials) -> bool:
    try:
        ec2 = boto3.client(
            'ec2',
            aws_access_key_id=credentials.access_key,
            aws_secret_access_key=credentials.secret_key,
            region_name=credentials.region
        )
        ec2.describe_instances()
        return True
    except (ClientError, NoCredentialsError):
        return False
    

def get_ec2_instance_counts_from_config(file_path="config.json"):
    default_response = {
        "total": 0,
        "running": 0,
        "stopped": 0
    }

    if not os.path.exists(file_path):
        return default_response

    with open(file_path, "r") as f:
        creds_data = json.load(f)

    credentials = AWSCredentials(
        access_key=creds_data.get("access_key", ""),
        secret_key=creds_data.get("secret_key", ""),
        region=creds_data.get("region", "")
    )

    if not validate_ec2_access(credentials):
        return default_response

    ec2 = boto3.client(
        'ec2',
        aws_access_key_id=credentials.access_key,
        aws_secret_access_key=credentials.secret_key,
        region_name=credentials.region
    )

    try:
        response = ec2.describe_instances()
    except Exception:
        return default_response

    total = 0
    running = 0
    stopped = 0

    for reservation in response.get('Reservations', []):
        for instance in reservation.get('Instances', []):
            total += 1
            state = instance.get('State', {}).get('Name', '')
            if state == 'running':
                running += 1
            elif state == 'stopped':
                stopped += 1

    return {
        "total": total,
        "running": running,
        "stopped": stopped
    }



def get_instance_type_counts_from_config(file_path="config.json"):
    if not os.path.exists(file_path):
        return {}

    with open(file_path, "r") as f:
        creds_data = json.load(f)

    credentials = AWSCredentials(
        access_key=creds_data.get("access_key", ""),
        secret_key=creds_data.get("secret_key", ""),
        region=creds_data.get("region", "")
    )

    if not validate_ec2_access(credentials):
        return {}

    ec2 = boto3.client(
        'ec2',
        aws_access_key_id=credentials.access_key,
        aws_secret_access_key=credentials.secret_key,
        region_name=credentials.region
    )

    try:
        response = ec2.describe_instances()
    except Exception:
        return {}

    instance_type_counts = defaultdict(int)

    for reservation in response.get('Reservations', []):
        for instance in reservation.get('Instances', []):
            instance_type = instance.get('InstanceType', 'unknown')
            instance_type_counts[instance_type] += 1

    return dict(instance_type_counts)



def get_aws_credentials(file_path="config.json"):
    if not os.path.exists(file_path):
        return None

    with open(file_path, "r") as f:
        return json.load(f)
    
def load_aws_credentials():
    config_path = "config.json"
    if not os.path.exists(config_path):
        raise FileNotFoundError("config.json not found")
    
    with open(config_path) as f:
        config = json.load(f)
    
    return config["access_key"], config["secret_key"], config["region"]