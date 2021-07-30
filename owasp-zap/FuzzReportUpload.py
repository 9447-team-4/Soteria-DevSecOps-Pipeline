import boto3
import logging
from botocore.exceptions import ClientError

s3 = boto3.resource('s3')


def main():
    if not check_bucket('soteriafuzzreport'):
        create_bucket('soteriafuzzreport', 'ap-southeast-2')

    data = open('report.html', 'rb')
    s3.Bucket('soteriafuzzreport').put_object(Key='report.html', Body=data)
    data.close()

    data = open('report.json', 'rb')
    s3.Bucket('soteriafuzzreport').put_object(Key='report.json', Body=data)
    data.close()

    return


def check_bucket(bucket_name: str):
    """Check if an S3 bucket exists in aws account
    :param bucket_name: Bucket to check for
    """
    for bucket in s3.buckets.all():
        if bucket.name == bucket_name:
            return True

    return False


def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True


if __name__ == "__main__":
    main()
