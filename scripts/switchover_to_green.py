import boto3
import json
from datetime import datetime

rds_client = boto3.client('rds')

def lambda_handler(event, context):
    try:
        # ✅ Get the latest Blue/Green deployment identifier
        deployments = rds_client.describe_blue_green_deployments()
        deployment_identifier = deployments['BlueGreenDeployments'][0]['BlueGreenDeploymentIdentifier']
        print(f"Found Deployment Identifier: {deployment_identifier}")

        # ✅ Initiate switchover to green environment
        switchover_response = rds_client.switchover_blue_green_deployment(
            BlueGreenDeploymentIdentifier=deployment_identifier
        )
        print("Switchover response received.")

        # ✅ Clean datetime format for JSON response
        if 'BlueGreenDeployment' in switchover_response:
            if 'CreateTime' in switchover_response['BlueGreenDeployment']:
                switchover_response['BlueGreenDeployment']['CreateTime'] = switchover_response['BlueGreenDeployment']['CreateTime'].isoformat()

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Switchover initiated successfully',
                'response': switchover_response
            })
        }

    except Exception as e:
        print(f"Error during switchover: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
