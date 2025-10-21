from database.connection import execute_query
from datetime import datetime, timedelta

class DashboardModel:
    @staticmethod
    def get_estatisticas_entregas():
        """Obtém estatísticas principais de entregas"""
        try:
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
            result = execute_query(sql_estatisticas, fetch=True)
            
            if result:
                return {
                    'total_entregas': result['total_entregas'] or 0,
                    'entregues': result['entregues'] or 0,
                    'em_transito': result['em_transito'] or 0,
                    'pendentes': result['pendentes'] or 0,
                    'atrasadas': result['atrasadas'] or 0,
                    'com_problema': result['com_problema'] or 0
                }
            else:
                return {
                    'total_entregas': 0, 'entregues': 0, 'em_transito': 0, 
                    'pendentes': 0, 'atrasadas': 0, 'com_problema': 0
                }
                
        except Exception as e:
            print(f"Erro ao buscar estatísticas: {e}")
            return {
                'total_entregas': 0, 'entregues': 0, 'em_transito': 0, 
                'pendentes': 0, 'atrasadas': 0, 'com_problema': 0
            }

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
            LEFT JOIN rota r ON e.id_rota = r.id_rota
            LEFT JOIN veiculo v ON e.id_veiculo = v.id_veiculo
            LEFT JOIN motorista m ON e.id_motorista = m.id_motorista
            LEFT JOIN usuario u ON m.id_usuario = u.id_usuario
            LEFT JOIN carga c ON e.id_carga = c.id_carga
            ORDER BY e.dataprevista DESC
            LIMIT %s
            """
            result = execute_query(sql, (limite,), fetch_all=True)
            return result or []
            
        except Exception as e:
            print(f"Erro ao buscar entregas recentes: {e}")
            return []

    @staticmethod
    def get_alertas_ativos():
        """Obtém alertas ativos recentes"""
        try:
            sql = """
            SELECT 
                a.id_alerta,
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
            LEFT JOIN rota r ON a.id_rota = r.id_rota
            LEFT JOIN veiculo v ON a.id_veiculo = v.id_veiculo
            LEFT JOIN motorista m ON a.id_motorista = m.id_motorista
            LEFT JOIN usuario u ON m.id_usuario = u.id_usuario
            LEFT JOIN entrega e ON a.id_entrega = e.identrega
            WHERE a.status = 'ATIVO'
            ORDER BY a.criado_em DESC
            LIMIT 20
            """
            result = execute_query(sql, fetch_all=True)
            return result or []
            
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
            result = execute_query(sql, fetch_all=True)
            return result or []
            
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
            LEFT JOIN rota r ON e.id_rota = r.id_rota
            LEFT JOIN veiculo v ON e.id_veiculo = v.id_veiculo
            LEFT JOIN motorista m ON e.id_motorista = m.id_motorista
            LEFT JOIN usuario u ON m.id_usuario = u.id_usuario
            WHERE DATE(e.dataprevista) = CURDATE()
            ORDER BY e.dataprevista ASC
            """
            result = execute_query(sql, fetch_all=True)
            return result or []
            
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
            
            if result:
                return {
                    'total_usuarios': result['total_usuarios'] or 0,
                    'total_veiculos': result['total_veiculos'] or 0,
                    'veiculos_disponiveis': result['veiculos_disponiveis'] or 0,
                    'total_motoristas': result['total_motoristas'] or 0,
                    'motoristas_ativos': result['motoristas_ativos'] or 0,
                    'total_cargas': result['total_cargas'] or 0,
                    'cargas_em_transito': result['cargas_em_transito'] or 0
                }
            else:
                return {
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
            LEFT JOIN rota r ON e.id_rota = r.id_rota
            LEFT JOIN veiculo v ON e.id_veiculo = v.id_veiculo
            LEFT JOIN motorista m ON e.id_motorista = m.id_motorista
            LEFT JOIN usuario u ON m.id_usuario = u.id_usuario
            WHERE e.dataprevista < CURDATE() 
            AND e.status NOT IN ('ENTREGUE', 'CANCELADA')
            ORDER BY e.dataprevista ASC
            LIMIT 10
            """
            result = execute_query(sql, fetch_all=True)
            return result or []
            
        except Exception as e:
            print(f"Erro ao buscar entregas atrasadas: {e}")
            return []