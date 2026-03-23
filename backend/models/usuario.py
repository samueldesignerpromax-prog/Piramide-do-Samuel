from dataclasses import dataclass, field


@dataclass
class Usuario:
    id: int
    nome: str
    email: str
    cursos_comprados: list[int] = field(default_factory=list)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "cursos_comprados": self.cursos_comprados
        }
