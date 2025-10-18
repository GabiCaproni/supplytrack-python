from database.connection import execute_query

class MotoristaModel:
    @staticmethod
    def cadastrar(id_usuario, cnh, status='LIVRE'):
        """Cadastra um novo motorista"""
        try:
            sql = "INSERT INTO motorista (id_usuario, cnh, status) VALUES (%s, %s, %s)"
            result = execute_query(sql, (id_usuario, cnh, status))
            
            # Retorno consistente - sempre retorna uma tupla
            if result:
                return result, "Motorista cadastrado com sucesso"
            else:
                return None, "Erro ao cadastrar motorista"
                
        except Exception as e:
            return None, f"Erro ao cadastrar motorista: {str(e)}"

    @staticmethod
    def listar_motoristas():
        """Lista todos os motoristas"""
        try:
            sql = """
            SELECT m.id_motorista, u.nome, u.email, m.cnh, m.status 
            FROM motorista m 
            JOIN usuario u ON m.id_usuario = u.id_usuario
            """
            result = execute_query(sql, fetch_all=True)
            return result if result else []
        except Exception as e:
            print(f"Erro ao listar motoristas: {str(e)}")
            return []

    @staticmethod
    def buscar_por_id(id_motorista):
        """Busca um motorista pelo ID"""
        try:
            sql = """
            SELECT m.id_motorista, u.nome, u.email, m.cnh, m.status 
            FROM motorista m 
            JOIN usuario u ON m.id_usuario = u.id_usuario
            WHERE m.id_motorista = %s
            """
            return execute_query(sql, (id_motorista,), fetch_one=True)
        except Exception as e:
            print(f"Erro ao buscar motorista: {str(e)}")
            return None

    @staticmethod
    def atualizar_status(id_motorista, status):
        """Atualiza o status de um motorista"""
        try:
            sql = "UPDATE motorista SET status = %s WHERE id_motorista = %s"
            result = execute_query(sql, (status, id_motorista))
            return result is not None
        except Exception as e:
            print(f"Erro ao atualizar status do motorista: {str(e)}")
            return False