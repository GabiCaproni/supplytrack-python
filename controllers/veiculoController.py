from models.veiculo import VeiculoModel
from models.motorista import MotoristaModel

class VeiculoController:
    @staticmethod
    def cadastrar_veiculo(dados):
        """
        Cadastra um novo veículo com validações
        """
        try:
            placa = dados.get('placa')
            capacidade = dados.get('capacidade')
            u_motorista = dados.get('u_motorista')
            status = dados.get('status', 'DISPONIVEL')
            
            # Validações
            if not placa or not capacidade:
                return False, "Placa e capacidade são obrigatórios"
            
            # Validar formato da placa (exemplo básico)
            if len(placa) < 6:
                return False, "Placa inválida"
            
            # Verificar se motorista existe (se fornecido)
            if u_motorista:
                motorista = MotoristaModel.buscar_por_id(u_motorista)
                if not motorista:
                    return False, "Motorista não encontrado"
            
            # Cadastrar veículo
            veiculo_id, mensagem = VeiculoModel.cadastrar(
                placa, capacidade, u_motorista, status
            )
            
            if veiculo_id:
                return True, {
                    'message': mensagem,
                    'veiculo_id': veiculo_id
                }
            else:
                return False, mensagem
            
                
        except Exception as e:
            return False, f"Erro no cadastro: {str(e)}"

    @staticmethod
    def listar_veiculos(filtro_status=None):
        """
        Lista veículos com filtro opcional por status
        """
        try:
            veiculos = VeiculoModel.listar_veiculos()
            
            if filtro_status:
                veiculos = [v for v in veiculos if v['status'] == filtro_status]
            
            return True, veiculos
        except Exception as e:
            return False, f"Erro ao listar veículos: {str(e)}"

    @staticmethod
    def atualizar_status_veiculo(u_veiculo, novo_status):
        """
        Atualiza status do veículo
        """
        try:
            success, message = VeiculoModel.atualizar_status(u_veiculo, novo_status)
            return success, message
        except Exception as e:
            return False, f"Erro ao atualizar status: {str(e)}"

    @staticmethod
    def get_veiculos_disponiveis():
        """
        Retorna veículos disponíveis para novas rotas
        """
        try:
            veiculos = VeiculoModel.buscar_veiculos_disponiveis()
            return True, veiculos
        except Exception as e:
            return False, f"Erro ao buscar veículos disponíveis: {str(e)}"