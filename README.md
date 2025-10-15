# ComfyUI Gemini Image Generator 🎨

A comprehensive ComfyUI custom node for generating images using Google's Gemini 2.5 Flash Image models (aka "Nano Banana") USING YOUR OWN API KEY. This node provides native integration with Google's latest image generation AI directly within ComfyUI workflows.


## Purpose
- This is a bring-your-own API key node. It lets you enter and save your own Google AI API key so you do NOT need to buy into ComfyUI's Token system.
- If you like this, check the my other repositories for additional Custom API nodes (e.g., OpenAI image generation, etc.).

## Features

- ✨ **Latest Models**: Support for Gemini 2.5 Flash Image (stable) and Preview versions
- 🔑 **Bring Your Own Key**: Enter your Google AI API key directly in the node (no ComfyUI Tokens required)
- 🗝️ **API Key Storage**: Saves your key to `config.json` locally; field is masked in the UI (via a small JS extension)
- 🖼️ **Optional Image Input**: Provide an `IMAGE` input for text+image (image editing) workflows
- 📐 **Multiple Aspect Ratios**: Support for 1:1, 3:4, 4:3, 9:16, and 16:9
- 🎯 **Response Modes**: Choose between image-only or text+image responses
- ⚙️ **Auto‑Install Dependencies**: If `google-genai` is missing in the ComfyUI venv, the node will attempt to install it automatically, and also falls back to system site‑packages when possible
- 🔄 **Easy Integration**: Seamless integration with ComfyUI workflows
- 💾 **Persistent Configuration**: API key saved securely for future use

## Installation

### Method 1: Manual Installation

1. Navigate to your ComfyUI custom_nodes directory:
```
cd ComfyUI/custom_nodes/
```

2. Download or copy the folder `ComfyUI-Gemini-Custom-API` into the `custom_nodes/` directory.

3. (Optional) Install the required dependencies into the ComfyUI environment. In ComfyUI Desktop, open the Terminal panel and run:
```
python -m pip install -r "<path-to>/custom_nodes/ComfyUI-Gemini-Custom-API/requirements.txt"
```

### Method 2: Using ComfyUI Manager

1. Open ComfyUI Manager
2. Search for "Gemini Image Generator"
3. Click Install
4. Restart ComfyUI

### Dependency auto‑install (what the node will do for you)
- If `google-genai` is not available in the ComfyUI venv, the node will try to locate system Python site‑packages and import from there.
- If still missing, it will attempt to run `pip install google-genai` in the current ComfyUI venv automatically and retry the import.
- You can always install manually in the Desktop Terminal:
```
python -m pip install google-genai pillow numpy torch
```

## Getting Your API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Get API Key" or "Create API Key"
4. Copy the generated API key
5. Paste it into the node's `api_key` field in ComfyUI

**Note**: The API key is stored locally in `config.json` and never shared externally.

## Usage

### Basic Workflow

1. **Add the Node**: In ComfyUI, right-click and select `Add Node` > `Gemini` > `Gemini Image Generator (Custom API)`

2. **Configure Parameters**:
- **prompt**: Describe the image you want to generate
- **model**: Choose between:
- `gemini-2.5-flash-image` (default, stable version)
- `gemini-2.5-flash-image-preview` (latest preview features)
- **aspect_ratio**: Select from 1:1, 3:4, 4:3, 9:16, or 16:9
- **response_modalities**: 
- `Image` - Returns only the generated image
- `Text and Image` - Returns both image and descriptive text
- **api_key**: Your Google AI API key
- **save_api_key**: Check to save API key for future sessions
- **image** (optional): Connect an `IMAGE` to use text+image generation (image editing)

3. **Generate**: Connect the output to a `SaveImage` node or any other image processing nodes

### Example Prompts

```
Create a serene mountain landscape at sunset with a lake reflection
```

```
A futuristic city with flying cars and neon lights, cyberpunk style
```

```
A cute cartoon robot playing with a puppy in a garden, colorful and cheerful
```

## Node Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| prompt | STRING | - | Text description of the image to generate |
| image | IMAGE (optional) | - | Optional reference image for text+image (image editing) |
| model | DROPDOWN | gemini-2.5-flash-image | Select Gemini model version |
| aspect_ratio | DROPDOWN | 1:1 | Output image aspect ratio |
| response_modalities | DROPDOWN | Image | Output type (Image only or Text+Image) |
| api_key | STRING | - | Your Google AI API key |
| save_api_key | BOOLEAN | True | Save API key to config file |
| seed | INT | 0 | Optional seed (for workflow compatibility) |

