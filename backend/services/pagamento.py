from uuid import uuid4


class PagamentoService:
    def processar_pagamento(self, venda):
        venda.aprovar_pagamento()

        return {
            "aprovado": True,
            "transacao_id": uuid4().hex[:12]
        }
