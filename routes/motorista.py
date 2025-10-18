from flask import Blueprint, request, jsonify
from controllers.motorista_controller import MotoristaController

motorista_bp = Blueprint('motorista', __name__)

@motorista_bp.route('/api/motorista/<int:u_motorista>/entregas', methods=['GET'])
def listar_entregas_motorista(u_motorista):
    try:
        filtro_status = request.args.get('status')
        
        success, result = MotoristaController.get_entregas_motorista(u_motorista, filtro_status)
        
        if success:
            return jsonify({
                'success': True,
                'entregas': result
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

@motorista_bp.route('/api/motorista/<int:u_motorista>/entregas/<int:identrega>/status', methods=['PUT'])
def atualizar_status_entrega(u_motorista, identrega):
    try:
        dados = request.get_json()
        novo_status = dados.get('status')
        observacoes = dados.get('observacoes')
        
        if not novo_status:
            return jsonify({
                'success': False,
                'message': 'Status é obrigatório'
            }), 400
        
        success, message = MotoristaController.atualizar_status_entrega(
            u_motorista, identrega, novo_status, observacoes
        )
        
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

@motorista_bp.route('/api/motorista/<int:u_motorista>/entregas/<int:identrega>/simular', methods=['POST'])
def simular_viagem(u_motorista, identrega):
    try:
        success, resultados = MotoristaController.simular_viagem(u_motorista, identrega)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Simulação concluída',
                'resultados': resultados
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Erro na simulação',
                'resultados': resultados
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }), 500

@motorista_bp.route('/api/motorista/<int:u_motorista>/dashboard', methods=['GET'])
def dashboard_motorista(u_motorista):
    try:
        from models.entrega_model import EntregaModel
        
        # Estatísticas do motorista
        entregas = EntregaModel.listar_entregas_motorista(u_motorista)
        
        stats = {
            'total_entregas': len(entregas),
            'entregas_pendentes': len([e for e in entregas if e['status'] in ['PENDENTE', 'ATRASADA']]),
            'entregas_andamento': len([e for e in entregas if e['status'] == 'EM_TRANSITO']),
            'entregas_concluidas': len([e for e in entregas if e['status'] == 'ENTREGUE']),
            'entregas_hoje': len([e for e in entregas if e.get('dataprevista') == datetime.now().date()])
        }
        
        # Próximas entregas
        proximas_entregas = [e for e in entregas if e['status'] in ['PENDENTE', 'EM_TRANSITO']][:5]
        
        return jsonify({
            'success': True,
            'stats': stats,
            'proximas_entregas': proximas_entregas
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }), 500