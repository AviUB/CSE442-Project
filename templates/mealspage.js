

//var foodname = document.getElementById("fname8").value;

var Breakfast = [""];
var Lunch = [""];
var Dinner = [""];
var Snacks = [""];
var str = "";
/*
function xmlGetUserFood(mealType) {
  if (mealType = "B") {} //xml req for breakfast, should update Breakfast array and make it display everything stored for breakfast from the server
  else if (mealType = "L") {}
  else if (mealType = "D") {}
  else if (mealType = "S") {}
  else {}
  // call this every time we submit to get stuff from database in server
  // can make one for each breakfast lunch and dinner instead
}
*/
/*
function doAPI(name) {
  var x = new XMLHttpRequest();
  var url =
  const url2 = url + name

  x.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var jsonStuff = JSON.parse(this.responseText);
        console.log("we got : " + this.responseText + " from the server");
        str = parseAPI(jsonStuff);

  }}
  x.open("GET", url, true);
  x.send();


}*/
/*
function parseAPI(jsonStuff) {
  console.log(jsonStuff);
  name1 = jsonStuff.foods[0].description;
  console.log(name1);
  nutrients =(jsonStuff.foods[0].foodNutrients);

  protein = nutrients[0].value;
  console.log(protein);
  fat = nutrients[1].value;
  console.log(fat);
  carbs = nutrients[2].value;
  console.log(carbs);
  calories = nutrients[3].value;
  console.log(calories);
  var astr = name1+"   "+calories + "   " +carbs+"   " + fat+"    "+protein+"   "+"12";
  console.log(astr);
  return astr;
  //var my_div= document.getElementById("demo").innerHTML += "<br />" +name1+astr;
  // Begin accessing JSON data here
}*/



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

// using the xml send, we can determine what to do with the data depending on what we set the xml to
// we can set the xml to something like "1: <input value from html>" and "2: <input>"... and so on

//xmlGetUserFood() {}
/*
var xhr = new XMLHttpRequest()
 xhr.open("POST", "myscript.php"); xhr.onload=function(event){ 	alert("The server says: " + event.target.response); };
  var formData = new FormData(document.getElementById("myForm"));
   xhr.send(formData);
*/



function xmlBreakfast() {
  var x = new XMLHttpRequest();
  var url = "/mealspage";
  var foodSent = document.getElementById("inputOne").value;
  console.log("sending " + foodSent + " to the server");

  x.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var jsonStuff = JSON.parse(this.responseText);
        console.log("we got : " + this.responseText + " from the server");
        B_response(jsonStuff);
  }}
  x.open("POST", url, true);
  x.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
  x.send("name=b" + foodSent);

}

function xmlLunch() {
  var x = new XMLHttpRequest();
  var url = "/mealspage";
  var foodSent = document.getElementById("inputTwo").value;
  console.log("sending " + foodSent + " to the server");

  x.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var jsonStuff = JSON.parse(this.responseText);
        console.log("we got : " + this.responseText + " from the server");
        L_response(jsonStuff);
  }}
  x.open("POST", url, true);
  x.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
  x.send("name=l" + foodSent);

}

function xmlDinner() {
  var x = new XMLHttpRequest();
  var url = "/mealspage";
  var foodSent = document.getElementById("inputThree").value;
  console.log("sending " + foodSent + " to the server");

  x.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var jsonStuff = JSON.parse(this.responseText);
        console.log("we got : " + this.responseText + " from the server");
        D_response(jsonStuff);
  }}
  x.open("POST", url, true);
  x.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
  x.send("name=d" + foodSent);

}

function xmlSnacks() {
  var x = new XMLHttpRequest();
  var url = "/mealspage";
  var foodSent = document.getElementById("inputFour").value;
  console.log("sending " + foodSent + " to the server");

  x.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var jsonStuff = JSON.parse(this.responseText);
        console.log("we got : " + this.responseText + " from the server");
        S_response(jsonStuff);
  }}
  x.open("POST", url, true);
  x.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
  x.send("name=s" + foodSent);

}

function B_response(jsonStuff) {
  // json stuff will be the food info from the api that we get from our server
  //var foodElement = jsonStuff["1"]; //do something with jsonStuff
  b = document.getElementById("B")
  while (b.hasChildNodes()) {
    b.removeChild(b.firstChild);
  }


  for (let i = 1; i < 9; i++) {
    if (jsonStuff[i.toString()] != ""){
      var p = document.createElement("p");
       //doAPI(jsonStuff[i.toString()]);
      //var thing = str;
      //console.log(str);
      //console.log(thing);
      p.appendChild( document.createTextNode(jsonStuff[i.toString()]) );
      document.getElementById("B").appendChild(p);
    }

}

}

function L_response(jsonStuff) {
  // json stuff will be the food info from the api that we get from our server
  //var foodElement = jsonStuff["1"]; //do something with jsonStuff
  b = document.getElementById("L")
  while (b.hasChildNodes()) {
    b.removeChild(b.firstChild);
  }


  for (let i = 1; i < 9; i++) {
    if (jsonStuff[i.toString()] != ""){
      var p = document.createElement("p");
      p.appendChild( document.createTextNode(jsonStuff[i.toString()]) );
      document.getElementById("L").appendChild(p);
    }

}

}

