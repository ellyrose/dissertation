//code for question 4

var video = document.getElementById("video");
var videoDiv = document.getElementById("videoDiv")
var questions= document.getElementById("questions")
video.style.display = "none"
questions.style.display = "none";

function play() {
    video.play();
    document.getElementById("play").style.display = "none";
    document.getElementById("videoDiv").style.display = "none";
}

function showQuestions(){

    document.getElementById("questions").style.display = "block";
}


function questions() {
    play();
    setTimeout(showQuestions, 17500);
    
}


playButton= document.getElementById("play");
playButton.addEventListener('click', questions, false);