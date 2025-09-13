### Usage
Download the custom node from this repo and put it in your custom_node/ folder. Launch ComfyUI.

In the workflow you want to use as an API, replace your existing preview/save image node with this custom node located in api > image > Send Image (WebSocket Base64 PNG)

To use the output base64 image data, create a prompt and related websocket session as described in [this example script](https://github.com/comfyanonymous/ComfyUI/blob/master/script_examples/websockets_api_example.py). When the Websocket Base64 PNG node is reached, it will output a message in the websocket containing the image data. The format of the message is `{"type": "base64_image_output", "data": ["iVBORw0KGgoAAAANS", "more image base64 here"]}` and you should look for this in your code.

I made this because the normal Websocket Image Save node wasn't working for me. Also I like encoding images to base64 while transporting them.
