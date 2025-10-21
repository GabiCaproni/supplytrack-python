from database.connection import execute_query

class CargaModel:
    @staticmethod
    def cadastrar(volume, peso, status, localizacaoAtual, id_armazem):
        """Cadastra uma nova carga"""
        try:
            print(f"Model - Cadastrando carga: {volume}, {peso}, {status}, {localizacaoAtual}, {id_armazem}")  # Debug
            
            sql = """
            INSERT INTO carga (volume, peso, status, localizacaoAtual, id_armazem) 
            VALUES (%s, %s, %s, %s, %s)
            """
            params = (volume, peso, status, localizacaoAtual, id_armazem)
            
            print(f"Executando SQL: {sql}")
            print(f"Com parâmetros: {params}")
            
            carga_id = execute_query(sql, params)
            
            if carga_id:
                return carga_id, "✅ Carga cadastrada com sucesso"
            else:
                return None, "❌ Erro ao cadastrar carga"
                
        except Exception as e:
            print(f"✗ Erro ao cadastrar carga: {e}")
            return None, f"❌ Erro interno: {str(e)}"

    @staticmethod
    def listar_cargas():
        """Lista todas as cargas"""
        try:
            sql = """
            SELECT 
                id_carga,
                volume,
                peso,
                status,
                localizacaoAtual,
                id_armazem
            FROM carga 
            """
            return execute_query(sql, fetch_all=True) or []
        except Exception as e:
            print(f"✗ Erro ao listar cargas: {e}")
            return []