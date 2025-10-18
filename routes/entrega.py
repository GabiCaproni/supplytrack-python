from flask import Blueprint, request, jsonify
from models.entrega import EntregaModel

entrega_bp = Blueprint('entregas', __name__)

@entrega_bp.route('/entregas', methods=['GET'])
def listar_entregas():
    """Lista todas as entregas"""
    try:
        filtro_status = request.args.get('status')
        entregas = EntregaModel.listar_entregas(filtro_status)
        
        return jsonify({
            'success': True,
            'entregas': entregas
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@entrega_bp.route('/entregas', methods=['POST'])
def criar_entrega():
    """Cria uma nova entrega"""
    try:
        data = request.get_json()
        
        entrega_id, mensagem = EntregaModel.criar_entrega(
            data['dataprevista'],
            data['u_rota'],
            data['u_veiculo'],
            data['u_motorista'],
            data['idcarga'],
            data.get('status', 'PENDENTE')
        )
        
        if entrega_id:
            return jsonify({
                'success': True,
                'message': mensagem,
                'entrega_id': entrega_id
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

@entrega_bp.route('/entregas/<int:identrega>/status', methods=['PUT'])
def atualizar_status_entrega(identrega):
    """Atualiza status de uma entrega"""
    try:
        data = request.get_json()
        novo_status = data.get('status')
        observacoes = data.get('observacoes')
        
        if not novo_status:
            return jsonify({
                'success': False,
                'message': 'Status é obrigatório'
            }), 400
        
        # Para atualização geral (admin)
        success, message = EntregaModel.atualizar_status(identrega, novo_status, observacoes)
        
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

@entrega_bp.route('/motorista/<int:u_motorista>/entregas/<int:identrega>/status', methods=['PUT'])
def motorista_atualizar_status(u_motorista, identrega):
    """Motorista atualiza status da sua entrega"""
    try:
        data = request.get_json()
        novo_status = data.get('status')
        observacoes = data.get('observacoes')
        
        if not novo_status:
            return jsonify({
                'success': False,
                'message': 'Status é obrigatório'
            }), 400
        
        success, message = EntregaModel.atualizar_status_motorista(
            identrega, u_motorista, novo_status, observacoes
        )
        
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