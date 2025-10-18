from models.dashboard_model import DashboardModel

class DashboardController:
    @staticmethod
    def get_dashboard_data():
        """
        Obtém todos os dados para o dashboard de forma otimizada
        """
        try:
            # Buscar dados em paralelo (simulação - em produção poderia ser assíncrono)
            estatisticas = DashboardModel.get_estatisticas_entregas()
            alertas_ativos = DashboardModel.get_alertas_ativos()
            entregas_recentes = DashboardModel.get_entregas_recentes(5)
            metricas_operacionais = DashboardModel.get_metricas_operacionais()
            entregas_hoje = DashboardModel.get_entregas_hoje()
            entregas_atrasadas = DashboardModel.get_entregas_atrasadas()
            entregas_por_status = DashboardModel.get_entregas_por_status()
            
            # Calcular métricas derivadas
            taxa_entrega = (estatisticas['entregues'] / estatisticas['total_entregas'] * 100) if estatisticas['total_entregas'] > 0 else 0
            taxa_atraso = (estatisticas['atrasadas'] / estatisticas['total_entregas'] * 100) if estatisticas['total_entregas'] > 0 else 0
            
            dashboard_data = {
                'estatisticas_principais': {
                    'total_entregas': estatisticas['total_entregas'],
                    'entregues': estatisticas['entregues'],
                    'em_transito': estatisticas['em_transito'],
                    'pendentes': estatisticas['pendentes'],
                    'atrasadas': estatisticas['atrasadas'],
                    'com_problema': estatisticas['com_problema'],
                    'taxa_entrega': round(taxa_entrega, 1),
                    'taxa_atraso': round(taxa_atraso, 1)
                },
                
                'metricas_operacionais': metricas_operacionais,
                
                'alertas': {
                    'ativos': len(alertas_ativos),
                    'lista': alertas_ativos[:5],  # Últimos 5 alertas
                    'criticos': len([a for a in alertas_ativos if a.get('tipo') in ['ATRASO', 'VEICULO_PROBLEMA']])
                },
                
                'entregas': {
                    'recentes': entregas_recentes,
                    'hoje': entregas_hoje,
                    'atrasadas': entregas_atrasadas,
                    'por_status': entregas_por_status
                },
                
                'resumo_dia': {
                    'entregas_previstas_hoje': len(entregas_hoje),
                    'entregas_concluidas_hoje': len([e for e in entregas_hoje if e.get('status') == 'ENTREGUE']),
                    'alertas_hoje': len([a for a in alertas_ativos if str(a.get('criado_em', ''))[:10] == str(datetime.now().date())])
                }
            }
            
            return True, dashboard_data
            
        except Exception as e:
            print(f"Erro no controller do dashboard: {e}")
            return False, f"Erro ao carregar dados do dashboard: {str(e)}"

    @staticmethod
    def get_alertas_resumido():
        """Obtém apenas dados de alertas para atualização em tempo real"""
        try:
            alertas = DashboardModel.get_alertas_ativos()
            
            return True, {
                'total_alertas': len(alertas),
                'alertas_recentes': alertas[:3],
                'alertas_criticos': [a for a in alertas if a.get('tipo') in ['ATRASO', 'VEICULO_PROBLEMA']][:3]
            }
        except Exception as e:
            return False, f"Erro ao carregar alertas: {str(e)}"

    @staticmethod
    def get_entregas_resumido():
        """Obtém apenas dados de entregas para atualização em tempo real"""
        try:
            estatisticas = DashboardModel.get_estatisticas_entregas()
            entregas_hoje = DashboardModel.get_entregas_hoje()
            
            return True, {
                'estatisticas': estatisticas,
                'entregas_hoje': len(entregas_hoje),
                'entregas_pendentes_hoje': len([e for e in entregas_hoje if e.get('status') in ['PENDENTE', 'EM_TRANSITO']])
            }
        except Exception as e:
            return False, f"Erro ao carregar entregas: {str(e)}"