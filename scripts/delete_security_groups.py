import boto3

def delete_security_groups(region_name):
    ec2 = boto3.client('ec2', region_name=region_name)
    try:
        # Describe all security groups
        response = ec2.describe_security_groups()
        for sg in response['SecurityGroups']:
            if sg['GroupName'] != 'default':  # Skip default security groups
                sg_id = sg['GroupId']
                print(f"Deleting security group {sg_id} in {region_name}")
                ec2.delete_security_group(GroupId=sg_id)
    except Exception as e:
        print(f"Error deleting security group in {region_name}: {e}")

def main():
    # Get list of all regions
    ec2 = boto3.client('ec2')
    regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]

    # Iterate over each region and delete security groups
    for region in regions:
        print(f"Processing region: {region}")
        delete_security_groups(region)

if __name__ == "__main__":
    main()
