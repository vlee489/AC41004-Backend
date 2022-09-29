"""Loads Config"""
import toml


class Config:
    mongo_uri: str
    db_name: str
    redis_uri: str
    session_secret: str
    debug: bool

    @staticmethod
    def __get_key_or_default(config: dict, key_name: str, default_value):
        """
        Gets a value from env, if env have no value, will return the default value given
        :param config: TOML Config
        :param key_name: key name
        :param default_value: default value
        :return: key/default value
        """
        if not (return_value := config.get(key_name)):
            return_value = default_value
        return return_value

    def __init__(self, config_file: str = "config.toml"):
        self.__config = toml.load(config_file)
        self.mongo_uri = self.__config["mongoUri"]
        self.db_name = self.__get_key_or_default(self.__config, "db_name", "dev")
        self.redis_uri = self.__get_key_or_default(self.__config, "redis_uri", "redis://redis:6379/1")
        self.session_secret = self.__config["session_secret"]
        self.debug = self.__get_key_or_default(self.__config, "debug", False)

