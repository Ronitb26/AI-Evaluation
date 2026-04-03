import logging
import os

def setup_logger():
    """
    Initializes the observability and telemetry logger.
    Outputs clean info to the console, and deep traces to outputs/evaluation.log.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    outputs_dir = os.path.join(base_dir, "..", "outputs")
    os.makedirs(outputs_dir, exist_ok=True)
    log_file = os.path.join(outputs_dir, "evaluation.log")
    logger = logging.getLogger("AIEvalFramework")
    
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        # 1. Console Handler (Keeps the terminal clean)
        c_handler = logging.StreamHandler()
        c_handler.setLevel(logging.INFO)
        c_format = logging.Formatter('%(message)s')
        c_handler.setFormatter(c_format)

        # 2. File Handler (Records the deep forensic trace)
        f_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        f_handler.setLevel(logging.DEBUG)
        f_format = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s')
        f_handler.setFormatter(f_format)

        # Attach handlers
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

    return logger

logger = setup_logger()