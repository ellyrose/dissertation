const host= "http://127.0.0.1/";


// code for sound toggle 

if (window.location.href == host){

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

}


// code for question 2 

if (window.location.href == host + 'fluency2')

{

    var video = document.getElementById("video");
    var videoDiv = document.getElementById("videoDiv")
    video.style.display = "none";
    var questionBlock= document.getElementById("questions")
    questionBlock.style.display = "none";

    function play() {
        video.play();
        document.getElementById("play").style.display = "none";
        document.getElementById("videoDiv").style.display = "none";
    }

    function showQuestions(){

        questionBlock.style.display = "block";
    }


    function questions() {
        play();
        setTimeout(showQuestions, 17500);
        
    }


    playButton= document.getElementById("play");
    playButton.addEventListener('click', questions, false);

}

// code for question 6 

if (window.location.href == host + 'fluency6')

{
    var canvas;
    var stage;
    var flower;
    var can;
    var points = 0;

    function init() {

        canvas= document.getElementById("canvas");
        stage= new createjs.Stage(canvas);
        flower= new Image();
        flower.src= "static/flower2.png";
        flower.onload = loadFlower;
        can = new Image();
        can.src= "static/can3.png";
        can.onload = loadCan;

        
        stage.update();



    }


    function loadFlower(event) {

        var image = event.target;
        var flower = new createjs.Bitmap(image);
        stage.addChild(flower);
        flower.x= canvas.width-700;
        flower.y= canvas.height/2-200
    
        var mover = new createjs.Container();
        mover.x = mover.y = 100;
        mover.addChild(flower);
        stage.addChild(mover);

        mover.on("mousedown", function (evt) {
            // keep a record on the offset between the mouse position and the container
            // position. currentTarget will be the container that the event listener was added to:
            evt.currentTarget.offset = {x: this.x - evt.stageX, y: this.y - evt.stageY};
        });
        
        mover.on("pressmove",function(evt) {
            // Calculate the new X and Y based on the mouse new position plus the offset.
            evt.currentTarget.x = evt.stageX + evt.currentTarget.offset.x;
            evt.currentTarget.y = evt.stageY + evt.currentTarget.offset.y;
            // make sure to redraw the stage to show the change:
            stage.update();   
        });

    
        
        stage.update();
    }

    function loadCan(event) {

        var image = event.target;
        var can = new createjs.Bitmap(image);
        stage.addChild(can);
        can.x= canvas.width-400;
        can.y= canvas.height/2-100
        var mover = new createjs.Container();
        mover.x = mover.y = 100;
        mover.addChild(can);
        stage.addChild(mover);

        mover.on("mousedown", function (evt) {
            evt.currentTarget.offset = {x: this.x - evt.stageX, y: this.y - evt.stageY};
        });
        
        mover.on("pressmove",function(evt) {
            evt.currentTarget.x = evt.stageX + evt.currentTarget.offset.x;
            evt.currentTarget.y = evt.stageY + evt.currentTarget.offset.y;
            stage.update();   
        });
        
        stage.update();
    }

    var start = document.getElementById("start");

    start.addEventListener('click', one, false);


    flower.addEventListener("click", evaluateAns, false);   

    can.addEventListener("click",evaluateAns, false);   


    function evaluateAns(event){

        if (event.target == flower){

            points += 1;
        }

        else{
            pass

        }
        console.log(points)
    }

}
