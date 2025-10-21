from database.connection import execute_query

class EntregaModel:
    @staticmethod
    def listar_entregas():
        """Lista todas as entregas"""
        try:
            print("📦 MODEL - Listando todas as entregas")
            
            sql = """
            SELECT 
                e.id_entrega,
                e.data_entrega,
                e.status,
                e.local_entrega,
                e.observacoes,
                r.idRota,
                r.DataSaida,
                r.dataEntrega,
                r.distancia,
                r.status as status_rota,
                c.id_carga,
                c.volume,
                c.peso,
                c.status as status_carga
            FROM entrega e
            LEFT JOIN rota r ON e.id_rota = r.idRota
            LEFT JOIN carga c ON e.id_carga = c.id_carga
            ORDER BY e.data_entrega DESC
            """
            
            entregas = execute_query(sql, fetch_all=True)
            print(f"📊 Entregas recuperadas: {len(entregas) if entregas else 0}")
            
            return entregas or []
            
        except Exception as e:
            print(f"❌ Erro ao listar entregas no model: {e}")
            return []

    @staticmethod
    def listar_entregas_ativas():
        """Lista apenas entregas ativas"""
        try:
            print("📦 MODEL - Listando entregas ativas")
            
            sql = """
            SELECT 
                e.id_entrega,
                e.data_entrega,
                e.status,
                e.local_entrega,
                e.observacoes,
                r.idRota,
                r.DataSaida,
                r.dataEntrega,
                r.distancia,
                r.status as status_rota,
                c.id_carga,
                c.volume,
                c.peso,
                c.status as status_carga
            FROM entrega e
            LEFT JOIN rota r ON e.id_rota = r.idRota
            LEFT JOIN carga c ON e.id_carga = c.id_carga
            WHERE e.status IN ('PENDENTE', 'EM_ANDAMENTO', 'AGENDADA')
            ORDER BY e.data_entrega ASC
            """
            
            entregas = execute_query(sql, fetch_all=True)
            print(f"📊 Entregas ativas recuperadas: {len(entregas) if entregas else 0}")
            
            return entregas or []
            
        except Exception as e:
            print(f"❌ Erro ao listar entregas ativas no model: {e}")
            return []

    @staticmethod
    def criar_entrega(data_entrega, status, local_entrega, id_rota=None, id_carga=None, observacoes=None):
        """Cria uma nova entrega"""
        try:
            print(f"🎯 MODEL - Criando entrega:")
            print(f"   data_entrega: {data_entrega}")
            print(f"   status: {status}")
            print(f"   local_entrega: {local_entrega}")
            print(f"   id_rota: {id_rota}")
            print(f"   id_carga: {id_carga}")
            
            sql = """
            INSERT INTO entrega (data_entrega, status, local_entrega, id_rota, id_carga, observacoes) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (data_entrega, status, local_entrega, id_rota, id_carga, observacoes)
            
            print(f"🔍 SQL: {sql}")
            print(f"🔍 Params: {params}")
            
            entrega_id = execute_query(sql, params)
            
            if entrega_id:
                return entrega_id, "✅ Entrega cadastrada com sucesso"
            else:
                return None, "❌ Erro ao cadastrar entrega"
                
        except Exception as e:
            print(f"❌ Erro no model de entrega: {str(e)}")
            return None, f"❌ Erro interno: {str(e)}"