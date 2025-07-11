import boto3
import json

# Initialize the RDS client
rds = boto3.client('rds')

def lambda_handler(event, context):
    try:
        # ✅ Get the latest Blue/Green deployment
        response = rds.describe_blue_green_deployments()
        latest_deployment = response['BlueGreenDeployments'][-1]

        # Extract old (blue) DB instance ID
        old_instance_id = latest_deployment['SwitchoverDetails'][0]['SourceMember'].split(':')[-1]
        
        print(f"Latest Deployment ID: {latest_deployment['BlueGreenDeploymentIdentifier']}")
        print(f"Old (blue) DB Instance: {old_instance_id}")
        
        # ✅ Check current status of the old instance
        instance_info = rds.describe_db_instances(DBInstanceIdentifier=old_instance_id)
        instance_status = instance_info['DBInstances'][0]['DBInstanceStatus']
        print(f"Current status of {old_instance_id}: {instance_status}")
        
        # ✅ Delete instance only if it's in available state
        if instance_status == 'available':
            print(f"Deleting old DB instance: {old_instance_id}")
            rds.delete_db_instance(DBInstanceIdentifier=old_instance_id, SkipFinalSnapshot=True)
            print(f"Deletion triggered for: {old_instance_id}")
        elif instance_status == 'deleting':
            print(f"Instance {old_instance_id} is already being deleted.")
        else:
            print(f"Instance {old_instance_id} is in state '{instance_status}'. Skipping deletion.")

        # ✅ Delete Blue/Green deployment if switchover is complete
        if latest_deployment['Status'] == 'SWITCHOVER_COMPLETED':
            print(f"Deleting Blue/Green deployment: {latest_deployment['BlueGreenDeploymentIdentifier']}")
            rds.delete_blue_green_deployment(
                BlueGreenDeploymentIdentifier=latest_deployment['BlueGreenDeploymentIdentifier']
            )
            print(f"Deleted Blue/Green deployment: {latest_deployment['BlueGreenDeploymentIdentifier']}")
        
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Cleanup completed successfully"})
        }
        
    except Exception as e:
        print(f"Error during cleanup: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
