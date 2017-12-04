import os
from flask import Flask, redirect, render_template, request, url_for
from flask_assets import Environment, Bundle
import redis
import short_url

app = Flask(__name__)
assets = Environment(app)

javascript = Bundle(
    '../bower_components/bower-webfontloader/webfont.js',
    '../bower_components/snap.svg/dist/snap.svg-min.js',
    '../bower_components/underscore/underscore-min.js',
    '../bower_components/js-sequence-diagrams/dist/sequence-diagram-min.js',
    filters='jsmin',
    output='gen/packed.js'
)

assets.register('javascript', javascript)

css = Bundle(
    '../bower_components/js-sequence-diagrams/dist/sequence-diagram-min.css',
    filters='cssmin',
    output='screen.css'
)

assets.register('css', css)

app.redis_client = redis.StrictRedis.from_url(
    os.getenv('REDIS_URL'),
    errors='strict'
)

@app.route('/', methods=['POST'])
def create_chart():
    new_chart_id = app.redis_client.incr('chart:chart_id')
    encoded_new_chart_id = short_url.encode_url(new_chart_id)
    app.redis_client.set('chart:%s:data' % encoded_new_chart_id, request.values['data'])
    return redirect(url_for('get_chart', chart_id=encoded_new_chart_id))


@app.route('/', methods=['GET'])
def new_chart():
    template_data = {
        'chart_id': None,
        'chart_data': 'gabbagabbahey'
    }
    return render_template('chart.html', template_data=template_data)


@app.route('/<chart_id>', methods=['GET'])
def get_chart(chart_id=None):
    chart_data = app.redis_client.get('chart:%s:data' % chart_id)
    template_data = {
        'chart_id': chart_id,
        'chart_data': chart_data
    }
    return render_template('chart.html', template_data=template_data)
