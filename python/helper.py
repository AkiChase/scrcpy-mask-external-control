import asyncio
import json
import time
from asyncio import Future
from enum import Enum
from typing import Dict, Tuple
from websockets import WebSocketServerProtocol


class SendKeyAction(Enum):
    Default = 0
    Down = 1
    Up = 2


class AndroidKeycode(Enum):
    AKEYCODE_UNKNOWN = 0
    AKEYCODE_SOFT_LEFT = 1
    AKEYCODE_SOFT_RIGHT = 2
    AKEYCODE_HOME = 3
    AKEYCODE_BACK = 4
    AKEYCODE_CALL = 5
    AKEYCODE_ENDCALL = 6
    AKEYCODE_0 = 7
    AKEYCODE_1 = 8
    AKEYCODE_2 = 9
    AKEYCODE_3 = 10
    AKEYCODE_4 = 11
    AKEYCODE_5 = 12
    AKEYCODE_6 = 13
    AKEYCODE_7 = 14
    AKEYCODE_8 = 15
    AKEYCODE_9 = 16
    AKEYCODE_STAR = 17
    AKEYCODE_POUND = 18
    AKEYCODE_DPAD_UP = 19
    AKEYCODE_DPAD_DOWN = 20
    AKEYCODE_DPAD_LEFT = 21
    AKEYCODE_DPAD_RIGHT = 22
    AKEYCODE_DPAD_CENTER = 23
    AKEYCODE_VOLUME_UP = 24
    AKEYCODE_VOLUME_DOWN = 25
    AKEYCODE_POWER = 26
    AKEYCODE_CAMERA = 27
    AKEYCODE_CLEAR = 28
    AKEYCODE_A = 29
    AKEYCODE_B = 30
    AKEYCODE_C = 31
    AKEYCODE_D = 32
    AKEYCODE_E = 33
    AKEYCODE_F = 34
    AKEYCODE_G = 35
    AKEYCODE_H = 36
    AKEYCODE_I = 37
    AKEYCODE_J = 38
    AKEYCODE_K = 39
    AKEYCODE_L = 40
    AKEYCODE_M = 41
    AKEYCODE_N = 42
    AKEYCODE_O = 43
    AKEYCODE_P = 44
    AKEYCODE_Q = 45
    AKEYCODE_R = 46
    AKEYCODE_S = 47
    AKEYCODE_T = 48
    AKEYCODE_U = 49
    AKEYCODE_V = 50
    AKEYCODE_W = 51
    AKEYCODE_X = 52
    AKEYCODE_Y = 53
    AKEYCODE_Z = 54
    AKEYCODE_COMMA = 55
    AKEYCODE_PERIOD = 56
    AKEYCODE_ALT_LEFT = 57
    AKEYCODE_ALT_RIGHT = 58
    AKEYCODE_SHIFT_LEFT = 59
    AKEYCODE_SHIFT_RIGHT = 60
    AKEYCODE_TAB = 61
    AKEYCODE_SPACE = 62
    AKEYCODE_SYM = 63
    AKEYCODE_EXPLORER = 64
    AKEYCODE_ENVELOPE = 65
    AKEYCODE_ENTER = 66
    AKEYCODE_DEL = 67
    AKEYCODE_GRAVE = 68
    AKEYCODE_MINUS = 69
    AKEYCODE_EQUALS = 70
    AKEYCODE_LEFT_BRACKET = 71
    AKEYCODE_RIGHT_BRACKET = 72
    AKEYCODE_BACKSLASH = 73
    AKEYCODE_SEMICOLON = 74
    AKEYCODE_APOSTROPHE = 75
    AKEYCODE_SLASH = 76
    AKEYCODE_AT = 77
    AKEYCODE_NUM = 78
    AKEYCODE_HEADSETHOOK = 79
    AKEYCODE_FOCUS = 80
    AKEYCODE_PLUS = 81
    AKEYCODE_MENU = 82
    AKEYCODE_NOTIFICATION = 83
    AKEYCODE_SEARCH = 84
    AKEYCODE_MEDIA_PLAY_PAUSE = 85
    AKEYCODE_MEDIA_STOP = 86
    AKEYCODE_MEDIA_NEXT = 87
    AKEYCODE_MEDIA_PREVIOUS = 88
    AKEYCODE_MEDIA_REWIND = 89
    AKEYCODE_MEDIA_FAST_FORWARD = 90
    AKEYCODE_MUTE = 91
    AKEYCODE_PAGE_UP = 92
    AKEYCODE_PAGE_DOWN = 93
    AKEYCODE_PICTSYMBOLS = 94
    AKEYCODE_SWITCH_CHARSET = 95
    AKEYCODE_BUTTON_A = 96
    AKEYCODE_BUTTON_B = 97
    AKEYCODE_BUTTON_C = 98
    AKEYCODE_BUTTON_X = 99
    AKEYCODE_BUTTON_Y = 100
    AKEYCODE_BUTTON_Z = 101
    AKEYCODE_BUTTON_L1 = 102
    AKEYCODE_BUTTON_R1 = 103
    AKEYCODE_BUTTON_L2 = 104
    AKEYCODE_BUTTON_R2 = 105
    AKEYCODE_BUTTON_THUMBL = 106
    AKEYCODE_BUTTON_THUMBR = 107
    AKEYCODE_BUTTON_START = 108
    AKEYCODE_BUTTON_SELECT = 109
    AKEYCODE_BUTTON_MODE = 110
    AKEYCODE_ESCAPE = 111
    AKEYCODE_FORWARD_DEL = 112
    AKEYCODE_CTRL_LEFT = 113
    AKEYCODE_CTRL_RIGHT = 114
    AKEYCODE_CAPS_LOCK = 115
    AKEYCODE_SCROLL_LOCK = 116
    AKEYCODE_META_LEFT = 117
    AKEYCODE_META_RIGHT = 118
    AKEYCODE_FUNCTION = 119
    AKEYCODE_SYSRQ = 120
    AKEYCODE_BREAK = 121
    AKEYCODE_MOVE_HOME = 122
    AKEYCODE_MOVE_END = 123
    AKEYCODE_INSERT = 124
    AKEYCODE_FORWARD = 125
    AKEYCODE_MEDIA_PLAY = 126
    AKEYCODE_MEDIA_PAUSE = 127
    AKEYCODE_MEDIA_CLOSE = 128
    AKEYCODE_MEDIA_EJECT = 129
    AKEYCODE_MEDIA_RECORD = 130
    AKEYCODE_F1 = 131
    AKEYCODE_F2 = 132
    AKEYCODE_F3 = 133
    AKEYCODE_F4 = 134
    AKEYCODE_F5 = 135
    AKEYCODE_F6 = 136
    AKEYCODE_F7 = 137
    AKEYCODE_F8 = 138
    AKEYCODE_F9 = 139
    AKEYCODE_F10 = 140
    AKEYCODE_F11 = 141
    AKEYCODE_F12 = 142
    AKEYCODE_NUM_LOCK = 143
    AKEYCODE_NUMPAD_0 = 144
    AKEYCODE_NUMPAD_1 = 145
    AKEYCODE_NUMPAD_2 = 146
    AKEYCODE_NUMPAD_3 = 147
    AKEYCODE_NUMPAD_4 = 148
    AKEYCODE_NUMPAD_5 = 149
    AKEYCODE_NUMPAD_6 = 150
    AKEYCODE_NUMPAD_7 = 151
    AKEYCODE_NUMPAD_8 = 152
    AKEYCODE_NUMPAD_9 = 153
    AKEYCODE_NUMPAD_DIVIDE = 154
    AKEYCODE_NUMPAD_MULTIPLY = 155
    AKEYCODE_NUMPAD_SUBTRACT = 156
    AKEYCODE_NUMPAD_ADD = 157
    AKEYCODE_NUMPAD_DOT = 158
    AKEYCODE_NUMPAD_COMMA = 159
    AKEYCODE_NUMPAD_ENTER = 160
    AKEYCODE_NUMPAD_EQUALS = 161
    AKEYCODE_NUMPAD_LEFT_PAREN = 162
    AKEYCODE_NUMPAD_RIGHT_PAREN = 163
    AKEYCODE_VOLUME_MUTE = 164
    AKEYCODE_INFO = 165
    AKEYCODE_CHANNEL_UP = 166
    AKEYCODE_CHANNEL_DOWN = 167
    AKEYCODE_ZOOM_IN = 168
    AKEYCODE_ZOOM_OUT = 169
    AKEYCODE_TV = 170
    AKEYCODE_WINDOW = 171
    AKEYCODE_GUIDE = 172
    AKEYCODE_DVR = 173
    AKEYCODE_BOOKMARK = 174
    AKEYCODE_CAPTIONS = 175
    AKEYCODE_SETTINGS = 176
    AKEYCODE_TV_POWER = 177
    AKEYCODE_TV_INPUT = 178
    AKEYCODE_STB_POWER = 179
    AKEYCODE_STB_INPUT = 180
    AKEYCODE_AVR_POWER = 181
    AKEYCODE_AVR_INPUT = 182
    AKEYCODE_PROG_RED = 183
    AKEYCODE_PROG_GREEN = 184
    AKEYCODE_PROG_YELLOW = 185
    AKEYCODE_PROG_BLUE = 186
    AKEYCODE_APP_SWITCH = 187
    AKEYCODE_BUTTON_1 = 188
    AKEYCODE_BUTTON_2 = 189
    AKEYCODE_BUTTON_3 = 190
    AKEYCODE_BUTTON_4 = 191
    AKEYCODE_BUTTON_5 = 192
    AKEYCODE_BUTTON_6 = 193
    AKEYCODE_BUTTON_7 = 194
    AKEYCODE_BUTTON_8 = 195
    AKEYCODE_BUTTON_9 = 196
    AKEYCODE_BUTTON_10 = 197
    AKEYCODE_BUTTON_11 = 198
    AKEYCODE_BUTTON_12 = 199
    AKEYCODE_BUTTON_13 = 200
    AKEYCODE_BUTTON_14 = 201
    AKEYCODE_BUTTON_15 = 202
    AKEYCODE_BUTTON_16 = 203
    AKEYCODE_LANGUAGE_SWITCH = 204
    AKEYCODE_MANNER_MODE = 205
    AKEYCODE_3D_MODE = 206
    AKEYCODE_CONTACTS = 207
    AKEYCODE_CALENDAR = 208
    AKEYCODE_MUSIC = 209
    AKEYCODE_CALCULATOR = 210
    AKEYCODE_ZENKAKU_HANKAKU = 211
    AKEYCODE_EISU = 212
    AKEYCODE_MUHENKAN = 213
    AKEYCODE_HENKAN = 214
    AKEYCODE_KATAKANA_HIRAGANA = 215
    AKEYCODE_YEN = 216
    AKEYCODE_RO = 217
    AKEYCODE_KANA = 218
    AKEYCODE_ASSIST = 219
    AKEYCODE_BRIGHTNESS_DOWN = 220
    AKEYCODE_BRIGHTNESS_UP = 221
    AKEYCODE_MEDIA_AUDIO_TRACK = 222
    AKEYCODE_SLEEP = 223
    AKEYCODE_WAKEUP = 224
    AKEYCODE_PAIRING = 225
    AKEYCODE_MEDIA_TOP_MENU = 226
    AKEYCODE_11 = 227
    AKEYCODE_12 = 228
    AKEYCODE_LAST_CHANNEL = 229
    AKEYCODE_TV_DATA_SERVICE = 230
    AKEYCODE_VOICE_ASSIST = 231
    AKEYCODE_TV_RADIO_SERVICE = 232
    AKEYCODE_TV_TELETEXT = 233
    AKEYCODE_TV_NUMBER_ENTRY = 234
    AKEYCODE_TV_TERRESTRIAL_ANALOG = 235
    AKEYCODE_TV_TERRESTRIAL_DIGITAL = 236
    AKEYCODE_TV_SATELLITE = 237
    AKEYCODE_TV_SATELLITE_BS = 238
    AKEYCODE_TV_SATELLITE_CS = 239
    AKEYCODE_TV_SATELLITE_SERVICE = 240
    AKEYCODE_TV_NETWORK = 241
    AKEYCODE_TV_ANTENNA_CABLE = 242
    AKEYCODE_TV_INPUT_HDMI_1 = 243
    AKEYCODE_TV_INPUT_HDMI_2 = 244
    AKEYCODE_TV_INPUT_HDMI_3 = 245
    AKEYCODE_TV_INPUT_HDMI_4 = 246
    AKEYCODE_TV_INPUT_COMPOSITE_1 = 247
    AKEYCODE_TV_INPUT_COMPOSITE_2 = 248
    AKEYCODE_TV_INPUT_COMPONENT_1 = 249
    AKEYCODE_TV_INPUT_COMPONENT_2 = 250
    AKEYCODE_TV_INPUT_VGA_1 = 251
    AKEYCODE_TV_AUDIO_DESCRIPTION = 252
    AKEYCODE_TV_AUDIO_DESCRIPTION_MIX_UP = 253
    AKEYCODE_TV_AUDIO_DESCRIPTION_MIX_DOWN = 254
    AKEYCODE_TV_ZOOM_MODE = 255
    AKEYCODE_TV_CONTENTS_MENU = 256
    AKEYCODE_TV_MEDIA_CONTEXT_MENU = 257
    AKEYCODE_TV_TIMER_PROGRAMMING = 258
    AKEYCODE_HELP = (259,)
    AKEYCODE_NAVIGATE_PREVIOUS = (260,)
    AKEYCODE_NAVIGATE_NEXT = (261,)
    AKEYCODE_NAVIGATE_IN = (262,)
    AKEYCODE_NAVIGATE_OUT = 263
    AKEYCODE_STEM_PRIMARY = 264
    AKEYCODE_STEM_1 = 265
    AKEYCODE_STEM_2 = 266
    AKEYCODE_STEM_3 = 267
    AKEYCODE_DPAD_UP_LEFT = 268
    AKEYCODE_DPAD_DOWN_LEFT = 269
    AKEYCODE_DPAD_UP_RIGHT = 270
    AKEYCODE_DPAD_DOWN_RIGHT = 271
    AKEYCODE_MEDIA_SKIP_FORWARD = 272
    AKEYCODE_MEDIA_SKIP_BACKWARD = 273
    AKEYCODE_MEDIA_STEP_FORWARD = 274
    AKEYCODE_MEDIA_STEP_BACKWARD = 275
    AKEYCODE_SOFT_SLEEP = 276
    AKEYCODE_CUT = 277
    AKEYCODE_COPY = 278
    AKEYCODE_PASTE = 279
    AKEYCODE_SYSTEM_NAVIGATION_UP = 280
    AKEYCODE_SYSTEM_NAVIGATION_DOWN = 281
    AKEYCODE_SYSTEM_NAVIGATION_LEFT = 282
    AKEYCODE_SYSTEM_NAVIGATION_RIGHT = 283
    AKEYCODE_ALL_APPS = 284


