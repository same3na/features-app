import logging

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,  # Set the logging level to DEBUG
        format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
        handlers=[
            logging.StreamHandler()  # Stream logs to stdout (Docker captures stdout)
        ]
    )