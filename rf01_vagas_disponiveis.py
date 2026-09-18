from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict

class TipoUsuario(Enum):
    ALUNO = "aluno"
    FUNCIONARIO = "funcionario"
    VISITANTE = "visitante"

class TipoVaga(Enum):
    GERAL = "geral"
    FUNCIONARIO = "funcionario"
    PCD = "pcd"
    CARRO_ELETRICO = "carro_eletrico"

@dataclass
class Vaga:
    id_vaga: int
    setor: str
    is_ocupada: bool = False
    tipo: TipoVaga = TipoVaga.GERAL
    
    @property
    def is_reservada_funcionario(self) -> bool:
        """Facilitador para checar se é reservada a funcionários."""
        return self.tipo == TipoVaga.FUNCIONARIO

    @property
    def cor_mapa(self) -> str:
        """Atende ao Critério de Aceitação 3: Cor diferenciada no mapa."""
        if self.tipo == TipoVaga.FUNCIONARIO:
            return "#FF9800"  # Laranja (Alerta)
        elif self.tipo == TipoVaga.PCD:
            return "#2196F3"  # Azul
        return "#4CAF50"      # Verde (Geral/Disponível)


class ValidadorReservaService:
    """Regra de negócio para validar seleção e destino de vagas."""
    
    @staticmethod
    def selecionar_vaga(vaga: Vaga, usuario: TipoUsuario) -> dict:
        """
        Atende aos Critérios 1 e 2:
        - Exibe alerta visual ao clicar na vaga (CA1)
        - Emite mensagem de aviso ao tentar confirmar como destino (CA2)
        """
        resultado = {
            "vaga_id": vaga.id_vaga,
            "cor_exibicao": vaga.cor_mapa,
            "pode_estacionar": True,
            "alerta_visual": None,
            "mensagem_aviso": None
        }

        # Regra para Vagas de Funcionários
        if vaga.is_reservada_funcionario and usuario == TipoUsuario.ALUNO:
            resultado["pode_estacionar"] = False
            # Critério 1: Alerta visual destacando a restrição
            resultado["alerta_visual"] = {
                "tipo": "RESTRIÇÃO_ACESSO",
                "titulo": "Vaga Exclusiva",
                "icone": "icone_lock_funcionario"
            }
            # Critério 2: Mensagem de aviso ao selecionar/confirmar destino
            resultado["mensagem_aviso"] = (
                "Esta vaga é reservada exclusivamente para funcionários. "
                "Alunos que estacionarem aqui estão sujeitos a penalidades."
            )

        return resultado