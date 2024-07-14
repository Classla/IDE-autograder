import logging
import sys

# Configure logging to write to stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:\t%(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)
