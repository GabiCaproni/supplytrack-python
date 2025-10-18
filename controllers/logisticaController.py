from models.carga import CargaModel
from models.rota import RotaModel
from models.entrega import EntregaModel
from models.veiculo import VeiculoModel
from models.motorista import MotoristaModel

class LogisticaController:
    @staticmethod
    def registrar_carga_e_roteirizar(dados):
        """
        Processo completo: Registra carga e cria rota/entrega
        Versão CORRIGIDA para MER
        """
        try:
            # Dados da carga
            volume = dados.get('volume')
            peso = dados.get('peso')
            idarmazem = dados.get('idarmazem')
            
            # Dados da entrega
            dataprevista = dados.get('dataprevista')
            origem = dados.get('origem')
            destino = dados.get('destino')
            u_veiculo = dados.get('u_veiculo')
            u_motorista = dados.get('u_motorista')
            
            # Validações básicas
            if not all([volume, peso, dataprevista, origem, destino, u_veiculo, u_motorista]):
                return False, "Todos os campos são obrigatórios"
            
            # 1. Registrar carga
            carga_id, mensagem_carga = CargaModel.registrar_carga(
                volume, peso, idarmazem, 'NO_ARMAZEM', origem
            )
            if not carga_id:
                return False, f"Erro na carga: {mensagem_carga}"
            
            # 2. Criar rota
            rota_id, mensagem_rota = RotaModel.criar_rota(
                origem, destino, 
                dados.get('distancia_km'),
                dados.get('tempo_estimado'),
                'PLANEJADA'
            )
            if not rota_id:
                # Rollback: excluir carga se rota falhar
                CargaModel.excluir(carga_id)
                return False, f"Erro na rota: {mensagem_rota}"
            
            # 3. Criar entrega
            entrega_id, mensagem_entrega = EntregaModel.criar_entrega(
                dataprevista, rota_id, u_veiculo, u_motorista, carga_id, 'PENDENTE'
            )
            if not entrega_id:
                # Rollback: excluir carga e rota se entrega falhar
                CargaModel.excluir(carga_id)
                RotaModel.excluir(rota_id)
                return False, f"Erro na entrega: {mensagem_entrega}"
            
            return True, {
                'message': 'Processo concluído com sucesso',
                'ids': {
                    'carga_id': carga_id,
                    'rota_id': rota_id,
                    'entrega_id': entrega_id
                }
            }
            
        except Exception as e:
            return False, f"Erro no processo: {str(e)}"

    @staticmethod
    def listar_entregas_ativas():
        """Lista entregas em andamento"""
        try:
            entregas = EntregaModel.listar_entregas('EM_TRANSITO')
            return True, entregas
        except Exception as e:
            return False, f"Erro ao listar entregas: {str(e)}"

    @staticmethod
    def atualizar_status_entrega(identrega, novo_status):
        """Atualiza status da entrega e recursos relacionados"""
        try:
            # Implementar lógica de atualização em cadeia
            # (atualizar carga, veículo, etc. conforme status)
            return True, "Status atualizado"
        except Exception as e:
            return False, f"Erro ao atualizar status: {str(e)}"