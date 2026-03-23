class ChatbotIA:
    def __init__(self):
        self.respostas = {
            "preço": "💰 Temos cursos a partir de R$ 397,00.",
            "preco": "💰 Temos cursos a partir de R$ 397,00.",
            "valor": "💰 Temos cursos a partir de R$ 397,00.",
            "certificado": "🎓 Sim, os cursos possuem certificado.",
            "acesso": "🔓 O acesso é liberado logo após a compra aprovada.",
            "garantia": "✅ Temos garantia de 7 dias.",
            "parcelado": "💳 Você pode parcelar conforme a plataforma de pagamento.",
            "parcelamento": "💳 Você pode parcelar conforme a plataforma de pagamento.",
            "afiliado": "🤝 O programa de afiliados paga comissão por venda.",
            "suporte": "💬 Você pode tirar dúvidas sobre cursos, acesso e pagamento."
        }

    def responder(self, mensagem: str) -> str:
        texto = (mensagem or "").strip().lower()

        if not texto:
            return "👋 Manda sua dúvida sobre curso, preço, certificado ou afiliados."

        for chave, resposta in self.respostas.items():
            if chave in texto:
                return resposta

        return (
            "📚 Posso te ajudar com preço, certificado, acesso, suporte e afiliados. "
            "Manda sua dúvida de forma mais específica."
        )

    def gerar_link_afiliado(self, curso_slug: str, afiliado_id: int) -> str:
        return f"https://afiliados-vendas.vercel.app/?curso={curso_slug}&ref={afiliado_id}"
