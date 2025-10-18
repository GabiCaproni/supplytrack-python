from models.entrega import EntregaModel
from models.motorista import MotoristaModel

class MotoristaController:
    @staticmethod
    def get_entregas_motorista(u_motorista, filtro_status=None):
        """Obtém entregas de um motorista"""
        try:
            # Verificar se motorista existe
            motorista = MotoristaModel.buscar_por_id(u_motorista)
            if not motorista:
                return False, "Motorista não encontrado"
            
            entregas = EntregaModel.listar_entregas_motorista(u_motorista, filtro_status)
            return True, entregas
            
        except Exception as e:
            return False, f"Erro ao buscar entregas: {str(e)}"

    @staticmethod
    def atualizar_status_entrega(u_motorista, identrega, novo_status, observacoes=None):
        """
        Atualiza status da entrega com todas as validações
        """
        try:
            # Verificar se motorista existe
            motorista = MotoristaModel.buscar_por_id(u_motorista)
            if not motorista:
                return False, "Motorista não encontrado"
            
            # Atualizar status
            success, message = EntregaModel.atualizar_status_motorista(
                identrega, u_motorista, novo_status, observacoes
            )
            
            return success, message
            
        except Exception as e:
            return False, f"Erro ao atualizar status: {str(e)}"

    @staticmethod
    def simular_viagem(u_motorista, identrega):
        """
        Simula o processo completo de uma viagem para testes
        """
        try:
            resultados = []
            
            # 1. Iniciar viagem
            success, message = MotoristaController.atualizar_status_entrega(
                u_motorista, identrega, 'EM_TRANSITO', 'Viagem iniciada'
            )
            resultados.append(f"1. Iniciar viagem: {'✅' if success else '❌'} {message}")
            
            if not success:
                return False, resultados
            
            # 2. Simular problema (opcional)
            import random
            if random.choice([True, False]):
                success, message = MotoristaController.atualizar_status_entrega(
                    u_motorista, identrega, 'PROBLEMA', 'Trânsito intenso'
                )
                resultados.append(f"2. Reportar problema: {'✅' if success else '❌'} {message}")
                
                # 3. Retomar viagem após problema
                success, message = MotoristaController.atualizar_status_entrega(
                    u_motorista, identrega, 'EM_TRANSITO', 'Problema resolvido'
                )
                resultados.append(f"3. Retomar viagem: {'✅' if success else '❌'} {message}")
            
            # 4. Finalizar entrega
            success, message = MotoristaController.atualizar_status_entrega(
                u_motorista, identrega, 'ENTREGUE', 'Entrega concluída com sucesso'
            )
            resultados.append(f"4. Finalizar entrega: {'✅' if success else '❌'} {message}")
            
            return True, resultados
            
        except Exception as e:
            return False, [f"❌ Erro na simulação: {str(e)}"]