from flask import Blueprint, request, jsonify
from controllers.entregaController import EntregaController

entrega_bp = Blueprint('entrega', __name__)

@entrega_bp.route('/entregas', methods=['GET'])
def listar_entregas():
    """Lista todas as entregas"""
    try:
        print("📨 GET /api/entregas - Listando todas as entregas")
        
        success, result = EntregaController.listar_entregas()
        
        if success:
            return jsonify({
                'success': True,
                'entregas': result,
                'total': len(result)
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result
            }), 400
            
    except Exception as e:
        print(f"❌ Erro na rota GET /entregas: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

@entrega_bp.route('/entregas/ativas', methods=['GET'])
def listar_entregas_ativas():
    """Lista apenas entregas ativas"""
    try:
        print("📨 GET /api/entregas/ativas - Listando entregas ativas")
        
        success, result = EntregaController.listar_entregas_ativas()
        
        if success:
            return jsonify({
                'success': True,
                'entregas': result,
                'total': len(result)
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result
            }), 400
            
    except Exception as e:
        print(f"❌ Erro na rota GET /entregas/ativas: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

@entrega_bp.route('/entregas', methods=['POST'])
def criar_entrega():
    """Cria uma nova entrega"""
    try:
        print("📨 POST /api/entregas - Criando entrega")
        
        # Pegar dados do request
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        
        print(f"📦 Dados recebidos: {data}")
        
        # Extrair dados
        data_entrega = data.get('data_entrega')
        status = data.get('status', 'PENDENTE')
        local_entrega = data.get('local_entrega')
        id_rota = data.get('id_rota')
        id_carga = data.get('id_carga')
        observacoes = data.get('observacoes')
        
        # Validar campos obrigatórios
        if not all([data_entrega, status, local_entrega]):
            return jsonify({
                'success': False,
                'error': 'Campos obrigatórios faltando: data_entrega, status, local_entrega'
            }), 400
        
        # Chamar controller
        success, result = EntregaController.criar_entrega(
            data_entrega=data_entrega,
            status=status,
            local_entrega=local_entrega,
            id_rota=id_rota,
            id_carga=id_carga,
            observacoes=observacoes
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': result.get('message'),
                'id_entrega': result.get('id_entrega')
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': result
            }), 400
            
    except Exception as e:
        print(f"❌ Erro no routes POST /entregas: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500