import logging

logging.basicConfig(
    filename="market_mock.log", 
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)