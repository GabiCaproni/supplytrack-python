from models.carga import CargaModel

class CargaController:
    @staticmethod
    def criar_carga(volume, peso, id_armazem, status='PENDENTE', localizacao=None):
        """Cria uma nova carga"""
        try:
            print(f"Controller - Volume: {volume}, Peso: {peso}, Armazém: {id_armazem}, Status: {status}, Localização: {localizacao}")
            
            # Validações básicas
            if not volume or not peso:
                return False, "Volume e peso são obrigatórios"
            
            if not id_armazem:
                return False, "Armazém é obrigatório"
            
            # Chamar o modelo para cadastrar
            carga_id, mensagem = CargaModel.cadastrar(volume, peso, id_armazem, status, localizacao)
            
            if carga_id:
                return True, {
                    'id_carga': carga_id,
                    'message': mensagem
                }
            else:
                return False, mensagem
                
        except Exception as e:
            print(f"Erro no CargaController: {e}")
            return False, f"Erro interno: {str(e)}"

    @staticmethod
    def listar_cargas():
        """Lista todas as cargas"""
        try:
            cargas = CargaModel.listar_cargas()
            return True, cargas
        except Exception as e:
            print(f"Erro ao listar cargas: {e}")
            return False, f"Erro ao listar cargas: {str(e)}"

    @staticmethod
    def atualizar_status(id_carga, status):
        """Atualiza status da carga"""
        try:
            if not id_carga or not status:
                return False, "ID da carga e status são obrigatórios"
            
            success, mensagem = CargaModel.atualizar_status(id_carga, status)
            return success, mensagem
        except Exception as e:
            print(f"Erro ao atualizar status da carga: {e}")
            return False, f"Erro interno: {str(e)}"

    @staticmethod
    def atualizar_localizacao(id_carga, localizacao):
        """Atualiza localização da carga"""
        try:
            if not id_carga:
                return False, "ID da carga é obrigatório"
            
            success, mensagem = CargaModel.atualizar_localizacao(id_carga, localizacao)
            return success, mensagem
        except Exception as e:
            print(f"Erro ao atualizar localização da carga: {e}")
            return False, f"Erro interno: {str(e)}"
        