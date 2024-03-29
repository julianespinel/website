import click
import os
import toml
from enum import IntEnum

"""
This file is used to deploy the content generated by Pelican using
AWS S3 and CloudFront.

The entry point of this file is the funcion `deploy()`

How to deploy using this file? Run the following command:

```bash
python deploy.py -uv <major|minor|patch>
```

Where `-uv` stands for update-version and can take the following
possible values:

- `major`
- `minor`
- `patch`

The `-uv` parameter is used to determine what is the next version number.

For example:

Let's suppose we are in version `1.1.1`:

- If you run this file with `-uv major` then the version will be: `2.0.0`
- If you run this file with `-uv minor` then the version will be: `1.2.0`
- If you run this file with `-uv patch` then the version will be: `1.1.2`
"""

PUBLIC_FILE = 'public.toml'
SECRETS_FILE = 'secrets.toml'


class VersionPart(IntEnum):
    MAJOR = 0
    MINOR = 1
    PATCH = 2

    @staticmethod
    def fromstr(string):
        return VersionPart[string.upper()]


def __get_updated_version(current_version: str, part_to_increase: VersionPart) -> str:
    parts = current_version.split('.')

    new_version = ""
    for index, part in enumerate(parts):
        if index < part_to_increase:
            # Preserve all numbers before the part we want to increase
            new_version += f'{part}.'
        elif index == part_to_increase:
            # Increase the number of part we want
            number = int(part)
            increased_part = number + 1
            new_version += f'{increased_part}.'
        else:
            # Set to 0 all the parts after the part we want to increase
            new_version += '0.'

    # Remove last extra dot
    fixed_version = new_version[:-1]
    return fixed_version


def increase_version_patch(config: dict, part_to_increase: VersionPart) -> None:
    current_version = config['website']['version']
    print(f'current version: {current_version}')
    updated_version = __get_updated_version(current_version, part_to_increase)
    config['website']['version'] = updated_version
    print(f'updated version: {updated_version}')
    # Update config file version
    with open(PUBLIC_FILE, 'w') as config_file:
        toml.dump(config, config_file)


class AwsCredentials:
    def __init__(self, access_key: str, secret_key: str):
        self.access_key = access_key
        self.secret_key = secret_key

    def to_command(self):
        credentials = f'AWS_ACCESS_KEY_ID={self.access_key} AWS_SECRET_ACCESS_KEY={self.secret_key}'
        return credentials


def __get_aws_credentials(secrets: dict) -> AwsCredentials:
    access_key = secrets['aws']['access_key']
    secret_key = secrets['aws']['secret_key']
    return AwsCredentials(access_key, secret_key)


def sync_s3_bucket(credentials: AwsCredentials, source_path: str, bucket: str) -> None:
    command = f'{credentials.to_command()} aws s3 sync {source_path} s3://{bucket}'
    result = os.system(command)
    assert result == 0, f'The s3 sync was not successful, error code: {result}'


def invalidate_cloudfront_cache(credentials: AwsCredentials, cloudfront_distribution_id: str) -> None:
    command = f'{credentials.to_command()} aws cloudfront create-invalidation --distribution-id {cloudfront_distribution_id} --paths "/*"'
    result = os.system(command)
    assert result == 0, f'The cloudfront invalidation was not successful, error code: {result}'


def upload_to_s3(secrets: dict):
    source_path = 'output'  # Folder that contains the generated static content
    aws_credentials = __get_aws_credentials(secrets)

    bucket = secrets['aws']['s3_bucket']
    sync_s3_bucket(aws_credentials, source_path, bucket)

    cloudfront_distribution_id = secrets['aws']['cloudfront_distribution_id']
    invalidate_cloudfront_cache(aws_credentials, cloudfront_distribution_id)


@click.command()
@click.option('--update-version', '-uv', required=True,
              type=click.Choice(['major', 'minor', 'patch'],
                                case_sensitive=False),
              help='part of the version to update: major, minor, patch')
def deploy(update_version: str) -> None:
    os.system('make clean')  # clean generated files

    public = toml.load(PUBLIC_FILE)
    part_to_increase = VersionPart.fromstr(update_version)
    increase_version_patch(public, part_to_increase)

    os.system('make publish')  # regenerate files
    secrets = toml.load(SECRETS_FILE)
    upload_to_s3(secrets)


if __name__ == "__main__":
    deploy()
