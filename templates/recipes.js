//Copied from the mealspage.js

function doxml(){
    xmlb();
    xmlL();
    xmlD();
    xmlS();
    return true;
}

function xmlB() {
  var x = new XMLHttpRequest();
  var url = "/mealspage";


  x.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var jsonStuff = JSON.parse(this.responseText);
        console.log("we got : " + this.responseText + " from the server");
        B_response(jsonStuff);

  }}

  x.open("POST", url, true);
  x.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
  x.send("name=zb");

}


function xmlL() {
  var x = new XMLHttpRequest();
  var url = "/mealspage";


  x.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var jsonStuff = JSON.parse(this.responseText);
        console.log("we got : " + this.responseText + " from the server");
        L_response(jsonStuff);

  }}

  x.open("POST", url, true);
  x.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
  x.send("name=zl");

}

function xmlD() {
  var x = new XMLHttpRequest();
  var url = "/mealspage";


  x.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var jsonStuff = JSON.parse(this.responseText);
        console.log("we got : " + this.responseText + " from the server");
        D_response(jsonStuff);

  }}

  x.open("POST", url, true);
  x.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
  x.send("name=zd");

}

function xmlS() {
  var x = new XMLHttpRequest();
  var url = "/mealspage";


  x.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var jsonStuff = JSON.parse(this.responseText);
        console.log("we got : " + this.responseText + " from the server");
        S_response(jsonStuff);
  }}

  x.open("POST", url, true);
  x.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
  x.send("name=zs");

}

function B_response(jsonStuff) {
  // json stuff will be the food info from the api that we get from our server
  //var foodElement = jsonStuff["1"]; //do something with jsonStuff
  b = document.getElementById("B")
    while (b.hasChildNodes()) {
	b.removeChild(b.firstChild);
    }
    
    
    var f = document.createElement("form");
    f.setAttribute('method', 'post');
    f.setAttribute('action', '/recipes');

    for (let i = 1; i < 9; i++) {
	if (jsonStuff[i.toString()] != ""){
	    trimLen = jsonStuff[i.toString()][0].indexOf(",");
	    if(trimLen == -1){
		trimLen = jsonStuff[i.toString()][0].indexOf(" | ");
	    }
	    var ch = document.createElement("input");
	    ident = "food" + i;
	    ch.setAttribute("id", ident)
	    var lb = document.createElement("label");
	    var brk = document.createElement("br")
	    lb.setAttribute("for", ident);
	    ch.type = "checkbox";
	    if(trimLen == -1){
		ch.text = jsonStuff[i.toString()][0];
		ch.value = jsonStuff[i.toString()][0];
		lb.innerHTML = jsonStuff[i.toString()][0];
		//ch.name = jsonStuff[i.toString()];
		ch.name = "foods";
	    }
	    else {
		ch.text = jsonStuff[i.toString()][0].slice(0, trimLen);
		ch.value = jsonStuff[i.toString()][0].slice(0, trimLen);
		lb.innerHTML = jsonStuff[i.toString()][0].slice(0, trimLen);
		//ch.name = jsonStuff[i.toString()].slice(0, trimLen);
		ch.name = "foods";
	    }
	    f.appendChild(ch);
	    f.appendChild(lb);
	    f.appendChild(brk);
	}


    }
    var sub = document.createElement("input");
    sub.type = "submit"
    sub.value = "Find Recipes"
    f.append(sub)
    document.getElementById("B").appendChild(f);

}

function L_response(jsonStuff) {
  b = document.getElementById("L")
    while (b.hasChildNodes()) {
	b.removeChild(b.firstChild);
    }
    
    
    var f = document.createElement("form");
    f.setAttribute('method', 'post');
    f.setAttribute('action', '/recipes');

    for (let i = 1; i < 9; i++) {
	if (jsonStuff[i.toString()] != ""){
	    trimLen = jsonStuff[i.toString()][0].indexOf(",");
	    if(trimLen == -1){
		trimLen = jsonStuff[i.toString()][0].indexOf(" | ");
	    }
	    var ch = document.createElement("input");
	    ident = "food" + i;
	    ch.setAttribute("id", ident)
	    var lb = document.createElement("label");
	    var brk = document.createElement("br")
	    lb.setAttribute("for", ident);
	    ch.type = "checkbox";
	    if(trimLen == -1){
		ch.text = jsonStuff[i.toString()][0];
		ch.value = jsonStuff[i.toString()][0];
		lb.innerHTML = jsonStuff[i.toString()][0];
		//ch.name = jsonStuff[i.toString()];
		ch.name = "foods";
	    }
	    else {
		ch.text = jsonStuff[i.toString()][0].slice(0, trimLen);
		ch.value = jsonStuff[i.toString()][0].slice(0, trimLen);
		lb.innerHTML = jsonStuff[i.toString()][0].slice(0, trimLen);
		//ch.name = jsonStuff[i.toString()].slice(0, trimLen);
		ch.name = "foods";
	    }
	    f.appendChild(ch);
	    f.appendChild(lb);
	    f.appendChild(brk);
	}


    }
    var sub = document.createElement("input");
    sub.type = "submit"
    sub.value = "Find Recipes"
    f.append(sub)
    document.getElementById("B").appendChild(f);

}

