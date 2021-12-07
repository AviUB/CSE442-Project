

var date = new Date(); // current date
// var weekday = d.getDay(); // 0 through 6
// var mon = d.getMonth(); // 0 through 11
var Year = date.getFullYear();
var Month = date.getMonth(); // month 0 through 11



var Jan = 31;
var Feb = 28; // 29 if leap year
var Mar = 31;
var Apr = 30;
var May = 31;
var Jun = 30;
var Jul = 31;
var Aug = 31;
var Sep = 30;
var Oct = 31;
var Nov = 30;
var Dec = 31;

var mealDict = {};
var recCals = 0;

var dict = {
  "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0,
  "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0,
  "15": 0, "16": 0, "17": 0, "18": 0, "19": 0, "20": 0, "21": 0,
  "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0, "28": 0,
  "29": 0, "30": 0, "31": 0, "32": 0, "33": 0, "34": 0, "35": 0,
  "36": 0, "37": 0, "38": 0, "39": 0, "40": 0, "41": 0, "42": 0
};


function hello() { document.getElementById("a5").innerHTML = "99";}

function totalCals(day) {
  var grandTotal = 0;
  for (let someDate in mealDict){
    if (someDate == (  (Month+1).toString() + "-" + day +"-" +Year.toString()  )) {


      for (let i=0; i<8; i++){
        //console.log(mealDict[someDate]["break"])
        console.log(mealDict[someDate]["break"][i])
        if (mealDict[someDate]["break"][i] != ""){
            //console.log(elem)
            console.log("Yay we made it with"+ mealDict[someDate]["break"][i])
            const theArray = mealDict[someDate]["break"][i].split("|");
            console.log(theArray)
            for (let q=0; q<theArray.length; q++){
              console.log(theArray[q])
              if (theArray[q].includes("calories")){
                var theCals = parseInt(theArray[q].trim().split(" ")[0]);
                grandTotal += theCals;
              }
            }

        }
      }
      for (let i=0; i<8; i++){
        //console.log(mealDict[someDate]["break"])
        console.log(mealDict[someDate]["lunch"][i])
        if (mealDict[someDate]["lunch"][i] != ""){
            //console.log(elem)
            //console.log("Yay we made it with"+ mealDict[someDate]["break"][i])
            const theArray = mealDict[someDate]["lunch"][i].split("|");
            console.log(theArray)
            for (let q=0; q<theArray.length; q++){
              console.log(theArray[q])
              if (theArray[q].includes("calories")){
                var theCals = parseInt(theArray[q].trim().split(" ")[0]);
                grandTotal += theCals;
              }
            }

        }
      }
      for (let i=0; i<8; i++){
        //console.log(mealDict[someDate]["break"])
        console.log(mealDict[someDate]["dinner"][i])
        if (mealDict[someDate]["dinner"][i] != ""){
            //console.log(elem)
            //console.log("Yay we made it with"+ mealDict[someDate]["break"][i])
            const theArray = mealDict[someDate]["dinner"][i].split("|");
            console.log(theArray)
            for (let q=0; q<theArray.length; q++){
              console.log(theArray[q])
              if (theArray[q].includes("calories")){
                var theCals = parseInt(theArray[q].trim().split(" ")[0]);
                grandTotal += theCals;
              }
            }

        }
      }
      for (let i=0; i<8; i++){
        //console.log(mealDict[someDate]["break"])
        console.log(mealDict[someDate]["snack"][i])
        if (mealDict[someDate]["snack"][i] != ""){
            //console.log(elem)
            //console.log("Yay we made it with"+ mealDict[someDate]["break"][i])
            const theArray = mealDict[someDate]["snack"][i].split("|");
            console.log(theArray)
            for (let q=0; q<theArray.length; q++){
              console.log(theArray[q])
              if (theArray[q].includes("calories")){
                var theCals = parseInt(theArray[q].trim().split(" ")[0]);
                grandTotal += theCals;
              }
            }

        }
      }


    }


  }
  return grandTotal;
}

