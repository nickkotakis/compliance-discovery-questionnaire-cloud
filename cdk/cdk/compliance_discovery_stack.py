from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_apigateway as apigw,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    Duration,
    RemovalPolicy,
    CfnOutput,
)
from constructs import Construct
import os


class ComplianceDiscoveryStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB Table for Sessions
        sessions_table = dynamodb.Table(
            self, "SessionsTable",
            partition_key=dynamodb.Attribute(
                name="session_id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,  # Change to RETAIN for production
            point_in_time_recovery=True,
        )

        # Lambda Function for API with bundled dependencies
        api_lambda = lambda_.Function(
            self, "ApiFunction",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="lambda_handler.handler",
            code=lambda_.Code.from_asset("../backend/lambda_package"),
            environment={
                "SESSIONS_TABLE": sessions_table.table_name,
                "CORS_ORIGINS": "*",  # Will update after frontend deployment
            },
            timeout=Duration.seconds(30),
            memory_size=512,
        )

        # Grant Lambda permissions to DynamoDB
        sessions_table.grant_read_write_data(api_lambda)

        # API Gateway
        api = apigw.RestApi(
            self, "ComplianceDiscoveryApi",
            rest_api_name="Compliance Discovery API",
            description="API for Compliance Discovery Questionnaire",
            binary_media_types=[
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # Excel
                "application/pdf",  # PDF
                "application/octet-stream",  # Generic binary
            ],
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
                allow_headers=["Content-Type", "Authorization"],
            ),
        )

        # API Integration
        integration = apigw.LambdaIntegration(api_lambda)
        
        # Add proxy resource to handle all paths
        api.root.add_proxy(
            default_integration=integration,
            any_method=True,
        )

        # S3 Bucket for Frontend
        frontend_bucket = s3.Bucket(
            self, "FrontendBucket",
            public_read_access=False,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        # CloudFront Origin Access Identity
        oai = cloudfront.OriginAccessIdentity(
            self, "OAI",
            comment="OAI for Compliance Discovery Frontend"
        )

        frontend_bucket.grant_read(oai)

        # CloudFront Distribution
        distribution = cloudfront.Distribution(
            self, "FrontendDistribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(
                    frontend_bucket,
                    origin_access_identity=oai
                ),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD_OPTIONS,
                cached_methods=cloudfront.CachedMethods.CACHE_GET_HEAD_OPTIONS,
            ),
            default_root_object="index.html",
            error_responses=[
                cloudfront.ErrorResponse(
                    http_status=404,
                    response_http_status=200,
                    response_page_path="/index.html",
                ),
                cloudfront.ErrorResponse(
                    http_status=403,
                    response_http_status=200,
                    response_page_path="/index.html",
                ),
            ],
        )

        # Deploy Frontend (will need to build first)
        # s3deploy.BucketDeployment(
        #     self, "DeployFrontend",
        #     sources=[s3deploy.Source.asset("../frontend/dist")],
        #     destination_bucket=frontend_bucket,
        #     distribution=distribution,
        #     distribution_paths=["/*"],
        # )

        # Outputs
        CfnOutput(
            self, "ApiUrl",
            value=api.url,
            description="API Gateway URL",
            export_name="ComplianceDiscoveryApiUrl"
        )

        CfnOutput(
            self, "FrontendUrl",
            value=f"https://{distribution.distribution_domain_name}",
            description="CloudFront Distribution URL",
            export_name="ComplianceDiscoveryFrontendUrl"
        )

        CfnOutput(
            self, "FrontendBucketName",
            value=frontend_bucket.bucket_name,
            description="S3 Bucket for Frontend",
            export_name="ComplianceDiscoveryFrontendBucket"
        )

        CfnOutput(
            self, "SessionsTableName",
            value=sessions_table.table_name,
            description="DynamoDB Sessions Table",
            export_name="ComplianceDiscoverySessionsTable"
        )
