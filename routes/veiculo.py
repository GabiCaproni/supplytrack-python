from flask import Blueprint, request, jsonify
from controllers.veiculoController import VeiculoController

veiculo_bp = Blueprint('veiculo', __name__)

@veiculo_bp.route('/veiculos', methods=['GET'])
def listar_veiculos():
    """Lista todos os veículos"""
    success, result = VeiculoController.listar_veiculos()
    
    if success:
        return jsonify({
            'success': True,
            'veiculos': result
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': result
        }), 400

@veiculo_bp.route('/veiculos', methods=['POST'])
def criar_veiculo():
    """Cria um novo veículo"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Dados JSON são obrigatórios'
            }), 400
        
        placa = data.get('placa')
        capacidade = data.get('capacidade')
        id_motorista = data.get('id_motorista')  # Opcional
        
        success, result = VeiculoController.criar_veiculo(placa, capacidade, id_motorista)
        
        if success:
            return jsonify({
                'success': True,
                'message': result['message'],
                'id_veiculo': result['id_veiculo']
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': result
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500