import time
import random
import logging
from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics

# Configure logging to stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Static information as metric
metrics.info('app_info', 'Application info', version='1.0.0')


@app.route('/')
def home():
    logger.info('Home endpoint accessed')
    return jsonify({
        'service': 'observability-demo',
        'status': 'running'
    })


@app.route('/health')
def health():
    logger.info('Health check successful')
    return jsonify({'status': 'healthy'})


@app.route('/api/data')
def api_data():
    logger.info('API data requested')
    return jsonify({
        'data': [random.randint(1, 100) for _ in range(5)],
        'timestamp': time.time(),
        'source': 'observability-demo'
    })


@app.route('/error')
def error():
    logger.error('Simulated application error')
    return jsonify({'error': 'Simulated internal server error'}), 500


@app.route('/slow')
def slow():
    delay = random.uniform(1.0, 3.0)
    logger.warning(f'Slow request detected - sleeping {delay:.2f}s')
    time.sleep(delay)
    return jsonify({
        'message': 'slow response',
        'delay_seconds': round(delay, 2)
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
