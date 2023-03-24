from src._base.settings import config


def get_prefix():
    return str(f"/{config.api_prefix}/v{int(config.project_version)}")
