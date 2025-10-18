from database.connection import execute_query
from datetime import datetime

class EntregaModel:
    
    @staticmethod
    def listar_entregas():
        """Lista todas as entregas"""
        try:
            sql = """
            SELECT e.*, r.DataSaida, r.distancia, v.placa, u.nome as motorista_nome,
                   c.volume, c.peso, a.nome as armazem_nome
            FROM entrega e
            LEFT JOIN rota r ON e.idRota = r.idRota
            LEFT JOIN motorista m ON e.id_motorista = m.id_motorista
            LEFT JOIN usuario u ON m.id_usuario = u.id_usuario
            LEFT JOIN veiculo v ON r.id_veiculo = v.id_veiculo
            LEFT JOIN carga c ON e.id_carga = c.id_carga
            LEFT JOIN armazem a ON c.id_armazem = a.id_armazem
            ORDER BY e.dataPrevista DESC
            """
            result = execute_query(sql, fetch_all=True)
            return result if result else []
        except Exception as e:
            print(f"Erro ao listar entregas: {str(e)}")
            return []

    @staticmethod
    def buscar_entrega_por_motorista(identrega, id_motorista):
        """Busca entrega verificando se pertence ao motorista"""
        try:
            sql = """
            SELECT e.*, r.DataSaida, r.distancia, v.placa, m.cnh, 
                   c.volume, c.peso, c.id_carga, u.nome as motorista_nome
            FROM entrega e
            LEFT JOIN rota r ON e.idRota = r.idRota
            LEFT JOIN veiculo v ON r.id_veiculo = v.id_veiculo
            LEFT JOIN motorista m ON e.id_motorista = m.id_motorista
            LEFT JOIN carga c ON e.id_carga = c.id_carga
            LEFT JOIN usuario u ON m.id_usuario = u.id_usuario
            WHERE e.idEntrega = %s AND e.id_motorista = %s
            """
            result = execute_query(sql, (identrega, id_motorista), fetch_one=True)
            return result if result else None
        except Exception as e:
            print(f"Erro ao buscar entrega do motorista: {e}")
            return None

    @staticmethod
    def atualizar_status_motorista(identrega, id_motorista, novo_status, observacoes=None):
        """
        Atualiza status da entrega com verificações de segurança
        """
        try:
            # Validar status
            status_validos = ['PENDENTE', 'EM_TRANSITO', 'ENTREGUE', 'CANCELADA', 'ATRASADA', 'PROBLEMA']
            if novo_status not in status_validos:
                return False, f"Status inválido. Use: {', '.join(status_validos)}"
            
            # Verificar se entrega pertence ao motorista
            entrega = EntregaModel.buscar_entrega_por_motorista(identrega, id_motorista)
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
                sql = "UPDATE entrega SET status = %s, observacoes = %s, dataRealizada = %s WHERE idEntrega = %s"
                params = (novo_status, observacoes, 
                         datetime.now().date() if novo_status == 'ENTREGUE' else None, 
                         identrega)
            else:
                sql = "UPDATE entrega SET status = %s, dataRealizada = %s WHERE idEntrega = %s"
                params = (novo_status, 
                         datetime.now().date() if novo_status == 'ENTREGUE' else None, 
                         identrega)
            
            result = execute_query(sql, params)
            
            if result is not None:
                # Atualizar status da carga relacionada
                if novo_status == 'ENTREGUE' and entrega.get('id_carga'):
                    from models.carga import CargaModel
                    CargaModel.atualizar_status(entrega['id_carga'], 'ENTREGUE')
                elif novo_status == 'EM_TRANSITO' and entrega.get('id_carga'):
                    from models.carga import CargaModel
                    CargaModel.atualizar_status(entrega['id_carga'], 'EM_TRANSITO')
                
                return True, "Status atualizado com sucesso"
            else:
                return False, "Erro ao atualizar status"
                
        except Exception as e:
            print(f"Erro ao atualizar status da entrega: {e}")
            return False, f"Erro interno: {str(e)}"

    @staticmethod
    def listar_entregas_motorista(id_motorista, filtro_status=None):
        """Lista entregas de um motorista específico"""
        try:
            sql = """
            SELECT e.*, r.DataSaida, r.distancia, v.placa, 
                   c.volume, c.peso, c.localizacaoAtual,
                   CASE 
                     WHEN e.dataPrevista < CURDATE() AND e.status = 'PENDENTE' THEN 'ATRASADA'
                     ELSE e.status
                   END as status_calculado
            FROM entrega e
            LEFT JOIN rota r ON e.idRota = r.idRota
            LEFT JOIN veiculo v ON r.id_veiculo = v.id_veiculo
            LEFT JOIN carga c ON e.id_carga = c.id_carga
            WHERE e.id_motorista = %s
            """
            
            params = [id_motorista]
            
            if filtro_status:
                if filtro_status == 'ATRASADA':
                    sql += " AND e.dataPrevista < CURDATE() AND e.status = 'PENDENTE'"
                else:
                    sql += " AND e.status = %s"
                    params.append(filtro_status)
            
            sql += " ORDER BY e.dataPrevista ASC"
            
            entregas = execute_query(sql, tuple(params), fetch_all=True)
            return entregas if entregas else []
        except Exception as e:
            print(f"Erro ao listar entregas do motorista: {e}")
            return []

    @staticmethod
    def criar_entrega(idRota, dataPrevista, id_motorista, id_carga=None):
        """Cria uma nova entrega"""
        try:
            sql = """
            INSERT INTO entrega (idRota, dataPrevista, status, id_motorista, id_carga) 
            VALUES (%s, %s, 'PENDENTE', %s, %s)
            """
            result = execute_query(sql, (idRota, dataPrevista, id_motorista, id_carga))
            
            if result:
                return result, "Entrega criada com sucesso"
            else:
                return None, "Erro ao criar entrega"
                
        except Exception as e:
            return None, f"Erro ao criar entrega: {str(e)}"