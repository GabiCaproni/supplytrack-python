from models.veiculo import VeiculoModel

class VeiculoController:
    @staticmethod
    def criar_veiculo(placa, capacidade, id_motorista=None):
        """Cria um novo veículo"""
        try:
            # Validações básicas
            if not placa or not capacidade:
                return False, "Placa e capacidade são obrigatórios"
            
            # Chamar o modelo para cadastrar
            veiculo_id, mensagem = VeiculoModel.cadastrar(placa, capacidade, id_motorista)
            
            if veiculo_id:
                return True, {
                    'id_veiculo': veiculo_id,
                    'message': mensagem
                }
            else:
                return False, mensagem
                
        except Exception as e:
            print(f"Erro no VeiculoController: {e}")
            return False, f"Erro interno: {str(e)}"

    @staticmethod
    def listar_veiculos():
        """Lista todos os veículos"""
        try:
            veiculos = VeiculoModel.listar_veiculos()
            return True, veiculos
        except Exception as e:
            print(f"Erro ao listar veículos: {e}")
            return False, f"Erro ao listar veículos: {str(e)}"