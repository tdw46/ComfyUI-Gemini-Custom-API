GeminiExtension = None
comfy_entrypoint = None

# Try V3 extension first
try:
    from .node import GeminiExtension as _GeminiExtension, comfy_entrypoint as _comfy_entrypoint
    GeminiExtension = _GeminiExtension
    comfy_entrypoint = _comfy_entrypoint
except Exception:
    # V3 not available (older ComfyUI or missing comfy_api). Fall back to V1-only.
    pass

# Always try to expose V1-style registration for backward compatibility
try:
    from .gemini_image_node import GeminiImageGenerator as GeminiImageGeneratorV1  # type: ignore
    NODE_CLASS_MAPPINGS = {
        "Gemini Image Generator (Custom API)": GeminiImageGeneratorV1,
    }
    NODE_DISPLAY_NAME_MAPPINGS = {
        "Gemini Image Generator (Custom API)": "Gemini Image Generator (Custom API) 🎨",
    }
except Exception:
    NODE_CLASS_MAPPINGS = {}
    NODE_DISPLAY_NAME_MAPPINGS = {}

__all__ = [name for name in [
    "GeminiExtension",
    "comfy_entrypoint",
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
] if globals().get(name) is not None]
