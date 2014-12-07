"use strict"
//document.getElementsByTagName('p')[0].addEventListener('click', function(){alert('?');}, false);
//document.querySelectorAll('.dummyclass')[0].addEventListener('click', function(){alert('?');}, false);
//definition
var md = {};
md.onLoadTasks = function(){
	alert("?");
}
//Load all patients AJAX req-response
md.loadAllPatients = {}
md.loadAllPatients.callbackFunc = function(responseText){
	var patientsObj = JSON.parse(responseText);
	var patientsTable = document.getElementById("patientList");	
	patientsTable.innerHTML = "<tr><th>NAME</th><th>VISIT ID</th><th>DOB</th><th>ROOM</th><th>STATUS</th><th>ARRIVAL</th><th>PROVIDER</th></tr>";
	for(var i=0; i<patientsObj.length; i++){
		var oneRow = document.createElement('tr');
		oneRow.innerHTML = 
			"<td>"+patientsObj[i]["name"]+"</td>"+
			"<td>"+patientsObj[i]["dob"]+"</td>"+
			"<td>"+patientsObj[i]["visit_id"]+"</td>"+
			"<td>"+patientsObj[i]["room"]+"</td>"+
			"<td>"+patientsObj[i]["status"]+"</td>"+
			"<td>"+patientsObj[i]["arrival"]+"</td>"+
			"<td>"+patientsObj[i]["provider"]+"</td>";
		patientsTable.appendChild(oneRow);
	}
}
md.loadAllPatients.xhr = function(){
	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function(){
		if(xhr.readyState===4){
			if(xhr.status >= 200 && xhr.status < 300 || xhr.status == 304){
				console.log("Loaded patients' list successfully");
				md.loadAllPatients.callbackFunc(xhr.responseText);
			}else{
				console.log("Patients' list load request unsuccessful : " + xhr.status);	
			}			
		}else{
			console.log("Patients' list load request unsuccessful (Request timed out; never reached xhr.readyState==4): " + xhr.status);
		}
	}
	xhr.open('GET','scripts/gw.py?table=allpatients', true);
	xhr.timeout = 2000;
	xhr.ontimeout = function(){
		console.log("Failed to load Patients' list.")
	}
	xhr.send(null);
}

//attachment
//window.addEventListener('load', md.onLoadTasks(), false);
document.getElementById('buttonPatients').addEventListener('click', md.loadAllPatients.xhr, false);