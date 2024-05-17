import asyncio
import tkinter
from threading import Thread

from async_tkinter_loop import async_handler, async_mainloop

from typing import Optional

from websockets.server import serve
from websockets import WebSocketServerProtocol

from helper import (
    AndroidKeycode,
    SendKeyAction,
    SwipeAction,
    TouchAction,
    WebSocketHelper,
)


async def socket_handler(websocket: WebSocketServerProtocol):
    print("WebSocket connected.")
    global global_helper
    try:
        global_helper = WebSocketHelper(websocket)
        while True:
            await global_helper.recv()

    except Exception as e:
        print(e)
    finally:
        print("Connection dropped.")
        if global_helper:
            await global_helper.close()
        global_helper = None


async def start_server():
    host = "localhost"
    port = 8765
    async with serve(socket_handler, host, port):
        print(f"WebSocket server started at ws://{host}:{port}")
        await asyncio.Future()


@async_handler
async def exec_show_message():
    if global_helper:
        await global_helper.message_show_message("message from python")
    else:
        print("Websocket not connected")


@async_handler
async def exec_get_controlled_device():
    if global_helper:
        res = await global_helper.message_get_controlled_device()
        print(res)
    else:
        print("Websocket not connected")


@async_handler
async def exec_send_key():
    if global_helper:
        await global_helper.message_send_key(
            SendKeyAction.Default, AndroidKeycode.AKEYCODE_HOME
        )
    else:
        print("Websocket not connected")


@async_handler
async def exec_touch():
    if global_helper:
        await global_helper.message_touch(TouchAction.Default, 0, (100, 100), 100)
    else:
        print("Websocket not connected")


@async_handler
async def exec_swipe():
    if global_helper:
        await global_helper.message_swipe(
            SwipeAction.Default, 0, ((100, 100), (500, 200), (500, 500)), 1000
        )
    else:
        print("Websocket not connected")


@async_handler
async def exec_shutdown():
    if global_helper:
        await global_helper.message_shutdown()
    else:
        print("Websocket not connected")


def gui():
    win = tkinter.Tk()
    win.wm_title("scrcpy-mask-rpc")
    tkinter.Button(text="showMessage", command=exec_show_message).pack(padx=20, pady=5)
    tkinter.Button(text="getControlledDevice", command=exec_get_controlled_device).pack(
        padx=20, pady=5
    )
    tkinter.Button(text="sendKey", command=exec_send_key).pack(padx=20, pady=5)
    tkinter.Button(text="touch", command=exec_touch).pack(padx=20, pady=5)
    tkinter.Button(text="swipe", command=exec_swipe).pack(padx=20, pady=5)
    tkinter.Button(text="shutdown", command=exec_shutdown).pack(padx=20, pady=5)
    async_mainloop(win)


def main():
    Thread(target=lambda: asyncio.run(start_server())).start()
    gui()


if __name__ == "__main__":
    global_helper: Optional[WebSocketHelper] = None
    main()
