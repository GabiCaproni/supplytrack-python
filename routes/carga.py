from flask import Blueprint, request, jsonify
from controllers.cargaController import CargaController

carga_bp = Blueprint('carga', __name__)

@carga_bp.route('/cargas', methods=['GET'])
def listar_cargas():
    """Lista todas as cargas"""
    try:
        success, result = CargaController.listar_cargas()
        
        if success:
            return jsonify({
                'success': True,
                'cargas': result
            }), 200
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

@carga_bp.route('/cargas', methods=['POST'])
def criar_carga():
    """Cria uma nova carga com todos os campos"""
    try:
        # Aceita tanto JSON quanto form data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()

        print(f"Dados recebidos: {data}")

        # Extrair dados com valores padrão
        volume = data.get('volume', '').strip()
        peso = data.get('peso', '').strip()
        id_armazem = data.get('id_armazem', '1').strip()
        status = data.get('status', 'PENDENTE').strip()
        localizacao = data.get('localizacao', '').strip()

        # Validações básicas
        if not volume:
            return jsonify({
                'success': False,
                'error': 'Volume é obrigatório'
            }), 400

        if not peso:
            return jsonify({
                'success': False,
                'error': 'Peso é obrigatório'
            }), 400

        # Converter id_armazem para inteiro
        try:
            id_armazem = int(id_armazem)
        except (ValueError, TypeError):
            id_armazem = 1

        # Se localização estiver vazia, usar None
        if not localizacao:
            localizacao = None

        # Chamar o controller
        success, result = CargaController.criar_carga(volume, peso, id_armazem, status, localizacao)
        
        if success:
            return jsonify({
                'success': True,
                'message': result['message'],
                'id_carga': result['id_carga']
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': result
            }), 400
            
    except Exception as e:
        print(f"Erro na rota de criar carga: {e}")
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

# Rota para atualizar status
@carga_bp.route('/cargas/<int:id_carga>/status', methods=['PUT'])
def atualizar_status_carga(id_carga):
    """Atualiza o status de uma carga"""
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()

        status = data.get('status', '').strip()

        if not status:
            return jsonify({
                'success': False,
                'error': 'Status é obrigatório'
            }), 400

        success, result = CargaController.atualizar_status(id_carga, status)
        
        if success:
            return jsonify({
                'success': True,
                'message': result
            }), 200
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

# Rota para atualizar localização
@carga_bp.route('/cargas/<int:id_carga>/localizacao', methods=['PUT'])
def atualizar_localizacao_carga(id_carga):
    """Atualiza a localização de uma carga"""
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()

        localizacao = data.get('localizacao', '').strip()

        success, result = CargaController.atualizar_localizacao(id_carga, localizacao)
        
        if success:
            return jsonify({
                'success': True,
                'message': result
            }), 200
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

# Rota alternativa para teste rápido
@carga_bp.route('/cargas/rapido', methods=['POST'])
def criar_carga_rapida():
    """Cria uma carga com dados completos para teste"""
    try:
        data = {
            'volume': '1m³',
            'peso': '100kg', 
            'id_armazem': 1,
            'status': 'PENDENTE',
            'localizacao': 'Armazém Centro - Setor A'
        }
        
        success, result = CargaController.criar_carga(
            data['volume'], 
            data['peso'], 
            data['id_armazem'],
            data['status'],
            data['localizacao']
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': result['message'],
                'id_carga': result['id_carga']
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