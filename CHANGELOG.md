# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-14

### Added
- Initial release of ComfyUI Gemini Image Generator
- Support for Gemini 2.5 Flash Image (stable) model
- Support for Gemini 2.5 Flash Image Preview model
- Integrated API key management with persistent storage
- Multiple aspect ratio options:
  - 1:1 (Square)
  - 3:4 (Portrait)
  - 4:3 (Landscape)
  - 9:16 (Vertical)
  - 16:9 (Wide)
- Response modality options:
  - Image only
  - Text and Image
- Automatic API key saving and loading
- Comprehensive error handling with fallback placeholder images
- Full ComfyUI workflow integration
- Detailed README documentation
- Installation guide
- Example configuration file
- Requirements.txt for easy dependency management
- GNU GPL v3.0 License

### Features
- Native Google Gemini API integration
- Real-time image generation from text prompts
- Configurable image generation parameters
- Support for both stable and preview model versions
- Persistent configuration across ComfyUI sessions
- Error messages displayed in text output
- Console logging for debugging
- Tensor output compatible with all ComfyUI image nodes

### Developer Notes
- Built using google-genai Python SDK
- ComfyUI node architecture compliance
- Proper NODE_CLASS_MAPPINGS and NODE_DISPLAY_NAME_MAPPINGS
- Standard ComfyUI tensor format [B, H, W, C]
- RGB color space normalization (0-1 range)

### Known Limitations
- Gemini API does not support seed-based generation (seed parameter included for workflow compatibility only)
- API rate limits apply based on Google AI account tier
- Internet connection required for all operations
- SynthID watermark automatically applied to generated images

## [Unreleased]

### Planned Features
- Image-to-image generation support
- Multi-image fusion capabilities
- Batch generation support
- Advanced prompt templates
- Generation history and caching
- Negative prompt support (if API adds support)
- Custom safety settings
- API usage statistics
- Local model caching for faster repeated generations

---

For more information about each release, visit the [GitHub Releases](https://github.com/yourusername/ComfyUI-Gemini-YourAPI/releases) page.
