from models.entrega import EntregaModel

class EntregaController:
    @staticmethod
    def listar_entregas():
        """Controller para listar todas as entregas"""
        try:
            print("🎯 CONTROLLER - Listando todas as entregas")
            
            entregas = EntregaModel.listar_entregas()
            print(f"📋 Total de entregas encontradas: {len(entregas)}")
            
            return True, entregas
            
        except Exception as e:
            print(f"❌ Erro ao listar entregas no controller: {str(e)}")
            return False, f"Erro ao buscar entregas: {str(e)}"

    @staticmethod
    def listar_entregas_ativas():
        """Controller para listar entregas ativas"""
        try:
            print("🎯 CONTROLLER - Listando entregas ativas")
            
            entregas = EntregaModel.listar_entregas_ativas()
            print(f"📋 Entregas ativas encontradas: {len(entregas)}")
            
            return True, entregas
            
        except Exception as e:
            print(f"❌ Erro ao listar entregas ativas no controller: {str(e)}")
            return False, f"Erro ao buscar entregas ativas: {str(e)}"

    @staticmethod
    def criar_entrega(data_entrega, status, local_entrega, id_rota=None, id_carga=None, observacoes=None):
        """Controller para criar uma nova entrega"""
        try:
            print(f"🎯 CONTROLLER - Criando entrega:")
            print(f"   data_entrega: {data_entrega}")
            print(f"   status: {status}")
            print(f"   local_entrega: {local_entrega}")
            print(f"   id_rota: {id_rota}")
            print(f"   id_carga: {id_carga}")
            
            # Chamar model para cadastrar entrega
            entrega_id, mensagem = EntregaModel.criar_entrega(
                data_entrega=data_entrega,
                status=status,
                local_entrega=local_entrega,
                id_rota=id_rota,
                id_carga=id_carga,
                observacoes=observacoes
            )
            
            if entrega_id:
                return True, {
                    'message': mensagem,
                    'id_entrega': entrega_id
                }
            else:
                return False, mensagem
                
        except Exception as e:
            print(f"❌ Erro no controller de entrega: {str(e)}")
            return False, f"Erro interno: {str(e)}"