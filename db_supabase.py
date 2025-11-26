# db_supabase.py
from supabase import create_client, Client
from datetime import date
from typing import Optional
from config import SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, DEFAULT_USER_ID, logger

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


def get_or_create_categoria(nombre: str, tipo: str = "gasto") -> Optional[int]:
    """
    Busca una categoría por nombre (case insensitive).
    Si no existe, la crea.
    Devuelve id_categoria o None si algo falla.
    """
    logger.info("[DB] get_or_create_categoria: %s (%s)", nombre, tipo)

    try:
        res = (
            supabase.table("categorias")
            .select("id_categoria")
            .eq("id_usuario", DEFAULT_USER_ID)
            .ilike("nombre_categoria", nombre)
            .execute()
        )
        data = res.data or []
        if data:
            return data[0]["id_categoria"]

        # Crear nueva categoría
        insert_res = (
            supabase.table("categorias")
            .insert(
                {
                    "id_usuario": DEFAULT_USER_ID,
                    "nombre_categoria": nombre,
                    "tipo_categoria": "ingreso" if tipo.startswith("ingreso") else "gasto",
                    "descripcion": f"Creada automáticamente para {nombre}",
                }
            )
            .execute()
        )
        return insert_res.data[0]["id_categoria"]
    except Exception as e:
        logger.error("[DB] Error get_or_create_categoria: %s", e, exc_info=True)
        return None


def insertar_gasto(monto: float, categoria_str: str, fecha_str: Optional[str], descripcion: str):
    logger.info("[DB] Insertar gasto: monto=%s, cat=%s, fecha=%s", monto, categoria_str, fecha_str)

    id_categoria = get_or_create_categoria(categoria_str, tipo="gasto")

    payload = {
        "id_usuario": DEFAULT_USER_ID,
        "id_categoria": id_categoria,
        "id_tipo": 2,  # por ahora, por defecto "Variable"
        "monto": monto,
        "descripcion": descripcion,
    }

    if fecha_str:
        payload["fecha"] = fecha_str
    else:
        payload["fecha"] = str(date.today())

    try:
        supabase.table("gastos").insert(payload).execute()
        logger.info("[DB] Gasto insertado correctamente.")
    except Exception as e:
        logger.error("[DB] Error al insertar gasto: %s", e, exc_info=True)


def insertar_ingreso(monto: float, categoria_ingreso: str, fecha_str: Optional[str], descripcion: str):
    logger.info("[DB] Insertar ingreso: monto=%s, cat=%s, fecha=%s", monto, categoria_ingreso, fecha_str)

    id_categoria = get_or_create_categoria(categoria_ingreso, tipo="ingreso")

    payload = {
        "id_usuario": DEFAULT_USER_ID,
        "id_categoria": id_categoria,
        "monto": monto,
        "descripcion": descripcion,
    }

    if fecha_str:
        payload["fecha"] = fecha_str
    else:
        payload["fecha"] = str(date.today())

    try:
        supabase.table("ingresos").insert(payload).execute()
        logger.info("[DB] Ingreso insertado correctamente.")
    except Exception as e:
        logger.error("[DB] Error al insertar ingreso: %s", e, exc_info=True)
