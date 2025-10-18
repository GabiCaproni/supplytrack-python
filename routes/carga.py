from flask import Blueprint, request, jsonify
from models.carga import CargaModel

carga_bp = Blueprint('cargas', __name__)

@carga_bp.route('/cargas', methods=['GET'])
def listar_cargas():
    """Lista todas as cargas"""
    try:
        filtro_status = request.args.get('status')
        cargas = CargaModel.listar_cargas(filtro_status)
        
        return jsonify({
            'success': True,
            'cargas': cargas
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@carga_bp.route('/cargas', methods=['POST'])
def criar_carga():
    """Registra uma nova carga"""
    try:
        data = request.get_json()
        
        carga_id, mensagem = CargaModel.registrar_carga(
            data['volume'],
            data['peso'],
            data.get('idarmazem'),
            data.get('status', 'NO_ARMAZEM'),
            data.get('localizacao_atual')
        )
        
        if carga_id:
            return jsonify({
                'success': True,
                'message': mensagem,
                'carga_id': carga_id
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

@carga_bp.route('/cargas/<int:idcarga>/status', methods=['PUT'])
def atualizar_status_carga(idcarga):
    """Atualiza status da carga"""
    try:
        data = request.get_json()
        novo_status = data.get('status')
        localizacao = data.get('localizacao_atual')
        
        if not novo_status:
            return jsonify({
                'success': False,
                'message': 'Status é obrigatório'
            }), 400
        
        success, message = CargaModel.atualizar_status(idcarga, novo_status, localizacao)
        
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