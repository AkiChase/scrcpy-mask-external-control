## Introduction

[中文文档](./README-zh.md)

External programs can control Scrcpy Mask by connecting via WebSocket and invoking the external control interface provided by Scrcpy Mask. This includes sending touch events, key events, and more to the controlled Android device.

This repository provides control instructions, interface documentation, and offers control utility classes and code examples in several common languages.

## Connection

External programs start a WebSocket Server, fill in the WebSocket Server address in the external control input box on the Scrcpy Mask device page, and click connect to establish a connection.

## Invocation

After successful connection, external programs can call the respective interfaces by sending specific formatted JSON strings, known as **request messages**, to Scrcpy Mask via WebSocket. If the interface has a return value, Scrcpy Mask will respond with a JSON string formatted as a **response message**.

> External programs can attach a random `msgID` field when sending the request JSON string. Scrcpy Mask will include the same `msgID` when replying to the request. External programs can use this to identify which response message corresponds to which request message.

## Interfaces

### `showMessage`

Display a message of a specific type at the top of the Scrcpy Mask window.

#### Request Format

```TypeScript
{  
    "type": "showMessage",  
    "msgType": "success" | "info" | "warning" | "error",
    "msgContent": string
}
```

#### Response Format

No return value

### `getControlledDevice`

Retrieve information about the Android device currently controlled by Scrcpy Mask, returns null if no device is being controlled.

#### Request Format

```TypeScript
{  
    "type": "getControlledDevice"
}
```

#### Response Format

```TypeScript
{
	"msgID": string,
	"controledDevice": {
	  "scid": string,
	  "deviceName": string,
	  "deviceID": string
	}
}
// or
{
	"msgID": string,
	"controledDevice": null
}
```

### `sendKey`

Send a key event to the controlled device.

#### Request Format

```TypeScript
{  
    "type": "sendKey",  
    "action": number, // SendKeyAction: Default = 0, Down = 1, Up = 2
    "keycode": number, // AndroidKeycode
    "metastate": number // Optional. AndroidMetastate: can be combined by Bitwise OR operation
}
```

Refer to `src/frontcommand/scrcpyMaskCmd.ts` and `src/frontcommand/android.ts` for specific values.

#### Response Format

No return value

### `touch`

Send a touch event to the controlled device.

#### Request Format

```TypeScript
{  
    "type": "touch",  
    "action": number, // TouchAction: Default = 0, Down = 1, Up = 2, Move = 3
    "pointerId": number,
    "pos": { "x": number; "y": number }, // pos relative to Android device
    "time": number // Optional. valid only when action is Default, default 80 milliseconds
}
```

#### Response Format

No return value

### `swipe`

Send a swipe event to the controlled device, including coordinates of all **turning points** in the swipe path.

> For longer path segments, it will automatically split into multiple shorter segments.

#### Request Format

```TypeScript
{  
    "type": "swipe",  
    "action": number, // SwipeAction: Default = 0, NoUp = 1, NoDown = 2
    "pointerId": number,
    "pos": { "x": number; "y": number }[], // pos path array relative to Android device
    "intervalBetweenPos": number
}
```

#### Response Format

No return value

### `shutdown`

Terminate control of the controlled device.

#### Request Format

```TypeScript
{  
    "type": "shutdown"
}
```

#### Response Format

No return value

### TODO

Interfaces in the `controlMsg.ts` file are currently not needed and will not be added for now.