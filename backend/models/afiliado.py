from dataclasses import dataclass


@dataclass
class Afiliado:
    id: int
    nome: str
    comissao_percentual: float
    saldo: float = 0.0
    total_vendas: int = 0

    def registrar_comissao(self, valor: float):
        self.saldo += valor
        self.total_vendas += 1

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "comissao_percentual": self.comissao_percentual,
            "saldo": round(self.saldo, 2),
            "total_vendas": self.total_vendas
        }
