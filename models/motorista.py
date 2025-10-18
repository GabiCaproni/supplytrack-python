from database.connection import execute_query

class MotoristaModel:
    @staticmethod
    def cadastrar(id_usuario, cnh, status='LIVRE'):
        sql = "INSERT INTO motorista (id_usuario, cnh, status) VALUES (%s, %s, %s)"
        return execute_query(sql, (id_usuario, cnh, status))

    @staticmethod
    def listar_motoristas():
        sql = """
        SELECT m.id_motorista, u.nome, u.email, m.cnh, m.status 
        FROM motorista m 
        JOIN usuario u ON m.id_usuario = u.id_usuario
        """
        return execute_query(sql, fetch_all=True) or []