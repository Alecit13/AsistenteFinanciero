# nlp_category.py
import os
import logging
import unicodedata
from setfit import SetFitModel

logger = logging.getLogger(__name__)

# ======================
# 1. Cargar modelo SetFit
# ======================

SETFIT_MODEL_PATH = "Alecit1234/modelo_finanzas_peru_v1"

logger.info("Cargando modelo SetFit desde HuggingFace...")

model_setfit = SetFitModel.from_pretrained(
    SETFIT_MODEL_PATH,
    use_auth_token=os.getenv("HUGGINGFACE_AUTH_TOKEN")
)

logger.info("Modelo SetFit cargado correctamente.")


# ===========================
# 2. Categorías (Label Map)
# ===========================

CATEGORY_LABEL_MAP = {
    0:"comida", 1:"supermercado", 2:"transporte", 3:"taxi", 4:"entretenimiento",
    5:"educacion", 6:"tecnologia", 7:"servicios", 8:"fitness", 9:"imprevistos",
    10:"delivery", 11:"mascotas", 12:"familia", 13:"salud",
    14:"ingreso_beca", 15:"ingreso_trabajo", 16:"ingreso_familia",
    17:"ingreso_venta", 18:"ingreso_freelance", 19:"ingreso_extra"
}


# ======================
# 3. Normalizar texto
# ======================

def _normalizar(texto: str) -> str:
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


# ======================
# 4. Predicción categoría
# ======================

def predecir_categoria(texto: str) -> str:
    """
    Predice categoría usando SOLO el texto completo.
    NER aporta monto y fecha, pero NO categoría.
    """

    if not texto or texto.strip() == "":
        logger.warning("Texto vacío recibido en predecir_categoria()")
        return "otros"

    texto_norm = _normalizar(texto)

    logger.debug(f"[SETFIT] Texto normalizado: {texto_norm}")

    pred_id = model_setfit.predict([texto_norm])[0].item()
    categoria = CATEGORY_LABEL_MAP[pred_id]

    logger.info(f"[SETFIT] Categoría predicha: {categoria} (id={pred_id})")

    return categoria