function D_response(jsonStuff) {
  // json stuff will be the food info from the api that we get from our server
  //var foodElement = jsonStuff["1"]; //do something with jsonStuff
  b = document.getElementById("D")
  while (b.hasChildNodes()) {
    b.removeChild(b.firstChild);
  }


  for (let i = 1; i < 9; i++) {
    if (jsonStuff[i.toString()] != ""){
      var p = document.createElement("p");
      p.appendChild( document.createTextNode(jsonStuff[i.toString()]) );
      document.getElementById("D").appendChild(p);
    }

}
}


function S_response(jsonStuff) {
  // json stuff will be the food info from the api that we get from our server
  //var foodElement = jsonStuff["1"]; //do something with jsonStuff
  b = document.getElementById("S")
  while (b.hasChildNodes()) {
    b.removeChild(b.firstChild);
  }


  for (let i = 1; i < 9; i++) {
    if (jsonStuff[i.toString()] != ""){
      var p = document.createElement("p");
      p.appendChild( document.createTextNode(jsonStuff[i.toString()]) );
      document.getElementById("S").appendChild(p);
    }

}

}
function caloriestotal() {
  b = document.getElementById("S")
  while (b.hasChildNodes()) {
    document.getElementById("C").appendChild(b.firstChild);
  }
}



/*
function mealMade() {
  var x = new XMLHttpRequest();
  // x.open('POST', 'achievements', true);
  var url = "the website api thing";

  x.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var jsonstuff = JSON.parse(this.responseText);
        thisiswhereyoudostuffwithjsonfromapi(jsonStuff);
    }
  };
  x.open("POST", url, true);
  x.send();
}


function submitForm() {
  var name =document.getElementById("fname").value;
    const https = require('https')
    const url = 'https://api.nal.usda.gov/fdc/v1/foods/search?api_key=dhIFeY8WhF9o0tUGenudfxO0tAQEvByUb3N9bGIj&dataType=Survey (FNDDS)&query=';
    const url2 = url + name

    https.get(url2, res => {
        let data = '';
        res.on('data', chunk => {
            data += chunk;
        });
        res.on('end', () => {
            data = JSON.parse(data);
            console.log(data);
            name1 = data.foods[0].description
            console.log(name1)
            nutrients =(data.foods[0].foodNutrients)

            protein = nutrients[0]
            console.log(protein.value)
            fat = nutrients[1]
            console.log(fat.value)
            carbs = nutrients[2]
            console.log(carbs.value)
            calories = nutrients[3]
            console.log(calories.value)
            var astr = "   "+calories + "   " +carbs+"   " + fat+"    "+protein+"   "+"12"
            document.getElementById("demo").innerHTML = name1+astr;
        })
    }).on('error', err => {
        console.log(err.message);
    })

}





function submitForm1() {
  mealsMade()
}
function mealsMade(){
    var name =document.getElementById("fname1").value;
    const https = require('https')
    const url = 'https://api.nal.usda.gov/fdc/v1/foods/search?api_key=dhIFeY8WhF9o0tUGenudfxO0tAQEvByUb3N9bGIj&dataType=Survey (FNDDS)&query=';
    const url2 = url + name

    https.get(url2, res => {
        let data = '';
        res.on('data', chunk => {
            data += chunk;
        });
        res.on('end', () => {
            data = JSON.parse(data);
            console.log(data);
            name1 = data.foods[0].description
            console.log(name1)
            nutrients =(data.foods[0].foodNutrients)

            protein = nutrients[0]
            console.log(protein.value)
            fat = nutrients[1]
            console.log(fat.value)
            carbs = nutrients[2]
            console.log(carbs.value)
            calories = nutrients[3]
            console.log(calories.value)
            var astr = "   "+calories + "   " +carbs+"   " + fat+"    "+protein+"   "+"12"
            document.getElementById("demo").innerHTML = name1+astr;
        })
    }).on('error', err => {
        console.log(err.message);
    })

}


function submitForm2() {
  var name =document.getElementById("fname3").value;
  document.getElementById("demo3").innerHTML = name;
}




function passvalue() {
    var foodname = document.getElementById("fname5").value;
    localStorage.setItem("foodvalue", foodname);
    return false

}

function submitForm3() {
  var name =document.getElementById("fname4").value;
  document.getElementById("demo4").innerHTML = name;
    document.getElementById("snacks").innerHTML = name;
}



mealMade();


thisiswhereyoudostuffwithjsonfromapi(jsonstuff) {
  // this is a json you get from the server
  dsfljkl
}
*/
setTimeout(function() { xmlB(); }, 1000);
setTimeout(function() { xmlL(); }, 1500);
setTimeout(function() { xmlD(); }, 2000);
setTimeout(function() { xmlS(); }, 2500);
