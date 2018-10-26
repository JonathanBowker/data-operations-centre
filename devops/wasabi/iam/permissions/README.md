Specifying Permissions in a Policy
Amazon S3 defines a set of permissions that you can specify in a policy. These are keywords, each of which maps to specific Amazon S3 operations (see Operations on Buckets, and Operations on Objects in the Amazon Simple Storage Service API Reference).

## Topics

⋅Permissions for Object Operations
⋅Permissions Related to Bucket Operations
⋅Permissions Related to Bucket Subresource Operations
⋅Permissions for Object Operations

This section provides a list of the permissions for object operations that you can specify in a policy.

| Amazon S3 | Permissions for Object Operations |
| -- | -- |
| Permissions |	Amazon S3 Operations|
| s3:AbortMultipartUpload |	Abort Multipart Upload |
| s3:DeleteObject | DELETE Object|
| s3:DeleteObjectTagging | DELETE Object tagging |
| s3:DeleteObjectVersion | DELETE Object (a Specific Version of the Object) |
| s3:DeleteObjectVersionTagging | DELETE Object tagging (for a Specific Version of the Object)|
| s3:GetObject | GET Object, HEAD Object, SELECT Object Content. When you grant this permission on a version-enabled bucket, you always get the latest version data.|
| s3:GetObjectAcl | GET Object ACL | 
| s3:GetObjectTagging | GET Object tagging | 
| s3:GetObjectTorrent |	GET Object torrent | 
| s3:GetObjectVersion | GET Object, HEAD Object. To grant permission for version-specific object data, you must grant this permission. That is, when you specify version number when making any of these requests, you need this Amazon S3 permission. | 
| s3:GetObjectVersionAcl | GET ACL (for a Specific Version of the Object) | 
| s3:GetObjectVersionTagging  | GET Object tagging (for a Specific Version of the Object) | 
| s3:GetObjectVersionTorrent | GET Object Torrent versioning | 
| s3:ListMultipartUploadParts | List Parts | 
| s3:PutObject | PUT Object, POST Object, Initiate Multipart Upload, Upload Part, Complete Multipart Upload, PUT Object - Copy | 
| s3:PutObjectAcl | PUT Object ACL | 
| s3:PutObjectTagging | PUT Object tagging | 
| s3:PutObjectVersionAcl | PUT Object ACL (for a Specific Version of the Object) |
| s3:PutObjectVersionTagging | PUT Object tagging (for a Specific Version of the Object) |
| s3:RestoreObject | POST Object restore |

