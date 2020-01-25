from random import randint
from time import strftime
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import whoosh_retrieval
import pandas as pd
from random import sample
import whoosh_retrieval

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'

class ReusableForm(Form):
    name = TextField('Business:', validators=[validators.required()])

def get_time():
    time = strftime("%Y-%m-%dT%H:%M")
    return time

def write_to_disk(business):
    data = open('file.log', 'a')
    timestamp = get_time()
    data.write('DateStamp={}, Name={} \n'.format(timestamp, business))
    data.close()


review_data = pd.read_csv('business_review_users_tags.csv')
business_tags = review_data.drop_duplicates(subset=['business_id'])
business_tags = business_tags[['business_name', 'tks_output']]
Businesses = business_tags['business_name'].tolist()

@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
    business = ""
    #print(form.errors)
    if request.method == 'POST':
        business=request.form['business']

        write_to_disk(business)
        if business in Businesses:
            flash('Reviews for Selected Business: {}'.format(business))

        else:
            flash('Error: No Reviews to Display')

    if business != "" and business in Businesses:
        selectBusinessData = business_tags.loc[business_tags['business_name'] == business]
        listselectBusinessData = selectBusinessData['tks_output'].tolist()[0]
        listselectBusinessData = listselectBusinessData.replace('[', '')
        listselectBusinessData = listselectBusinessData.replace(']', '')
        listselectBusinessData = listselectBusinessData.split(',')

        final_tags = []
        for tag in listselectBusinessData:
            temp = tag.replace('\'', '').strip()

            final_tags.append(temp)

        selectBusinessTags = sample(final_tags,10) if len(final_tags) > 10 else final_tags
        tagLen = len(selectBusinessTags)
        reviews = {}
        for t in selectBusinessTags:
            reviews[t] = whoosh_retrieval.search_review(t, business)

    else:
        tagLen = 0
        selectBusinessTags = []
        reviews = {}
    return render_template('./index.html', form=form, tagLen=tagLen, Tags=selectBusinessTags, businessLen=len(Businesses), Businesses=Businesses, reviews=reviews)

if __name__ == "__main__":
    app.run()