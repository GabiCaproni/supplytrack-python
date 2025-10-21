from database.connection import execute_query

class RotaModel:
    @staticmethod
    def cadastrar(dataSaida, dataEntrega, distancia, status):
        """Cadastra uma nova rota"""
        try:
            print(f"🎯 MODEL - Cadastrando rota:")
            print(f"   dataSaida: {dataSaida}")
            print(f"   dataEntrega: {dataEntrega}") 
            print(f"   distancia: {distancia}")
            print(f"   status: {status}")
            
            # ✅ CORRIGIDO: Mapear status para valores válidos do ENUM
            status_validos = {
                'PLANEJADA': 'PENDENTE',  # Mapear PLANEJADA para PENDENTE
                'PENDENTE': 'PENDENTE',
                'EM_TRANSITO': 'EM_ANDAMENTO',  # Mapear EM_TRANSITO para EM_ANDAMENTO
                'EM_ANDAMENTO': 'EM_ANDAMENTO',
                'ENTREGUE': 'CONCLUIDA',  # Mapear ENTREGUE para CONCLUIDA
                'CONCLUIDA': 'CONCLUIDA',
                'CANCELADA': 'CANCELADA',
                'ATRASADA': 'PENDENTE'  # Mapear ATRASADA para PENDENTE
            }
            
            # Converter status para valor válido
            status_valido = status_validos.get(status, 'PENDENTE')
            print(f"🔄 Status convertido: '{status}' → '{status_valido}'")
            
            sql = """
            INSERT INTO rota (DataSaida, dataEntrega, distancia, status) 
            VALUES (%s, %s, %s, %s)
            """
            params = (dataSaida, dataEntrega, distancia, status_valido)
            
            print(f"🔍 SQL: {sql}")
            print(f"🔍 Params: {params}")
            
            rota_id = execute_query(sql, params)
            
            if rota_id:
                return rota_id, "✅ Rota cadastrada com sucesso"
            else:
                return None, "❌ Erro ao cadastrar rota"
                
        except Exception as e:
            print(f"❌ Erro no model: {str(e)}")
            return None, f"❌ Erro interno: {str(e)}"

    @staticmethod
    def listar_rotas():
        """Lista todas as rotas"""
        try:
            print("📋 MODEL - Listando rotas do banco")
            
            sql = """
            SELECT 
                idRota,
                DataSaida,
                dataEntrega,
                distancia,
                status,
                id_veiculo,
                id_motorista
            FROM rota 
            ORDER BY DataSaida DESC
            """
            
            rotas = execute_query(sql, fetch_all=True)
            print(f"📊 Rotas recuperadas: {len(rotas) if rotas else 0}")
            
            return rotas or []
            
        except Exception as e:
            print(f"❌ Erro ao listar rotas no model: {e}")
            return []