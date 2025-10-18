from database.connection import execute_query
from werkzeug.security import generate_password_hash, check_password_hash

class UsuarioModel:
    @staticmethod
    def cadastrar(nome, email, senha, tipo_perfil):
        """Cadastra um novo usuário - CORRIGIDO: sem id_motorista"""
        try:
            # Verificar se email já existe
            usuario_existente = UsuarioModel.buscar_por_email(email)
            if usuario_existente:
                return None, "Email já cadastrado"
            
            senha_hash = generate_password_hash(senha)
            
            # CORREÇÃO: Removido id_motorista do INSERT
            sql = """
            INSERT INTO usuario (nome, email, senha, tipo_perfil) 
            VALUES (%s, %s, %s, %s)
            """
            params = (nome, email, senha_hash, tipo_perfil)
            
            usuario_id = execute_query(sql, params)
            
            if usuario_id:
                # CORREÇÃO: Se for motorista, criar registro na tabela motorista APÓS criar usuário
                if tipo_perfil == 'MOTORISTA':
                    from models.motorista import MotoristaModel
                    # Gera uma CNH fictícia baseada no ID
                    cnh = f"CNH{usuario_id:06d}"
                    motorista_id = MotoristaModel.cadastrar(usuario_id, cnh, 'LIVRE')
                    if motorista_id:
                        print(f"✓ Motorista cadastrado com CNH: {cnh}")
                
                return usuario_id, "Usuário cadastrado com sucesso"
            else:
                return None, "Erro ao cadastrar usuário"
                
        except Exception as e:
            print(f"✗ Erro no cadastro de usuário: {e}")
            return None, f"Erro interno: {str(e)}"

    @staticmethod
    def buscar_por_email(email):
        """Busca usuário por email."""
        try:
            sql = "SELECT * FROM usuario WHERE email = %s"
            result = execute_query(sql, (email,), fetch=True) 
            return result if result else None
        except Exception as e:
            print(f"✗ Erro ao buscar usuário por email: {e}")
            return None

    @staticmethod
    def verificar_login(email, senha):
        """Verifica a senha de login."""
        try:
            usuario = UsuarioModel.buscar_por_email(email)
            if usuario and check_password_hash(usuario['senha'], senha):
                return usuario
            return None
        except Exception as e:
            print(f"✗ Erro ao verificar senha: {e}")
            return None

    @staticmethod
    def listar_usuarios():
        """Lista todos os usuários - CORRIGIDO: sem id_motorista"""
        try:
            # CORREÇÃO: Removido id_motorista da consulta
            sql = "SELECT id_usuario, nome, email, tipo_perfil FROM usuario ORDER BY nome"
            return execute_query(sql, fetch_all=True) or []
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