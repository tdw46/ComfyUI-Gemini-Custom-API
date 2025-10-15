# Installation Guide

## Quick Start

### 1. Install Dependencies

Navigate to this directory and run:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install google-genai pillow torch numpy
```

### 2. Get Your API Key

1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Get API Key" or "Create API Key"
4. Copy the generated API key

### 3. Configure the Node

You have two options:

#### Option A: Enter API Key in ComfyUI (Recommended)
1. Start ComfyUI
2. Add the "Gemini Image Generator 🎨" node
3. Paste your API key in the `api_key` field
4. Make sure `save_api_key` is checked
5. The key will be saved automatically

#### Option B: Manual Configuration
1. Copy `config.json.example` to `config.json`:
   ```bash
   cp config.json.example config.json
   ```
2. Edit `config.json` and replace `YOUR_GOOGLE_AI_API_KEY_HERE` with your actual API key
3. Save the file

### 4. Restart ComfyUI

Restart ComfyUI to load the new node.

### 5. Test the Node

1. In ComfyUI, right-click and select: `Add Node` > `image/generation` > `Gemini Image Generator 🎨`
2. Enter a prompt like: "A beautiful sunset over mountains"
3. Leave other settings at default
4. Connect to a "Save Image" node
5. Click "Queue Prompt"

## Troubleshooting

### Module Not Found Error

If you get import errors:

```bash
# Make sure you're in the ComfyUI environment
cd ComfyUI
python -m pip install -r custom_nodes/ComfyUI-Gemini-YourAPI/requirements.txt
```

### API Key Not Saving

1. Check file permissions on the node directory
2. Manually create `config.json` with your key
3. Ensure the path is correct

### "No module named 'google'" Error

Install the correct package:

```bash
pip install google-genai
# NOT google-api-python-client
```

### Images Not Generating

1. Check your internet connection
2. Verify API key is valid at [Google AI Studio](https://aistudio.google.com)
3. Check ComfyUI console for error messages
4. Try the preview model: `gemini-2.5-flash-image-preview`

## Updating

To update to the latest version:

```bash
cd custom_nodes/ComfyUI-Gemini-YourAPI
git pull
pip install -r requirements.txt --upgrade
```

Then restart ComfyUI.

## System Requirements

- Python 3.8 or higher
- ComfyUI (latest version recommended)
- Internet connection for API calls
- Google AI API key (free tier available)

## Supported Platforms

- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu 20.04+, other distros)

## Need Help?

- Read the [README.md](README.md) for detailed documentation
- Check [Gemini API Docs](https://ai.google.dev/gemini-api/docs/image-generation)
- Open an issue on GitHub
