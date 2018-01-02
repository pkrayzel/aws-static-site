# aws-static-site
AWS Cloudformation template for static site hosting with AWS S3, AWS CloudFront and AWS Route 53.
Also contains tool for deployment + CloudFront CDN invalidation.

## Templates
<strong>static_site.json</strong> which contains:
- Buckets (root and www) and public access policy for the www bucket.
- CloudFront Distributions for both buckets (root and www) and Route 53 record sets for these.

### Prerequisities:
- HostedZone created for given domain name in the AWS region
- ACM Certificate exists for the given domain in AWS Certificate Manager 

### Template parameters
- <strong>DomainName</strong> - name of the domain without leading www (eg. intervention.ninja)
- <strong>AcmCertificateArn</strong> - ARN of the certificate which will be used for CloudFront distribution and HTTPS

## Deployment tool
For easy deployment of your website into s3 you can use script <strong>deploy.py</strong>

### Prerequisities:
- You have to be logged into AWS in current terminal session - that means that following env. variables have to be set: 
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_SESSION_TOKEN

### Installation
```
virtualenv ~/ass -p python3
source ~/ass/bin/activate
pip install -r requirements.txt
```

### Run
``` 
python deploy.py --source-directory YOUR_SITE_DIR/ --domain-name yourdomain.com --invalidate-file-names /index.html,/error.html
```
 