class AndroidMetastate(Enum):
    AMETA_NONE = 0
    AMETA_ALT_ON = 0x02
    AMETA_ALT_LEFT_ON = 0x10
    AMETA_ALT_RIGHT_ON = 0x20
    AMETA_SHIFT_ON = 0x01
    AMETA_SHIFT_LEFT_ON = 0x40
    AMETA_SHIFT_RIGHT_ON = 0x80
    AMETA_SYM_ON = 0x04
    AMETA_FUNCTION_ON = 0x08
    AMETA_CTRL_ON = 0x1000
    AMETA_CTRL_LEFT_ON = 0x2000
    AMETA_CTRL_RIGHT_ON = 0x4000
    AMETA_META_ON = 0x10000
    AMETA_META_LEFT_ON = 0x20000
    AMETA_META_RIGHT_ON = 0x40000
    AMETA_CAPS_LOCK_ON = 0x100000
    AMETA_NUM_LOCK_ON = 0x200000
    AMETA_SCROLL_LOCK_ON = 0x400000

    def __or__(self, other):
        if isinstance(other, int):
            return self.value | other
        elif isinstance(other, AndroidMetastate):
            return self.value | other.value
        raise TypeError(
            "unsupported operand type(s) for |: 'AndroidMetastate' and '{}'".format(
                type(other)
            )
        )


