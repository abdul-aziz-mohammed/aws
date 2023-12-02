import subprocess
import boto3
import time

def get_all_regions():
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
    return regions

def delete_task_definitions(region_name):
    ecs_client = boto3.client('ecs', region_name=region_name)

    for status in ['ACTIVE', 'INACTIVE']:
        paginator = ecs_client.get_paginator('list_task_definitions')
        for page in paginator.paginate(status=status):
            for task_def_arn in page['taskDefinitionArns']:
                subprocess.run(f"aws ecs deregister-task-definition --task-definition {task_def_arn} --region {region_name} --no-cli-pager", shell=True)
                print(f"Deregistered {task_def_arn}")
                subprocess.run(f"aws ecs delete-task-definitions --task-definitions {task_def_arn} --region {region_name} --no-cli-pager", shell=True)
                print(f"Deleted {task_def_arn}")
                time.sleep(1)

def main():
    regions = get_all_regions()
    for region in regions:
        print(f"Processing region: {region}")
        delete_task_definitions(region)

if __name__ == "__main__":
    main()
