from pathlib import Path
from aws_cdk import (
    aws_lambda,
    core,
)
from aws_lambda_asset.zip_asset_code import ZipAssetCode

class AlexaConstruct(core.Construct):

    @property
    def function(self):
        return self._function

    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)
        work_dir = Path(__file__).parents[3]
        self._function = aws_lambda.Function(
            scope=self,
            id='alexacloud_skill',
            code=ZipAssetCode(work_dir=work_dir, include='src/lambdas/alexacloud_skill', file_name='.assets/alexacloud_skill.zip'),
            handler='lambdas.alexacloud_skill/handler',
            runtime=aws_lambda.Runtime.PYTHON_3_7
        )
