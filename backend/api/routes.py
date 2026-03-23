from flask import Blueprint, jsonify, request

from models import Usuario, Curso, Venda
from services import ChatbotIA, PagamentoService, AfiliadoService

api_bp = Blueprint("api", __name__, url_prefix="/api")

chatbot = ChatbotIA()
pagamento_service = PagamentoService()
afiliado_service = AfiliadoService()

usuarios: dict[int, Usuario] = {}
vendas: dict[int, Venda] = {}
next_usuario_id = 1
next_venda_id = 1

cursos: dict[int, Curso] = {
    1: Curso(
        id=1,
        nome="Marketing Digital",
        preco=497.00,
        descricao="Aprenda estratégias práticas para vender mais online.",
        slug="marketing-digital",
        categoria="Marketing",
        carga_horaria="40h"
    ),
    2: Curso(
        id=2,
        nome="Python do Zero",
        preco=397.00,
        descricao="Programação Python do básico ao intermediário.",
        slug="python-do-zero",
        categoria="Programação",
        carga_horaria="36h"
    ),
    3: Curso(
        id=3,
        nome="IA para Negócios",
        preco=597.00,
        descricao="Use IA para vender, automatizar e ganhar produtividade.",
        slug="ia-para-negocios",
        categoria="Inteligência Artificial",
        carga_horaria="32h"
    ),
}

afiliado_service.cadastrar_afiliado("João Silva", 30.0)
afiliado_service.cadastrar_afiliado("Maria Santos", 35.0)


def _get_json():
    return request.get_json(silent=True) or {}


def _find_user_by_email(email: str):
    for usuario in usuarios.values():
        if usuario.email.lower() == email.lower():
            return usuario
    return None


@api_bp.get("/health")
def health():
    return jsonify({"ok": True})


@api_bp.get("/cursos")
def listar_cursos():
    return jsonify([curso.to_dict() for curso in cursos.values()])


@api_bp.get("/cursos/<int:curso_id>")
def detalhar_curso(curso_id: int):
    curso = cursos.get(curso_id)
    if not curso:
        return jsonify({"error": "Curso não encontrado"}), 404
    return jsonify(curso.to_dict())


@api_bp.post("/cursos/<int:curso_id>/link-afiliado")
def gerar_link_afiliado(curso_id: int):
    data = _get_json()
    afiliado_id = data.get("afiliado_id")

    curso = cursos.get(curso_id)
    if not curso:
        return jsonify({"error": "Curso não encontrado"}), 404

    if not afiliado_id:
        return jsonify({"error": "afiliado_id é obrigatório"}), 400

    afiliado = afiliado_service.get_afiliado(int(afiliado_id))
    if not afiliado:
        return jsonify({"error": "Afiliado não encontrado"}), 404

    link = chatbot.gerar_link_afiliado(curso.slug, afiliado.id)
    return jsonify({
        "link": link,
        "curso": curso.nome,
        "afiliado": afiliado.nome
    })


@api_bp.route("/chatbot", methods=["GET", "POST"])
def chatbot_message():
    mensagem = ""

    if request.method == "GET":
        mensagem = request.args.get("mensagem", "")
    else:
        data = _get_json()
        mensagem = data.get("mensagem", "")

    resposta = chatbot.responder(mensagem)
    return jsonify({"resposta": resposta})


@api_bp.post("/comprar")
def comprar_curso():
    global next_usuario_id, next_venda_id

    data = _get_json()

    curso_id = data.get("curso_id")
    usuario_nome = (data.get("usuario_nome") or "").strip()
    usuario_email = (data.get("usuario_email") or "").strip()
    afiliado_id = data.get("afiliado_id")

    if not curso_id:
        return jsonify({"error": "curso_id é obrigatório"}), 400
    if not usuario_nome:
        return jsonify({"error": "usuario_nome é obrigatório"}), 400
    if not usuario_email:
        return jsonify({"error": "usuario_email é obrigatório"}), 400

    curso = cursos.get(int(curso_id))
    if not curso:
        return jsonify({"error": "Curso não encontrado"}), 404

    usuario = _find_user_by_email(usuario_email)

    if usuario is None:
        usuario = Usuario(
            id=next_usuario_id,
            nome=usuario_nome,
            email=usuario_email
        )
        usuarios[next_usuario_id] = usuario
        next_usuario_id += 1

    if curso.id in usuario.cursos_comprados:
        return jsonify({"error": "Usuário já possui este curso"}), 400

    afiliado = None
    if afiliado_id:
        afiliado = afiliado_service.get_afiliado(int(afiliado_id))
        if not afiliado:
            return jsonify({"error": "Afiliado não encontrado"}), 404

    venda = Venda(
        id=next_venda_id,
        usuario=usuario,
        curso=curso,
        afiliado=afiliado
    )

    resultado_pagamento = pagamento_service.processar_pagamento(venda)

    if not resultado_pagamento["aprovado"]:
        return jsonify({
            "status": "error",
            "message": "Pagamento não aprovado"
        }), 400

    vendas[next_venda_id] = venda
    usuario.cursos_comprados.append(curso.id)
    next_venda_id += 1

    return jsonify({
        "status": "success",
        "message": "Compra realizada com sucesso",
        "venda": venda.to_dict(),
        "transacao_id": resultado_pagamento["transacao_id"]
    })


@api_bp.get("/afiliados")
def listar_afiliados():
    return jsonify([item.to_dict() for item in afiliado_service.listar_afiliados()])


@api_bp.get("/afiliados/<int:afiliado_id>/saldo")
def saldo_afiliado(afiliado_id: int):
    afiliado = afiliado_service.get_afiliado(afiliado_id)
    if not afiliado:
        return jsonify({"error": "Afiliado não encontrado"}), 404

    return jsonify({
        "id": afiliado.id,
        "nome": afiliado.nome,
        "saldo": afiliado.saldo,
        "total_vendas": afiliado.total_vendas,
        "comissao_percentual": afiliado.comissao_percentual
    })


@api_bp.get("/vendas")
def listar_vendas():
    return jsonify([venda.to_dict() for venda in vendas.values()])
