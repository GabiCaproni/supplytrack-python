from database.connection import execute_query

class AlertaModel:
    @staticmethod
    def criar_alerta(tipo, descricao, id_rota=None, id_veiculo=None, id_motorista=None):
        """Cria um novo alerta"""
        from datetime import datetime
        
        try:
            sql = """
            INSERT INTO alerta (tipo, horario, status, idRota, id_veiculo, id_motorista) 
            VALUES (%s, %s, 'ABERTO', %s, %s, %s)
            """
            horario = datetime.now().strftime('%H:%M:%S')
            params = (tipo, horario, id_rota, id_veiculo, id_motorista)
            
            alerta_id = execute_query(sql, params)
            return alerta_id, "Alerta criado com sucesso" if alerta_id else (None, "Erro ao criar alerta")
            
        except Exception as e:
            return None, f"Erro: {str(e)}"

    @staticmethod
    def listar_alertas():
        sql = """
        SELECT a.*, r.idRota, v.placa, u.nome as motorista_nome 
        FROM alerta a 
        LEFT JOIN rota r ON a.idRota = r.idRota 
        LEFT JOIN veiculo v ON a.id_veiculo = v.id_veiculo 
        LEFT JOIN motorista m ON a.id_motorista = m.id_motorista 
        LEFT JOIN usuario u ON m.id_usuario = u.id_usuario
        ORDER BY a.horario DESC
        """
        return execute_query(sql, fetch_all=True) or []