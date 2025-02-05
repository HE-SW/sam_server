from dataclasses import dataclass
import torch

from dependency_injector.containers import DeclarativeContainer



@dataclass(frozen=True)
class Constructor:
    if torch.cuda.is_available() or torch.backends.mps.is_available():
        if torch.cuda.is_available(): print("CUDA 사용가능")
        if torch.backends.mps.is_available(): print("mps 사용가능")
        from container.ai.container import AiContainer
        ai_container: DeclarativeContainer = AiContainer()
    else:
        print("[ERROR : HIGH] GPU not found. Ai Controller will not be serving.")
