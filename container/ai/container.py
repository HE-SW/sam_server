from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Singleton

import torch
import tomlkit
from dataclasses import dataclass
from segment_anything.modeling.sam import Sam
from segment_anything import sam_model_registry
from service.ai import AiService

class AiContainer(DeclarativeContainer):
    with open("core/ai/config.toml", 'rb') as toml_file:
        config_file: tomlkit.TOMLDocument = tomlkit.load(toml_file)
        sam_config: tomlkit.TOMLDocument = config_file["sam"]

    sam_model:Sam = sam_model_registry[sam_config.get('sam_model_type')](sam_config.get('sam_model_path'))
    device = torch.device(sam_config.get("cuda_index")) if torch.cuda.is_available() else torch.device('mps') if torch.backends.mps.is_available()  else torch.device('cpu')
    sam_model.to(device=device)

    ai_service = Singleton(AiService, sam_model)

    wiring_config: WiringConfiguration = WiringConfiguration(modules=["controller.ai.controller"])
