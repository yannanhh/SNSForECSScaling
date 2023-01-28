from aws_cdk import (
    Stack,
    aws_sns as sns,
    aws_iam as iam,
    aws_ec2 as ec2
)
from constructs import Construct

class SnsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        topic = sns.Topic(
            self,
            "SnsTopic",
            display_name="ScaleECSTopic",
        )

        topic.add_to_resource_policy(
            iam.PolicyStatement(
                principals=[iam.AccountPrincipal("116266104059")],
                actions=["SNS:Subscribe"],
                resources=["*"]
            )
        )

        vpc = ec2.Vpc(self, "VpcForCrossAccessAPIGW")

        security_group = ec2.SecurityGroup(self, "SG",
                                           vpc=vpc,
                                           security_group_name="SGForCrossAccessAPIGW"
                                           )

        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22))
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(443))

        # VPC endpoint to access private API Gateway in antoher account.
        vpc.add_interface_endpoint(
            "VPCEForCrossAccessAPIGW",
            service=ec2.InterfaceVpcEndpointService(
                name="com.amazonaws.us-west-2.execute-api"),
            security_groups=[security_group],
            private_dns_enabled=True
        )
