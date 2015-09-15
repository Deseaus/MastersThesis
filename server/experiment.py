import datetime
import json
import os
import re
import sys
import time
import uuid
import sh
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect, url_for, jsonify, Markup

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Website Endpoints

@app.errorhandler(500)
def internal_error(exception):
    """Render the error template with the error message."""
    return render_template('500.html',
                           error=exception,
                           version=sys.version,
                           path=sys.executable,
                           env=os.environ), 500

@app.route("/")
def index():
    return render_template('landing.html')

@app.route("/main/<participant_id>/<order>")
def main(participant_id, order):
    return render_exp("index.html", participant_id, order, "MAIN")

@app.route('/pre-survey/<participant_id>/<order>')
def pre_survery(participant_id, order):
    """Render the Google Docs pre-Survey."""
    return render_exp("pre_survey.html", participant_id, order, "PRE-QUESTIONNAIRE")

@app.route('/brief/<participant_id>/<order>')
def brief(participant_id, order):
    return render_exp("brief.html", participant_id, order, "BRIEF")

@app.route('/setup-one/<participant_id>/<order>')
def scratch(participant_id, order):
    return render_exp("setup_scratch.html", participant_id, order, "SCRATCH")
                           
@app.route('/setup-two/<participant_id>/<order>')
def postedit(participant_id, order):
    return render_exp("setup_pe.html", participant_id, order, "PE")

@app.route('/setup-three/<participant_id>/<order>')
def style_guide(participant_id, order):
    return render_exp("setup_style.html", participant_id, order, "STYLE")

@app.route('/post-survey/<participant_id>/<order>')
def post_survey(participant_id, order):
    """Render the Google Docs post-Survey."""
    exp = Experiment(order=order,
                     participant_id=participant_id,
                     setup="POST-QUESTIONNAIRE",
                     start=int(time.time()))
    setup_one = Experiment(order=order,
                     participant_id=participant_id,
                     setup="SCRATCH",
                     start=0)
    setup_two = Experiment(order=order,
                     participant_id=participant_id,
                     setup="PE",
                     start=0)
    setup_three = Experiment(order=order,
                     participant_id=participant_id,
                     setup="STYLE",
                     start=0)
    return render_template("post_survey.html",
                           experiment=exp,
                           setup_one=setup_one,
                           setup_two=setup_two,
                           setup_three=setup_three)

@app.route('/final')
def final():
    return render_template('thanks.html')

def render_exp(template, participant_id, order, setup):
    """Render a template with the given information."""
    exp = Experiment(order=order,
                     participant_id=participant_id,
                     setup=setup,
                     start=int(time.time()))
    return render_template(template, experiment=exp)


# ********************************
#           API
# ********************************

@app.route('/check-style', methods=['POST'])
def check_style():
    """Return a JSON object containing style hints for a given sentence."""

    # If the sentence is empty, return 500
    if not request.form['sentence']:
        return json.dumps({'success':False}), 500, {'ContentType':'application/json'} 
    # Get the request data
    participant_id = request.form['participant_id']
    order = request.form['order']
    raw_sentence = request.form['sentence']

    # Remove any html tags
    soup = BeautifulSoup(raw_sentence)
    sentence = soup.get_text()

    # Get the participant directory and create the filename
    participant_dir = participant_directory(participant_id)
    filename = os.path.join(participant_dir, "hints.txt")

    # Tokenise and parse a sentence
    perl = sh.Command("/usr/bin/perl")
    translate = sh.Command("/usr/bin/pgf-translate")
    raw = translate("Wiki.pgf", "Phr", "WikiMaster", "WikiHint",
            _in=perl("tokenizer.perl", "-l es", "-no-escape", _in=sentence))
    hints = _parse_hints(raw)


    # Write to the log
    style = render_template('style.txt',
                             participant_id=participant_id,
                             order=order,
                             original=raw_sentence,
                             hints=hints,
                             nowunix=time.time(),
                             now=datetime.datetime.now())
    with open(filename, "a", encoding="utf-8") as f:
        f.write(style)

    #if len(sentence.split()) > 15:
    #    # Used in: 3.D
    #    # 1.2 Encyclopaedic Style
    #    # http://es.wikipedia.org/wiki/Wikipedia:Manual_de_estilo#Estilo_enciclop.C3.A9dico
    #    hints.append("Siempre que sea posible, escribir oraciones cortas, convenientemente separadas por puntos. Es habitual ver oraciones que se alargan innecesariamente tres, cuatro y más líneas sin una pausa principal (punto).")
    hints = list(set(hints))

    return jsonify(hints=hints)

def _parse_hints(raw):
    """Parse the raw ouput from pgf-translate and return a list of hints."""
    parse = raw.split("\n")[2] # Take just the first parse 
    hints = re.findall("\|\|\| (.*?) \|\|\|", parse)

    return hints

