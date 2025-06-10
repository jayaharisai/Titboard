from fastapi import APIRouter, HTTPException
from structure.cloud_apis import AWSCredentials, InstanceRequest
import json
from helper.utils  import (
    validate_s3_access, 
    validate_ec2_access,
    get_ec2_instance_counts_from_config,
    get_instance_type_counts_from_config,
    get_aws_credentials,
    load_aws_credentials
    )
import os
import boto3

router = APIRouter()


@router.post("/aws/validate-and-store")
def validate_and_store_aws_credentials(credentials: AWSCredentials):
    try:
        has_s3_access = validate_s3_access(credentials)
        has_ec2_access = validate_ec2_access(credentials)

        if not has_s3_access or not has_ec2_access:
            return {
                "success": False,
                "message": "AWS credentials need access to both EC2 and S3."
            }

        # Store credentials in JSON file
        creds_data = {
            "access_key": credentials.access_key,
            "secret_key": credentials.secret_key,
            "region": credentials.region,
            "s3_access": has_s3_access,
            "ec2_access": has_ec2_access
        }

        with open("config.json", "w") as f:
            json.dump(creds_data, f, indent=4)

        return {
            "success": True,
            "message": "Credentials validated successfully and stored."
        }
    except:
        return {
            "success": False,
            "message": "Not a valid credentials."
        }

@router.get("/aws/get-credentials")
def get_stored_credentials():
    default_response = {
        "access_key": "",
        "secret_key": "",
        "region": "",
        "s3_access": False,
        "ec2_access": False
    }

    if not os.path.exists("config.json"):
        return default_response

    with open("config.json", "r") as f:
        creds_data = json.load(f)
    
    return creds_data

@router.get("/aws/ec2-instance-status")
def ec2_instance_status():
    return get_ec2_instance_counts_from_config()

@router.get("/aws/ec2-instance-types")
def ec2_instance_type_counts():
    return get_instance_type_counts_from_config()


@router.get("/aws/regions")
def get_aws_regions():
    creds = get_aws_credentials()
    if not creds:
        return {"error": "AWS credentials not found."}

    try:
        ec2 = boto3.client(
            "ec2",
            aws_access_key_id=creds["access_key"],
            aws_secret_access_key=creds["secret_key"],
            region_name=creds["region"] or "us-east-1"  # fallback region
        )
        response = ec2.describe_regions()
        regions = [region['RegionName'] for region in response['Regions']]
        return {"regions": regions}
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/aws/ec2-instance-details")
def get_instance_details():
    try:
        access_key, secret_key, region = load_aws_credentials()

        ec2 = boto3.client(
            "ec2",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )

        instances_info = []
        reservations = ec2.describe_instances()["Reservations"]

        for reservation in reservations:
            for instance in reservation["Instances"]:
                name = next(
                    (tag["Value"] for tag in instance.get("Tags", []) if tag["Key"] == "Name"),
                    "N/A"
                )
                instance_info = {
                    "name": name,
                    "status": instance.get("State", {}).get("Name", "unknown"),
                    "instance_id": instance.get("InstanceId"),
                    "public_ip": instance.get("PublicIpAddress", "N/A"),
                    "instance_type": instance.get("InstanceType"),
                    "launch_date": instance.get("LaunchTime").strftime("%d %b, %Y")
                }
                instances_info.append(instance_info)

        return {"instances": instances_info}
    
    except FileNotFoundError as e:
        return {"success": False, "message": str(e)}
    except Exception as e:
        return {"success": False, "message": f"Failed to retrieve instances: {str(e)}"}

@router.post("/start-instance")
def start_instance(req: InstanceRequest):
    with open("config.json") as f:
        config = json.load(f)

    ec2_client = boto3.client(
        'ec2',
        aws_access_key_id=config['access_key'],
        aws_secret_access_key=config['secret_key'],
        region_name=config['region']
    )
    try:
        response = ec2_client.start_instances(InstanceIds=[req.instance_id])
        return {"message": f"Starting instance {req.instance_id}", "response": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/stop-instance")
def stop_instance(req: InstanceRequest):
    with open("config.json") as f:
        config = json.load(f)

    ec2_client = boto3.client(
        'ec2',
        aws_access_key_id=config['access_key'],
        aws_secret_access_key=config['secret_key'],
        region_name=config['region']
    )
    try:
        response = ec2_client.stop_instances(InstanceIds=[req.instance_id])
        return {"message": f"Stopping instance {req.instance_id}", "response": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

