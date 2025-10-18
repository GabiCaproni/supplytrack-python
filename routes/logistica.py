from flask import Blueprint, request, jsonify
from controllers.logisticaController import LogisticaController


logistica_bp = Blueprint('logistica', __name__)

@logistica_bp.route('/logistica/registrar-carga', methods=['POST'])
def registrar_carga_roteirizar():
    """Processo completo: registra carga e cria rota/entrega"""
    try:
        data = request.get_json()
        
        success, result = LogisticaController.registrar_carga_e_roteirizar(data)
        
        if success:
            return jsonify({
                'success': True,
                'message': result['message'],
                'ids': result['ids']
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': result
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@logistica_bp.route('/logistica/entregas-ativas', methods=['GET'])
def listar_entregas_ativas():
    """Lista entregas em andamento"""
    try:
        success, result = LogisticaController.listar_entregas_ativas()
        
        if success:
            return jsonify({
                'success': True,
                'entregas': result
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': result
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500