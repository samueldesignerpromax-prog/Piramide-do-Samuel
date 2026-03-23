from flask import Blueprint, jsonify, request

webhook_bp = Blueprint("webhooks", __name__, url_prefix="/webhook")


@webhook_bp.post("/pagamento")
def webhook_pagamento():
    data = request.get_json(silent=True) or {}
    return jsonify({
        "ok": True,
        "tipo": "pagamento",
        "payload_recebido": data
    })


@webhook_bp.post("/afiliado")
def webhook_afiliado():
    data = request.get_json(silent=True) or {}
    return jsonify({
        "ok": True,
        "tipo": "afiliado",
        "payload_recebido": data
    })
