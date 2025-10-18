from flask import Blueprint, request, jsonify
from controllers.veiculo_controller import VeiculoController

veiculo_bp = Blueprint('veiculo', __name__)

@veiculo_bp.route('/api/veiculos/cadastrar', methods=['POST'])
def cadastrar_veiculo():
    try:
        dados = request.get_json()
        
        # Validações básicas
        if not dados.get('placa') or not dados.get('capacidade'):
            return jsonify({
                'success': False,
                'message': 'Placa e capacidade são obrigatórios'
            }), 400
        
        # Cadastrar veículo
        success, result = VeiculoController.cadastrar_veiculo(dados)
        
        if success:
            return jsonify({
                'success': True,
                'message': result['message'],
                'veiculo_id': result['veiculo_id']
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': result
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }), 500

@veiculo_bp.route('/api/veiculos', methods=['GET'])
def listar_veiculos():
    try:
        # Filtro opcional por status
        filtro_status = request.args.get('status')
        
        success, result = VeiculoController.listar_veiculos(filtro_status)
        
        if success:
            return jsonify({
                'success': True,
                'veiculos': result
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': result
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }), 500

@veiculo_bp.route('/api/veiculos/disponiveis', methods=['GET'])
def listar_veiculos_disponiveis():
    try:
        success, result = VeiculoController.get_veiculos_disponiveis()
        
        if success:
            return jsonify({
                'success': True,
                'veiculos': result
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': result
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }), 500

@veiculo_bp.route('/api/veiculos/<int:u_veiculo>/status', methods=['PUT'])
def atualizar_status_veiculo(u_veiculo):
    try:
        dados = request.get_json()
        novo_status = dados.get('status')
        
        if not novo_status:
            return jsonify({
                'success': False,
                'message': 'Status é obrigatório'
            }), 400
        
        success, message = VeiculoController.atualizar_status_veiculo(u_veiculo, novo_status)
        
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
            'message': f'Erro interno: {str(e)}'
        }), 500

@veiculo_bp.route('/api/veiculos/<int:u_veiculo>', methods=['DELETE'])
def excluir_veiculo(u_veiculo):
    try:
        from models.veiculo_model import VeiculoModel
        
        success, message = VeiculoModel.excluir(u_veiculo)
        
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
            'message': f'Erro interno: {str(e)}'
        }), 500