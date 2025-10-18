from flask import Blueprint, request, jsonify
from models.motorista import MotoristaModel

motorista_bp = Blueprint('motoristas', __name__)

@motorista_bp.route('/motoristas', methods=['GET'])
def listar_motoristas():
    """Lista todos os motoristas"""
    try:
        motoristas = MotoristaModel.listar_motoristas()
        return jsonify({
            'success': True,
            'motoristas': motoristas
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@motorista_bp.route('/motoristas', methods=['POST'])
def criar_motorista():
    """Cadastra um novo motorista"""
    try:
        data = request.get_json()
        
        motorista_id, mensagem = MotoristaModel.cadastrar(
            data['cnh'],
            data.get('status', 'ATIVO'),
            data.get('u_rota')
        )
        
        if motorista_id:
            return jsonify({
                'success': True,
                'message': mensagem,
                'motorista_id': motorista_id
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

@motorista_bp.route('/motoristas/<int:u_motorista>/entregas', methods=['GET'])
def listar_entregas_motorista(u_motorista):
    """Lista entregas de um motorista específico"""
    try:
        from models.entrega import EntregaModel
        entregas = EntregaModel.listar_entregas_motorista(u_motorista)
        
        return jsonify({
            'success': True,
            'entregas': entregas
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@motorista_bp.route('/motoristas/<int:u_motorista>/status', methods=['PUT'])
def atualizar_status_motorista(u_motorista):
    """Atualiza status do motorista"""
    try:
        data = request.get_json()
        novo_status = data.get('status')
        
        success, message = MotoristaModel.atualizar_status(u_motorista, novo_status)
        
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