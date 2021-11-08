// we can get a running list of achivements from the server with
// a json file, I don't think it should all be through html

// we will ultimately want to send information for users' achievements
// through a json file, which is made with info from the database


// clone from git

// go in server and create path information and find a way to send json here

// have the server send json and here we unpack it and automatically
// generate all of the achievement information sent in the JSON

// after all of that maybe make rudimentary code that sends info to the server
// to update achievement information

// get json from server
// getTheJSON();
jsonThing = {"1": ["Achievement: Would you look at the time!", "Successfully logged in for the first time.", "1"],
            "2": ["Achievement: Here comes the plane!", "Create your first meal.", "0"],
            "3": ["Achievement: Who's hungry?", "Login on 3 separate occasions.", "0"]};
//generateAchs(jsonThing);


function getTheJSON() {
  var x = new XMLHttpRequest();
  // x.open('POST', 'achievements', true);
  var url = "/achievements";

  x.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var jsonStuff = JSON.parse(this.responseText);
        generateAchs(jsonStuff);
    }
  };
  x.open("POST", url, true);
  x.send();
}




function generateAchs(ob) {
  console.log("hil");
  var i = 1;
  while (i <= Object.keys(ob).length){

    console.log("woo");
    var y = i.toString();
    console.log(y);
    var diction = ob[y];

    var t = document.createElement("div");

    var eOne = document.createElement("h3");
    console.log(diction[0]);
    eOne.appendChild(document.createTextNode(diction[0]));

    var eTwo = document.createElement("h4");
    console.log(diction[2]);
    var txt = "";
    if (diction[2] == 0) {
      eTwo.className = "locked";
      txt = "locked";
    } else {
      eTwo.className = "unlocked";
      txt = "unlocked";
    }

    eTwo.appendChild(document.createTextNode(txt));

    var eThree = document.createElement("h4");
    console.log(diction[1]);
    eThree.className = "text";
    eThree.appendChild(document.createTextNode(diction[1]));

    t.className = "ach";
    t.appendChild(eOne);
    t.appendChild(eTwo);
    t.appendChild(eThree);

    var bod = document.getElementById("bod");

    bod.appendChild(t);

    i++;
  }
}
