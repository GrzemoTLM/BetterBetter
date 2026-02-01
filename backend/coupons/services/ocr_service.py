import logging
from pathlib import Path
from typing import Union, Dict, Any
from PIL import Image

logger = logging.getLogger(__name__)

PADDLE_AVAILABLE = False

try:
    from paddleocr import PaddleOCR
    PADDLE_AVAILABLE = True
    logger.info("PaddleOCR is available")
except ImportError:
    logger.warning("PaddleOCR not available")


class OCRService:

    def __init__(self, use_gpu: bool = False, backend: str = 'auto'):
        self.backend = None
        self.ocr = None
        self.use_gpu = use_gpu

        if not PADDLE_AVAILABLE:
            raise Exception("PaddleOCR not available. Install: pip install paddleocr")
        self._init_paddle()

    def _init_paddle(self):
        try:
            self.ocr = PaddleOCR(
                use_textline_orientation=True,
                lang='en'
            )
            self.backend = 'paddle'
            logger.info("PaddleOCR initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing PaddleOCR: {str(e)}")
            raise
    
    def extract_text_from_image(self, image_path: Union[str, Path]) -> str:
        try:
            image_path = Path(image_path)
            
            if not image_path.exists():
                logger.error(f"Image file not found: {image_path}")
                return ""
            
            with Image.open(image_path) as img:
                logger.info(f"Processing image: {image_path} ({self.backend})")

            extracted_text = self._extract_paddle(str(image_path))

            logger.info(f"Text extracted from {image_path}: {len(extracted_text)} characters")
            return extracted_text
            
        except Exception as e:
            logger.error(f"Error extracting text from image {image_path}: {str(e)}")
            raise
    
    def _extract_paddle(self, image_path: str) -> str:
        result = self.ocr.predict(image_path)
        return self._parse_paddle_result(result)

    def _parse_paddle_result(self, ocr_result) -> str:
        text_lines = []
        
        if not ocr_result:
            return ""
        
        for result_item in ocr_result:
            texts = None

            if isinstance(result_item, dict) and 'rec_texts' in result_item:
                texts = result_item['rec_texts']
            elif hasattr(result_item, 'rec_texts'):
                texts = result_item.rec_texts
            elif hasattr(result_item, '__getitem__'):
                try:
                    texts = result_item['rec_texts']
                except (KeyError, TypeError):
                    pass

            if texts:
                for text in texts:
                    if text and text.strip():
                        text_lines.append(text)

        return '\n'.join(text_lines)
    
    def extract_text_with_confidence(self, image_path: Union[str, Path]) -> Dict[str, Any]:
        try:
            image_path = Path(image_path)
            
            if not image_path.exists():
                logger.error(f"Image file not found: {image_path}")
                return {"text": "", "raw_result": [], "success": False}
            
            return self._extract_paddle_with_confidence(str(image_path))

        except Exception as e:
            logger.error(f"Error extracting text with confidence: {str(e)}")
            return {"text": "", "raw_result": [], "success": False, "error": str(e)}

    def _extract_paddle_with_confidence(self, image_path: str) -> Dict[str, Any]:
        result = self.ocr.predict(image_path)

        text_items = []
        total_confidence = 0
        count = 0

        if result:
            for result_item in result:
                texts = None
                scores = None

                if isinstance(result_item, dict):
                    texts = result_item.get('rec_texts', [])
                    scores = result_item.get('rec_scores', [])
                elif hasattr(result_item, 'rec_texts'):
                    texts = result_item.rec_texts
                    scores = result_item.rec_scores if hasattr(result_item, 'rec_scores') else []
                elif hasattr(result_item, '__getitem__'):
                    try:
                        texts = result_item['rec_texts']
                        scores = result_item.get('rec_scores', []) if isinstance(result_item, dict) else result_item.rec_scores
                    except (KeyError, TypeError, AttributeError):
                        pass

                if texts:
                    for idx, text in enumerate(texts):
                        if text and text.strip():
                            confidence = float(scores[idx]) if idx < len(scores) else 1.0
                            text_items.append({
                                'text': text,
                                'confidence': confidence
                            })
                            total_confidence += confidence
                            count += 1

        avg_confidence = total_confidence / count if count > 0 else 0
        extracted_text = '\n'.join([item['text'] for item in text_items])

        return {
            "text": extracted_text,
            "raw_result": text_items,
            "average_confidence": round(avg_confidence, 4),
            "total_items": count,
            "success": True,
            "backend": "paddle"
        }

