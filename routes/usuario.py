from database.connection import execute_query
from werkzeug.security import generate_password_hash, check_password_hash

class UsuarioModel:
    @staticmethod
    def cadastrar(nome, email, senha, tipo_perfil):
        """Cadastra um novo usuário"""
        try:
            # Verificar se email já existe
            usuario_existente = UsuarioModel.buscar_por_email(email)
            if usuario_existente:
                return None, "Email já cadastrado"
            
            senha_hash = generate_password_hash(senha)
            
            sql = "INSERT INTO usuario (nome, email, senha, tipo_perfil) VALUES (%s, %s, %s, %s)"
            params = (nome, email, senha_hash, tipo_perfil)
            
            usuario_id = execute_query(sql, params)
            
            if usuario_id:
                # Se for motorista, criar registro na tabela motorista
                if tipo_perfil == 'MOTORISTA':
                    from models.motorista import MotoristaModel
                    MotoristaModel.cadastrar(usuario_id, f"CNH-{usuario_id}")
                
                return usuario_id, "Usuário cadastrado com sucesso"
            else:
                return None, "Erro ao cadastrar usuário"
                
        except Exception as e:
            print(f"✗ Erro no cadastro: {e}")
            return None, f"Erro interno: {str(e)}"

    @staticmethod
    def buscar_por_email(email):
        sql = "SELECT * FROM usuario WHERE email = %s"
        return execute_query(sql, (email,), fetch=True)

    @staticmethod
    def verificar_login(email, senha):
        usuario = UsuarioModel.buscar_por_email(email)
        if usuario and check_password_hash(usuario['senha'], senha):
            return usuario
        return None

    @staticmethod
    def listar_usuarios():
        sql = "SELECT id_usuario, nome, email, tipo_perfil FROM usuario ORDER BY nome"
        return execute_query(sql, fetch_all=True) or []