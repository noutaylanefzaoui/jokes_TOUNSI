import logging

def configure_logging() -> None:
    """Basic console logging for the app."""
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    handler.setFormatter(formatter)

    # Avoid adding multiple handlers if create_app is called more than once
    if not root_logger.handlers:
        root_logger.addHandler(handler)
