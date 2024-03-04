from logging import WARNING

import uvicorn

from src.presentation.api.cfg import api_settings


if __name__ == "__main__":
    # TODO: use logger
    print("Server Start...")
    uvicorn.run(
                app="src.presentation.api.main:app",
                host=api_settings.HOST,
                port=api_settings.PORT,
                log_level=WARNING,
                )