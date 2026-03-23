from dataclasses import dataclass


@dataclass
class Curso:
    id: int
    nome: str
    preco: float
    descricao: str
    slug: str
    categoria: str = "Geral"
    carga_horaria: str = "40h"
    imagem: str | None = None

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "preco": round(self.preco, 2),
            "descricao": self.descricao,
            "slug": self.slug,
            "categoria": self.categoria,
            "carga_horaria": self.carga_horaria,
            "imagem": self.imagem
        }
