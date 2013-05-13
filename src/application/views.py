"""
views.py

This module contains all necessary view functions.
"""
from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import request, render_template, flash, url_for, redirect

from flask_cache import Cache

from application import app, vm_start_time
#from decorators import login_required, admin_required
#from forms import ExampleForm, ChatForm
from models import ChatMessage
import datetime
from google.appengine.ext import ndb

# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)


@app.route('/')
def home():
    return redirect(url_for('chatroom_all'))


@app.route('/talk', methods=['GET', 'POST'])
def chatroom_all():
    messages = ndb.gql('SELECT * FROM ChatMessage ORDER BY timestamp')
    if request.method == 'POST':
        user, message, timestamp = request.form.get('name'), request.form.get('message'), datetime.datetime.now()
        chat_msg = ChatMessage(user=user, timestamp=timestamp, message=message)
        chat_msg.put()
        messages = ndb.gql('SELECT * FROM ChatMessage ORDER BY timestamp')
    return render_template('chatroom.html', messages=messages, vm_time=vm_start_time, mode='chatroom_all')


@app.route('/limited/count', methods=['GET', 'POST'])
def chatroom_count():
    messages = ndb.gql('SELECT * FROM ChatMessage ORDER BY timestamp DESC LIMIT 20').fetch(20)
    messages.reverse()
    if request.method == 'POST':
        user, message, timestamp = request.form.get('name'), request.form.get('message'), datetime.datetime.now()
        chat_msg = ChatMessage(user=user, timestamp=timestamp, message=message)
        chat_msg.put()
        messages = ndb.gql('SELECT * FROM ChatMessage ORDER BY timestamp DESC LIMIT 20').fetch(20)
        messages.reverse()
    return render_template('chatroom.html', messages=messages, vm_time=vm_start_time, mode='chatroom_count')


@app.route('/limited/time', methods=['GET', 'POST'])
def chatroom_time():
    messages = ChatMessage.gql('WHERE timestamp > :fiveago ORDER BY timestamp',
            fiveago=datetime.datetime.now() - datetime.timedelta(minutes=5))
    if request.method == 'POST':
        user, message, timestamp = request.form.get('name'), request.form.get('message'), datetime.datetime.now()
        chat_msg = ChatMessage(user=user, timestamp=timestamp, message=message)
        chat_msg.put()
        messages = ChatMessage.gql('WHERE timestamp > :fiveago ORDER BY timestamp',
            fiveago=datetime.datetime.now() - datetime.timedelta(minutes=5))
    return render_template('chatroom.html', messages=messages, vm_time=vm_start_time, mode='chatroom_time')


##### Error handling pages #####
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


#@login_required
#def list_examples():
    #"""List all examples"""
    #examples = ExampleModel.query()
    #form = ExampleForm()
    #if form.validate_on_submit():
        #example = ExampleModel(
            #example_name = form.example_name.data,
            #example_description = form.example_description.data,
            #added_by = users.get_current_user()
        #)
        #try:
            #example.put()
            #example_id = example.key.id()
            #flash(u'Example %s successfully saved.' % example_id, 'success')
            #return redirect(url_for('list_examples'))
        #except CapabilityDisabledError:
            #flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            #return redirect(url_for('list_examples'))
    #return render_template('list_examples.html', examples=examples, form=form)

#@login_required
#def edit_example(example_id):
    #example = ExampleModel.get_by_id(example_id)
    #form = ExampleForm(obj=example)
    #if request.method == "POST":
        #if form.validate_on_submit():
            #example.example_name = form.data.get('example_name')
            #example.example_description = form.data.get('example_description')
            #example.put()
            #flash(u'Example %s successfully saved.' % example_id, 'success')
            #return redirect(url_for('list_examples'))
    #return render_template('edit_example.html', example=example, form=form)



#@login_required
#def delete_example(example_id):
    #"""Delete an example object"""
    #example = ExampleModel.get_by_id(example_id)
    #try:
        #example.key.delete()
        #flash(u'Example %s successfully deleted.' % example_id, 'success')
        #return redirect(url_for('list_examples'))
    #except CapabilityDisabledError:
        #flash(u'App Engine Datastore is currently in read-only mode.', 'info')
        #return redirect(url_for('list_examples'))


#@admin_required
#def admin_only():
    #"""This view requires an admin account"""
    #return 'Super-seekrit admin page.'


#@cache.cached(timeout=60)
#def cached_examples():
    #"""This view should be cached for 60 sec"""
    #examples = ExampleModel.query()
    #return render_template('list_examples_cached.html', examples=examples)


def warmup():
    #"""App Engine warmup handler
    #See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    #"""
    return ''
