"use strict"
//document.getElementsByTagName('p')[0].addEventListener('click', function(){alert('?');}, false);
//document.querySelectorAll('.dummyclass')[0].addEventListener('click', function(){alert('?');}, false);
//definition
var md = {};

md.gracefullyRemove = function(domElement){
	domElement.setAttribute('style','opacity:0; transition-duration:0.5s;'); 
		setTimeout(function(){domElement.remove();},1000);
}

md.showPatientDetails = function(patientID){
	//Container div
	var patientsDetailsDiv = document.createElement('div');
	patientsDetailsDiv.setAttribute('class','coverDiv');
	patientsDetailsDiv.id = "patientsDetailsDiv";
	patientsDetailsDiv.innerHTML = patientID;
	patientsDetailsDiv.addEventListener('dblclick',
		function(){md.gracefullyRemove(patientsDetailsDiv);});
	document.body.appendChild(patientsDetailsDiv);
	//table(s)
	var resultsTablesHolder = document.createElement('div');
	resultsTablesHolder.id = "resultsTablesHolder";
	resultsTablesHolder.innerHTML = "<div class=\"resultsHeader\">RESULTS</div>";
	patientsDetailsDiv.appendChild(resultsTablesHolder);
	var resultsTable = [];
	resultsTable[0] = document.createElement('table');
	resultsTable[0].innerHTML = 
	"<tr><th>Basic Metabolic Panel</th><th>Norm</th><th>26-Feb-14 16:00</th><th>27-Feb-14 16:00</th></tr>"+
	"<tr><td>Glucose Level</td><td>10-110</td><td>112</td><td>112</td></tr>";
	resultsTable[1] = document.createElement('table');
	resultsTable[1].innerHTML = 
	"<tr><th>Hemogram</th><th>Norm</th><th>26-Feb-14 16:00</th></tr>";
	"<tr><td>WBC Count</td><td>4.8-10.8</td><td>5.0</td></tr>";
	for(var i=0; i<resultsTable.length; i++){
		resultsTablesHolder.appendChild(resultsTable[i]);
	}
	patientsDetailsDiv.appendChild(resultsTablesHolder);
}
//Load all patients AJAX req-response- callback function
md.loadAllPatients = {}
md.loadAllPatients.callbackFunc = function(responseText){
	//alert(responseText);
	var patientsObj = JSON.parse(responseText);
	var patientsTable = document.getElementById("patientList");
	patientsTable.innerHTML = "<tr><th>NAME</th><th>VISIT ID</th><th>DOB</th><th>ROOM</th><th>STATUS</th><th>ARRIVAL</th><th>PROVIDER</th></tr>";
	for(var patientKey in patientsObj){
		var oneRow = document.createElement('tr');
		oneRow.setAttribute('patientID' , patientKey)
		oneRow.innerHTML = 
			"<td>"+patientsObj[patientKey]["name"]+"</td>"+
			"<td>"+patientKey+"</td>"+
			"<td>"+patientsObj[patientKey]["dob"]+"</td>"+
			"<td>"+patientsObj[patientKey]["room"]+"</td>"+
			"<td>"+patientsObj[patientKey]["status"]+"</td>"+
			"<td>"+patientsObj[patientKey]["arrival"]+"</td>"+
			"<td>"+patientsObj[patientKey]["provider"]+"</td>";
		patientsTable.appendChild(oneRow);
		oneRow.addEventListener('click', function(){
			md.showPatientDetails(this.getAttribute('patientID'))}, 
			false);
	}
}
//Common GET XHR request-function
md.xhrWorkerGET = function(xhrReqObj){
	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function(){
		if(xhr.readyState===4){
			if(xhr.status>=200 && xhr.status<300 || xhr.status==304){
				xhrReqObj.callbackFunc(xhr.responseText);
			}else{
				console.log(xhrReqObj.url + "load request unsuccessful : " + xhr.status);
			}
		}else{
			console.log(xhrReqObj.url + "load request unsuccessful (Request timed out; never reached xhr.readyState==4): " + xhr.status);	
		}
	}
	xhr.open('GET',xhrReqObj.url, true);
	xhr.timeout=xhrReqObj.timeout;
	xhr.ontimeout = xhrReqObj.ontimeoutFunc();
	xhr.send(null);
}

var xhrReqObj = {'callbackFunc' : md.loadAllPatients.callbackFunc,
				'url':'scripts/gw.py?table=allpatients',
				'timeout':2000,
				'ontimeoutFunc': function(){console.log("Failed to load Patients' list.");}};
//attachment				
document.getElementById('buttonPatients').addEventListener('click', function(){
	var prevDivAll = document.querySelectorAll('.coverDiv');
	for(var i=0; i<prevDivAll.length;i++){
		md.gracefullyRemove(prevDivAll[i]);
	}
	md.xhrWorkerGET(xhrReqObj);
}, false);