function updateMenu(day) {

  var elem = document.getElementById("b");
  while (elem.hasChildNodes()) {
    elem.removeChild(elem.firstChild);
  }
  elem = document.getElementById("l");
  while (elem.hasChildNodes()) {
    elem.removeChild(elem.firstChild);
  }
  elem = document.getElementById("d");
  while (elem.hasChildNodes()) {
    elem.removeChild(elem.firstChild);
  }
  elem = document.getElementById("s");
  while (elem.hasChildNodes()) {
    elem.removeChild(elem.firstChild);
  }

  document.getElementById("recCals").innerHTML = recCals.toString();
  document.getElementById("totCals").innerHTML = totalCals(day).toString();

  // day, Year, Month
  var thePath = "/mealspage/" + (Month+1).toString() + "-" + day +"-" +Year.toString();
  console.log(thePath);
  document.getElementById("mealsLink").setAttribute("href", thePath);
  document.getElementById("menu").innerHTML = "Meals page for " + (Month+1).toString() + "/"+day;
  for (let someDate in mealDict) {
    if (someDate == (  (Month+1).toString() + "-" + day +"-" +Year.toString()  ) ) {
      for (let i=0; i<8; i++) {
        if ( mealDict[someDate]["break"][i] != "" ){
          var p = document.createElement("P");
          p.appendChild( document.createTextNode(mealDict[someDate]["break"][i]) );
          document.getElementById("b").appendChild( p );
        }

        if ( mealDict[someDate]["lunch"][i] != "" ) {
          var p1 = document.createElement("P");
          p1.appendChild( document.createTextNode(mealDict[someDate]["lunch"][i]) );
          document.getElementById("l").appendChild( p1 );
        }

        if (mealDict[someDate]["dinner"][i] != "") {
          var p2 = document.createElement("P");
          p2.appendChild( document.createTextNode(mealDict[someDate]["dinner"][i]) );
          document.getElementById("d").appendChild( p2 );
        }

        if ( mealDict[someDate]["snack"][i] != "" ) {
          var p3 = document.createElement("P");
          p3.appendChild( document.createTextNode(mealDict[someDate]["snack"][i]) );
          document.getElementById("s").appendChild( p3 );
        }


      }

    }
  }


}


function getRecCals() {
  // this gets all the meals from the server in a JSON
  var x = new XMLHttpRequest();
  var url = "/calendar";


  x.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var jsonStuff = JSON.parse(this.responseText);
        console.log("we got : " + this.responseText + " from the server");
        parseRecCal(jsonStuff);

  }}
  x.open("POST", url, true);
  x.send();
}

function parseRecCal(someJSON) {
  // {"Rec": int (calorie number)}
  console.log("Here is your recommended daily calorie intake"+someJSON["Rec"]);
  recCals = someJSON["Rec"];

}



function getMeals() {
  // this gets all the meals from the server in a JSON
  var x = new XMLHttpRequest();
  var url = "/doWork/getMeals";


  x.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var jsonStuff = JSON.parse(this.responseText);
        console.log("we got : " + this.responseText + " from the server");
        parseMeals(jsonStuff);

  }}
  x.open("POST", url, true);
  x.send();
}


function parseMeals(jsonStuff) {
  /*{"meals":[
    {"10-10-1960":["","","","","","","",""],"11-11-1911":["","","","","","","",""],"11-27-2021":["Crisp, apple, apple dessert   |   157 calories  |   30.7 grams   |   3.54 grams   |   2.09 grams","","","","","","",""]},
    {"10-10-1960":["","","","","","","",""],"11-11-1911":["","","","","","","",""]},
    {"10-10-1960":["","","","","","","",""],"11-11-1911":["","","","","","","",""]},
    {"10-10-1960":["","","","","","","",""],"11-11-1911":["","","","","","","",""]}]}*/
  var dictList = jsonStuff["meals"];

  var snackDict = dictList[3];
  var dinnerDict = dictList[2];
  var lunchDict = dictList[1];
  var breakDict = dictList[0];

  //var dateDict = {date: {snack: [], lunch: [], dinner: [], breakfast: []}}
  var dateDict = {"11-12-1911": {"break": ["","","","","","","",""], "lunch": ["","","","","","","",""], "dinner": ["","","","","","","",""], "snack": ["","","","","","","",""]} };

  for (let dateKey in breakDict) {dateDict[dateKey] = {"break": ["","","","","","","",""], "lunch": ["","","","","","","",""], "dinner": ["","","","","","","",""], "snack": ["","","","","","","",""]    };}
  for (let dateKey in lunchDict) {dateDict[dateKey] = {"break": ["","","","","","","",""], "lunch": ["","","","","","","",""], "dinner": ["","","","","","","",""], "snack": ["","","","","","","",""]   };}
  for (let dateKey in dinnerDict) {dateDict[dateKey] = {"break": ["","","","","","","",""], "lunch": ["","","","","","","",""], "dinner": ["","","","","","","",""], "snack": ["","","","","","","",""] };}
  for (let dateKey in snackDict) {dateDict[dateKey] = {"break": ["","","","","","","",""], "lunch": ["","","","","","","",""], "dinner": ["","","","","","","",""], "snack": ["","","","","","","",""] };}

  for (let dateKey in breakDict) {
    breakList = ["","","","","","","",""];

    for (let i=0; i<8; i++) {
      breakList[i] = breakDict[dateKey][i];
    }

    dateDict[dateKey]["break"] = breakList;
  }




  for (let dateKey in lunchDict) {
    lunchList = ["","","","","","","",""];

    for (let i=0; i<8; i++) {
      lunchList[i] = lunchDict[dateKey][i];
    }

    dateDict[dateKey]["lunch"] = lunchList;
  }




  for (let dateKey in dinnerDict) {
    dinnerList = ["","","","","","","",""];

    for (let i=0; i<8; i++) {
      dinnerList[i] = dinnerDict[dateKey][i];
    }

    dateDict[dateKey]["dinner"] = dinnerList;
  }



  for (let dateKey in snackDict) {
    snackList = ["","","","","","","",""];

    for (let i=0; i<8; i++) {
      snackList[i] = snackDict[dateKey][i];
    }

    dateDict[dateKey]["snack"] = snackList;
  }
  //console.log(dateDict["10-10-1960"]["snack"]);
  //console.log(dateDict["10-10-1960"]["dinner"]);
  //console.log(dateDict["10-10-1960"]["lunch"]);
  //console.log(dateDict["10-10-1960"]["break"]);
  console.log(dateDict);
  mealDict = dateDict;
}






