@app.route('/save-experiment', methods=['POST', 'GET'])
def save_experiment():
    """Save the results of a single text translation to a file."""

    # Get the request data
    participant_id = request.form['participant_id']
    setup = request.form['setup']
    order = request.form['order']
    _initial_time = float(request.form['initial_time'])
    start = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(_initial_time))
    total_time = time.time() - _initial_time
    translation = request.form['translation'].split("\n")

    # Get the participant directory and create the filename
    participant_dir = participant_directory(participant_id)
    filename = os.path.join(participant_dir, ".".join([setup, "txt"]))

    # Generate the result template and save it
    result = render_template('result.txt',
                             participant_id=participant_id,
                             order=order,
                             setup=setup,
                             start=start,
                             end=datetime.datetime.now(),
                             total=total_time,
                             startunix=_initial_time,
                             endunix=time.time(),
                             translation=translation)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(result)

    # Return a success code
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/style-click', methods=['POST'])
def click_style():
    """Record each time a participant clicks on a link to the Wikipedia style guide."""
    participant_id = request.form['participant_id']
    setup = request.form['setup']
    order = request.form['order']

    click = render_template('click.txt',
                             participant_id=participant_id,
                             order=order,
                             setup=setup,
                             nowunix=time.time(),
                             now=datetime.datetime.now())

    # Get the participant directory and create the filename
    participant_dir = participant_directory(participant_id)
    filename = os.path.join(participant_dir, "clicks.txt")

    with open(filename, "a", encoding="utf-8") as f:
        f.write(click)

    # Return a success code
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/key', methods=['POST'])
def key_log():
    """Record each time a participant clicks on a link to the Wikipedia style guide."""
    participant_id = request.form['participant_id']
    setup = request.form['setup']
    order = request.form['order']
    key = request.form['key']
    sent_id = request.form['sent_id']

    click = render_template('key.txt',
                             participant_id=participant_id,
                             order=order,
                             setup=setup,
                             key=key,
                             sent_id=sent_id,
                             nowunix=time.time(),
                             now=datetime.datetime.now())

    # Get the participant directory and create the filename
    participant_dir = participant_directory(participant_id)
    filename = os.path.join(participant_dir, ".".join(["key", setup, "txt"]))

    with open(filename, "a", encoding="utf-8") as f:
        f.write(click)

    # Return a success code
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

# ********************************
#       EXPERIMENT 
# ********************************

class Experiment():

    def __init__(self, order, participant_id, setup, start):
        self.order = order
        self.participant_id = participant_id
        self.setup = setup
        self._text_id = self._text_no(self.order, self.setup)
        self.start = start

    @property
    def source(self):
        """Return the source text as a list of sentences."""
        # TODO raise error if self.setup is not provided
        return self._st_text(self._text_id)

    @property
    def mt(self):
        """Return the MT of a specific text as a list of sentences."""
        return self._st_text_mt(self._text_id)

    @property
    def title(self):
        """Return the text title."""
        return self._st_text_title(self._text_id)

    @property
    def aligned(self):
        """Return a list of tuples containing (source, mt)."""
        return zip(self.source, self.mt)

    @staticmethod
    def _st_text(text_id):
        """Return a list of sentences in the required text."""
        texts = {"1": "ai.txt", "2": "charlotte.txt", "3": "garfield.txt"}
        with open("/".join([os.getcwd(), "texts", texts[text_id]]), encoding="utf-8") as f:
            # Wrap it in Markup so it doesn't escape html
            return [Markup(sent) for sent in f]

    @staticmethod
    def _st_text_title(text_id):
        """Return the filename for a given order and setup."""
        text_names = {"1": "History of Artificial Intelligence",
                    "2": "Charlotte Gyllenhammar",
                    "3": "Garfield"}
        return text_names[text_id]

    @staticmethod
    def _st_text_mt(text_id):
        """Return a list of MT translated sentences for the appropriate text."""
        texts_pe = {"1": "ai_google.txt", "2": "charlotte_google.txt", "3": "garfield_google.txt"}
        with open("/".join([os.getcwd(), "texts", texts_pe[text_id]]), encoding="utf-8") as f:
            # Wrap it in Markup so it doesn't escape html
            return [Markup(sent) for sent in f]

    @staticmethod
    def _text_no(order, setup):
        if setup == "BRIEF":
            return None
        elif setup == "PRE-QUESTIONNAIRE":
            return None
        elif setup == "POST-QUESTIONNAIRE":
            return None
        elif setup == "MAIN":
            return None
        else:
            item = {"SCRATCH": 0,
                    "PE": 1,
                    "STYLE": 2}
            return order[item[setup]]


# ********************************
#       UTILS
# ********************************

def participant_directory(participant_id):
    """Return the path for the unique participant directory."""
    participant_dir = os.path.join(os.getcwd(), "results", participant_id)
    if not os.path.exists(participant_dir):
        os.makedirs(participant_dir)
    return participant_dir

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
