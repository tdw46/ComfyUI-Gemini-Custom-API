#!/usr/bin/env python3
"""
Test script to verify the Gemini node can be imported correctly.
Run this from the ComfyUI custom_nodes directory.
"""

import sys
import os
import importlib.util

print("=" * 60)
print("Testing Gemini Image Generator Node Import")
print("=" * 60)

try:
    # Get the path to the node directory
    node_dir = os.path.dirname(os.path.abspath(__file__))
    init_file = os.path.join(node_dir, "__init__.py")
    
    print(f"\nNode directory: {node_dir}")
    print(f"Loading from: {init_file}")
    
    # Load the module using importlib to handle relative imports
    spec = importlib.util.spec_from_file_location("ComfyUI_Gemini_YourAPI", init_file)
    if spec is None or spec.loader is None:
        raise ImportError("Could not load module spec")
    
    module = importlib.util.module_from_spec(spec)
    sys.modules["ComfyUI_Gemini_YourAPI"] = module
    
    # Add the node directory to sys.path so relative imports work
    if node_dir not in sys.path:
        sys.path.insert(0, node_dir)
    
    print("\n1. Loading module...")
    spec.loader.exec_module(module)
    print("✓ Successfully loaded __init__.py")
    
    NODE_CLASS_MAPPINGS = module.NODE_CLASS_MAPPINGS
    NODE_DISPLAY_NAME_MAPPINGS = module.NODE_DISPLAY_NAME_MAPPINGS
    
    print("\n2. Checking node mappings...")
    print(f"   NODE_CLASS_MAPPINGS keys: {list(NODE_CLASS_MAPPINGS.keys())}")
    print(f"   NODE_DISPLAY_NAME_MAPPINGS: {NODE_DISPLAY_NAME_MAPPINGS}")
    
    print("\n3. Testing node class...")
    node_class = NODE_CLASS_MAPPINGS["Gemini Image Generator (Custom API)"]
    print(f"   Node class: {node_class}")
    print(f"   Category: {node_class.CATEGORY}")
    
    print("\n4. Testing INPUT_TYPES...")
    input_types = node_class.INPUT_TYPES()
    print(f"   Required inputs: {list(input_types['required'].keys())}")
    if 'optional' in input_types:
        print(f"   Optional inputs: {list(input_types['optional'].keys())}")
    
    print("\n5. Testing node instantiation...")
    node_instance = node_class()
    print(f"   ✓ Node instance created successfully")
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS PASSED!")
    print("=" * 60)
    print("\nThe node should appear in ComfyUI under category: Gemini")
    print("Node name: Gemini Image Generator (Custom API) 🎨")
    print("\nIf the node still doesn't appear:")
    print("1. Make sure ComfyUI is fully restarted")
    print("2. Check the ComfyUI console for any error messages")
    print("3. Verify all dependencies are installed: pip install -r requirements.txt")
    
except ImportError as e:
    print(f"\n✗ Import Error: {e}")
    print("\nPossible causes:")
    print("1. Module name mismatch")
    print("2. Missing dependencies")
    print("3. Python path issues")
    
except KeyError as e:
    print(f"\n✗ Key Error: {e}")
    print("Node mapping key doesn't match")
    
except Exception as e:
    print(f"\n✗ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n")