function addMonth () {
  if (Month == 11) {
    Month = 0;
    Year += 1;
    var d = new Date(Year, Month, 3, 3, 3, 3, 3);
    var wD = getDayOne(d);
    var daysInMonth = getMon(d.getMonth());
    setDict(daysInMonth, wD);
    setCalendar();
    document.getElementById("Month").innerHTML = getMonString(Month) + "  " + Year.toString();
  }else if (Month == 0 && Year%4 == 0) {
    Month = 1;

    var d = new Date(Year, Month, 3, 3, 3, 3, 3);
    var wD = getDayOne(d);

    var daysInMonth = 29;
    setDict(daysInMonth, wD);
    setCalendar();
    document.getElementById("Month").innerHTML = getMonString(Month) + "  " + Year.toString();
  } else {
    Month += 1;
    var d = new Date(Year, Month, 3, 3, 3, 3, 3);
    var wD = getDayOne(d);
    var daysInMonth = getMon(d.getMonth());
    setDict(daysInMonth, wD);
    setCalendar();
    document.getElementById("Month").innerHTML = getMonString(Month) + "  " + Year.toString();
  }

}

function subMonth () {
  if (Month == 0) {
    Month = 11;
    Year = Year - 1;
    var d = new Date(Year, Month, 3, 3, 3, 3, 3);
    var wD = getDayOne(d);

    var daysInMonth = getMon(d.getMonth());
    setDict(daysInMonth, wD);
    setCalendar();
    document.getElementById("Month").innerHTML = getMonString(Month) + "  " + Year.toString();
  }else if (Month == 2 && Year%4 == 0) {
    Month = 1;

    var d = new Date(Year, Month, 3, 3, 3, 3, 3);
    var wD = getDayOne(d);

    var daysInMonth = 29;
    setDict(daysInMonth, wD);
    setCalendar();
    document.getElementById("Month").innerHTML = getMonString(Month) + "  " + Year.toString();
  } else {
    Month = Month - 1;
    var d = new Date(Year, Month, 3, 3, 3, 3, 3);
    var wD = getDayOne(d);
    var daysInMonth = getMon(d.getMonth());
    setDict(daysInMonth, wD);
    setCalendar();
    document.getElementById("Month").innerHTML = getMonString(Month) + "  " + Year.toString();
  }
}


function setDict(month, week) { // month is number of days in month, week is day of week of first day
  var start = 0;
  var day = 2;
  var secondStart = 0;
  switch (week) {
    case 0: dict["1"]=1; start=2; secondStart=month+1; break;
    case 1: dict["1"]=0; dict["2"]=1; start=3; secondStart=month+2; break;
    case 2: dict["1"]=0; dict["2"]=0; dict["3"]=1; start=4; secondStart=month+3; break;
    case 3: dict["1"]=0; dict["2"]=0; dict["3"]=0; dict["4"]=1; start=5; secondStart=month+4; break;
    case 4: dict["1"]=0; dict["2"]=0; dict["3"]=0; dict["4"]=0; dict["5"]=1; start=6; secondStart=month+5; break;
    case 5: dict["1"]=0; dict["2"]=0; dict["3"]=0; dict["4"]=0; dict["5"]=0; dict["6"]=1; start=7; secondStart=month+6; break;
    case 6: dict["1"]=0; dict["2"]=0; dict["3"]=0; dict["4"]=0; dict["5"]=0; dict["6"]=0; dict["7"]=1; start=8; secondStart=month+7; break;
    default: console.log("You shouldn't be seeing this message.");
  }
  for (let i=start; day<=month; i++) {
    var num = i.toString();
    console.log("setting dict[" + num + "] to "+ day.toString() );
    dict[num] = day;
    day+=1;

  }
  for (let i=secondStart; i<43; i++) {
    console.log("setting dict[" + i.toString()+ "] to zero" );
    dict[i.toString()] = 0;
  }
  console.log("day of the week for day one: " + week.toString());
  console.log("month : " + month.toString());
  console.log("Now lets print the full dicitonary!");
  console.log(dict);
}

