from app.settings.common import CommonSettings


def get_settings() -> CommonSettings:
    """
    Return an instance of the appropriate settings class
    based on the ENV environment variable. for now only one kind of settings
    """
    return CommonSettings()


settings = get_settings()
