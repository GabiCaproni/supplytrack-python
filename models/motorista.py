from database.connection import execute_query

class MotoristaModel:
    @staticmethod
    def cadastrar(id_usuario, cnh, status='LIVRE'):
        """Cadastra um novo motorista"""
        try:
            # Verificar se CNH já existe
            sql_verificar = "SELECT id_motorista FROM motorista WHERE cnh = %s"
            existe = execute_query(sql_verificar, (cnh,), fetch=True)
            
            if existe:
                return None, "❌ CNH já cadastrada"
            
            # Verificar se usuário já é motorista
            sql_verificar_usuario = "SELECT id_motorista FROM motorista WHERE id_usuario = %s"
            existe_usuario = execute_query(sql_verificar_usuario, (id_usuario,), fetch=True)
            
            if existe_usuario:
                return None, "❌ Este usuário já é um motorista"
            
            # Inserir motorista
            sql_inserir = """
            INSERT INTO motorista (id_usuario, cnh, status) 
            VALUES (%s, %s, %s)
            """
            params = (id_usuario, cnh, status)
            
            motorista_id = execute_query(sql_inserir, params)
            
            if motorista_id:
                return motorista_id, "✅ Motorista cadastrado com sucesso"
            else:
                return None, "❌ Erro ao cadastrar motorista"
                
        except Exception as e:
            print(f"✗ Erro ao cadastrar motorista: {e}")
            return None, f"❌ Erro interno: {str(e)}"

    @staticmethod
    def listar_motoristas():
        """Lista todos os motoristas"""
        try:
            sql = """
            SELECT 
                m.id_motorista,
                m.cnh,
                m.status,
                u.id_usuario,
                u.nome,
                u.email
            FROM motorista m
            JOIN usuario u ON m.id_usuario = u.id_usuario
            ORDER BY u.nome
            """
            return execute_query(sql, fetch_all=True) or []
        except Exception as e:
            print(f"✗ Erro ao listar motoristas: {e}")
            return []

    @staticmethod
    def buscar_por_id(id_motorista):
        """Busca motorista por ID"""
        try:
            sql = """
            SELECT 
                m.*,
                u.nome,
                u.email
            FROM motorista m
            JOIN usuario u ON m.id_usuario = u.id_usuario
            WHERE m.id_motorista = %s
            """
            result = execute_query(sql, (id_motorista,), fetch=True)
            return result if result else None
        except Exception as e:
            print(f"✗ Erro ao buscar motorista por ID: {e}")
            return None

    @staticmethod
    def buscar_por_usuario_id(id_usuario):
        """Busca motorista por ID do usuário"""
        try:
            sql = """
            SELECT 
                m.*,
                u.nome,
                u.email
            FROM motorista m
            JOIN usuario u ON m.id_usuario = u.id_usuario
            WHERE m.id_usuario = %s
            """
            result = execute_query(sql, (id_usuario,), fetch=True)
            return result if result else None
        except Exception as e:
            print(f"✗ Erro ao buscar motorista por usuário: {e}")
            return None

    @staticmethod
    def atualizar_status(id_motorista, status):
        """Atualiza status do motorista"""
        try:
            sql = "UPDATE motorista SET status = %s WHERE id_motorista = %s"
            execute_query(sql, (status, id_motorista))
            return True, "Status atualizado com sucesso"
        except Exception as e:
            print(f"✗ Erro ao atualizar status do motorista: {e}")
            return False, f"Erro ao atualizar status: {str(e)}"