from nano_banana_bot.config.env.base import EnvSettings


class ServerConfig(EnvSettings, env_prefix="SERVER_"):
    port: int
    host: str
    url: str

    def build_url(self, path: str):
        return f"{self.url}{path}"
