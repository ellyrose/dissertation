// code for sound toggle 

var image = document.getElementById("sound");
image.src = "static/soundOn.png";
var sound = document.getElementById("audio");
sound.play()

function togglePlay() {
    if (sound.paused) {
        image.src= "static/soundOn.png";
        sound.play();
    }
    else {
        sound.pause();
        image.src="static/soundOff.png";
    }
};

image.addEventListener("click",togglePlay, false);   
