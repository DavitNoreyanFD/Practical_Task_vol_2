import websockets
import logging
import datetime
import datetime as dt
import asyncio
from pyngrok import ngrok
import constants
from moon import Moon


logging.basicConfig(level=logging.INFO)


async def message_for_sent(cur_time: datetime.datetime) -> str:
    """
    it is an asynchronous function designed to process the content of the request response
    """
    obj = Moon(cur_time)
    ra = obj.ra_dec_calculate()['ra']
    dec = obj.ra_dec_calculate()['dec']
    moon_ra_dec = f'moon ra is a {ra} -- moon dec is a {dec}'
    return moon_ra_dec


async def handle(ws: websockets.WebSocketServerProtocol, path) -> None:
    """
    this is an asynchronous function for processing a request that returns content on a request
    response periodically every 10 seconds
    """
    try:
        logging.info(f'{ws.remote_address} -- connected')
        while True:
            curr_time = dt.datetime.now()
            moon_ra_dec = await message_for_sent(curr_time)
            await ws.send(moon_ra_dec)
            for sec in range(constants.time_sleap):
                await ws.send('')
                await asyncio.sleep(1)
    except websockets.ConnectionClosedError:
        logging.info(f'{ws.remote_address} -- disconnected')
    except websockets.ConnectionClosedOK:
        logging.info(f'{ws.remote_address} -- disconnected, the client closed the browser')


def websocket_running_func(ip: str, prt: int) -> None:
    """
    this is a function for starting the server, during startup the function automatically
    makes the localhost public using pyngrok
    """
    try:
        ngrok_tunnel = ngrok.connect(prt)
        logging.info(f' ngrok tunnel is : {ngrok_tunnel.public_url}')
        start_server = websockets.serve(handle, ip, prt)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        logging.info('the server was down')
