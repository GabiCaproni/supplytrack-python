from database.connection import execute_query

class VeiculoModel:
    @staticmethod
    def cadastrar(placa, capacidade, id_motorista=None):
        """Cadastra um novo veículo"""
        try:
            # Verificar se a placa já existe
            sql_verificar = "SELECT id_veiculo FROM veiculo WHERE placa = %s"
            existe = execute_query(sql_verificar, (placa,), fetch=True)
            
            if existe:
                return None, "❌ Placa já cadastrada"
            
            # Inserir veículo
            sql_inserir = """
            INSERT INTO veiculo (placa, capacidade, id_motorista, status) 
            VALUES (%s, %s, %s, 'DISPONIVEL')
            """
            params = (placa, capacidade, id_motorista)
            
            veiculo_id = execute_query(sql_inserir, params)
            
            if veiculo_id:
                return veiculo_id, "✅ Veículo cadastrado com sucesso"
            else:
                return None, "❌ Erro ao cadastrar veículo"
                
        except Exception as e:
            print(f"✗ Erro ao cadastrar veículo: {e}")
            return None, f"❌ Erro interno: {str(e)}"

    @staticmethod
    def listar_veiculos():
        """Lista todos os veículos"""
        try:
            sql = """
            SELECT 
                v.id_veiculo,
                v.placa,
                v.capacidade,
                v.status,
                v.id_motorista,
                u.nome as motorista_nome
            FROM veiculo v
            LEFT JOIN motorista m ON v.id_motorista = m.id_motorista
            LEFT JOIN usuario u ON m.id_usuario = u.id_usuario
            ORDER BY v.placa
            """
            return execute_query(sql, fetch_all=True) or []
        except Exception as e:
            print(f"✗ Erro ao listar veículos: {e}")
            return []

    @staticmethod
    def buscar_por_id(id_veiculo):
        """Busca veículo por ID"""
        try:
            sql = "SELECT * FROM veiculo WHERE id_veiculo = %s"
            result = execute_query(sql, (id_veiculo,), fetch=True)
            return result if result else None
        except Exception as e:
            print(f"✗ Erro ao buscar veículo por ID: {e}")
            return None

    @staticmethod
    def atualizar_status(id_veiculo, status):
        """Atualiza status do veículo"""
        try:
            sql = "UPDATE veiculo SET status = %s WHERE id_veiculo = %s"
            execute_query(sql, (status, id_veiculo))
            return True, "Status atualizado com sucesso"
        except Exception as e:
            print(f"✗ Erro ao atualizar status do veículo: {e}")
            return False, f"Erro ao atualizar status: {str(e)}"

    @staticmethod
    def vincular_motorista(id_veiculo, id_motorista):
        """Vincula um motorista ao veículo"""
        try:
            sql = "UPDATE veiculo SET id_motorista = %s WHERE id_veiculo = %s"
            execute_query(sql, (id_motorista, id_veiculo))
            return True, "Motorista vinculado com sucesso"
        except Exception as e:
            print(f"✗ Erro ao vincular motorista: {e}")
            return False, f"Erro ao vincular motorista: {str(e)}"