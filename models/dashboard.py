from database.connection import execute_query
from datetime import datetime, timedelta

class DashboardModel:
    @staticmethod
    def get_estatisticas_entregas():
        """Obtém estatísticas principais de entregas"""
        try:
            # Estatísticas básicas
            sql_estatisticas = """
            SELECT 
                COUNT(*) as total_entregas,
                SUM(CASE WHEN status = 'ENTREGUE' THEN 1 ELSE 0 END) as entregues,
                SUM(CASE WHEN status = 'EM_TRANSITO' THEN 1 ELSE 0 END) as em_transito,
                SUM(CASE WHEN status = 'PENDENTE' THEN 1 ELSE 0 END) as pendentes,
                SUM(CASE WHEN status = 'ATRASADA' THEN 1 ELSE 0 END) as atrasadas,
                SUM(CASE WHEN status = 'PROBLEMA' THEN 1 ELSE 0 END) as com_problema
            FROM entrega
            """
            stats = execute_query(sql_estatisticas, fetch=True)
            
            return stats[0] if stats else {
                'total_entregas': 0, 'entregues': 0, 'em_transito': 0, 
                'pendentes': 0, 'atrasadas': 0, 'com_problema': 0
            }
            
        except Exception as e:
            print(f"Erro ao buscar estatísticas: {e}")
            return {'total_entregas': 0, 'entregues': 0, 'em_transito': 0, 'pendentes': 0, 'atrasadas': 0, 'com_problema': 0}

    @staticmethod
    def get_entregas_recentes(limite=10):
        """Obtém as entregas mais recentes"""
        try:
            sql = """
            SELECT 
                e.identrega,
                e.dataprevista,
                e.datarealizada,
                e.status,
                e.observacoes,
                r.origem,
                r.destino,
                v.placa,
                m.cnh,
                u.nome as motorista_nome,
                c.volume,
                c.peso
            FROM entrega e
            LEFT JOIN rota r ON e.u_rota = r.u_rota
            LEFT JOIN veiculo v ON e.u_veiculo = v.u_veiculo
            LEFT JOIN motorista m ON e.u_motorista = m.u_motorista
            LEFT JOIN usuario u ON m.u_motorista = u.u_motorista
            LEFT JOIN carga c ON e.idcarga = c.idcarga
            ORDER BY e.dataprevista DESC
            LIMIT %s
            """
            return execute_query(sql, (limite,), fetch=True) or []
            
        except Exception as e:
            print(f"Erro ao buscar entregas recentes: {e}")
            return []

    @staticmethod
    def get_alertas_ativos():
        """Obtém alertas ativos recentes"""
        try:
            sql = """
            SELECT 
                a.idalerta,
                a.tipo,
                a.titulo,
                a.descricao,
                a.horario,
                a.criado_em,
                r.origem,
                r.destino,
                v.placa,
                u.nome as motorista_nome,
                e.identrega
            FROM alerta a
            LEFT JOIN rota r ON a.u_rota = r.u_rota
            LEFT JOIN veiculo v ON a.u_veiculo = v.u_veiculo
            LEFT JOIN motorista m ON a.u_motorista = m.u_motorista
            LEFT JOIN usuario u ON m.u_motorista = u.u_motorista
            LEFT JOIN entrega e ON a.identrega = e.identrega
            WHERE a.status = 'ATIVO'
            ORDER BY a.criado_em DESC
            LIMIT 20
            """
            return execute_query(sql, fetch=True) or []
            
        except Exception as e:
            print(f"Erro ao buscar alertas ativos: {e}")
            return []

    @staticmethod
    def get_entregas_por_status():
        """Obtém distribuição de entregas por status para gráfico"""
        try:
            sql = """
            SELECT 
                status,
                COUNT(*) as quantidade
            FROM entrega 
            GROUP BY status
            ORDER BY quantidade DESC
            """
            return execute_query(sql, fetch=True) or []
            
        except Exception as e:
            print(f"Erro ao buscar entregas por status: {e}")
            return []

    @staticmethod
    def get_entregas_hoje():
        """Obtém entregas previstas para hoje"""
        try:
            sql = """
            SELECT 
                e.identrega,
                e.status,
                r.destino,
                v.placa,
                u.nome as motorista_nome,
                TIMEDIFF(e.dataprevista, NOW()) as tempo_restante
            FROM entrega e
            LEFT JOIN rota r ON e.u_rota = r.u_rota
            LEFT JOIN veiculo v ON e.u_veiculo = v.u_veiculo
            LEFT JOIN motorista m ON e.u_motorista = m.u_motorista
            LEFT JOIN usuario u ON m.u_motorista = u.u_motorista
            WHERE DATE(e.dataprevista) = CURDATE()
            ORDER BY e.dataprevista ASC
            """
            return execute_query(sql, fetch=True) or []
            
        except Exception as e:
            print(f"Erro ao buscar entregas de hoje: {e}")
            return []

    @staticmethod
    def get_metricas_operacionais():
        """Obtém métricas operacionais do sistema"""
        try:
            sql = """
            SELECT 
                (SELECT COUNT(*) FROM usuario) as total_usuarios,
                (SELECT COUNT(*) FROM veiculo) as total_veiculos,
                (SELECT COUNT(*) FROM veiculo WHERE status = 'DISPONIVEL') as veiculos_disponiveis,
                (SELECT COUNT(*) FROM motorista) as total_motoristas,
                (SELECT COUNT(*) FROM motorista WHERE status = 'ATIVO') as motoristas_ativos,
                (SELECT COUNT(*) FROM carga) as total_cargas,
                (SELECT COUNT(*) FROM carga WHERE status = 'EM_TRANSITO') as cargas_em_transito
            """
            result = execute_query(sql, fetch=True)
            return result[0] if result else {
                'total_usuarios': 0, 'total_veiculos': 0, 'veiculos_disponiveis': 0,
                'total_motoristas': 0, 'motoristas_ativos': 0, 'total_cargas': 0, 'cargas_em_transito': 0
            }
            
        except Exception as e:
            print(f"Erro ao buscar métricas operacionais: {e}")
            return {
                'total_usuarios': 0, 'total_veiculos': 0, 'veiculos_disponiveis': 0,
                'total_motoristas': 0, 'motoristas_ativos': 0, 'total_cargas': 0, 'cargas_em_transito': 0
            }

    @staticmethod
    def get_entregas_atrasadas():
        """Obtém entregas atrasadas (data prevista passou e não foram entregues)"""
        try:
            sql = """
            SELECT 
                e.identrega,
                e.dataprevista,
                r.destino,
                v.placa,
                u.nome as motorista_nome,
                DATEDIFF(CURDATE(), e.dataprevista) as dias_atraso
            FROM entrega e
            LEFT JOIN rota r ON e.u_rota = r.u_rota
            LEFT JOIN veiculo v ON e.u_veiculo = v.u_veiculo
            LEFT JOIN motorista m ON e.u_motorista = m.u_motorista
            LEFT JOIN usuario u ON m.u_motorista = u.u_motorista
            WHERE e.dataprevista < CURDATE() 
            AND e.status NOT IN ('ENTREGUE', 'CANCELADA')
            ORDER BY e.dataprevista ASC
            LIMIT 10
            """
            return execute_query(sql, fetch=True) or []
            
        except Exception as e:
            print(f"Erro ao buscar entregas atrasadas: {e}")
            return []