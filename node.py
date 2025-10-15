from comfy_api.latest import ComfyExtension, io
from comfy_api.latest import ui as comfy_ui

import os
import json
from io import BytesIO

"""Gemini Image Generator V3 node.

This file avoids heavy imports at module load to ensure Comfy can import
the extension even if dependencies aren't installed yet.
"""

# google-genai is imported lazily in execute()


NODE_CATEGORY = "Gemini"
# Align node_id with existing workflows; keep emoji only in UI if desired
DISPLAY_NAME = "Gemini Image Generator (Custom API)"


class GeminiImageGenerator(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="GeminiImageGenerator",
            display_name=DISPLAY_NAME,
            category=NODE_CATEGORY,
            description="Generate images with Google Gemini 2.5 Flash Image models.",
            inputs=[
                io.String.Input(
                    "prompt",
                    default="Create a beautiful landscape with mountains and a sunset",
                    multiline=True,
                ),
                # Optional reference image for image+text to image editing
                io.Image.Input("image", optional=True),
                io.Combo.Input(
                    "model",
                    options=[
                        "gemini-2.5-flash-image",
                        "gemini-2.5-flash-image-preview",
                    ],
                    default="gemini-2.5-flash-image",
                ),
                io.Combo.Input(
                    "aspect_ratio",
                    options=["1:1", "3:4", "4:3", "9:16", "16:9"],
                    default="1:1",
                ),
                io.Combo.Input(
                    "response_modalities",
                    options=["Image", "Text and Image"],
                    default="Image",
                ),
                io.String.Input(
                    "api_key",
                    multiline=False,
                    default="",
                    tooltip="Your Google AI API key (stored locally if Save API Key is enabled). This field is masked by the node's JS extension.",
                ),
                io.Boolean.Input(
                    "save_api_key",
                    default=True,
                ),
            ],
            outputs=[
                io.Image.Output(),
            ],
        )

    @staticmethod
    def _config_path() -> str:
        return os.path.join(os.path.dirname(__file__), "config.json")

    @classmethod
    def _load_api_key(cls) -> str:
        path = cls._config_path()
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f).get("api_key", "")
            except Exception:
                return ""
        return ""

    @classmethod
    def _save_api_key(cls, api_key: str) -> None:
        try:
            with open(cls._config_path(), "w", encoding="utf-8") as f:
                json.dump({"api_key": api_key}, f, indent=2)
        except Exception:
            pass

    # client is created inside execute after lazy import of google-genai

    @classmethod
    def execute(
        cls,
        prompt: str,
        image,
        model: str,
        aspect_ratio: str,
        response_modalities: str,
        api_key: str,
        save_api_key: bool,
    ) -> io.NodeOutput:
        # Helper: extend sys.path with common Windows system Python site-packages
        def _extend_with_system_sitepackages():
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
            # Per-user installs (pip --user)
            appdata_roam = os.environ.get("APPDATA")
            if appdata_roam:
                for ver in ("Python312","Python311","Python310","Python39","Python38"):
                    sp = os.path.join(appdata_roam, "Python", ver, "site-packages")
                    if os.path.isdir(sp):
                        candidates.append(sp)
            program_files = os.environ.get("ProgramFiles")
            if program_files:
                for ver in ("Python312","Python311","Python310","Python39","Python38"):
                    sp = os.path.join(program_files, ver, "Lib", "site-packages")
                    if os.path.isdir(sp):
                        candidates.append(sp)
            # Deduplicate and prepend so they take precedence
            for sp in candidates:
                if sp not in sys.path:
                    sys.path.insert(0, sp)
        
        def _pip_install_into_current_env(packages: list[str]) -> tuple[bool, str]:
            import sys, subprocess
            try:
                # Install packages one by one to improve error visibility
                for p in packages:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", p])
                return True, "installed"
            except Exception as e:
                return False, str(e)

        # Lazy-import dependencies so the extension loads before deps are installed
        try:
            from google import genai  # type: ignore
            from google.genai import types  # type: ignore
            import numpy as np  # type: ignore
            import torch  # type: ignore
            from PIL import Image  # type: ignore
        except Exception as import_err:
            # Try to fall back to system Python's site-packages
            _extend_with_system_sitepackages()
            try:
                from google import genai  # type: ignore
                from google.genai import types  # type: ignore
                import numpy as np  # type: ignore
                import torch  # type: ignore
                from PIL import Image  # type: ignore
            except Exception:
                # Try to install into the current ComfyUI venv and retry
                ok, why = _pip_install_into_current_env(["google-genai"])  # minimal requirement
                if ok:
                    try:
                        from google import genai  # type: ignore
                        from google.genai import types  # type: ignore
                        import numpy as np  # type: ignore
                        import torch  # type: ignore
                        from PIL import Image  # type: ignore
                    except Exception as e:
                        return io.NodeOutput(
                            None,
                            ui=comfy_ui.Notification(
                                title="Gemini API",
                                message=f"Installed google-genai but import still failed: {e}",
                                level="error",
                            ),
                        )
                else:
                    # Give a helpful error without relying on torch
                    import sys
                    return io.NodeOutput(
                        None,
                        ui=comfy_ui.Notification(
                            title="Gemini API",
                            message=(
                                "Missing dependencies and auto-install failed.\n"
                                "Run manually in ComfyUI venv:\n"
                                f"\n{sys.executable} -m pip install google-genai pillow numpy torch\n"
                            ),
                            level="error",
                        ),
                    )
        if not api_key:
            api_key = cls._load_api_key()
        if save_api_key and api_key:
            cls._save_api_key(api_key)

        # Create client after importing google-genai
        client = None
        if api_key:
            os.environ["GOOGLE_API_KEY"] = api_key
            try:
                from google import genai as _genai  # type: ignore
                client = _genai.Client(api_key=api_key)
            except Exception:
                client = None
        if client is None:
            # Return a black image with a message via UI preview
            import numpy as np  # type: ignore
            import torch  # type: ignore
            img = torch.zeros((1, 512, 512, 3), dtype=torch.float32)
            return io.NodeOutput(
                img,
                ui=comfy_ui.Notification(
                    title="Gemini API",
                    message="API key is required. Provide it in the node and enable Save API Key.",
                    level="error",
                ),
            )

        try:
            modalities = ["Image"] if response_modalities == "Image" else ["Text", "Image"]
            cfg = types.GenerateContentConfig(
                response_modalities=modalities,
                image_config=types.ImageConfig(aspect_ratio=aspect_ratio),
            )

            # Build contents: prompt plus optional image
            contents = [prompt]
            if image is not None:
                import numpy as np  # type: ignore
                from PIL import Image  # type: ignore
                # Expecting [B,H,W,C] floats 0-1; take first image in batch
                try:
                    import torch  # type: ignore
                    if isinstance(image, torch.Tensor):
                        np_img = (image[0].clamp(0, 1).cpu().numpy() * 255.0).astype("uint8")
                    else:
                        # Assume numpy-like already in 0..1
                        np_img = (np.array(image)[0] * 255.0).astype("uint8")
                except Exception:
                    np_img = (np.array(image)[0] * 255.0).astype("uint8")
                pil_img = Image.fromarray(np_img)
                contents = [prompt, pil_img]

            result = client.models.generate_content(
                model=model,
                contents=contents,
                config=cfg,
            )

            import numpy as np  # type: ignore
            import torch  # type: ignore
            from PIL import Image  # type: ignore
            image_tensor = None
            for part in result.candidates[0].content.parts:
                if getattr(part, "inline_data", None) is not None:
                    data = part.inline_data.data
                    pil = Image.open(BytesIO(data)).convert("RGB")
                    arr = (np.array(pil).astype(np.float32) / 255.0)
                    image_tensor = torch.from_numpy(arr).unsqueeze(0)
                    break

            if image_tensor is None:
                # Fallback if no image was returned
                image_tensor = torch.zeros((1, 512, 512, 3), dtype=torch.float32)
                return io.NodeOutput(
                    image_tensor,
                    ui=comfy_ui.Notification(
                        title="Gemini API",
                        message="No image returned by the model.",
                        level="warning",
                    ),
                )

            return io.NodeOutput(
                image_tensor,
                ui=comfy_ui.PreviewImage(image_tensor, cls=cls),
            )
        except Exception as e:
            import torch  # type: ignore
            image_tensor = torch.zeros((1, 512, 512, 3), dtype=torch.float32)
            return io.NodeOutput(
                image_tensor,
                ui=comfy_ui.Notification(title="Gemini API", message=str(e), level="error"),
            )


class GeminiExtension(ComfyExtension):
    async def get_node_list(self):
        return [GeminiImageGenerator]


async def comfy_entrypoint() -> GeminiExtension:
    return GeminiExtension()
