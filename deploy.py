import os
import boto3
import argparse
from datetime import datetime


def get_arguments():
    parser = argparse.ArgumentParser(
        description='Deployment tool')
    parser.add_argument('--source-directory',
                        help='Name of the local directory to deploy (with tailing /)',
                        required=True)
    parser.add_argument('--domain-name',
                        help='Domain name for deployment (without www prefix)',
                        required=True)
    parser.add_argument('--invalidate-file-names',
                        help='Comma separated list of files to invalidate after deployment',
                        required=True)
    return parser.parse_args()


def upload_files(bucket_name, local_source_dir, s3_dest_dir=''):
    print('************************')
    print('Uploading files to s3 bucket')
    print('************************')
    upload_file_tuples = []
    for (sourceDir, dirname, files) in os.walk(local_source_dir):
        for filename in files:
            local_path = os.path.join(sourceDir, filename)
            relative_path = os.path.relpath(local_path, local_source_dir)
            s3_path = os.path.join(s3_dest_dir, relative_path)
            upload_file_tuples.append((local_path, s3_path))

    s3 = boto3.resource('s3')

    for item in upload_file_tuples:
        print('uploading local file: {} to path: {} in bucket: {}'.format(item[0], item[1], bucket_name))
        s3.Object(bucket_name, item[1]).upload_file(item[0])


def invalidate_cloudfront_distribution(domain_name, invalidate_file_names):
    print('************************')
    print('Invalidating cloudfront distribution')
    print('************************')
    client = boto3.client('cloudfront')

    distributions = client.list_distributions(Marker='', MaxItems='100')
    invalidate_dist_ids = []
    for item in distributions['DistributionList']['Items']:
        for origin in item['Origins']['Items']:
            origin_domain_name = origin['DomainName']

            if origin_domain_name.startswith(domain_name) \
                or origin_domain_name.startswith('www.{}'.format(domain_name)):
                invalidate_dist_ids.append(item['Id'])

    unique_id = str(datetime.now().timestamp() * 1000)
    for item in invalidate_dist_ids:
        response = client.create_invalidation(
            DistributionId=item,
            InvalidationBatch={
                'Paths': {
                    'Quantity': len(invalidate_file_names),
                    'Items': invalidate_file_names
                },
                'CallerReference': unique_id
            }
        )
        print(response)


if __name__ == '__main__':
    args = get_arguments()

    os.system('aws s3 cp --recursive {} s3://www.{}'
              .format(args.source_directory, args.domain_name))

    files = args.invalidate_file_names.split(',')
    invalidate_cloudfront_distribution(args.domain_name, files)
