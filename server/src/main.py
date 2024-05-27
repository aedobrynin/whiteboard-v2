import asyncio
import logging

from internal.server import WhiteBoardServer

if __name__ == '__main__':
    logging.basicConfig(
        level='INFO',
        format='%(asctime)s - %(levelname)s - %(message)s',
    )
    server = WhiteBoardServer()
    asyncio.run(server.serve())
