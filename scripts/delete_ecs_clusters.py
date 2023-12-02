import boto3
import time

def stop_and_delete_services(ecs_client, cluster_name):
    # List all services in the cluster
    response = ecs_client.list_services(cluster=cluster_name)

    # Iterate through the services and stop them first
    for service_arn in response['serviceArns']:
        service_name = service_arn.split('/')[-1]

        # Stop the service
        print(f"Stopping service '{service_name}' in cluster '{cluster_name}'...")
        try:
            ecs_client.update_service(cluster=cluster_name, service=service_name, desiredCount=0)
            print(f"Service '{service_name}' in cluster '{cluster_name}' stopped successfully")
        except Exception as e:
            print(f"Error stopping service '{service_name}' in cluster '{cluster_name}': {e}")

    # Wait for services to stop
    print(f"Waiting for services in cluster '{cluster_name}' to stop...")
    waiter = ecs_client.get_waiter('services_inactive')
    waiter.wait(cluster=cluster_name, services=response['serviceArns'])

    # Now that all services are stopped, delete them
    for service_arn in response['serviceArns']:
        service_name = service_arn.split('/')[-1]

        # Delete the service
        print(f"Deleting service '{service_name}' in cluster '{cluster_name}'...")
        try:
            ecs_client.delete_service(cluster=cluster_name, service=service_name)
            print(f"Service '{service_name}' in cluster '{cluster_name}' deleted successfully")
        except Exception as e:
            print(f"Error deleting service '{service_name}' in cluster '{cluster_name}': {e}")

def main():
    # List all AWS regions
    ec2_client = boto3.client('ec2', region_name='us-east-1')
    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

    # Iterate through all regions
    for region in regions:
        print(f"Processing region: {region}")

        # Initialize ECS client for the current region
        ecs_client = boto3.client('ecs', region_name=region)

        # List all ECS clusters in the current region
        response = ecs_client.list_clusters()

        # Iterate through the clusters, stop and delete services, and then delete the cluster
        for cluster_arn in response['clusterArns']:
            cluster_name = cluster_arn.split('/')[-1]

            # Stop and delete services within the cluster
            stop_and_delete_services(ecs_client, cluster_name)

            # Delete the cluster
            print(f"Deleting ECS cluster '{cluster_name}' in {region}...")
            try:
                ecs_client.delete_cluster(cluster=cluster_name)
                print(f"Cluster '{cluster_name}' in {region} deleted successfully")
            except Exception as e:
                print(f"Error deleting cluster '{cluster_name}' in {region}: {e}")

    print("All ECS clusters deleted.")

if __name__ == "__main__":
    main()
