from dataclasses import dataclass, field
from datetime import datetime

from .afiliado import Afiliado
from .curso import Curso
from .usuario import Usuario


@dataclass
class Venda:
    id: int
    usuario: Usuario
    curso: Curso
    afiliado: Afiliado | None = None
    status: str = "pendente"
    criado_em: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    @property
    def valor_total(self) -> float:
        return self.curso.preco

    def aprovar_pagamento(self) -> float:
        self.status = "aprovado"
        comissao = 0.0

        if self.afiliado:
            comissao = self.valor_total * (self.afiliado.comissao_percentual / 100)
            self.afiliado.registrar_comissao(comissao)

        return round(comissao, 2)

    def to_dict(self):
        return {
            "id": self.id,
            "status": self.status,
            "criado_em": self.criado_em,
            "valor_total": round(self.valor_total, 2),
            "usuario": self.usuario.to_dict(),
            "curso": self.curso.to_dict(),
            "afiliado": self.afiliado.to_dict() if self.afiliado else None
        }
