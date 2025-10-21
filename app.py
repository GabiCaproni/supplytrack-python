from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

# Importar todas as rotas
from routes.usuario import usuario_bp
from routes.veiculo import veiculo_bp
from routes.motorista import motorista_bp
from routes.entrega import entrega_bp
from routes.carga import carga_bp
from routes.rota import rota_bp
from routes.logistica import logistica_bp
from routes.dashboard import dashboard_bp  # Agora importa o blueprint corrigido

def create_app():
    app = Flask(__name__)
    CORS(app)  # Permitir requisições de diferentes origens
    
    # Configurações
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.config['JSON_SORT_KEYS'] = False
    
    # ========== REGISTRAR TODAS AS ROTAS ==========
    
    app.register_blueprint(usuario_bp, url_prefix='/api')
    app.register_blueprint(veiculo_bp, url_prefix='/api')
    app.register_blueprint(motorista_bp, url_prefix='/api')
    app.register_blueprint(entrega_bp, url_prefix='/api')
    app.register_blueprint(carga_bp, url_prefix='/api')
    app.register_blueprint(rota_bp, url_prefix='/api')
    app.register_blueprint(logistica_bp, url_prefix='/api')
    app.register_blueprint(dashboard_bp, url_prefix='/api')  # Agora registra o blueprint corrigido
    
    # ========== ROTAS BÁSICAS ==========
    
    @app.route('/')
    def home():
        """Página inicial do SupplyTrack"""
        try:
            return send_from_directory('frontend', 'index.html')
        except FileNotFoundError:
            return jsonify({
                'message': '🚚 SupplyTrack API - Sistema de Gestão Logística',
                'version': '1.0.0',
                'endpoints': {
                    'dashboard': '/dashboard',
                    'api_tester': '/api-tester', 
                    'documentation': 'https://github.com/GabiCaproni/supplytrack-python'
                }
            })
    
    @app.route('/health')
    def health_check():
        return jsonify({'status': 'healthy', 'service': 'supplytrack-api'})
    
    # ========== SERVER FRONTEND DO DASHBOARD ==========
    
    @app.route('/api-tester')
    def api_tester():
        """Serve a página de teste de APIs"""
        try:
            return send_from_directory('frontend', 'api-tester.html')
        except FileNotFoundError:
            return jsonify({'error': 'API Tester não encontrado'}), 404

    @app.route('/dashboard')
    def serve_dashboard():
        """Serve a interface web do dashboard"""
        try:
            return send_from_directory('frontend', 'dashboard.html')
        except FileNotFoundError:
            return jsonify({'error': 'Dashboard não encontrado'}), 404
    
    # ========== ROTA PARA DADOS DO DASHBOARD ==========
    
    @app.route('/api/dashboard')
    def api_dashboard():
        """Rota alternativa para o dashboard (para compatibilidade)"""
        try:
            from controllers.dashboardController import dashboardController
            success, result = dashboardController.get_dashboard_data()
            
            if success:
                return jsonify({
                    'success': True,
                    'data': result
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': result
                }), 500
                
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/<path:filename>')
    def serve_static(filename):
        """Serve arquivos estáticos (CSS, JS, imagens)"""
        try:
            return send_from_directory('frontend', filename)
        except FileNotFoundError:
            return jsonify({'error': 'Arquivo não encontrado'}), 404
    
    return app

# Criar e configurar a aplicação
app = create_app()

if __name__ == '__main__':
    print("🚀 Iniciando SupplyTrack API...")
    print("📊 Dashboard disponível em: http://localhost:5000/dashboard")
    print("🔗 API disponível em: http://localhost:5000/api")
    print("⏹️  Para parar: Ctrl+C")
    
    # Executar a aplicação
    app.run(
        host='0.0.0.0', 
        port=5000, 
        debug=True,  # Modo desenvolvimento - desative em produção
        threaded=True
    )