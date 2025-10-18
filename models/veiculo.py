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
            
            veiculo_id = execute_query(sql, params)
            return veiculo_id, "Veículo cadastrado com sucesso" if veiculo_id else (None, "Erro ao cadastrar veículo")
            
        except Exception as e:
            return None, f"Erro: {str(e)}"

    @staticmethod
    def listar_veiculos():
        sql = """
        SELECT v.*, u.nome as motorista_nome 
        FROM veiculo v 
        LEFT JOIN motorista m ON v.id_motorista = m.id_motorista 
        LEFT JOIN usuario u ON m.id_usuario = u.id_usuario
        """
        return execute_query(sql, fetch_all=True) or []

    @staticmethod
    def atualizar_status(id_veiculo, status):
        sql = "UPDATE veiculo SET status = %s WHERE id_veiculo = %s"
        return execute_query(sql, (status, id_veiculo))