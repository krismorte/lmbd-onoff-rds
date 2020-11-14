import boto3
import botocore
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)


rds_client = boto3.client('rds', region_name=os.environ['RDS_REGION'])

def lambda_handler(event, context):
    #CLUSTER
    cmd = os.environ['CMD']
    values = os.environ['TAG_VALUES'].split(",")
    db_cluster_info = rds_client.describe_db_clusters()

    for each_db in db_cluster_info['DBClusters']: 

        response = rds_client.list_tags_for_resource(
        ResourceName=each_db['DBClusterArn'])
        
        for tag_db in response['TagList']: 
            if tag_db['Key']==os.environ['TAG_KEY'] and tag_db['Value'] in values:
                print (each_db['DBClusterIdentifier'])
                try:
                    if cmd =='START':
                        response = rds_client.start_db_cluster(DBClusterIdentifier=each_db['DBClusterIdentifier'])
                    if cmd == 'STOP':
                        response = rds_client.stop_db_cluster(DBClusterIdentifier=each_db['DBClusterIdentifier'])
                except:
                    print ()

    #INSTANCE
    db_instance_info = rds_client.describe_db_instances()

    for each_db in db_instance_info['DBInstances']: 

        response = rds_client.list_tags_for_resource(
        ResourceName=each_db['DBInstanceArn'])
                
        for tag_db in response['TagList']: 
            if tag_db['Key']=="Environment" and tag_db['Value'] in values:
                print (each_db['DBInstanceIdentifier'])
                try:
                    if cmd =='START':
                        response = rds_client.start_db_instance(DBInstanceIdentifier=each_db['DBInstanceIdentifier'])
                    if cmd == 'STOP':
                        response = rds_client.stop_db_instance(DBInstanceIdentifier=each_db['DBInstanceIdentifier'])
                except:
                    print ()
