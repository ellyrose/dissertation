var video = document.getElementById("video");
document.getElementById("questions").style.display = "none";

function play() {
    video.play();
    document.getElementById("play").style.display = "none";
    document.getElementById("videoDiv").style.display = "none";
}

setTimeout(function showQuestions(){

    document.getElementById("questions").style.display = "block";
}, 18000)


function questions() {
    play();
    showQuestions();
    
}


playButton= document.getElementById("play");
playButton.addEventListener('click', play, false);




