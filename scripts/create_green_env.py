import boto3
import json
import time  # For unique deployment naming

rds_client = boto3.client('rds')
ssm_client = boto3.client('ssm')

def lambda_handler(event, context):
    try:
        blue_instance_id = event['blue_instance_id']
        new_instance_class = event['new_instance_class']

        print(f"Starting Blue/Green Deployment for scaling up: {blue_instance_id}")

        # Fetch existing DB configuration
        db_instance = rds_client.describe_db_instances(DBInstanceIdentifier=blue_instance_id)['DBInstances'][0]

        # Extract required parameters
        target_engine_version = db_instance['EngineVersion']
        allocated_storage = db_instance['AllocatedStorage']
        storage_type = db_instance['StorageType']
        db_parameter_group_name = db_instance['DBParameterGroups'][0]['DBParameterGroupName']
        iops = db_instance.get('Iops')
        storage_throughput = db_instance.get('StorageThroughput')

        # Generate a unique deployment name using timestamp
        unique_suffix = int(time.time())
        deployment_name = f"{blue_instance_id}-scale-up-{unique_suffix}"

        # Construct deployment request
        blue_green_params = {
            "BlueGreenDeploymentName": deployment_name,
            "Source": f"arn:aws:rds:<your-region>:<your-account-id>:db:{blue_instance_id}",  # Masked
            "TargetDBInstanceClass": new_instance_class,
            "TargetEngineVersion": target_engine_version,
            "Tags": [{'Key': 'Environment', 'Value': 'Production'}],
            "TargetAllocatedStorage": allocated_storage,
            "TargetStorageType": storage_type,
            "TargetDBParameterGroupName": db_parameter_group_name
        }

        if iops is not None:
            blue_green_params["TargetIops"] = iops

        if storage_throughput is not None and storage_type in ["gp3", "io1"]:
            blue_green_params["TargetStorageThroughput"] = storage_throughput

        # Create Blue/Green Deployment
        response = rds_client.create_blue_green_deployment(**blue_green_params)
        deployment_identifier = response['BlueGreenDeployment']['BlueGreenDeploymentIdentifier']
        print(f"Deployment Identifier: {deployment_identifier}")

        # Store identifier in SSM Parameter Store
        ssm_client.put_parameter(
            Name='/bluegreen/deployment_identifier',
            Value=deployment_identifier,
            Type='String',
            Overwrite=True
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Blue/Green deployment for scaling up created successfully',
                'deployment_identifier': deployment_identifier
            })
        }

    except Exception as e:
        print(f"Error creating Blue/Green Deployment: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
