import os
import platform
import zipfile
from pathlib import Path

import docker
import pytest
import requests

from cdk_stack.aws_lambda_asset import zip_asset_code
from cdk_stack.aws_lambda_asset.zip_asset_code import LambdaPackaging, ZipAssetCode


def prepare_workspace(path: Path) -> Path:
    # Create module dir
    module_dir = (path / 'productfolder')
    module_dir.mkdir()

    # Prepare a sample requirements.txt
    (path / module_dir / 'requirements.txt').write_text(
        """boto3>=1.9
         """)

    # Prepare a sample lambda.py
    (path / module_dir / 'lambda.py').write_text(
        """import json
           def handler(event, context):
               print('request: {}'.format(json.dumps(event)))
               return {
                   'statusCode': 200,
                   'headers': {
                       'Content-Type': 'text/plain'
                   },
                   'body': 'Hello, CDK! You have hit {}\n'.format(event['path'])
               }
         """)

    return module_dir


def test_packaging_linux(tmp_path, monkeypatch):
    def linux() -> bool:
        return True

    monkeypatch.setattr(zip_asset_code, 'is_linux', linux)
    asset = LambdaPackaging(include_path=(prepare_workspace(tmp_path)), work_dir=tmp_path, out_file='asset.zip').package()

    assert ['bin', 'dateutil', 'urllib3'] == sorted(next(os.walk(str(tmp_path / '.build')))[1])
    assert 'lambda.py' in next(os.walk(str(tmp_path / '.build')))[2]
    assert asset.exists()
    assert asset.is_file()
    zipfile.ZipFile(asset)


@pytest.mark.skipif(platform.system().lower() == 'linux', reason="Requires Docker daemon running (or docker-in-docker)")
def test_packaging_not_linux(tmp_path, monkeypatch):
    def not_linux() -> bool:
        return False

    monkeypatch.setattr(zip_asset_code, 'is_linux', not_linux)
    asset = LambdaPackaging(include_path=(prepare_workspace(tmp_path)), work_dir=tmp_path, out_file='asset.zip').package()

    assert ['bin', 'dateutil', 'urllib3'] == sorted(next(os.walk(str(tmp_path / '.build')))[1])
    assert 'lambda.py' in next(os.walk(str(tmp_path / '.build')))[2]
    assert asset.exists()
    assert asset.is_file()


def test_fails_without_docker(tmp_path, monkeypatch):
    def not_linux() -> bool:
        return False

    def from_env():
        raise requests.exceptions.ConnectionError('Can not connect to Docker')

    monkeypatch.setattr(zip_asset_code, 'is_linux', not_linux)
    monkeypatch.setattr(docker, 'from_env', from_env)

    with pytest.raises(Exception) as ex:
        LambdaPackaging(include_path=(prepare_workspace(tmp_path)), work_dir=tmp_path, out_file='asset.zip').package()
    assert 'Could not connect to Docker daemon.' in str(ex.value)


def test_build_error(tmp_path, monkeypatch):
    def prepare_build():
        raise requests.exceptions.ConnectionError('Can not connect to Docker')

    monkeypatch.setattr(LambdaPackaging, '_prepare_build', prepare_build)

    with pytest.raises(Exception) as ex:
        LambdaPackaging(include_path=(prepare_workspace(tmp_path)), work_dir=tmp_path, out_file='asset.zip').package()
    assert 'Error during build.' in str(ex.value)


def test_linux_detection(monkeypatch):
    def linux() -> str:
        return 'linux'

    def linux2() -> str:
        return 'linux2'

    def mac() -> str:
        return 'Mac'

    def osx() -> str:
        return 'darwin'

    def windows() -> str:
        return 'win32'

    monkeypatch.setattr(platform, 'system', linux)
    assert zip_asset_code.is_linux()

    monkeypatch.setattr(platform, 'system', linux2)
    assert not zip_asset_code.is_linux()

    monkeypatch.setattr(platform, 'system', mac)
    assert not zip_asset_code.is_linux()

    monkeypatch.setattr(platform, 'system', osx)
    assert not zip_asset_code.is_linux()

    monkeypatch.setattr(platform, 'system', windows)
    assert not zip_asset_code.is_linux()


def test_zip_asset_code(tmp_path, monkeypatch):
    def linux() -> bool:
        return True

    monkeypatch.setattr(zip_asset_code, 'is_linux', linux)
    asset_code = ZipAssetCode(work_dir=tmp_path, include=(prepare_workspace(tmp_path)), file_name='asset.zip')

    assert not asset_code.is_inline
    assert asset_code.path.endswith('/asset.zip')
