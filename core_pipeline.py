# core_pipeline.py
from typing import Dict, Any
from config import logger
from nlp_intent import predecir_intencion
from nlp_ner import extraer_entidades
from nlp_category import predecir_categoria
from db_supabase import insertar_gasto, insertar_ingreso
import re


def _parse_monto_str(monto_str: str) -> float:
    # Extrae número de algo como "50", "50.00", "S/ 50.90"
    if not monto_str:
        return 0.0
    numeros = re.findall(r"\d+[.,]?\d*", monto_str)
    if not numeros:
        return 0.0
    valor = numeros[0].replace(",", ".")
    try:
        return float(valor)
    except ValueError:
        return 0.0


def procesar_mensaje(texto: str) -> Dict[str, Any]:
    """
    Pipeline completo:
      1. Predice intención
      2. Extrae entidades (monto, fecha)
      3. Predice categoría usando SetFit con el TEXTO COMPLETO
      4. Aplica acción en Supabase según intención
      5. Devuelve dict con info + mensaje para usuario
    """
    logger.info("==== Procesando mensaje ====")
    logger.info("Texto: %s", texto)

    # 1. INTENCIÓN
    intencion = predecir_intencion(texto)

    # 2. ENTIDADES
    ents = extraer_entidades(texto)
    monto = _parse_monto_str(ents.get("monto"))
    fecha = ents.get("fecha")

    # 3. CATEGORÍA (texto completo, no la categoria_texto de NER)
    categoria_final = predecir_categoria(texto)

    # 4. LÓGICA DE NEGOCIO
    respuesta = ""

    if intencion == "agregar_gasto":
        insertar_gasto(
            monto=monto,
            categoria_str=categoria_final,
            fecha_str=fecha,
            descripcion=texto
        )
        respuesta = f"Anoté un gasto de S/ {monto:.2f} en la categoría '{categoria_final}'."

    elif intencion == "agregar_ingreso":
        insertar_ingreso(
            monto=monto,
            categoria_ingreso=categoria_final,
            fecha_str=fecha,
            descripcion=texto
        )
        respuesta = f"Registré un ingreso de S/ {monto:.2f} como '{categoria_final}'."

    elif intencion == "agregar_aporte":
        # TODO: integrar con metas_ahorro
        respuesta = "Detecté que quieres registrar un aporte a una meta de ahorro. Aún no he sido conectado a metas_ahorro 😅."

    elif intencion == "puedo_gastar":
        # TODO: leer presupuestos_mensuales y responder según límites
        respuesta = "Según tu presupuesto, todavía no tengo conectada la lógica para validar si puedes gastar eso 😅, pero la intención está detectada."

    else:
        respuesta = f"Detecté intención '{intencion}' con categoría '{categoria_final}', pero aún no tengo lógica asociada."

    logger.info("[PIPELINE] Resultado: intencion=%s, monto=%s, categoria=%s, fecha=%s",
                intencion, monto, categoria_final, fecha)

    return {
        "intencion": intencion,
        "monto": monto,
        "categoria_final": categoria_final,
        "fecha": fecha,
        "respuesta": respuesta,
    }
