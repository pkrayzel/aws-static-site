# aws-static-site

AWS CloudFormation template for static site hosting with AWS S3, AWS CloudFront and AWS Route 53.

**static_site.json** contains following resources:
- AWS S3 Bucket (www.site.com) and public access policy for this bucket.
- AWS CloudFront Distribution for this bucket
- AWS Route 53 record sets for both www.site.com and site.com.
 
**Prerequisites:**
- Hosted Zone created for given domain name in the AWS Route 53 in region of your choice
- Private certificate created and verified for the given domain in AWS Certificate Manager in the same region

**Template parameters**
- **DomainName** - name of the domain without leading www (eg. site.com)
- **AcmCertificateArn** - ARN of the certificate which will be used for CloudFront distribution and HTTPS

**How to create all resources**

1. Log into AWS console
2. Select service AWS CloudFormation
3. Click on the **Create stack** button
4. Select **Upload a template to AWS**, choose **static_site.json** and press **Next**.
5. Put name of your stack (eg. **site-com-static-site**).
6. Fill in all the values for parameters.
7. Press **Next** on the **Options** page.
8. Click on the **Create** button. 

After a while (CloudFront distribution take ~10 minutes to create) you should see a new stack in the state **CREATE_COMPLETE**. 

**How to deploy the content of the website**

**Prerequisities**

AWS cli is installed and configured properly - see the [documentation](https://docs.aws.amazon.com/cli/latest/userguide/installing.html).

**Uploading content to AWS S3**

Given the following sample project path

```
src/website/index.html
src/website/style.css
src/website/...
```

From the directory **src** run following command: 

``` 
aws s3 sync website s3://www.site.com
```

**Invalidate CloudFront distribution cache**

``` 
aws cloudfront create-invalidation --distribution-id DISTRIBUTION_ID --paths "/*"
```
