from database.connection import execute_query
from werkzeug.security import generate_password_hash, check_password_hash

class UsuarioModel:
    @staticmethod
    def cadastrar(nome, email, cpf, senha, tipo_perfil): # CPF ADICIONADO AQUI
        """Cadastra um novo usuário"""
        try:
            # Verificar se email já existe
            usuario_existente = UsuarioModel.buscar_por_email(email)
            if usuario_existente:
                return None, "❌ Email já cadastrado"
            
            senha_hash = generate_password_hash(senha)
            
            sql = """
            INSERT INTO usuario (nome, email, cpf, senha, tipo_perfil) 
            VALUES (%s, %s, %s, %s, %s)
            """
            params = (nome, email, cpf, senha_hash, tipo_perfil) # CPF ADICIONADO AQUI
            
            usuario_id = execute_query(sql, params)
            
            if usuario_id:
                # Se for motorista, criar registro na tabela motorista
                if tipo_perfil == 'MOTORISTA':
                    from models.motorista import MotoristaModel
                    cnh = f"CNH{usuario_id:06d}"
                    motorista_id = MotoristaModel.cadastrar(usuario_id, cnh, 'LIVRE')
                    if motorista_id:
                        print(f"✓ Motorista cadastrado com CNH: {cnh}")
                
                return usuario_id, "✅ Usuário cadastrado com sucesso"
            else:
                return None, "❌ Erro ao cadastrar usuário"
                
        except Exception as e:
            print(f"✗ Erro no cadastro de usuário: {e}")
            return None, f"❌ Erro interno: {str(e)}"
    @staticmethod
    def buscar_por_email(email):
        """Busca usuário por email."""
        try:
            sql = "SELECT * FROM usuario WHERE email = %s"
            result = execute_query(sql, (email,), fetch=True) 
            
            # Verifica se encontrou algum resultado
            if result and len(result) > 0:
                return result
            return None
        except Exception as e:
            print(f"✗ Erro ao buscar usuário por email: {e}")
            return None

    @staticmethod
    def verificar_login(email, senha):
        """Verifica as credenciais de login."""
        try:
            usuario = UsuarioModel.buscar_por_email(email)
            
            # Debug: Mostrar o que foi encontrado
            print(f"DEBUG - Usuário encontrado: {usuario}")
            print(f"DEBUG - Email digitado: {email}")
            print(f"DEBUG - Senha digitada: {senha}")
            
            if usuario:
                # Verifica se a senha está correta
                senha_correta = check_password_hash(usuario['senha'], senha)
                print(f"DEBUG - Senha correta: {senha_correta}")
                
                if senha_correta:
                    return usuario
                else:
                    print("DEBUG - Senha incorreta")
                    return None
            else:
                print("DEBUG - Usuário não encontrado")
                return None
                
        except Exception as e:
            print(f"✗ Erro ao verificar login: {e}")
            return None

    @staticmethod
    def listar_usuarios():
        """Lista todos os usuários"""
        try:
            sql = "SELECT id_usuario, nome, email, tipo_perfil FROM usuario ORDER BY nome"
            resultados = execute_query(sql, fetch_all=True)
            return resultados if resultados else []
        except Exception as e:
            print(f"✗ Erro ao listar usuários: {e}")
            return []

    @staticmethod
    def buscar_por_id(id_usuario):
        """Busca usuário por ID"""
        try:
            sql = "SELECT * FROM usuario WHERE id_usuario = %s"
            result = execute_query(sql, (id_usuario,), fetch=True)
            return result if result else None
        except Exception as e:
            print(f"✗ Erro ao buscar usuário por ID: {e}")
            return None