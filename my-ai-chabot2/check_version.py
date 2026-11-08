from importlib.metadata import version

import mlx_whisper
import sounddevice as sd
import numpy as np
import scipy

for name in ["mlx_whisper", "sounddevice", "numpy", "scipy"]:
    try:
        ver = version(name)
        print(f"{name} version: {ver}")
    except Exception as e:
        print(f"Error retrieving version for {name}: {e}")
