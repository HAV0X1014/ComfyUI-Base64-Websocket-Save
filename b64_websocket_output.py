#the format this sends images over the websocket is 
# {"type": "base64_image_output", "data": {"images": ["iVBORw0KGgoAAAANS", "more image base64 here"], "prompt_id": "4a8eff2"}}

import base64
import io
import torch
import numpy as np
from PIL import Image
from server import PromptServer
import comfy.utils
from comfy_execution.utils import get_executing_context

# Define the node class
class SendImageViaWebSocket:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "send_image_websocket"
    CATEGORY = "api/image" #put it with the other websocket node
    OUTPUT_NODE = True

    def send_image_websocket(self, images):
        server = PromptServer.instance
        if not server:
            print("ComfyUI server instance not found. Cannot send image via websocket.")
            return {}

        encoded_images = []
        step = 0
        
        for image_tensor in images:
            #convert tensor to image
            i = 255. * image_tensor.cpu().numpy()
            img = Image.fromarray(i.astype(np.uint8))

            #pil image to png
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            comfy.utils.ProgressBar(images.shape[0]).update_absolute(step, images.shape[0], ("PNG", img, None))
            step += 1

            #png to b64
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            encoded_images.append(img_str)

        try:
            payload = {"images": encoded_images, "prompt_id":  get_executing_context().prompt_id}
            server.send_sync("base64_image_output", payload)
            print(f"Sent {len(encoded_images)} image(s) via websocket with type 'custom_image_output' for prompt id {get_executing_context().prompt_id}")
        except Exception as e:
            print(f"Failed to send image via websocket: {e}")

        # Output nodes typically return an empty dictionary.
        return {}

NODE_CLASS_MAPPINGS = {
    "SendImageViaWebSocket": SendImageViaWebSocket
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SendImageViaWebSocket": "Send Image (WebSocket Base64 PNG)"
}
