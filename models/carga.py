from database.connection import execute_query

class CargaModel:
    @staticmethod
    def cadastrar(volume, peso, id_armazem):
        """Cadastra uma nova carga"""
        try:
            sql = """
            INSERT INTO carga (volume, peso, status, localizacaoAtual, id_armazem) 
            VALUES (%s, %s, 'CADASTRADA', (SELECT nome FROM armazem WHERE id_armazem = %s), %s)
            """
            params = (volume, peso, id_armazem, id_armazem)
            
            carga_id = execute_query(sql, params)
            
            # Correção no retorno - removendo a tupla duplicada
            if carga_id:
                return carga_id, "Carga cadastrada com sucesso"
            else:
                return None, "Erro ao cadastrar carga"
                
        except Exception as e:
            return None, f"Erro: {str(e)}"

    @staticmethod
    def listar_cargas():
        """Lista todas as cargas"""
        try:
            sql = """
            SELECT c.*, a.nome as armazem_nome 
            FROM carga c 
            LEFT JOIN armazem a ON c.id_armazem = a.id_armazem
            ORDER BY c.id_carga DESC
            """
            result = execute_query(sql, fetch_all=True)
            return result if result else []
        except Exception as e:
            print(f"Erro ao listar cargas: {str(e)}")
            return []

    @staticmethod
    def atualizar_status(id_carga, status):
        """Atualiza o status de uma carga"""
        try:
            sql = "UPDATE carga SET status = %s WHERE id_carga = %s"
            result = execute_query(sql, (status, id_carga))
            return result is not None
        except Exception as e:
            print(f"Erro ao atualizar status da carga: {str(e)}")
            return False

    @staticmethod
    def buscar_por_id(id_carga):
        """Busca uma carga pelo ID"""
        try:
            sql = """
            SELECT c.*, a.nome as armazem_nome 
            FROM carga c 
            LEFT JOIN armazem a ON c.id_armazem = a.id_armazem
            WHERE c.id_carga = %s
            """
            return execute_query(sql, (id_carga,), fetch_one=True)
        except Exception as e:
            print(f"Erro ao buscar carga: {str(e)}")
            return None

    @staticmethod
    def atualizar_localizacao(id_carga, nova_localizacao):
        """Atualiza a localização atual da carga"""
        try:
            sql = "UPDATE carga SET localizacaoAtual = %s WHERE id_carga = %s"
            result = execute_query(sql, (nova_localizacao, id_carga))
            return result is not None
        except Exception as e:
            print(f"Erro ao atualizar localização da carga: {str(e)}")
            return False