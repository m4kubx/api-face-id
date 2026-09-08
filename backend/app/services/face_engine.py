from deepface import DeepFace
import numpy as np
from typing import List, Dict, Optional
import os
from PIL import Image


class FaceEngine:
    def __init__(self, model_name: str = "ArcFace", detector_backend: str = "retinaface"):
        self.model_name = model_name
        self.detector_backend = detector_backend

    def extract_embedding(self, image_path: str) -> List[float]:
        try:
            result = DeepFace.represent(
                img_path=image_path,
                model_name=self.model_name,
                detector_backend=self.detector_backend,
                enforce_detection=True
            )
            return result[0]["embedding"]
        except Exception as e:
            raise ValueError(f"Could not extract face embedding: {str(e)}")

    def verify_faces(self, img1_path: str, img2_path: str, threshold: float = 0.4) -> Dict:
        try:
            result = DeepFace.verify(
                img1_path=img1_path,
                img2_path=img2_path,
                model_name=self.model_name,
                detector_backend=self.detector_backend,
                enforce_detection=True
            )
            return {
                "verified": result["verified"],
                "distance": result["distance"],
                "threshold": result["threshold"],
                "confidence": 1 - result["distance"]
            }
        except Exception as e:
            raise ValueError(f"Could not verify faces: {str(e)}")

    def find_face(self, query_path: str, db_embeddings: List[Dict], threshold: float = 0.4) -> Dict:
        try:
            query_emb = np.array(self.extract_embedding(query_path))
            best_match = None
            best_distance = float('inf')

            for record in db_embeddings:
                stored_emb = np.array(record["embedding"])
                distance = np.linalg.norm(query_emb - stored_emb)

                if distance < best_distance:
                    best_distance = distance
                    best_match = record

            is_match = best_match is not None and best_distance < threshold

            return {
                "match": is_match,
                "user_id": best_match["user_id"] if is_match else None,
                "distance": float(best_distance),
                "confidence": float(1 - best_distance)
            }
        except Exception as e:
            raise ValueError(f"Could not find face: {str(e)}")

    def analyze_face(self, image_path: str) -> Dict:
        try:
            result = DeepFace.analyze(
                img_path=image_path,
                actions=["age", "gender", "race"],
                detector_backend=self.detector_backend,
                enforce_detection=True
            )
            return {
                "age": result[0]["age"],
                "gender": result[0]["dominant_gender"],
                "race": result[0]["dominant_race"],
                "emotion": result[0].get("dominant_emotion")
            }
        except Exception as e:
            raise ValueError(f"Could not analyze face: {str(e)}")


face_engine = FaceEngine()
