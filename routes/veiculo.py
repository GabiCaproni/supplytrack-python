from flask import Blueprint, request, jsonify
from models.veiculo import VeiculoModel

veiculo_bp = Blueprint('veiculos', __name__)

@veiculo_bp.route('/veiculos', methods=['GET'])
def listar_veiculos():
    """Lista todos os veículos"""
    try:
        veiculos = VeiculoModel.listar_veiculos()
        return jsonify({
            'success': True,
            'veiculos': veiculos
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@veiculo_bp.route('/veiculos', methods=['POST'])
def criar_veiculo():
    """Cadastra um novo veículo"""
    try:
        data = request.get_json()
        
        veiculo_id, mensagem = VeiculoModel.cadastrar(
            data['placa'],
            data['capacidade'],
            data.get('u_motorista'),
            data.get('status', 'DISPONIVEL')
        )
        
        if veiculo_id:
            return jsonify({
                'success': True,
                'message': mensagem,
                'veiculo_id': veiculo_id
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

@veiculo_bp.route('/veiculos/<int:u_veiculo>', methods=['GET'])
def buscar_veiculo(u_veiculo):
    """Busca veículo por ID"""
    try:
        veiculo = VeiculoModel.buscar_por_id(u_veiculo)
        if veiculo:
            return jsonify({
                'success': True,
                'veiculo': veiculo
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Veículo não encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@veiculo_bp.route('/veiculos/<int:u_veiculo>/status', methods=['PUT'])
def atualizar_status_veiculo(u_veiculo):
    """Atualiza status do veículo"""
    try:
        data = request.get_json()
        novo_status = data.get('status')
        
        if not novo_status:
            return jsonify({
                'success': False,
                'message': 'Status é obrigatório'
            }), 400
        
        success, message = VeiculoModel.atualizar_status(u_veiculo, novo_status)
        
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

@veiculo_bp.route('/veiculos/disponiveis', methods=['GET'])
def listar_veiculos_disponiveis():
    """Lista veículos disponíveis"""
    try:
        veiculos = VeiculoModel.buscar_veiculos_disponiveis()
        return jsonify({
            'success': True,
            'veiculos': veiculos
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500