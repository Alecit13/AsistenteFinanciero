# app_whatsapp.py
from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
from core_pipeline import procesar_mensaje
from config import logger

app = FastAPI(title="Asistente Financiero WhatsApp")

# Twilio manda POST x-www-form-urlencoded a este endpoint
# Configura tu webhook en Twilio:  https://TU-SERVIDOR/ngrok/etc/whatsapp


@app.post("/whatsapp", response_class=PlainTextResponse)
async def whatsapp_webhook(
    Body: str = Form(...),
    From: str = Form(None),
    WaId: str = Form(None),
):
    """
    Webhook de Twilio WhatsApp.
    Body = mensaje de texto
    From = número del usuario (whatsapp:+51...)
    WaId = ID de WhatsApp del usuario
    """
    logger.info("===== WhatsApp WEBHOOK =====")
    logger.info("From: %s | WaId: %s | Body: %s", From, WaId, Body)

    resultado = procesar_mensaje(Body)
    respuesta_texto = resultado["respuesta"]

    # Respondemos en texto plano (Twilio lo acepta),
    # si quieres TwiML puedes devolver XML.
    return respuesta_texto