### Aspect Ratio Options

| Ratio | Size | Use Case |
|-------|------|----------|
| 1:1 | Square | Social media posts, avatars |
| 3:4 | Portrait | Vertical content, mobile |
| 4:3 | Landscape | Standard displays |
| 9:16 | Vertical | Mobile, stories |
| 16:9 | Wide | Desktop wallpapers, banners |

## Outputs

The node provides two outputs:

1. **IMAGE**: A ComfyUI-compatible image tensor that can be connected to any image processing nodes
2. **STRING**: Text response from the model (if text modality is enabled) or status message

## Models

### Gemini 2.5 Flash Image (Stable)
- **Model ID**: `gemini-2.5-flash-image`
- **Status**: Stable release
- **Best for**: Production workflows requiring consistency
- **Input limit**: 32,768 tokens
- **Output limit**: 32,768 tokens

### Gemini 2.5 Flash Image Preview
- **Model ID**: `gemini-2.5-flash-image-preview`
- **Status**: Preview with latest features
- **Best for**: Testing cutting-edge capabilities
- **Input limit**: 32,768 tokens
- **Output limit**: 32,768 tokens

## API Key Security

- API keys are stored locally in `config.json` in the node directory
- The file is created automatically when you save an API key
- **Never share your config.json file or commit it to version control**
- A `.example` file is provided as a template
- The UI masks the API key field so it is not displayed in plain text

## Troubleshooting

### "API key is required" Error
- Make sure you've entered a valid Google AI API key
- Check that `save_api_key` is enabled
- Verify the key at [Google AI Studio](https://aistudio.google.com)

### "No image was generated" Error
- Check your internet connection
- Verify your API key is still valid
- Try a different prompt or model
- Check the console for detailed error messages

### "google-genai is not installed" / Import Errors
- The node will try to locate system site‑packages automatically and import from there.
- If still missing, it will try to install `google-genai` into the ComfyUI venv and retry.
- You can also install manually in ComfyUI Desktop Terminal:
```
python -m pip install google-genai pillow numpy torch
```

### Image Not Appearing
- Check that the aspect ratio is compatible with your workflow
- Verify the node's outputs are connected properly
- Look for error messages in the ComfyUI console

## Best Practices

1. **Detailed Prompts**: More specific prompts generally produce better results
2. **Style Keywords**: Include style descriptors (realistic, cartoon, oil painting, etc.)
3. **Composition**: Specify layout, lighting, and mood
4. **Iteration**: Use the text response to refine your prompts
5. **API Limits**: Be mindful of API rate limits and quotas

## API Rate Limits

Google AI API has rate limits based on your account tier:
- Free tier: 60 requests per minute
- Check [Google AI pricing](https://ai.google.dev/pricing) for current limits

## Limitations

- Image generation does not support audio or video inputs
- The model may not always follow exact number specifications in prompts
- Works best with up to 3 reference images as input
- Best performance with languages: English, Spanish (Mexico), Japanese, Chinese, Hindi
- All generated images include a SynthID watermark for authenticity

## Examples

### Example 1: Basic Image Generation
```
Prompt: "A magical forest with glowing mushrooms and fireflies at night"
Model: gemini-2.5-flash-image
Aspect Ratio: 16:9
Response: Image
```

### Example 2: With Text Description
```
Prompt: "An elegant modern kitchen with marble countertops"
Model: gemini-2.5-flash-image-preview
Aspect Ratio: 4:3
Response: Text and Image
```

## Version History

### v1.0.0 (2025-01-14)
- Initial release
- Support for Gemini 2.5 Flash Image models
- API key management
- Multiple aspect ratios
- Configurable response modalities

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

## Acknowledgments

- Built for [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- Powered by [Google Gemini API](https://ai.google.dev/)
- Model nickname "Nano Banana" courtesy of Google

## Links

- [Google AI Studio](https://aistudio.google.com)
- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs/image-generation)
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- [Report Issues](https://github.com/yourusername/ComfyUI-Gemini-YourAPI/issues)

## Support

If you encounter issues or have questions:
1. Check the troubleshooting section above
2. Review the [Gemini API documentation](https://ai.google.dev/gemini-api/docs/image-generation)
3. Open an issue on GitHub with detailed information

---

Made with ❤️ for the ComfyUI community
