from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Singleton

import torch
from dataclasses import dataclass
from segment_anything.modeling.sam import Sam
from segment_anything import sam_model_registry
from service.ai import AiService
from core.config import config
class AiContainer(DeclarativeContainer):
    config = config

    sam_model:Sam = sam_model_registry[config.sam_model_type](config.sam_model_path)
    device = torch.device(config.device) if torch.cuda.is_available() else torch.device('mps') if torch.backends.mps.is_available()  else torch.device('cpu')
    sam_model.to(device=device)

    ai_service = Singleton(AiService, sam_model)

    wiring_config: WiringConfiguration = WiringConfiguration(modules=["controller.ai.controller"])
