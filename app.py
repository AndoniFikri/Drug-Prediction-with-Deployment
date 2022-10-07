from flask import Flask, render_template, request
import pickle
import pandas as pd




app=Flask(__name__)
#load the model
model=pickle.load(open('model.pkl', 'rb'))

df = pd.read_csv('Cleaned Drug.csv')
@app.route('/')
def home():
    result=''
    return render_template('index.html', **locals())

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    Age=(float(request.form['Age']))
    Age_scld = (Age - df['Age'].mean())/(df['Age'].std())
    
    tmpSex=request.form['Sex']
    
    if tmpSex=="M":
        tmpSex=1

    
    else:
        tmpSex=0
    
    Sex=float(tmpSex)

    tmpBP=request.form['BP']

    if tmpBP=="HIGH":
        tmpBP=2
    elif tmpBP=="NORMAL":
        tmpBP=1
    else:
        tmpBP=0
    BP=float(tmpBP)

    tmpCholesterol=request.form['Cholesterol']

    if tmpCholesterol=="HIGH":
        tmpCholesterol=1
    else:
        tmpCholesterol=0
    Cholesterol=float(tmpCholesterol)

    Na_to_K=float(request.form['Na_to_K'])
    Na_to_K_scld = (Na_to_K - df['Na_to_K'].mean())/(df['Na_to_K'].std())



    
    result=model.predict([[Sex, BP, Cholesterol, Age_scld,  Na_to_K_scld]])[0]
    if result == 0:
        return render_template('index.html', Drug= 'DrugA should be given to patient for better improvement!')
    elif result == 1:
        return render_template('index.html', Drug='DrugB should be given to patient for better improvement!')
    elif result == 2:
        return render_template('index.html', Drug='DrugC should be given to patient for better improvement!')
    elif result == 3:
        return render_template('index.html', Drug='DrugX should be given to patient for better improvement!')
    else:
        return render_template('index.html', Drug='DrugY should be given to patient for better improvement!')



if __name__=="__main__":
    app.run(debug=True)