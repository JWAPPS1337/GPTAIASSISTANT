import uvicorn
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("test_api.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("test_api")
logger.info("Starting test API server")

# Import error checking
try:
    from src.main import app
    logger.info("Successfully imported app from src.main")
except Exception as e:
    logger.error(f"Error importing app: {str(e)}")
    import traceback
    logger.error(f"Traceback: {traceback.format_exc()}")
    sys.exit(1)

if __name__ == "__main__":
    logger.info("Starting uvicorn server")
    try:
        uvicorn.run(app, host="127.0.0.1", port=8001, log_level="debug")
    except Exception as e:
        logger.error(f"Error running server: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}") 