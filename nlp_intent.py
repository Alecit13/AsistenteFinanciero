# nlp_intent.py
import os
import json
import torch
import logging
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from huggingface_hub import hf_hub_download

logger = logging.getLogger(__name__)

# ========== RUTA DEL MODELO ==========
INTENT_MODEL_PATH = "Alecit1234/modelo_intenciones"

logger.info("Cargando modelo de intenciones desde HuggingFace Hub: %s", INTENT_MODEL_PATH)

# ========== CARGA DEL MODELO ==========
tokenizer_int = AutoTokenizer.from_pretrained(
    INTENT_MODEL_PATH,
    use_auth_token=os.getenv("HUGGINGFACE_AUTH_TOKEN")
)

model_int = AutoModelForSequenceClassification.from_pretrained(
    INTENT_MODEL_PATH,
    use_auth_token=os.getenv("HUGGINGFACE_AUTH_TOKEN")
)

# ========== LABEL MAP ==========
label_map_path = hf_hub_download(
    repo_id=INTENT_MODEL_PATH,
    filename="label_map.json",
    use_auth_token=os.getenv("HUGGINGFACE_AUTH_TOKEN")
)

with open(label_map_path, "r", encoding="utf-8") as f:
    INTENT_LABEL_MAP = json.load(f)


# ========== FUNCIÓN PRINCIPAL ==========
def predecir_intencion(texto: str) -> str:
    """Predice intención de un texto usando modelo de clasificación."""
    if not texto or texto.strip() == "":
        logger.warning("[INTENT] Texto vacío recibido. Asignando intención 'otros'.")
        return "otros"

    logger.debug("[INTENT] Texto de entrada: %s", texto)

    inputs = tokenizer_int(
        texto,
        return_tensors="pt",
        truncation=True,
        max_length=64,
        padding="max_length"
    )

    with torch.no_grad():
        logits = model_int(**inputs).logits
        pred_id = torch.argmax(logits, dim=1).item()

    intent = INTENT_LABEL_MAP[str(pred_id)]

    logger.info("[INTENT] Predicción: %s (id=%s)", intent, pred_id)
    return intent
