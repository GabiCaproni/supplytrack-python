from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

# Importar todas as rotas
from routes.usuario_routes import usuario_bp
from routes.motorista_routes import motorista_bp
from routes.veiculo_routes import veiculo_bp
from routes.logistica_routes import logistica_bp
from routes.dashboard_routes import dashboard_bp

def create_app():
    app = Flask(__name__)
    CORS(app)  # Permitir requisições de diferentes origens
    
    # Configurações
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.config['JSON_SORT_KEYS'] = False
    
    # ========== REGISTRAR TODAS AS ROTAS ==========
    
    # Usuários
    app.register_blueprint(usuario_bp, url_prefix='/api')
    
    # Motoristas
    app.register_blueprint(motorista_bp, url_prefix='/api')
    
    # Veículos
    app.register_blueprint(veiculo_bp, url_prefix='/api')
    
    # Logística (cargas, rotas, entregas)
    app.register_blueprint(logistica_bp, url_prefix='/api')
    
    # Dashboard
    app.register_blueprint(dashboard_bp, url_prefix='/api')
    
    # ========== ROTAS BÁSICAS ==========
    
    @app.route('/')
    def home():
        return jsonify({
            'message': '🚚 SupplyTrack API - Sistema de Gestão Logística',
            'version': '1.0.0',
            'endpoints': {
                'usuarios': '/api/usuarios',
                'motoristas': '/api/motoristas', 
                'veiculos': '/api/veiculos',
                'entregas': '/api/entregas',
                'dashboard': '/api/dashboard',
                'interface_web': '/dashboard'
            }
        })
    
    @app.route('/health')
    def health_check():
        return jsonify({'status': 'healthy', 'service': 'supplytrack-api'})
    
    # ========== SERVER FRONTEND DO DASHBOARD ==========
    
    @app.route('/dashboard')
    def serve_dashboard():
        """Serve a interface web do dashboard"""
        try:
            return send_from_directory('frontend', 'dashboard.html')
        except FileNotFoundError:
            return jsonify({'error': 'Dashboard não encontrado'}), 404
    
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