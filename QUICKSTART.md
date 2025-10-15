# Quick Start Guide

## 🚀 Get Started in 3 Minutes

### Step 1: Install Dependencies (30 seconds)

Open terminal in the ComfyUI directory and run:

```bash
pip install google-genai pillow torch numpy
```

Or from this node's directory:

```bash
cd custom_nodes/ComfyUI-Gemini-YourAPI
pip install -r requirements.txt
```

### Step 2: Get API Key (1 minute)

1. Visit: https://aistudio.google.com/apikey
2. Click "Get API Key"
3. Copy your key

### Step 3: Use the Node (1 minute)

1. **Restart ComfyUI**

2. **Add the Node:**
   - Right-click in ComfyUI
   - Navigate to: `Add Node` → `image/generation` → `Gemini Image Generator 🎨`

3. **Configure:**
   - **prompt**: Type what you want to generate
   - **api_key**: Paste your API key
   - **save_api_key**: Keep checked ✓
   - Leave other settings as default

4. **Connect & Generate:**
   - Connect `image` output to a `SaveImage` node
   - Click "Queue Prompt"
   - Wait 5-10 seconds
   - Your image will appear!

## 📝 Example Prompts

Try these to get started:

```
A majestic dragon flying over a medieval castle at sunset
```

```
A cozy coffee shop interior with warm lighting and plants
```

```
A futuristic cityscape with flying cars, neon lights, cyberpunk style
```

```
A cute cartoon puppy playing in a flower garden, watercolor style
```

## ⚙️ Quick Settings Guide

### Models
- `gemini-2.5-flash-image` - Stable, recommended ✓
- `gemini-2.5-flash-image-preview` - Latest features

### Aspect Ratios
- `1:1` - Square (Instagram posts)
- `16:9` - Wide (Desktop wallpapers) 
- `9:16` - Vertical (Phone wallpapers)
- `4:3` - Classic (Presentations)
- `3:4` - Portrait (Posters)

### Response Types
- `Image` - Just the image (faster)
- `Text and Image` - Image + description

## 🔧 Troubleshooting

**"API key is required" error?**
→ Make sure you pasted your key and clicked Queue Prompt

**"Module not found" error?**
→ Run: `pip install google-genai`

**Node doesn't appear?**
→ Restart ComfyUI after installation

**Slow generation?**
→ Normal! First generation takes ~10 seconds

## 💡 Tips

1. **Be Specific**: More details = better results
   - ❌ "a cat"
   - ✓ "a fluffy orange cat sitting on a windowsill, soft morning light"

2. **Include Style**: Mention art style for consistent results
   - Examples: "photorealistic", "cartoon", "oil painting", "watercolor"

3. **Save Your Key**: Check `save_api_key` so you don't need to enter it again

4. **Aspect Ratio Matters**: Choose based on your use case
   - Social media? → 1:1 or 4:3
   - Wallpaper? → 16:9
   - Portrait? → 3:4

## 📚 Next Steps

- Read [README.md](README.md) for full documentation
- Check [INSTALL.md](INSTALL.md) for detailed installation
- Load [example_workflow.json](example_workflow.json) for a pre-made workflow
- Read [CHANGELOG.md](CHANGELOG.md) for version history

## 🆘 Need Help?

- Check the console/terminal for error messages
- Verify your API key at https://aistudio.google.com
- Read the troubleshooting section in [INSTALL.md](INSTALL.md)
- Open an issue on GitHub

## 🎉 You're Ready!

Start creating amazing images with Gemini AI in ComfyUI!

---

**Free Tier Limits**: 60 requests per minute  
**Average Generation Time**: 5-10 seconds  
**Cost**: Free tier available, check Google AI pricing for details
