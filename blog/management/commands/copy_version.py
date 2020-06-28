from django.core.management.base import BaseCommand
import yaml


class Command(BaseCommand):
    help = 'Copy Docker image version to settings'

    def handle(self, *args, **options):
        key = 'DOCKER_IMAGE_VERSION'
        version = self.__get_current_image_version()
        new_line = f"{key} = '{version}'"
        file_name = 'settings/base.py'
        with open(file_name, 'r') as base_settings:
            new_lines = []
            lines = base_settings.readlines()
            line_exists = False
            for line in lines:
                if key in line:
                    line_exists = True
                    new_lines.append(new_line)
                else:
                    new_lines.append(line)
            if not line_exists:
                new_lines.append('\n')
                new_lines.append(new_line)
            # Add empty line by the end of the file.
            new_lines.append('\n')
        with open(file_name, 'w') as base_settings:
            base_settings.writelines(new_lines)
        self.stdout.write(
            self.style.SUCCESS(f'Docker image version exported: {version}')
        )

    def __get_current_image_version(self):
        with open('buildspec.yml', 'r') as buildspec:
            yml_dict = yaml.safe_load(buildspec)
            version = yml_dict.get('env').get('variables').get('IMAGE_VERSION')
            return version
