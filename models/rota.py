from database.connection import execute_query

class RotaModel:
    @staticmethod
    def criar_rota(data_saida, distancia, id_veiculo, id_motorista):
        """Cria uma nova rota"""
        try:
            sql = """
            INSERT INTO rota (DataSaida, distancia, status, id_veiculo, id_motorista) 
            VALUES (%s, %s, 'PENDENTE', %s, %s)
            """
            params = (data_saida, distancia, id_veiculo, id_motorista)
            
            rota_id = execute_query(sql, params)
            return rota_id, "Rota criada com sucesso" if rota_id else (None, "Erro ao criar rota")
            
        except Exception as e:
            return None, f"Erro: {str(e)}"

    @staticmethod
    def listar_rotas():
        sql = """
        SELECT r.*, v.placa, u.nome as motorista_nome 
        FROM rota r 
        LEFT JOIN veiculo v ON r.id_veiculo = v.id_veiculo 
        LEFT JOIN motorista m ON r.id_motorista = m.id_motorista 
        LEFT JOIN usuario u ON m.id_usuario = u.id_usuario
        ORDER BY r.DataSaida DESC
        """
        return execute_query(sql, fetch_all=True) or []

    @staticmethod
    def atualizar_status_rota(id_rota, status):
        sql = "UPDATE rota SET status = %s WHERE idRota = %s"
        return execute_query(sql, (status, id_rota))

    @staticmethod
    def criar_entrega(id_rota, data_prevista, id_motorista):
        """Cria uma entrega para uma rota"""
        sql = """
        INSERT INTO entrega (idRota, dataPrevista, status, id_motorista) 
        VALUES (%s, %s, 'PENDENTE', %s)
        """
        return execute_query(sql, (id_rota, data_prevista, id_motorista))