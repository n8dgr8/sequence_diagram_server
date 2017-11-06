from flask import Flask, redirect, render_template, request, url_for
import redis
import short_url

app = Flask(__name__)

app.redis_client = redis.StrictRedis(
  host='localhost',
  port=6379,
  db=0
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
