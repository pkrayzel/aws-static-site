# aws-static-site
AWS Cloudformation template for static site hosting with AWS S3, AWS CloudFront and AWS Route 53.

## Templates

### static_site.json
- Buckets (root and www) and public access policy for the www bucket.

### static_site_dns_cdn.json

- CloudFront Distributions for both buckets (root and www) and Route 53 record sets for these. 

### static_site_all.json
- Contains the same resources as static_site.json and static_site_dns_cdn.json in one file.