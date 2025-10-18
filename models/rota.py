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
            
            # Correção no retorno - removendo a tupla duplicada
            if rota_id:
                return rota_id, "Rota criada com sucesso"
            else:
                return None, "Erro ao criar rota"
                
        except Exception as e:
            return None, f"Erro: {str(e)}"

    @staticmethod
    def listar_rotas():
        """Lista todas as rotas"""
        try:
            sql = """
            SELECT r.*, v.placa, u.nome as motorista_nome 
            FROM rota r 
            LEFT JOIN veiculo v ON r.id_veiculo = v.id_veiculo 
            LEFT JOIN motorista m ON r.id_motorista = m.id_motorista 
            LEFT JOIN usuario u ON m.id_usuario = u.id_usuario
            ORDER BY r.DataSaida DESC
            """
            result = execute_query(sql, fetch_all=True)
            return result if result else []
        except Exception as e:
            print(f"Erro ao listar rotas: {str(e)}")
            return []

    @staticmethod
    def atualizar_status_rota(id_rota, status):
        """Atualiza o status de uma rota"""
        try:
            sql = "UPDATE rota SET status = %s WHERE idRota = %s"
            result = execute_query(sql, (status, id_rota))
            return result is not None
        except Exception as e:
            print(f"Erro ao atualizar status da rota: {str(e)}")
            return False

    @staticmethod
    def criar_entrega(id_rota, data_prevista, id_motorista):
        """Cria uma entrega para uma rota"""
        try:
            sql = """
            INSERT INTO entrega (idRota, dataPrevista, status, id_motorista) 
            VALUES (%s, %s, 'PENDENTE', %s)
            """
            result = execute_query(sql, (id_rota, data_prevista, id_motorista))
            
            # Retorno consistente
            if result:
                return result, "Entrega criada com sucesso"
            else:
                return None, "Erro ao criar entrega"
                
        except Exception as e:
            return None, f"Erro ao criar entrega: {str(e)}"

    @staticmethod
    def buscar_por_id(id_rota):
        """Busca uma rota pelo ID"""
        try:
            sql = """
            SELECT r.*, v.placa, u.nome as motorista_nome 
            FROM rota r 
            LEFT JOIN veiculo v ON r.id_veiculo = v.id_veiculo 
            LEFT JOIN motorista m ON r.id_motorista = m.id_motorista 
            LEFT JOIN usuario u ON m.id_usuario = u.id_usuario
            WHERE r.idRota = %s
            """
            return execute_query(sql, (id_rota,), fetch_one=True)
        except Exception as e:
            print(f"Erro ao buscar rota: {str(e)}")
            return None

    @staticmethod
    def adicionar_carga_rota(id_rota, id_carga):
        """Adiciona uma carga à rota"""
        try:
            sql = "INSERT INTO rota_carga (idRota, id_carga) VALUES (%s, %s)"
            result = execute_query(sql, (id_rota, id_carga))
            return result is not None
        except Exception as e:
            print(f"Erro ao adicionar carga à rota: {str(e)}")
            return False