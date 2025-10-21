from models.rota import RotaModel

class RotaController:
    @staticmethod
    def listar_rotas():
        """Controller para listar todas as rotas"""
        try:
            print("🎯 CONTROLLER - Listando rotas")
            
            rotas = RotaModel.listar_rotas()
            print(f"📋 Rotas encontradas: {len(rotas)}")
            
            return True, rotas
            
        except Exception as e:
            print(f"❌ Erro ao listar rotas no controller: {str(e)}")
            return False, f"Erro ao buscar rotas: {str(e)}"

    @staticmethod
    def criar_rota(dataSaida, dataEntrega, distancia, status):
        """Controller para criar uma nova rota"""
        try:
            print(f"🎯 CONTROLLER - Criando rota:")
            print(f"   dataSaida: {dataSaida}")
            print(f"   dataEntrega: {dataEntrega}")
            print(f"   distancia: {distancia}") 
            print(f"   status: {status}")
            
            # Chamar model para cadastrar rota
            rota_id, mensagem = RotaModel.cadastrar(
                dataSaida=dataSaida,
                dataEntrega=dataEntrega,
                distancia=distancia,
                status=status
            )
            
            if rota_id:
                return True, {
                    'message': mensagem,
                    'id_rota': rota_id
                }
            else:
                return False, mensagem
                
        except Exception as e:
            print(f"❌ Erro no controller: {str(e)}")
            return False, f"Erro interno: {str(e)}"