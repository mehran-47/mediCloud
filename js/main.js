"use strict"
//document.getElementsByTagName('p')[0].addEventListener('click', function(){alert('?');}, false);
//document.querySelectorAll('.dummyclass')[0].addEventListener('click', function(){alert('?');}, false);
//definition
var md = {};
md.onLoadTasks = function(){
	alert("?");
}
md.loadAllPatients = {}
md.loadAllPatients.callbackFunc = function(responseText){
	alert(responseText);
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
	xhr.open('GET','doc/testJSON.json', true);
	//xhr.open('GET','scripts/helloworld.py', true);
	xhr.send(null);
}
//attachment
//window.addEventListener('load', md.onLoadTasks(), false);
document.getElementById('buttonPatients').addEventListener('click', md.loadAllPatients.xhr, false);