function setCalendar() {



  for (let i=1; i<43; i++) {
    var theID = getID(i);
    var key = i.toString();

    if (dict[key] != 0) {
      document.getElementById(theID).innerHTML=(dict[key]).toString();
    }else {
      document.getElementById(theID).innerHTML="";
    }


  }
}

function getMon(theMonth) {
  var returnVal = 30;
  switch (theMonth) {
    case 0: returnVal=Jan; break;
    case 1: returnVal=Feb; break;
    case 2: returnVal=Mar; break;
    case 3: returnVal=Apr; break;
    case 4: returnVal=May; break;
    case 5: returnVal=Jun; break;
    case 6: returnVal=Jul; break;
    case 7: returnVal=Aug; break;
    case 8: returnVal=Sep; break;
    case 9: returnVal=Oct; break;
    case 10: returnVal=Nov; break;
    case 11: returnVal=Dec; break;
    default: console.log("You shouldn't be seeing this");
  }
  return returnVal;
}

function getMonString(theMonth) {
  var returnVal = 30;
  switch (theMonth) {
    case 0: returnVal="January"; break;
    case 1: returnVal="February"; break;
    case 2: returnVal="March"; break;
    case 3: returnVal="April"; break;
    case 4: returnVal="May"; break;
    case 5: returnVal="June"; break;
    case 6: returnVal="July"; break;
    case 7: returnVal="August"; break;
    case 8: returnVal="September"; break;
    case 9: returnVal="October"; break;
    case 10: returnVal="November"; break;
    case 11: returnVal="December"; break;
    default: console.log("You shouldn't be seeing this");
  }
  return returnVal;
}


function getID(num) {
  var returnVal = "";
  switch (num) {
    case 1: returnVal = "a1"; break;
    case 2: returnVal = "a2"; break;
    case 3: returnVal = "a3"; break;
    case 4: returnVal = "a4"; break;
    case 5: returnVal = "a5"; break;
    case 6: returnVal = "a6"; break;
    case 7: returnVal = "a7"; break;
    case 8: returnVal = "b1"; break;
    case 9: returnVal = "b2"; break;
    case 10: returnVal = "b3"; break;
    case 11: returnVal = "b4"; break;
    case 12: returnVal = "b5"; break;
    case 13: returnVal = "b6"; break;
    case 14: returnVal = "b7"; break;
    case 15: returnVal = "c1"; break;
    case 16: returnVal = "c2"; break;
    case 17: returnVal = "c3"; break;
    case 18: returnVal = "c4"; break;
    case 19: returnVal = "c5"; break;
    case 20: returnVal = "c6"; break;
    case 21: returnVal = "c7"; break;
    case 22: returnVal = "d1"; break;
    case 23: returnVal = "d2"; break;
    case 24: returnVal = "d3"; break;
    case 25: returnVal = "d4"; break;
    case 26: returnVal = "d5"; break;
    case 27: returnVal = "d6"; break;
    case 28: returnVal = "d7"; break;
    case 29: returnVal = "e1"; break;
    case 30: returnVal = "e2"; break;
    case 31: returnVal = "e3"; break;
    case 32: returnVal = "e4"; break;
    case 33: returnVal = "e5"; break;
    case 34: returnVal = "e6"; break;
    case 35: returnVal = "e7"; break;
    case 36: returnVal = "f1"; break;
    case 37: returnVal = "f2"; break;
    case 38: returnVal = "f3"; break;
    case 39: returnVal = "f4"; break;
    case 40: returnVal = "f5"; break;
    case 41: returnVal = "f6"; break;
    case 42: returnVal = "f7"; break;
    default: console.log("You shouldn't be seeing this");
  }
  return returnVal;
}


function getDayOne(curDay) {
  var day = curDay.getDate(); // 1 to 31
  var week = curDay.getDay(); // 0 to 6
  if (day == 1) {
    return week;
  } else {

    for (let i=day; i>0; i=i-1) {

      if (i == 1) {
        return week;
      }


      if (week == 0) {
        week = 6
      } else {
        week = week - 1;
      }

    }


  }
}






function enter(theID) {
  document.getElementById(theID).setAttribute("style", "background-color:#606e78;");
}

function exit(theID) {
  document.getElementById(theID).setAttribute("style", "background-color:#f2f2f2;");
}

function aEnter(theID) {
  document.getElementById(theID).setAttribute("style", "background-color:#606e78;");
}

function aExit(theID) {
  document.getElementById(theID).setAttribute("style", "background-color:#f2f2f2;");
}

function mealDay(theID) {

}
