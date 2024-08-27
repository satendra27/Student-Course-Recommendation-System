from flask import Flask,render_template,request
import numpy as np
import pickle

app = Flask(__name__)

course = {0:"ba",1:"bcom",2:"bsc",3:"btech"}
rf = pickle.load(open('ssrs_model.pkl','rb'))

def predict_course(gender,stream,subject,marks):
    gender = 0 if(gender=="Female") else 1
    if(stream=="commerce"):
        stream=0
    elif(stream=="humanities"):
        stream=1
    else:
        stream=2

    if(subject=="chemistry"):
        subject = 0
    elif(subject == "economics"):
        subject = 1
    elif(subject=="history"):
        subject = 2
    elif(subject == "math"):
        subject = 3
    else:
        subject = 4
    
    a = np.array([[gender,stream,subject,marks]])
    predicted_value = rf.predict(a)
    return course[predicted_value[0]]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def prediction():
    gender = request.form.get('gender')
    stream = request.form.get('stream')
    subject = request.form.get('subject')
    marks = int(request.form.get('marks'))
    predicted_course = predict_course(gender,stream,subject,marks)

    print(gender,stream,subject,marks,predicted_course)
    return render_template('index.html', result=predicted_course)


if __name__ == "__main__":
    app.run(debug=True)