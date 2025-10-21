from flask import Blueprint, request, jsonify
from controllers.rotaController import RotaController

rota_bp = Blueprint('rota', __name__)

@rota_bp.route('/rotas', methods=['GET'])
def listar_rotas():
    """Lista todas as rotas"""
    try:
        print("📨 GET /api/rotas - Listando rotas")
        
        success, result = RotaController.listar_rotas()
        
        if success:
            return jsonify({
                'success': True,
                'rotas': result
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result
            }), 400
            
    except Exception as e:
        print(f"❌ Erro na rota GET /rotas: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

@rota_bp.route('/rotas', methods=['POST'])
def criar_rota():
    """Cria uma nova rota"""
    try:
        print("📨 POST /api/rotas - Criando rota")
        
        # Pegar dados do request
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        
        print(f"📦 Dados recebidos: {data}")
        
        # Extrair dados
        dataSaida = data.get('dataSaida')
        dataEntrega = data.get('dataEntrega')
        distancia = data.get('distancia')
        status = data.get('status', 'PENDENTE')
        
        # Validar campos obrigatórios
        if not all([dataSaida, dataEntrega, distancia, status]):
            return jsonify({
                'success': False,
                'error': 'Campos obrigatórios faltando: dataSaida, dataEntrega, distancia, status'
            }), 400
        
        # Chamar controller
        success, result = RotaController.criar_rota(
            dataSaida=dataSaida,
            dataEntrega=dataEntrega,
            distancia=distancia,
            status=status
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': result.get('message'),
                'id_rota': result.get('id_rota')
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': result
            }), 400
            
    except Exception as e:
        print(f"❌ Erro no routes POST: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500