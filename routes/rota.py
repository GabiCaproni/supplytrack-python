from flask import Blueprint, request, jsonify
from models.rota import RotaModel

rota_bp = Blueprint('rotas', __name__)

@rota_bp.route('/rotas', methods=['GET'])
def listar_rotas():
    """Lista todas as rotas"""
    try:
        filtro_status = request.args.get('status')
        rotas = RotaModel.listar_rotas(filtro_status)
        
        return jsonify({
            'success': True,
            'rotas': rotas
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@rota_bp.route('/rotas', methods=['POST'])
def criar_rota():
    """Cria uma nova rota"""
    try:
        data = request.get_json()
        
        rota_id, mensagem = RotaModel.criar_rota(
            data['origem'],
            data['destino'],
            data.get('distancia_km'),
            data.get('tempo_estimado'),
            data.get('status', 'PLANEJADA')
        )
        
        if rota_id:
            return jsonify({
                'success': True,
                'message': mensagem,
                'rota_id': rota_id
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': mensagem
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@rota_bp.route('/rotas/<int:u_rota>/status', methods=['PUT'])
def atualizar_status_rota(u_rota):
    """Atualiza status da rota"""
    try:
        data = request.get_json()
        novo_status = data.get('status')
        
        if not novo_status:
            return jsonify({
                'success': False,
                'message': 'Status é obrigatório'
            }), 400
        
        success, message = RotaModel.atualizar_status_rota(u_rota, novo_status)
        
        if success:
            return jsonify({
                'success': True,
                'message': message
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500