from dataclasses import dataclass,  field
from torch.cuda import is_available as cuda_is_available
from torch.backends.mps import is_available as mps_is_available

from fastapi import APIRouter

@dataclass(frozen=True)
class Constructor:
    ai_router: APIRouter = field(default_factory=APIRouter)

    def __post_init__(self):
        if cuda_is_available() or mps_is_available():
            from controller.ai.controller import ai_router
            object.__setattr__(self, "ai_router", ai_router)  # ✅ frozen=True에서도 변경 가능
        else:
            print("[ERROR] GPU not found, AI Service will not be serving")

