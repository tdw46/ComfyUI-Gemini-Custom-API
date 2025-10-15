// ComfyUI frontend extension to enhance the Gemini Custom API node UI
// - Masks the api_key input as a password field
// - Adds small UX niceties

app.registerExtension({
  name: "GeminiCustomAPI.MaskKey",
  async nodeCreated(node) {
    try {
      if (!node || !node.widgets || !node.title) return;
      if (!String(node.title).includes("Gemini Image Generator (Custom API)")) return;
      const w = node.widgets.find((w) => w && w.name === "api_key");
      if (w && w.inputEl) {
        w.inputEl.type = "password";
        w.inputEl.placeholder = "Enter Google AI API key";
      }
    } catch (e) {
      console.warn("GeminiCustomAPI.MaskKey nodeCreated error:", e);
    }
  },
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    try {
      if (!nodeData || nodeData.name !== "Gemini Image Generator (Custom API)") return;
      const onCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = function () {
        const r = onCreated ? onCreated.apply(this, arguments) : undefined;
        try {
          const w = this.widgets?.find((w) => w && w.name === "api_key");
          if (w && w.inputEl) {
            w.inputEl.type = "password";
            w.inputEl.placeholder = "Enter Google AI API key";
          }
        } catch (e) {
          console.warn("GeminiCustomAPI.MaskKey beforeRegisterNodeDef error:", e);
        }
        return r;
      };
    } catch (e) {
      console.warn("GeminiCustomAPI.MaskKey hook error:", e);
    }
  },
});
