from flask_socketio import SocketIO, send, join_room
from flask import Flask, flash, redirect, render_template, request, session, abort,url_for
import os
#import StockPrice as SP
import re
import sqlite3
import pandas as pd
import numpy as np
import requests

import matplotlib.pyplot as plt
import csv
import numpy as np
    
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
	return render_template('main.html')


def process(path):
	data = pd.read_csv(path,usecols=["Species","Destination","Port_of_Loading","Unit","Quantity","Value(INR)","Cost_per_Unit(INR)"])
	print(data)


	names=list(data.columns)
	correlations = data.corr()
	# plot correlation matrix
	fig = plt.figure()
	fig.canvas.set_window_title('Correlation Matrix')
	ax = fig.add_subplot(111)
	cax = ax.matshow(correlations, vmin=-1, vmax=1)
	fig.colorbar(cax)
	ticks = np.arange(0,9,1)
	ax.set_xticks(ticks)
	ax.set_yticks(ticks)
	ax.set_xticklabels(names)
	ax.set_yticklabels(names)
	fig.savefig('static/results/Correlation Matrix.png')

	


	fig, ax = plt.subplots(figsize=(15,7))    	
	ncols=3
	plt.clf()
	f = plt.figure(1)
	f.suptitle(" Data Histograms", fontsize=12)
	vlist = list(data.columns)
	nrows = len(vlist) // ncols
	if len(vlist) % ncols > 0:
		nrows += 1
	for i, var in enumerate(vlist):
		plt.subplot(nrows, ncols, i+1)
		plt.hist(data[var].values, bins=15)
		plt.title(var, fontsize=10)
		plt.tick_params(labelbottom='off', labelleft='off')
	plt.tight_layout()
	plt.subplots_adjust(top=0.88)
	fig.savefig('static/results/Data Histograms.png')



	fig, ax = plt.subplots(figsize=(15,7))
	data['Species'].value_counts().plot.bar(rot=0)
	n=data['Species'].value_counts().plot.bar(rot=0)
	ax.title.set_text('Number of Records Species')
	ax.set_ylabel('Sum Value')
	plt.savefig('static/results/Number of Records Species.png')
	
	fig, ax = plt.subplots(figsize=(15,7))
	data['Destination'].value_counts().plot.bar(rot=0)
	ax.title.set_text('Number of Records Destination')
	ax.set_ylabel('Sum Value')
	plt.savefig('static/results/Number of Records Destination.png')

	fig, ax = plt.subplots(figsize=(15,7))
	data['Port_of_Loading'].value_counts().plot.bar(rot=0)
	ax.title.set_text('Number of Records Port_of_Loading')
	ax.set_ylabel('Sum Value')
	plt.savefig('static/results/Number of Records Port_of_Loading.png')




	fig, ax = plt.subplots(figsize=(15,7))
	data[["Species", "Quantity"]].groupby("Species").sum().plot.bar(stacked=True,ax=ax)
	ax.title.set_text('Total Species Quantity')
	ax.set_ylabel('Sum Value')
	plt.savefig('static/results/Total Species Quantity.png')

	a = data[["Species", "Quantity"]].groupby("Species").sum()
	print(a)
	a.plot.pie(subplots=True,figsize=(20, 20))
	plt.title('Total Species Quantity')

	plt.savefig('static/results/Pie-Species Quantity.png')



	fig, ax = plt.subplots(figsize=(15,7))
	data[["Destination", "Quantity"]].groupby("Destination").sum().plot.bar(stacked=True,ax=ax)
	ax.title.set_text('Total Destination Quantity')
	ax.set_ylabel('Sum Value')
	plt.savefig('static/results/Total Destination Quantity.png')


	a = data[["Destination", "Quantity"]].groupby("Destination").sum()
	print(a)
	a.plot.pie(subplots=True,figsize=(20, 20))
	plt.title('Total Destination Quantity')
	plt.savefig('static/results/Pie-Destination Quantity.png')



	fig, ax = plt.subplots(figsize=(15,7))
	data[["Unit", "Quantity"]].groupby("Unit").sum().plot.bar(stacked=True,ax=ax)
	ax.title.set_text('Total Unit Quantity')
	ax.set_ylabel('Sum Value')
	plt.savefig('static/results/Total Unit Quantity.png')

	a = data[["Unit", "Quantity"]].groupby("Unit").sum()
	print(a)
	a.plot.pie(subplots=True,figsize=(20, 20))
	plt.title('Total Unit Quantity')
	plt.savefig('static/results/Pie-Unit Quantity.png')


	fig, ax = plt.subplots(figsize=(15,7))
	data[["Port_of_Loading", "Quantity"]].groupby("Port_of_Loading").sum().plot.bar(stacked=True,ax=ax)
	ax.title.set_text('Total Port_of_Loading Quantity')
	ax.set_ylabel('Sum Value')
	plt.savefig('static/results/Total Port_of_Loading Quantity.png')

	a = data[["Port_of_Loading", "Quantity"]].groupby("Port_of_Loading").sum()
	a.plot.pie(subplots=True,figsize=(20, 20))
	plt.title('Total Port_of_Loading Quantity')
	plt.savefig('static/results/Pie-Port_of_Loading Quantity.png')

	fig, ax = plt.subplots(figsize=(15,7))
	data[["Species", "Value(INR)"]].groupby("Species").sum().plot.bar(stacked=True,ax=ax)
	ax.title.set_text('Total Species Value(INR)')
	ax.set_ylabel('Sum Value')
	plt.savefig('static/results/Total Species Value(INR).png')

	a = data[["Species", "Value(INR)"]].groupby("Species").sum()
	print(a)
	a.plot.pie(subplots=True,figsize=(20, 20))
	plt.title('Total Species Value(INR)')
	plt.savefig('static/results/Pie-Species Value(INR).png')



	fig, ax = plt.subplots(figsize=(15,7))
	data[["Destination", "Value(INR)"]].groupby("Destination").sum().plot.bar(stacked=True,ax=ax)
	ax.title.set_text('Total Destination Value(INR)')
	ax.set_ylabel('Sum Value')
	plt.savefig('static/results/Total Destination Value(INR).png')


	a = data[["Destination", "Value(INR)"]].groupby("Destination").sum()
	print(a)
	a.plot.pie(subplots=True,figsize=(20, 20))
	plt.title('Total Destination Value(INR)')
	plt.savefig('static/results/Pie-Destination Value(INR).png')



	fig, ax = plt.subplots(figsize=(15,7))
	data[["Unit", "Value(INR)"]].groupby("Unit").sum().plot.bar(stacked=True,ax=ax)
	ax.title.set_text('Total Unit Value(INR)')
	ax.set_ylabel('Sum Value')
	plt.savefig('static/results/Total Unit Value(INR).png')


	a = data[["Unit", "Value(INR)"]].groupby("Unit").sum()
	print(a)
	a.plot.pie(subplots=True,figsize=(20, 20))
	plt.title('Total Unit Value(INR)')
	plt.savefig('static/results/Pie-Unit Value(INR).png')


	fig, ax = plt.subplots(figsize=(15,7))
	data[["Port_of_Loading", "Value(INR)"]].groupby("Port_of_Loading").sum().plot.bar(stacked=True,ax=ax)
	ax.title.set_text('Total Port_of_Loading Value(INR)')
	ax.set_ylabel('Sum Value')
	plt.savefig('static/results/Total Port_of_Loading Value(INR).png')

	a = data[["Port_of_Loading", "Value(INR)"]].groupby("Port_of_Loading").sum()
	a.plot.pie(subplots=True,figsize=(20, 20))
	plt.title('Total Port_of_Loading Value(INR)')
	plt.savefig('static/results/Pie-Port_of_Loading Value(INR).png')
	

@app.route('/process',methods=['POST'])
def process_page():
    	path=request.form['datasetfile']
    	print(path)
    	process(path)
    	message="Result"
    	return render_template('main.html',message=message)



# /////////socket io config ///////////////
#when message is recieved from the client    
@socketio.on('message')
def handleMessage(msg):
    print("Message recieved: " + msg)
 
# socket-io error handling
@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    pass


  
  
if __name__ == '__main__':
    socketio.run(app,debug=True,host='127.0.0.1', port=4000)
