""" 
This script reads all the reviews in the Dynamo table and creates files in S3
for the Bedrock knowledge base data source
"""
import json
import os
import boto3

# Create a Boto3 clients for DynamoDB and S3
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
reviews_table = dynamodb.Table('CityReviews')

reviews = reviews_table.scan()['Items']
for review in reviews:
    city_name = review['CityName']
    review_content = review['ReviewContent']
    review_id = review['ReviewId']
    stars = review['Stars']
    metadata = {"metadataAttributes": {"City": city_name, "Stars": int(stars)}}

    file_name = f"{city_name}_{review_id}.txt"
    metadata_file_name = f"{city_name}_{review_id}.txt.metadata.json"

    # save the meta data and review files to the s3 bucket
    print(f"Saving {file_name} and metadata to S3")
    s3.put_object(
        Body=review_content,
        Bucket=os.getenv("KNOWLEDGE_BASE_BUCKET"),
        Key=file_name)
    s3.put_object(
        Body=json.dumps(metadata),
        Bucket=os.getenv("KNOWLEDGE_BASE_BUCKET"),
        Key=metadata_file_name)
