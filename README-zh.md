## 介绍

外部程序可以在与 Scrcpy Mask 通过 WebSocket 连接后，调用 Scrcpy Mask 提供的外部控制接口，对 Scrcpy Mask 进行控制。比如发送触摸事件、按键事件到受控安卓设备等等。

本仓库提供控制说明与接口文档，并提供一些常见语言的控制工具类和代码示例。

## 连接

外部程序启动 Websocket Server ，在 Scrcpy Mask 设备页面的外部控制输入框中填入 Websocket Server 的地址，点击连接即可。

## 调用

连接成功后，外部程序通过 WebSocket 连接向 Scrcpy Mask 发送特定格式的 json 字符串**请求消息**即可调用相应的接口。若接口有返回值，那么 Scrcpy Mask 将发送一定格式的 json 字符串**回复消息**。

> 外部程序在请求 json 字符串时可以附加随机的 `msgID` 字段，Scrcpy Mask 回复该请求时将附带同样的 `msgID`。外部程序可借此判断回复消息对应的是哪一个请求消息。

## 接口

### `showMessage`

在 Scrcpy Mask 窗口顶部显示一条特定类型的消息。

#### 请求格式

```TypeScript
{  
    "type": "showMessage",  
    "msgType": "success" | "info" | "warning" | "error",
    "msgContent": string
}
```

#### 返回格式

无返回值

### `getControlledDevice`

获取 Scrcpy Mask 当前控制的安卓设备信息，无受控设备则为 null。

#### 请求格式

```TypeScript
{  
    "type": "getControlledDevice"
}
```

#### 返回格式

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

发送按键事件到受控设备。

#### 请求格式

```TypeScript
{  
    "type": "sendKey",  
    "action": number, // SendKeyAction: Default = 0, Down = 1, Up = 2
    "keycode": number, // AndroidKeycode
    "metastate": number // Optional. AndroidMetastate: can be combined by Bitwise OR operation
}
```

具体值请参考 `src/frontcommand/scrcpyMaskCmd.ts` 、`src/frontcommand/android.ts`

#### 返回格式

无返回值

### `touch`

发送触摸事件到受控设备。

#### 请求格式

```TypeScript
{  
    "type": "touch",  
    "action": number, // TouchAction: Default = 0, Down = 1, Up = 2, Move = 3
    "pointerId": number,
    "pos": { "x": number; "y": number }， // pos relative to Android device
    "time": number // Optional. valid only when action is Default, default 80 milliseconds
}
```

#### 返回格式

无返回值

### `swipe`

发送滑动事件到受控设备，需要传入滑动路径的所有**转折点**坐标。

> 对于较长的路径线段，将自动拆分为多个较短的线段

#### 请求格式

```TypeScript
{  
    "type": "swipe",  
    "action": number, // SwipeAction: Default = 0, NoUp = 1, NoDown = 2
    "pointerId": number,
    "pos": { "x": number; "y": number }[], // pos path array relative to Android device
    "intervalBetweenPos": number
}
```

#### 返回格式

无返回值

### `shutdown`

终止对受控设备的控制。

#### 请求格式

```TypeScript
{  
    "type": "shutdown"
}
```

#### 返回格式

无返回值

### TODO

 `controlMsg.ts` 文件中的接口，目前没有需求，暂不添加。
