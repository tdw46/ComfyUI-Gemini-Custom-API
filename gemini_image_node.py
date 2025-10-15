import os
import json
import torch
import numpy as np
from PIL import Image
from io import BytesIO
# Optional: google-genai; guard so import errors don't break ComfyUI load
try:
    from google import genai  # type: ignore
    from google.genai import types  # type: ignore
except Exception:  # pragma: no cover - best-effort fallback for loader
    genai = None  # type: ignore
    types = None  # type: ignore

class GeminiImageGenerator:
    """
    A ComfyUI node for generating images using Google Gemini Flash 2.5 Image models.
    """
    
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), "config.json")
        self.client = None
        
    def _load_api_key(self):
        """Load API key from config file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return config.get('api_key', '')
            except Exception as e:
                print(f"Error loading config: {e}")
        return ''
    
    def _save_api_key(self, api_key):
        """Save API key to config file"""
        try:
            config = {'api_key': api_key}
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def _initialize_client(self, api_key):
        """Initialize Gemini client with API key"""
        if api_key:
            os.environ['GOOGLE_API_KEY'] = api_key
            self.client = genai.Client(api_key=api_key)
            return True
        return False
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "Create a beautiful landscape with mountains and a sunset"
                }),
                "model": (["gemini-2.5-flash-image", "gemini-2.5-flash-image-preview"], {
                    "default": "gemini-2.5-flash-image"
                }),
                "aspect_ratio": (["1:1", "3:4", "4:3", "9:16", "16:9"], {
                    "default": "1:1"
                }),
                "response_modalities": (["Image", "Text and Image"], {
                    "default": "Image"
                }),
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "save_api_key": ("BOOLEAN", {
                    "default": True
                }),
            },
            "optional": {
                "image": ("IMAGE",),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "STRING",)
    RETURN_NAMES = ("image", "text_response",)
    FUNCTION = "generate_image"
    CATEGORY = "Custom API Node/Image/Gemini"
    OUTPUT_NODE = True
    
    def generate_image(self, prompt, model, aspect_ratio, response_modalities, api_key, save_api_key, seed=0, image=None):
        """
        Generate an image using Gemini Flash 2.5 Image models
        
        Args:
            prompt: Text description of the image to generate
            model: Which Gemini model to use
            aspect_ratio: Aspect ratio for generated image
            response_modalities: Whether to return just image or text + image
            api_key: Google AI API key
            save_api_key: Whether to save the API key for future use
            seed: Random seed (note: Gemini API doesn't use seeds, included for workflow compatibility)
        
        Returns:
            Tuple of (image_tensor, text_response)
        """
        
        try:
            # Load saved API key if current one is empty
            if not api_key:
                api_key = self._load_api_key()
            # Save API key if requested
            if save_api_key and api_key:
                self._save_api_key(api_key)

            global genai, types
            if genai is None or types is None:
                import sys, os
                candidates = []
                localapp = os.environ.get("LOCALAPPDATA")
                if localapp:
                    py_root = os.path.join(localapp, "Programs", "Python")
                    if os.path.isdir(py_root):
                        for d in os.listdir(py_root):
                            sp = os.path.join(py_root, d, "Lib", "site-packages")
                            if os.path.isdir(sp):
                                candidates.append(sp)
                program_files = os.environ.get("ProgramFiles")
                if program_files:
                    for ver in ("Python312","Python311","Python310","Python39","Python38"):
                        sp = os.path.join(program_files, ver, "Lib", "site-packages")
                        if os.path.isdir(sp):
                            candidates.append(sp)
                for sp in candidates:
                    if sp not in sys.path:
                        sys.path.insert(0, sp)
                try:
                    from google import genai as _genai  # type: ignore
                    from google.genai import types as _types  # type: ignore
                    genai = _genai
                    types = _types
                except Exception as e:
                    # Final fallback: try to install into current env
                    try:
                        import sys, subprocess
                        subprocess.check_call([sys.executable, "-m", "pip", "install", "google-genai"])  # minimal
                        from google import genai as _genai  # type: ignore
                        from google.genai import types as _types  # type: ignore
                        genai = _genai
                        types = _types
                    except Exception as e2:
                        raise ImportError(
                            "google-genai is not installed and auto-install failed. "
                            "Run: python -m pip install google-genai"
                        ) from e2

            # Initialize client
            if not self._initialize_client(api_key):
                raise ValueError("API key is required. Please provide a Google AI API key.")
            # Configure response modalities
            modalities = ['Image'] if response_modalities == "Image" else ['Text', 'Image']
            
            # Create generation config
            config = types.GenerateContentConfig(
                response_modalities=modalities,
                image_config=types.ImageConfig(
                    aspect_ratio=aspect_ratio
                )
            )
            
            # Generate content
            print(f"Generating image with Gemini {model}...")
            print(f"Prompt: {prompt}")
            print(f"Aspect Ratio: {aspect_ratio}")
            
            # Build contents list: prompt plus optional image
            contents = [prompt]
            if image is not None:
                # Convert Comfy tensor [B,H,W,C] float32 0..1 to PIL
                try:
                    img_np = (image[0].clamp(0, 1).cpu().numpy() * 255.0).astype(np.uint8)
                except Exception:
                    img_np = (np.array(image)[0] * 255.0).astype(np.uint8)
                pil_in = Image.fromarray(img_np)
                contents = [prompt, pil_in]

            response = self.client.models.generate_content(
                model=model,
                contents=contents,
                config=config
            )
            
            # Extract image and text from response
            image_tensor = None
            text_response = ""
            
            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    text_response += part.text
                    print(f"Text response: {part.text}")
                elif part.inline_data is not None:
                    # Convert image data to tensor
                    image_data = part.inline_data.data
                    pil_image = Image.open(BytesIO(image_data))
                    
                    # Convert PIL image to ComfyUI tensor format [B, H, W, C]
                    image_np = np.array(pil_image).astype(np.float32) / 255.0
                    if len(image_np.shape) == 2:  # Grayscale
                        image_np = np.stack([image_np] * 3, axis=-1)
                    image_tensor = torch.from_numpy(image_np).unsqueeze(0)
                    
                    print(f"Generated image size: {pil_image.size}")
            
            if image_tensor is None:
                raise ValueError("No image was generated by the model")
            
            return (image_tensor, text_response if text_response else "Image generated successfully")
        
        except Exception as e:
            error_msg = f"Error generating image: {str(e)}"
            print(error_msg)
            
            # Return a black placeholder image with error text
            placeholder = torch.zeros((1, 512, 512, 3), dtype=torch.float32)
            return (placeholder, error_msg)

# Note: NODE_CLASS_MAPPINGS are defined in __init__.py
