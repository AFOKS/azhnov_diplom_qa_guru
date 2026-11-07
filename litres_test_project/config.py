import os

from pydantic_settings import BaseSettings, SettingsConfigDict

CONTEXT = os.getenv('context', 'bstack')


class BstackConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    user_name: str
    access_key: str
    remote_browser_url: str = 'http://hub.browserstack.com/wd/hub'
    bstack_app_id: str
    device_name: str = 'Samsung Galaxy S22 Ultra'
    platform_version: str = '12.0'
    appium_version: str = '2.0.1'


class LocalConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env.local', extra='ignore')

    remote_browser_url: str = 'http://127.0.0.1:4723'
    app_path: str
    device_name: str = 'emulator-5554'
    platform_version: str = '12.0'


def load_config():
    return LocalConfig() if CONTEXT == 'local' else BstackConfig()