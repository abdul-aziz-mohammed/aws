import boto3

def deregister_inactive_task_definitions(region_name):
    ecs = boto3.client('ecs', region_name=region_name)
    try:
        # List all task definitions
        paginator = ecs.get_paginator('list_task_definitions')
        for page in paginator.paginate(status='INACTIVE'):
            for task_def_arn in page['taskDefinitionArns']:
                # Deregister inactive task definitions
                ecs.deregister_task_definition(taskDefinition=task_def_arn)
                print(f"Deregistered {task_def_arn} in {region_name}")
    except Exception as e:
        print(f"Error in {region_name}: {e}")

def main():
    # Get list of all regions
    ec2 = boto3.client('ec2')
    regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]

    # Iterate over each region and deregister inactive task definitions
    for region in regions:
        print(f"Processing region: {region}")
        deregister_inactive_task_definitions(region)

if __name__ == "__main__":
    main()
