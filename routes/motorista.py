from flask import Blueprint, request, jsonify
from controllers.motoristaController import MotoristaController

motorista_bp = Blueprint('motorista', __name__)

@motorista_bp.route('/motoristas', methods=['GET'])
def listar_motoristas():
    """Lista todos os motoristas"""
    success, result = MotoristaController.listar_motoristas()
    
    if success:
        return jsonify({
            'success': True,
            'motoristas': result
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': result
        }), 400

@motorista_bp.route('/motoristas', methods=['POST'])
def criar_motorista():
    """Cria um novo motorista (suporta duas formas)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Dados JSON são obrigatórios'
            }), 400
        
        # FORMA 1: Criar motorista a partir de usuário existente
        id_usuario = data.get('id_usuario')
        cnh = data.get('cnh')
        status = data.get('status', 'LIVRE')
        
        if id_usuario and cnh:
            success, result = MotoristaController.criar_motorista(id_usuario, cnh, status)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': result['message'],
                    'id_motorista': result['id_motorista']
                }), 201
            else:
                return jsonify({
                    'success': False,
                    'error': result
                }), 400
        
        # FORMA 2: Criar usuário e motorista juntos
        nome = data.get('nome')
        email = data.get('email')
        senha = data.get('senha')
        
        if nome and email and senha and cnh:
            success, result = MotoristaController.criar_motorista_completo(nome, email, senha, cnh, status)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': result['message'],
                    'id_usuario': result['id_usuario'],
                    'id_motorista': result['id_motorista']
                }), 201
            else:
                return jsonify({
                    'success': False,
                    'error': result
                }), 400
        
        # Se nenhuma forma foi satisfeita
        return jsonify({
            'success': False,
            'error': 'Dados insuficientes. Use: (id_usuario + cnh) OU (nome + email + senha + cnh)'
        }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

# ADICIONE ESTA ROTA NOVA AQUI:
@motorista_bp.route('/motoristas/simples', methods=['POST'])
def criar_motorista_simples():
    """Cria um motorista com dados mínimos (apenas para teste)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Dados JSON são obrigatórios'
            }), 400
        
        cnh = data.get('cnh')
        
        if not cnh:
            return jsonify({
                'success': False,
                'error': 'CNH é obrigatória'
            }), 400
        
        # Criar usuário automático para o motorista
        nome = f"Motorista {cnh}"
        email = f"motorista.{cnh}@supplytrack.com"
        senha = "123456"  # Senha padrão
        
        success, result = MotoristaController.criar_motorista_completo(nome, email, senha, cnh)
        
        if success:
            return jsonify({
                'success': True,
                'message': result['message'],
                'id_usuario': result['id_usuario'],
                'id_motorista': result['id_motorista']
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