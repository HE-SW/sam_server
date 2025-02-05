import cv2
import numpy as np
from io import BytesIO
import urllib.request
from abc import ABCMeta
from segment_anything import SamPredictor
from segment_anything.modeling.sam import Sam

from dependency_injector.wiring import inject, Provide

class AiService(metaclass=ABCMeta):
    @inject
    def __init__(self, sam_model:Sam):
        self.sam_predictor: SamPredictor = SamPredictor(sam_model)

    def get_image_npy_bytes(self, image_path:str):
        with urllib.request.urlopen(image_path) as response:
            image_bytes = np.asarray(bytearray(response.read()), dtype=np.uint8)
        image = cv2.imdecode(image_bytes, cv2.IMREAD_UNCHANGED)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  
        self.sam_predictor.set_image(image)
        image_embedding = self.sam_predictor.get_image_embedding().cpu().numpy()
        npy_buffer = BytesIO()
        np.save(npy_buffer, image_embedding)
        npy_buffer.seek(0)  # 스트림 처음으로 이동
    
        return npy_buffer.getvalue()  # 바이너리 데이터 반환