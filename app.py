from flask import Flask,render_template,request
import pickle
import numpy as np
from covid import Covid

covid=Covid()
ind=covid.get_status_by_country_name("india")

app=Flask(__name__)


@app.route("/")
def home():
	return render_template('index.html')


@app.route("/test",methods=['POST','GET'])
def test():
	if request.method=='POST':
		sex=int(request.form['sex'])
		age=int(request.form['age'])
		patient_type=int(request.form['patient_type'])
		pneumonia=float(request.form['pneumonia'])
		intubed=float(request.form['intubed'])
		contact_other_covid=float(request.form['contact_other_covid'])
		covid_res=int(request.form['covid_res'])
		diabetes=float(request.form['diabetes'])
		hypertension=float(request.form['hypertension'])
		with open('model.pkl','rb') as f:
			model=pickle.load(f)
		X_test=np.array([[age,patient_type,pneumonia,intubed,contact_other_covid,covid_res,diabetes,hypertension,sex]])
		y_pred=model.predict(X_test)
		return render_template('result.html',y_pred=y_pred)
	return render_template('test.html')


@app.route("/count")
def count():
	try:
		world_con=covid.get_total_confirmed_cases()
		world_act=covid.get_total_active_cases()
		world_det=covid.get_total_deaths()
		ind_con=ind.get("confirmed")
		ind_act=ind.get("active")
		ind_det=ind.get("deaths")
		return render_template('count.html',world_con=world_con,world_det=world_det,world_act=world_act,ind_con=ind_con,ind_act=ind_act,ind_det=ind_det)
	except:
		return "Connection Eroor"
if __name__=="__main__":
	app.run(debug=True)
