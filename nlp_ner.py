# nlp_ner.py
import os
import json
import logging
import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification
from huggingface_hub import hf_hub_download

logger = logging.getLogger(__name__)

# =====================================
# 1. NOMBRE DEL MODELO EN HUGGINGFACE
# =====================================
NER_MODEL_PATH = "Alecit1234/modelo_ner"

logger.info("Cargando modelo NER desde HuggingFace Hub: %s", NER_MODEL_PATH)

# =====================================
# 2. CARGAR TOKENIZER & MODEL
# =====================================
tokenizer_ner = AutoTokenizer.from_pretrained(
    NER_MODEL_PATH,
    use_auth_token=os.getenv("HUGGINGFACE_AUTH_TOKEN")
)

model_ner = AutoModelForTokenClassification.from_pretrained(
    NER_MODEL_PATH,
    use_auth_token=os.getenv("HUGGINGFACE_AUTH_TOKEN")
)

# =====================================
# 3. CARGAR LABEL_MAP DESDE HF
# =====================================
label_map_path = hf_hub_download(
    repo_id=NER_MODEL_PATH,
    filename="label_map.json",
    use_auth_token=os.getenv("HUGGINGFACE_AUTH_TOKEN")
)

with open(label_map_path, "r", encoding="utf-8") as f:
    NER_LABELS = json.load(f)

logger.info("Etiquetas NER cargadas: %s", NER_LABELS)


# =====================================
# 4. FUNCIÓN: EXTRAER ENTIDADES
# =====================================
def extraer_entidades(texto: str) -> dict:
    """
    Extrae entidades: monto, fecha, categoria_texto (solo referencia)
    """

    logger.debug("[NER] Procesando texto: %s", texto)

    inputs = tokenizer_ner(
        texto,
        return_tensors="pt",
        truncation=True,
        max_length=64
    )

    with torch.no_grad():
        outputs = model_ner(**inputs)

    preds = outputs.logits.argmax(dim=-1)[0].tolist()
    tokens = tokenizer_ner.convert_ids_to_tokens(inputs["input_ids"][0])

    entidades = {"monto": None, "categoria_texto": None, "fecha": None}

    palabra = ""
    tipo_actual = None

    for tok, pred_id in zip(tokens, preds):
        label = NER_LABELS[str(pred_id)]

        # Cuando cambia la etiqueta
        if label == "O":
            if tipo_actual and palabra:
                entidades[tipo_actual] = palabra
            palabra = ""
            tipo_actual = None
            continue

        # Asignación del tipo
        if label == "MONEY":
            tipo_actual = "monto"
        elif label == "CATEGORY":
            tipo_actual = "categoria_texto"
        elif label == "DATE":
            tipo_actual = "fecha"

        palabra += tok.replace("▁", "")

    # Último token acumulado
    if tipo_actual and palabra:
        entidades[tipo_actual] = palabra

    logger.info("[NER] Resultado entidades: %s", entidades)
    return entidades
