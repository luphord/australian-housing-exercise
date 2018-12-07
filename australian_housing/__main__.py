import sys
import logging
from . import main

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logger = logging.getLogger(__name__)
    main(prog_name='python3 -m australian_housing')
