from models import Afiliado


class AfiliadoService:
    def __init__(self):
        self.afiliados: dict[int, Afiliado] = {}
        self.proximo_id = 1

    def cadastrar_afiliado(self, nome: str, comissao: float = 30.0) -> Afiliado:
        afiliado = Afiliado(
            id=self.proximo_id,
            nome=nome,
            comissao_percentual=comissao
        )
        self.afiliados[self.proximo_id] = afiliado
        self.proximo_id += 1
        return afiliado

    def get_afiliado(self, afiliado_id: int):
        return self.afiliados.get(afiliado_id)

    def listar_afiliados(self):
        return list(self.afiliados.values())
