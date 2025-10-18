from flask import Blueprint, request, jsonify
from controllers.logistica_controller import LogisticaController

logistica_bp = Blueprint('logistica', __name__)

@logistica_bp.route('/api/logistica/registrar-carga', methods=['POST'])
def registrar_carga_roteirizar():
    try:
        dados = request.get_json()
        
        # Campos obrigatórios
        campos_obrigatorios = [
            'volume', 'peso', 'dataprevista', 'origem', 
            'destino', 'u_veiculo', 'u_motorista'
        ]
        
        for campo in campos_obrigatorios:
            if not dados.get(campo):
                return jsonify({
                    'success': False,
                    'message': f'Campo {campo} é obrigatório'
                }), 400
        
        # Processar registro
        success, result = LogisticaController.registrar_carga_e_roteirizar(dados)
        
        if success:
            return jsonify({
                'success': True,
                'message': result['message'],
                'ids': result['ids']
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

@logistica_bp.route('/api/entregas', methods=['GET'])
def listar_entregas():
    try:
        filtro_status = request.args.get('status')
        
        from models.entrega_model import EntregaModel
        entregas = EntregaModel.listar_entregas(filtro_status)
        
        return jsonify({
            'success': True,
            'entregas': entregas
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }), 500

@logistica_bp.route('/api/cargas', methods=['GET'])
def listar_cargas():
    try:
        filtro_status = request.args.get('status')
        
        from models.carga_model import CargaModel
        cargas = CargaModel.listar_cargas(filtro_status)
        
        return jsonify({
            'success': True,
            'cargas': cargas
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }), 500