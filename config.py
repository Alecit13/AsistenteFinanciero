# config.py
import os
from dotenv import load_dotenv
import logging

# Carga variables de entorno desde .env
load_dotenv()

# ========== LOGGING ==========
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("finanzas_app")

# ========== TWILIO ==========
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")  # para validar firma si quieres
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

# ========== SUPABASE ==========
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", SUPABASE_ANON_KEY)

# Usuario por defecto (tu UUID de la tabla usuarios)
DEFAULT_USER_ID = os.getenv(
    "DEFAULT_USER_ID",
    "c6f4a4b6-1234-45ab-b0a2-88ac4ed4d111"
)