class TouchAction(Enum):
    Default = 0
    Down = 1
    Up = 2
    Move = 3


class SwipeAction(Enum):
    Default = 0
    NoUp = 1
    NoDown = 2


class WebSocketHelper:
    _websocket: WebSocketServerProtocol
    _message_future_dict: Dict[str, Future]

    def __init__(self, websocket):
        self._websocket = websocket
        self._message_future_dict = {}

    async def recv(self):
        res = await self._websocket.recv()
        try:
            msg = json.loads(res)
            if "msgID" in msg:
                self._message_future_dict[msg["msgID"]].set_result(msg)
            else:
                print("Message without id", msg)
        except Exception as e:
            print(e)
            print("Invalid msg", res)

    async def send(self, data: Dict) -> None:
        await self._websocket.send(json.dumps(data))

    async def send_wait(self, data: Dict) -> Dict:
        msg_id = str(int(time.time()))
        data["msgID"] = msg_id
        self._message_future_dict[msg_id] = asyncio.Future()
        await self._websocket.send(json.dumps(data))
        return await self._message_future_dict[msg_id]

    async def close(self):
        await self._websocket.close()

    async def message_show_message(self, msg_content: str, msg_type="info") -> None:
        await self.send(
            {"type": "showMessage", "msgType": msg_type, "msgContent": msg_content}
        )

    async def message_get_controlled_device(self) -> Dict:
        return await self.send_wait({"type": "getControlledDevice"})

    async def message_send_key(
        self,
        action: SendKeyAction,
        keycode: AndroidKeycode,
        metastate: Tuple[AndroidMetastate] = (),
    ) -> None:
        meta = 0
        for x in metastate:
            meta |= x
        return await self.send(
            {
                "type": "sendKey",
                "action": action.value,
                "keycode": keycode.value,
                "metastate": meta,
            }
        )

    async def message_touch(
        self, action: TouchAction, pointer_id: int, pos: Tuple[int], time=80
    ) -> None:
        await self.send(
            {
                "type": "touch",
                "action": action.value,
                "pointerId": pointer_id,
                "pos": {"x": pos[0], "y": pos[1]},
                "time": time,
            }
        )

    async def message_swipe(
        self,
        action: SwipeAction,
        pointer_id: int,
        pos_list: Tuple[Tuple[int]],
        interval_between_pos: int,
    ) -> None:
        pos_list = [{"x": pos[0], "y": pos[1]} for pos in pos_list]
        await self.send(
            {
                "type": "swipe",
                "action": action.value,
                "pointerId": pointer_id,
                "pos": pos_list,
                "intervalBetweenPos": interval_between_pos,
            }
        )

    async def message_shutdown(self) -> None:
        await self.send({"type": "shutdown"})
