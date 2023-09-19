from datetime import datetime
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT email address?', validators=[Email()])
    submit = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

boostrap = Bootstrap(app)
moment = Moment(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        for field in ('name', 'email'):
            old_field = session.get(field)
            new_field = getattr(form, field).data
            if old_field is not None and old_field != new_field:
                flash(f'Looks like you have changed your {field}!')
            session[field] = new_field
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           email=session.get('email'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name,
                           current_time=datetime.utcnow())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
