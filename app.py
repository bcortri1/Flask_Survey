from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my key'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False



survey = surveys.satisfaction_survey

@app.route('/')
def main():
    session['responses'] = []
    return redirect("/questions/0")

@app.route('/questions/<int:num>')
def questions(num):
    responses = session['responses']
    if num != len(responses):
        flash("Invalid Question")
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[num].question
    choices = survey.questions[num].choices
    title = survey.title
    instructions = survey.instructions

    return render_template('questions.html', title = title, instructions = instructions, question = question, choices = choices)

@app.route('/answer', methods = ['POST'])
def answer():
    responses = session['responses']
    responses.append(request.form.get('choice'))
    session['responses'] = responses
    if len(responses) >= len(survey.questions): 
        return redirect('/end') 
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route('/end')
def end():
    return """<h1>Thank You</h1>"""