from flask import Blueprint, request, jsonify
from controllers.dashboard_controller import DashboardController

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/api/dashboard', methods=['GET'])
def get_dashboard_completo():
    """Retorna todos os dados do dashboard"""
    try:
        success, result = DashboardController.get_dashboard_data()
        
        if success:
            return jsonify({
                'success': True,
                'data': result,
                'timestamp': datetime.now().isoformat()
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': result
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }), 500

@dashboard_bp.route('/api/dashboard/alertas', methods=['GET'])
def get_alertas_dashboard():
    """Retorna apenas dados de alertas (para atualização em tempo real)"""
    try:
        success, result = DashboardController.get_alertas_resumido()
        
        if success:
            return jsonify({
                'success': True,
                'alertas': result
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': result
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }), 500

@dashboard_bp.route('/api/dashboard/entregas', methods=['GET'])
def get_entregas_dashboard():
    """Retorna apenas dados de entregas (para atualização em tempo real)"""
    try:
        success, result = DashboardController.get_entregas_resumido()
        
        if success:
            return jsonify({
                'success': True,
                'entregas': result
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': result
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }), 500

@dashboard_bp.route('/api/dashboard/metricas-rapidas', methods=['GET'])
def get_metricas_rapidas():
    """Retorna apenas as métricas rápidas para cards do dashboard"""
    try:
        from models.dashboard_model import DashboardModel
        
        estatisticas = DashboardModel.get_estatisticas_entregas()
        metricas = DashboardModel.get_metricas_operacionais()
        alertas = DashboardModel.get_alertas_ativos()
        
        metricas_rapidas = {
            'entregas_total': estatisticas['total_entregas'],
            'entregues_hoje': estatisticas['entregues'],  # Simplificado - em produção filtrar por data
            'em_transito': estatisticas['em_transito'],
            'atrasadas': estatisticas['atrasadas'],
            'alertas_ativos': len(alertas),
            'veiculos_disponiveis': metricas['veiculos_disponiveis'],
            'motoristas_ativos': metricas['motoristas_ativos']
        }
        
        return jsonify({
            'success': True,
            'metricas': metricas_rapidas
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }), 500