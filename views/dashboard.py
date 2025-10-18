from database.connection import execute_query

class Dashboard:
    @staticmethod
    def obter_estatisticas():
        """Obtém estatísticas para o dashboard"""
        stats = {}
        
        # Total de usuários
        stats['total_usuarios'] = execute_query("SELECT COUNT(*) as total FROM usuario", fetch=True)['total']
        
        # Total de veículos por status
        stats['veiculos_disponiveis'] = execute_query(
            "SELECT COUNT(*) as total FROM veiculo WHERE status = 'DISPONIVEL'", fetch=True
        )['total']
        
        # Total de cargas por status
        stats['cargas_pendentes'] = execute_query(
            "SELECT COUNT(*) as total FROM carga WHERE status IN ('CADASTRADA', 'EM_ARMEZEM')", fetch=True
        )['total']
        
        # Rotas em andamento
        stats['rotas_andamento'] = execute_query(
            "SELECT COUNT(*) as total FROM rota WHERE status = 'EM_ANDAMENTO'", fetch=True
        )['total']
        
        # Alertas abertos
        stats['alertas_abertos'] = execute_query(
            "SELECT COUNT(*) as total FROM alerta WHERE status = 'ABERTO'", fetch=True
        )['total']
        
        return stats

    @staticmethod
    def obter_entregas_recentes():
        """Obtém entregas recentes"""
        sql = """
        SELECT e.*, r.idRota, u.nome as motorista_nome 
        FROM entrega e 
        LEFT JOIN rota r ON e.idRota = r.idRota 
        LEFT JOIN motorista m ON e.id_motorista = m.id_motorista 
        LEFT JOIN usuario u ON m.id_usuario = u.id_usuario
        ORDER BY e.dataPrevista DESC LIMIT 5
        """
        return execute_query(sql, fetch_all=True) or []