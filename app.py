#!/usr/bin/env python3
"""
Web App - Chat & Image Vision
Flask Simple Interface
"""

import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from ai_engine import chat_with_ai, analyze_image
import logging

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Chat endpoint"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Pesan tidak boleh kosong'}), 400
        
        if len(message) > 1000:
            return jsonify({'error': 'Pesan terlalu panjang (max 1000 karakter)'}), 400
        
        logger.info(f"Chat request: {message}")
        
        response = chat_with_ai(message)
        
        return jsonify({
            'success': True,
            'response': response,
            'type': 'text'
        })
        
    except Exception as e:
        logger.error(f"Error in /api/chat: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze-image', methods=['POST'])
def api_analyze_image():
    """Image analysis endpoint"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Tidak ada file gambar'}), 400
        
        file = request.files['image']
        question = request.form.get('question', 'Apa yang ada di gambar ini?')
        
        if file.filename == '':
            return jsonify({'error': 'File tidak dipilih'}), 400
        
        # Validate file type
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
        if not file.filename.lower().endswith(tuple(allowed_extensions)):
            return jsonify({'error': 'Format file tidak didukung (JPG, PNG, GIF, WEBP)'}), 400
        
        # Save temp file
        temp_path = f"temp_image_{os.urandom(8).hex()}.jpg"
        file.save(temp_path)
        
        try:
            logger.info(f"Image analysis request: {question}")
            response = analyze_image(temp_path, question)
            
            return jsonify({
                'success': True,
                'response': response,
                'type': 'image'
            })
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)
        
    except Exception as e:
        logger.error(f"Error in /api/analyze-image: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/status', methods=['GET'])
def api_status():
    """Get API status"""
    try:
        from ai_engine import get_model_status
        status = get_model_status()
        return jsonify({
            'success': True,
            'status': status
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint tidak ditemukan'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Development
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    logger.info(f"🚀 Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
