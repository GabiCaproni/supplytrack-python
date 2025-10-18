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
            return carga_id, "Carga cadastrada com sucesso" if carga_id else (None, "Erro ao cadastrar carga")
            
        except Exception as e:
            return None, f"Erro: {str(e)}"

    @staticmethod
    def listar_cargas():
        sql = """
        SELECT c.*, a.nome as armazem_nome 
        FROM carga c 
        LEFT JOIN armazem a ON c.id_armazem = a.id_armazem
        ORDER BY c.id_carga DESC
        """
        return execute_query(sql, fetch_all=True) or []

    @staticmethod
    def atualizar_status(id_carga, status):
        sql = "UPDATE carga SET status = %s WHERE id_carga = %s"
        return execute_query(sql, (status, id_carga))