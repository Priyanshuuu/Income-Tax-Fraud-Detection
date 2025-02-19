# Flask Packages
from flask import Flask,render_template,request,url_for,Response
from flask_bootstrap import Bootstrap 
from flask_uploads import UploadSet,configure_uploads,IMAGES,DATA,ALL
from flask_sqlalchemy import SQLAlchemy 

import io
import random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from werkzeug import secure_filename

import os
import datetime
import time

import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import numpy as np
# EDA Packages
import pandas as pd 
import numpy as np 

# ML Packages
from sklearn.cluster import KMeans
from sklearn.datasets.samples_generator import make_blobs
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC


# ML Packages For Vectorization of Text For Feature Extraction
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer




app = Flask(__name__)
Bootstrap(app)
db = SQLAlchemy(app)

# Configuration for File Uploads
files = UploadSet('files',ALL)
app.config['UPLOADED_FILES_DEST'] = 'static/uploadsDB'
configure_uploads(app,files)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///static/uploadsDB/filestorage.db'

# Saving Data To Database Storage
class FileContents(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(300))
	modeldata = db.Column(db.String(300))
	data = db.Column(db.LargeBinary)


@app.route('/')
def index():
	return render_template('index.html')

# Route for our Processing and Details Page
@app.route('/dataupload',methods=['GET','POST'])
def dataupload():
	if request.method == 'POST' and 'csv_data' in request.files:
		file = request.files['csv_data']
		filename = secure_filename(file.filename)
		# os.path.join is used so that paths work in every operating system
        # file.save(os.path.join("wherever","you","want",filename))
		file.save(os.path.join('static/uploadsDB',filename))
		fullfile = os.path.join('static/uploadsDB',filename)

		# For Time
		date = str(datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S"))

		# EDA function
		df = pd.read_csv(os.path.join('static/uploadsDB',filename))
		df_size = df.size
		df_shape = df.shape
		df_columns = list(df.columns)
		df_targetname = df[df.columns[-1]].name
		df_featurenames = df_columns[0:-1] # select all columns till last column
		df_Xfeatures = df.iloc[:,0:-1] 
		df_Ylabels = df[df.columns[-1]] # Select the last column as target
		# same as above df_Ylabels = df.iloc[:,-1]
		

		# Model Building
		X = df_Xfeatures
		Y = df_Ylabels
		seed = 7
		# prepare models
		models = []
		models.append(('LR', LogisticRegression()))
		models.append(('LDA', LinearDiscriminantAnalysis()))
		models.append(('KNN', KNeighborsClassifier()))
		models.append(('CART', DecisionTreeClassifier()))
		models.append(('NB', GaussianNB()))
		models.append(('SVM', SVC()))
		# evaluate each model in turn
		

		results = []
		names = []
		allmodels = []
		scoring = 'accuracy'
		for name, model in models:
			kfold = model_selection.KFold(n_splits=10, random_state=seed)
			cv_results = model_selection.cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
			results.append(cv_results)
			names.append(name)
			msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
			allmodels.append(msg)
			model_results = results
			model_names = names 
			
		# Saving Results of Uploaded Files  to Sqlite DB
		newfile = FileContents(name=file.filename,data=file.read(),modeldata=msg)
		db.session.add(newfile)
		db.session.commit()		
		
	return render_template('details.html',filename=filename,date=date,
		df_size=df_size,
		df_shape=df_shape,
		df_columns =df_columns,
		df_targetname =df_targetname,
		model_results = allmodels,
		model_names = names,
		fullfile = fullfile,
		dfplot = df
		)



@app.route('/taxcal',methods=['POST'])
def taxcal():
	def sixty(age,z):
	    tax=0
	    if z<=250000:
	        pass
	    elif 250000<=z and z<=500000:
	        tax=5/100 * (z-250000)
	        if z<=350000:
	            tax=tax-2500
	            if tax<0:
	                tax=0
	        cess=tax*0.04
	        tax+=cess
	     
	    elif 500000<=z and z<=1000000:
	        tax += (0.05*(250000))
	        tax += (0.2 * (z-500000))
	        cess = 0.04*tax
	        tax += cess

	    elif z>1000000:
	        tax += (0.05*(250000))
	        tax += (0.2 * (500000))
	        tax += (0.3*(z-1000000))
	        cess = tax * 0.04
	        tax += cess
	    return tax
	  #  print("tax is :{}".format(tax))  #1

	def sixtyeight(age,z):
	    tax=0
	    if z<=300000:
	        pass
	    elif z>=300000 and z<500000:
	        tax=5/100 * (z-300000)
	        if z<=350000:
	            tax=tax-2500
	            if tax<0:
	                tax=0
	        cess=0.04*tax
	        tax+=cess
	        
	    elif z>=500000 and z<=1000000:
	        tax += (0.05*(200000))
	        tax += (0.2*(z-500000))
	        cess = 0.04*tax
	        tax += cess
	    elif z>1000000:
	        tax += (0.05*(200000))
	        tax += (0.2*(500000))
	        tax += (0.3*(z-1000000))
	        cess = 0.04*tax
	        tax += cess
	    return tax
	   # print("Tax is :{}".format(tax))


	def aboveeighty(age,z):
	    tax=0
	    if z<=500000:
	        pass
	    elif 500000<z<1000000:
	        tax=(0.2*(z-500000))
	        if z<=350000:
	            tax=tax-2500
	            if tax<0:
	                tax=0
	        cess=tax*0.04
	        tax+=cess
	    elif z>=1000000:
	        tax += (0.2*(500000))
	        tax += (0.3 * (z-1000000))
	        cess = 0.04*tax
	        tax += cess

	    return tax
	    


	if __name__=="__main__":
	 

	    
	    salary = int(request.form['Total_Income'])
	  

	    extra = int(request.form['Income_from_other_resources'])
	
	    total = salary+extra

	   
	    deductions = int(request.form['Enter_total_deductions'])
	    gross=total-deductions

	

	    earning = request.form['Salaried_or_Pensioner']

	    z = gross
	    #if person is earning
	    if earning=="yes" or earning=="Y":
	        p=50000
	        z=gross - p
	  
	    age = int(request.form['Age'])
	    if age<60:
	        ab=sixty(age,z)
	        return render_template('taxcal.html',Income_Tax=ab)
	    
	    elif(60<age<80):
	        b=sixtyeight(age,z)
	        return render_template('taxcal.html',Income_Tax=b)
	    
	    else:
	        c=aboveeighty(age,salary,z)
	        return render_template('taxcal.html',Income_Tax=c)


if __name__ == '__main__':
	app.run(debug=True)