The following example bucket policy grants the s3:PutObject and the s3:PutObjectAcl permissions to a user (Dave). If you remove the Principal element, you can attach the policy to a user. These are object operations, and accordingly the relative-id portion of the Resource ARN identifies objects (examplebucket/*). For more information, see Specifying Resources in a Policy.

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "statement1",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::AccountB-ID:user/Dave"
            },
            "Action":   ["s3:PutObject","s3:PutObjectAcl"],
            "Resource": "arn:aws:s3:::examplebucket/*"
        }
    ]
}
You can use a wildcard to grant permission for all Amazon S3 actions.

"Action":   "*"
Permissions Related to Bucket Operations
This section provides a list of the permissions related to bucket operations that you can specify in a policy.

## Amazon S3 Permissions Related to Bucket Operations

| Permission Keywords | Amazon S3 Operation(s) Covered |
| -- | -- |
| s3:CreateBucket | PUT Bucket |
| s3:DeleteBucket | DELETE Bucket |
| s3:ListBucket | GET Bucket (List Objects), HEAD Bucket |
| s3:ListBucketVersions | GET Bucket Object versions |
| s3:ListAllMyBuckets | GET Service |
| s3:ListBucketMultipartUploads | List Multipart Uploads |

The following example user policy grants the s3:CreateBucket, s3:ListAllMyBuckets, and the s3:GetBucketLocation permissions to a user. Note that for all these permissions, you set the relative-id part of the Resource ARN to "*". For all other bucket actions, you must specify a bucket name. For more information, see Specifying Resources in a Policy.

{
   "Version":"2012-10-17",
   "Statement":[
      {
         "Sid":"statement1",
         "Effect":"Allow",
         "Action":[
            "s3:CreateBucket", "s3:ListAllMyBuckets", "s3:GetBucketLocation"  
         ],
         "Resource":[
            "arn:aws:s3:::*"
         ]
       }
    ]
}
If your user is going to use the console to view buckets and see the contents of any of these buckets, the user must have the s3:ListAllMyBuckets and s3:GetBucketLocation permissions. For an example, see "Policy for Console Access" at Writing IAM Policies: How to Grant Access to an Amazon S3 Bucket.

## Permissions Related to Bucket Subresource Operations
This section provides a list of the permissions related to bucket subresource operations that you can specify in a policy.

Amazon S3 Permissions Related to Bucket Subresource Operations

| Permission Keywords | Amazon S3 Operation(s) Covered |
| -- | -- |
| s3:DeleteBucketPolicy	| DELETE Bucket policy |
| s3:DeleteBucketWebsite	| DELETE Bucket website |
| s3:GetAccelerateConfiguration	| GET Bucket accelerate |
| s3:GetAnalyticsConfiguration	| GET Bucket analytics, List Bucket Analytics Configurations |
| s3:GetBucketAcl | GET Bucket acl |
| s3:GetBucketCORS | GET Bucket cors |
| s3:GetBucketLocation | GET Bucket location |
| s3:GetBucketLogging | GET Bucket logging |
| s3:GetBucketNotification | GET Bucket notification |
| s3:GetBucketPolicy | GET Bucket policy |
| s3:GetBucketRequestPayment | GET Bucket requestPayment |
| s3:GetBucketTagging | GET Bucket tagging |
| s3:GetBucketVersioning | GET Bucket versioning |
| s3:GetBucketWebsite | GET Bucket website |
| s3:GetEncryptionConfiguration | GET Bucket encryption |
| s3:GetInventoryConfiguration | GET Bucket inventory, List Bucket Inventory Configurations |
| s3:GetLifecycleConfiguration | GET Bucket lifecycle |
| s3:GetMetricsConfiguration | GET Bucket metrics, List Bucket Metrics Configurations |
| s3:GetReplicationConfiguration | GET Bucket replication |
| s3:PutAccelerateConfiguration | PUT Bucket accelerate |
| s3:PutAnalyticsConfiguration | PUT Bucket analytics, DELETE Bucket analytics |
| s3:PutBucketAcl | PUT Bucket acl |
| s3:PutBucketCORS | PUT Bucket cors, DELETE Bucket cors |
| s3:PutBucketLogging | PUT Bucket logging |
| s3:PutBucketNotification | PUT Bucket notification |
| s3:PutBucketPolicy | PUT Bucket policy |
| s3:PutBucketRequestPayment | PUT Bucket requestPayment |
| s3:PutBucketTagging | DELETE Bucket tagging, PUT Bucket tagging |
| s3:PutBucketVersioning | PUT Bucket versioning |
| s3:PutBucketWebsite | PUT Bucket website |
| s3:PutEncryptionConfiguration | PUT Bucket encryption, DELETE Bucket encryption |
| s3:PutInventoryConfiguration | PUT Bucket inventory, DELETE Bucket inventory |
| s3:PutLifecycleConfiguration | PUT Bucket lifecycle, DELETE Bucket lifecycle |
| s3:PutMetricsConfiguration | PUT Bucket metrics, DELETE Bucket metrics |
| s3:PutReplicationConfiguration | PUT Bucket replication, DELETE Bucket replication |

The following user policy grants the s3:GetBucketAcl permission on the examplebucket bucket to user Dave.

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "statement1",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::Account-ID:user/Dave"
      },
      "Action": [
        "s3:GetObjectVersion",
        "s3:GetBucketAcl"
      ],
      "Resource": "arn:aws:s3:::examplebucket"
    }
  ]
}
You can delete objects either by explicitly calling the DELETE Object API or by configuring its lifecycle (see Object Lifecycle Management) so that Amazon S3 can remove the objects when their lifetime expires. To explicitly block users or accounts from deleting objects, you must explicitly deny them s3:DeleteObject, s3:DeleteObjectVersion, and s3:PutLifecycleConfiguration permissions. By default, users have no permissions. But as you create users, add users to groups, and grant them permissions, it is possible for users to get certain permissions that you did not intend to give. That is where you can use explicit deny, which supersedes all other permissions a user might have and denies the user permissions for specific actions.