function D_response(jsonStuff) {
  b = document.getElementById("D")
    while (b.hasChildNodes()) {
	b.removeChild(b.firstChild);
    }
    
    
    var f = document.createElement("form");
    f.setAttribute('method', 'post');
    f.setAttribute('action', '/recipes');

    for (let i = 1; i < 9; i++) {
	if (jsonStuff[i.toString()] != ""){
	    trimLen = jsonStuff[i.toString()][0].indexOf(",");
	    if(trimLen == -1){
		trimLen = jsonStuff[i.toString()][0].indexOf(" | ");
	    }
	    var ch = document.createElement("input");
	    ident = "food" + i;
	    ch.setAttribute("id", ident)
	    var lb = document.createElement("label");
	    var brk = document.createElement("br")
	    lb.setAttribute("for", ident);
	    ch.type = "checkbox";
	    if(trimLen == -1){
		ch.text = jsonStuff[i.toString()][0];
		ch.value = jsonStuff[i.toString()][0];
		lb.innerHTML = jsonStuff[i.toString()][0];
		//ch.name = jsonStuff[i.toString()];
		ch.name = "foods";
	    }
	    else {
		ch.text = jsonStuff[i.toString()][0].slice(0, trimLen);
		ch.value = jsonStuff[i.toString()][0].slice(0, trimLen);
		lb.innerHTML = jsonStuff[i.toString()][0].slice(0, trimLen);
		//ch.name = jsonStuff[i.toString()].slice(0, trimLen);
		ch.name = "foods";
	    }
	    f.appendChild(ch);
	    f.appendChild(lb);
	    f.appendChild(brk);
	}


    }
    var sub = document.createElement("input");
    sub.type = "submit"
    sub.value = "Find Recipes"
    f.append(sub)
    document.getElementById("B").appendChild(f);
}


function S_response(jsonStuff) {
  b = document.getElementById("S")
    while (b.hasChildNodes()) {
	b.removeChild(b.firstChild);
    }
    
    
    var f = document.createElement("form");
    f.setAttribute('method', 'post');
    f.setAttribute('action', '/recipes');

    for (let i = 1; i < 9; i++) {
	if (jsonStuff[i.toString()] != ""){
	    trimLen = jsonStuff[i.toString()][0].indexOf(",");
	    if(trimLen == -1){
		trimLen = jsonStuff[i.toString()][0].indexOf(" | ");
	    }
	    var ch = document.createElement("input");
	    ident = "food" + i;
	    ch.setAttribute("id", ident)
	    var lb = document.createElement("label");
	    var brk = document.createElement("br")
	    lb.setAttribute("for", ident);
	    ch.type = "checkbox";
	    if(trimLen == -1){
		ch.text = jsonStuff[i.toString()][0];
		ch.value = jsonStuff[i.toString()][0];
		lb.innerHTML = jsonStuff[i.toString()][0];
		//ch.name = jsonStuff[i.toString()];
		ch.name = "foods";
	    }
	    else {
		ch.text = jsonStuff[i.toString()][0].slice(0, trimLen);
		ch.value = jsonStuff[i.toString()][0].slice(0, trimLen);
		lb.innerHTML = jsonStuff[i.toString()][0].slice(0, trimLen);
		//ch.name = jsonStuff[i.toString()].slice(0, trimLen);
		ch.name = "foods";
	    }
	    f.appendChild(ch);
	    f.appendChild(lb);
	    f.appendChild(brk);
	}


    }
    var sub = document.createElement("input");
    sub.type = "submit"
    sub.value = "Find Recipes"
    f.append(sub)
    document.getElementById("B").appendChild(f);

}
