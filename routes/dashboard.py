from flask import Blueprint, jsonify
from controllers.dashboardController import DashboardController

# Mude o nome do blueprint para evitar conflito
dashboard_bp = Blueprint('dashboard_api', __name__)

# CORREÇÃO: Mude as rotas para /api/dashboard/data, /api/dashboard/alertas, etc.
@dashboard_bp.route('/dashboard/data', methods=['GET'])
def get_dashboard_completo():
    """Retorna todos os dados do dashboard"""
    try:
        success, result = DashboardController.get_dashboard_data()
        
        if success:
            return jsonify({
                'success': True,
                'data': result
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': result
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/dashboard/alertas', methods=['GET'])
def get_alertas_dashboard():
    """Retorna apenas dados de alertas"""
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
            'error': str(e)
        }), 500

@dashboard_bp.route('/dashboard/entregas', methods=['GET'])
def get_entregas_dashboard():
    """Retorna apenas dados de entregas"""
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
            'error': str(e)
        }), 500

@dashboard_bp.route('/dashboard/metricas-rapidas', methods=['GET'])
def get_metricas_rapidas():
    """Retorna métricas rápidas para cards"""
    try:
        from models.dashboard import DashboardModel
        
        estatisticas = DashboardModel.get_estatisticas_entregas()
        metricas = DashboardModel.get_metricas_operacionais()
        alertas = DashboardModel.get_alertas_ativos()
        
        metricas_rapidas = {
            'total_entregas': estatisticas['total_entregas'],
            'entregues': estatisticas['entregues'],
            'em_transito': estatisticas['em_transito'],
            'atrasadas': estatisticas['atrasadas'],
            'alertas_ativos': len(alertas),
            'veiculos_disponiveis': metricas['veiculos_disponiveis']
        }
        
        return jsonify({
            'success': True,
            'metricas': metricas_rapidas
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500