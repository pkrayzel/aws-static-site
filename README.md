# aws-static-site
AWS Cloudformation template for static site hosting with AWS S3, AWS CloudFront and AWS Route 53.

## Templates

### static_site.json
- Buckets (root and www) and public access policy for the www bucket.
- CloudFront Distributions for both buckets (root and www) and Route 53 record sets for these. 
