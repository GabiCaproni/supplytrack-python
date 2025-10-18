from database.connection import execute_query
from datetime import datetime

class EntregaModel:
    # ... (métodos anteriores permanecem)
    
    @staticmethod
    def buscar_entrega_por_motorista(identrega, u_motorista):
        """Busca entrega verificando se pertence ao motorista"""
        try:
            sql = """
            SELECT e.*, r.origem, r.destino, v.placa, m.cnh, 
                   c.volume, c.peso, c.idcarga, u.nome as motorista_nome
            FROM entrega e
            LEFT JOIN rota r ON e.u_rota = r.u_rota
            LEFT JOIN veiculo v ON e.u_veiculo = v.u_veiculo
            LEFT JOIN motorista m ON e.u_motorista = m.u_motorista
            LEFT JOIN carga c ON e.idcarga = c.idcarga
            LEFT JOIN usuario u ON m.u_motorista = u.u_motorista
            WHERE e.identrega = %s AND e.u_motorista = %s
            """
            result = execute_query(sql, (identrega, u_motorista), fetch=True)
            return result[0] if result and len(result) > 0 else None
        except Exception as e:
            print(f"Erro ao buscar entrega do motorista: {e}")
            return None

    @staticmethod
    def atualizar_status_motorista(identrega, u_motorista, novo_status, observacoes=None):
        """
        Atualiza status da entrega com verificações de segurança
        """
        try:
            # Validar status
            status_validos = ['PENDENTE', 'EM_TRANSITO', 'ENTREGUE', 'CANCELADA', 'ATRASADA', 'PROBLEMA']
            if novo_status not in status_validos:
                return False, f"Status inválido. Use: {', '.join(status_validos)}"
            
            # Verificar se entrega pertence ao motorista
            entrega = EntregaModel.buscar_entrega_por_motorista(identrega, u_motorista)
            if not entrega:
                return False, "Entrega não encontrada ou não pertence a este motorista"
            
            # Lógica de transição de status
            status_atual = entrega['status']
            transicoes_validas = {
                'PENDENTE': ['EM_TRANSITO', 'CANCELADA'],
                'EM_TRANSITO': ['ENTREGUE', 'ATRASADA', 'PROBLEMA'],
                'ATRASADA': ['ENTREGUE', 'PROBLEMA'],
                'PROBLEMA': ['EM_TRANSITO', 'ENTREGUE'],
                'ENTREGUE': [],  # Estado final
                'CANCELADA': []  # Estado final
            }
            
            if novo_status not in transicoes_validas.get(status_atual, []):
                return False, f"Transição de {status_atual} para {novo_status} não é permitida"
            
            # Atualizar entrega
            if observacoes:
                sql = "UPDATE entrega SET status = %s, observacoes = %s, datarealizada = %s WHERE identrega = %s"
                params = (novo_status, observacoes, 
                         datetime.now().date() if novo_status == 'ENTREGUE' else None, 
                         identrega)
            else:
                sql = "UPDATE entrega SET status = %s, datarealizada = %s WHERE identrega = %s"
                params = (novo_status, 
                         datetime.now().date() if novo_status == 'ENTREGUE' else None, 
                         identrega)
            
            result = execute_query(sql, params)
            
            if result is not None:
                # Atualizar status da carga relacionada
                from models.carga_model import CargaModel
                if novo_status == 'ENTREGUE':
                    CargaModel.atualizar_status(entrega['idcarga'], 'ENTREGUE', 'Destino')
                elif novo_status == 'EM_TRANSITO':
                    CargaModel.atualizar_status(entrega['idcarga'], 'EM_TRANSITO', 'Em trânsito')
                
                # Gerar alertas se necessário
                EntregaModel._gerar_alertas_automaticos(identrega, novo_status, entrega)
                
                return True, "Status atualizado com sucesso"
            else:
                return False, "Erro ao atualizar status"
                
        except Exception as e:
            print(f"Erro ao atualizar status da entrega: {e}")
            return False, f"Erro interno: {str(e)}"

    @staticmethod
    def _gerar_alertas_automaticos(identrega, novo_status, entrega):
        """Gera alertas automáticos baseados em mudanças de status"""
        try:
            from models.alerta_model import AlertaModel
            
            alertas = []
            
            if novo_status == 'ATRASADA':
                alertas.append({
                    'tipo': 'ATRASO',
                    'titulo': f'Entrega #{identrega} atrasada',
                    'descricao': f'Entrega para {entrega["destino"]} está atrasada',
                    'identrega': identrega,
                    'u_motorista': entrega['u_motorista']
                })
            elif novo_status == 'PROBLEMA':
                alertas.append({
                    'tipo': 'ROTA',
                    'titulo': f'Problema na entrega #{identrega}',
                    'descricao': f'Problema reportado na entrega para {entrega["destino"]}',
                    'identrega': identrega,
                    'u_motorista': entrega['u_motorista']
                })
            elif novo_status == 'ENTREGUE':
                alertas.append({
                    'tipo': 'ROTA',
                    'titulo': f'Entrega #{identrega} concluída',
                    'descricao': f'Entrega para {entrega["destino"]} foi concluída com sucesso',
                    'identrega': identrega,
                    'u_motorista': entrega['u_motorista']
                })
            
            for alerta in alertas:
                AlertaModel.criar_alerta(
                    tipo=alerta['tipo'],
                    titulo=alerta['titulo'],
                    descricao=alerta['descricao'],
                    identrega=alerta['identrega'],
                    u_motorista=alerta['u_motorista']
                )
                
        except Exception as e:
            print(f"Erro ao gerar alertas automáticos: {e}")

    @staticmethod
    def listar_entregas_motorista(u_motorista, filtro_status=None):
        """Lista entregas de um motorista específico"""
        try:
            sql = """
            SELECT e.*, r.origem, r.destino, v.placa, 
                   c.volume, c.peso, c.localizacao_atual,
                   CASE 
                     WHEN e.dataprevista < CURDATE() AND e.status = 'PENDENTE' THEN 'ATRASADA'
                     ELSE e.status
                   END as status_calculado
            FROM entrega e
            LEFT JOIN rota r ON e.u_rota = r.u_rota
            LEFT JOIN veiculo v ON e.u_veiculo = v.u_veiculo
            LEFT JOIN carga c ON e.idcarga = c.idcarga
            WHERE e.u_motorista = %s
            """
            
            params = [u_motorista]
            
            if filtro_status:
                if filtro_status == 'ATRASADA':
                    sql += " AND e.dataprevista < CURDATE() AND e.status = 'PENDENTE'"
                else:
                    sql += " AND e.status = %s"
                    params.append(filtro_status)
            
            sql += " ORDER BY e.dataprevista ASC"
            
            entregas = execute_query(sql, tuple(params), fetch=True)
            return entregas or []
        except Exception as e:
            print(f"Erro ao listar entregas do motorista: {e}")
            return []