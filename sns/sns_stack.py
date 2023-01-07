from aws_cdk import (
    Stack,
    aws_sns as sns,
    aws_iam as iam
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
                principals=[iam.AccountPrincipal("425039140189")],
                actions=["SNS:Subscribe"],
                resources=["*"]
            )
        )