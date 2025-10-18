from database.connection import execute_query

class VeiculoModel:
    @staticmethod
    def cadastrar(placa, capacidade, id_motorista=None):
        """Cadastra um novo veículo"""
        try:
            sql = """
            INSERT INTO veiculo (placa, capacidade, status, id_motorista) 
            VALUES (%s, %s, 'DISPONIVEL', %s)
            """
            params = (placa, capacidade, id_motorista)
            
            result = execute_query(sql, params)
            
            # Ajuste no retorno para ser consistente
            if result:
                return result, "Veículo cadastrado com sucesso"
            else:
                return None, "Erro ao cadastrar veículo"
                
        except Exception as e:
            return None, f"Erro: {str(e)}"

    @staticmethod
    def listar_veiculos():
        """Lista todos os veículos"""
        try:
            sql = """
            SELECT v.*, u.nome as motorista_nome 
            FROM veiculo v 
            LEFT JOIN motorista m ON v.id_motorista = m.id_motorista 
            LEFT JOIN usuario u ON m.id_usuario = u.id_usuario
            """
            result = execute_query(sql, fetch_all=True)
            return result if result else []
        except Exception as e:
            print(f"Erro ao listar veículos: {str(e)}")
            return []

    @staticmethod
    def atualizar_status(id_veiculo, status):
        """Atualiza o status de um veículo"""
        try:
            sql = "UPDATE veiculo SET status = %s WHERE id_veiculo = %s"
            result = execute_query(sql, (status, id_veiculo))
            return result is not None
        except Exception as e:
            print(f"Erro ao atualizar status: {str(e)}")
            return False

    @staticmethod
    def buscar_por_id(id_veiculo):
        """Busca um veículo pelo ID"""
        try:
            sql = """
            SELECT v.*, u.nome as motorista_nome 
            FROM veiculo v 
            LEFT JOIN motorista m ON v.id_motorista = m.id_motorista 
            LEFT JOIN usuario u ON m.id_usuario = u.id_usuario
            WHERE v.id_veiculo = %s
            """
            return execute_query(sql, (id_veiculo,), fetch_one=True)
        except Exception as e:
            print(f"Erro ao buscar veículo: {str(e)}")
            return None