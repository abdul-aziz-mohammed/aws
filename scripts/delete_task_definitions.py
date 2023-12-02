import boto3

def delete_task_definitions_in_region(ecs_client):
    # Pagination might be needed if there are many task definitions
    paginator = ecs_client.get_paginator('list_task_definitions')
    
    for page in paginator.paginate():
        for task_definition_arn in page['taskDefinitionArns']:
            # Deregister each task definition
            ecs_client.deregister_task_definition(taskDefinition=task_definition_arn)
            print(f"Deregistered task definition: {task_definition_arn}")

def main():
    # Create an EC2 client to list all regions
    ec2_client = boto3.client('ec2', region_name='us-east-1')
    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

    for region in regions:
        print(f"Processing region: {region}")
        
        # Create an ECS client for the current region
        ecs_client = boto3.client('ecs', region_name=region)

        # Delete all task definitions in the current region
        delete_task_definitions_in_region(ecs_client)

    print("All task definitions deleted across all regions.")

if __name__ == "__main__":
    main()
