from models.dashboard import DashboardModel
from datetime import datetime

class DashboardController:
    @staticmethod
    def get_dashboard_data():
        """Obtém todos os dados para o dashboard"""
        try:
            # Estatísticas principais
            estatisticas = DashboardModel.get_estatisticas_entregas()
            
            # Calcular taxas
            total_entregas = estatisticas['total_entregas']
            taxa_entrega = round((estatisticas['entregues'] / total_entregas * 100), 2) if total_entregas > 0 else 0
            taxa_atraso = round((estatisticas['atrasadas'] / total_entregas * 100), 2) if total_entregas > 0 else 0
            
            estatisticas_principais = {
                **estatisticas,
                'taxa_entrega': taxa_entrega,
                'taxa_atraso': taxa_atraso
            }
            
            # Métricas operacionais
            metricas_operacionais = DashboardModel.get_metricas_operacionais()
            
            # Alertas
            alertas_lista = DashboardModel.get_alertas_ativos()
            alertas_data = {
                'ativos': len(alertas_lista),
                'criticos': len([a for a in alertas_lista if a['tipo'] in ['ATRASO', 'PERIGO']]),
                'lista': alertas_lista
            }
            
            # Entregas
            entregas_recentes = DashboardModel.get_entregas_recentes(10)
            entregas_hoje = DashboardModel.get_entregas_hoje()
            entregas_atrasadas = DashboardModel.get_entregas_atrasadas()
            entregas_por_status = DashboardModel.get_entregas_por_status()
            
            entregas_data = {
                'recentes': entregas_recentes,
                'hoje': entregas_hoje,
                'atrasadas': entregas_atrasadas,
                'por_status': entregas_por_status
            }
            
            return True, {
                'estatisticas_principais': estatisticas_principais,
                'metricas_operacionais': metricas_operacionais,
                'alertas': alertas_data,
                'entregas': entregas_data,
                'ultima_atualizacao': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            }
            
        except Exception as e:
            print(f"Erro no DashboardController: {e}")
            return False, f"Erro ao carregar dados do dashboard: {str(e)}"

    @staticmethod
    def get_alertas_resumido():
        """Retorna dados resumidos de alertas"""
        try:
            alertas = DashboardModel.get_alertas_ativos()
            return True, {
                'ativos': len(alertas),
                'criticos': len([a for a in alertas if a['tipo'] in ['ATRASO', 'PERIGO']]),
                'lista': alertas[:5]  # Apenas 5 mais recentes
            }
        except Exception as e:
            return False, str(e)

    @staticmethod
    def get_entregas_resumido():
        """Retorna dados resumidos de entregas"""
        try:
            return True, {
                'recentes': DashboardModel.get_entregas_recentes(5),
                'hoje': DashboardModel.get_entregas_hoje(),
                'por_status': DashboardModel.get_entregas_por_status()
            }
        except Exception as e:
            return False, str(e)