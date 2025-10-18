from flask import Blueprint, request, jsonify
from models.usuario import UsuarioModel

usuario_bp = Blueprint('usuarios', __name__)

@usuario_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    try:
        usuarios = UsuarioModel.listar_usuarios()
        return jsonify({
            'success': True,
            'usuarios': usuarios
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@usuario_bp.route('/usuarios', methods=['POST'])
def criar_usuario():
    try:
        data = request.get_json()
        
        usuario_id, mensagem = UsuarioModel.cadastrar(
            data['nome'],
            data['email'], 
            data['senha'],
            data['tipo_perfil']
        )
        
        if usuario_id:
            return jsonify({
                'success': True,
                'message': mensagem,
                'usuario_id': usuario_id
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

@usuario_bp.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        usuario = UsuarioModel.verificar_login(data['email'], data['senha'])
        
        if usuario:
            return jsonify({
                'success': True,
                'message': 'Login realizado',
                'usuario': {
                    'id': usuario['u_usuario'],
                    'nome': usuario['nome'],
                    'email': usuario['email']
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Credenciais inválidas'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500