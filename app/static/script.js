const host= "http://127.0.0.1/";


// code for sound toggle 

if (window.location.href == host){

    var image = document.getElementById("sound");
    image.src = "static/soundOn.png";
    var sound = document.getElementById("audio");
    // sound.play()

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
    var startDiv = document.getElementById("startDiv");
    var soundDiv= document.getElementById("soundDiv");
    var div1= document.getElementById("div1");
    var div2= document.getElementById("div2");
    var div3= document.getElementById("div3");
    var div4= document.getElementById("div4");
    var next = document.getElementById("next");

    var start = document.getElementById("startBtn");
   

    soundDiv.style.display = "none";
    div1.style.display = "none";
    div2.style.display = "none";
    div3.style.display = "none";
    div4.style.display = "none";
   

    var audio1 = document.getElementById("audio1");
    var audio2 = document.getElementById("audio2");
    var audio3 = document.getElementById("audio3");
    var audio4 = document.getElementById("audio4");

    var flower1 = document.getElementById("flower1");
    var flower2 = document.getElementById("flower2");
    var flower3 = document.getElementById("flower3");
    var flower4 = document.getElementById("flower4");

    var can1 = document.getElementById("can1");
    var can2 = document.getElementById("can2");
    var can3 = document.getElementById("can3");
    var can4 = document.getElementById("can4");

    

    var finish1 = document.getElementById("finish1");
    var finish2 = document.getElementById("finish2");
    var finish3 = document.getElementById("finish3");
    var finish4 = document.getElementById("finish4");

    var points = 0;

    var clickedArray1 = []
    var clickedArray2 = []
    var clickedArray3 = []
    var clickedArray4 = []


    
   

    function playOne(){

        startDiv.style.display = "none";
        soundDiv.style.display ="block";
        audio1.play()
        


    }

    function showDiv1() {

        soundDiv.style.display ="none"
        div1.style.display = "block"

    }


    function begin() {

        playOne()
        setTimeout(showDiv1, 7000);
    }

    // code for step 1 

    function clicked1(event){

        if (event.target== flower1){

            clickedArray1.push('f')
        }

        if (event.target == can1){

            clickedArray1.push('c')
        }
        console.log(clickedArray1)
    }

 

    function evaluate1(){

        if (JSON.stringify(clickedArray1) === JSON.stringify(['f','c'])) {

            document.getElementById("v1").value = 1;
            div1.style.display = "none";
            soundDiv.style.display = "block";
            audio2.play()
        }
        else{

            document.getElementById("v1").value = 0;
            document.getElementById("v2").value = 0;
            document.getElementById("v3").value = 0;
            document.getElementById("v4").value = 0;
            document.getElementById("form").submit();
            
        }

    }
    
    function showDiv2(){

        soundDiv.style.display = "none";
        div2.style.display = "block";
    }

    function question1(){
        evaluate1()
        setTimeout(showDiv2, 7000);
    }



 // code for step 2 

    function clicked2(event){

        if (event.target== flower2){

            clickedArray2.push('f')
        }

        if (event.target == can2){

            clickedArray2.push('c')
        }
        
    }

 

    function evaluate2(){

        if (JSON.stringify(clickedArray2) === JSON.stringify(['c','f'])) {

            document.getElementById("v2").value = 1;
        
        }
        else{
            document.getElementById("v2").value = 0;
        }

        div2.style.display = "none";
        soundDiv.style.display = "block";
        audio3.play()
        

    }
    
    function showDiv3(){

        soundDiv.style.display = "none";
        div3.style.display = "block";
    }

    function question2(){
        evaluate2()
        setTimeout(showDiv3, 6000);
    }

    // code for step 3
    
    function clicked3(event){

        if (event.target== flower3){

            clickedArray3.push('f')
        }

        if (event.target == can3){

            clickedArray3.push('c')
        }
        
    }

 

    function evaluate3(){

        if (JSON.stringify(clickedArray3) === JSON.stringify(['f'])) {

            document.getElementById("v3").value = 1;
        
        }
        else{
            document.getElementById("v3").value = 0;
        }

        div3.style.display = "none";
        soundDiv.style.display = "block";
        audio4.play()
        

    }
    
    function showDiv4(){

        soundDiv.style.display = "none";
        div4.style.display = "block";
    }

    function question3(){
        evaluate3()
        setTimeout(showDiv4, 6000);
    }


    // code for step 4 

    function clicked4(event){

        if (event.target== flower4){

            clickedArray4.push('f')
        }

        if (event.target == can4){

            clickedArray4.push('c')
        }
        
    }

 

    function evaluate4(){

        if (JSON.stringify(clickedArray4) === JSON.stringify(['f','c'])) {

            document.getElementById("v4").value = 1;
        
        }
        else{
            document.getElementById("v4").value = 0;
        }

        document.getElementById("form").submit();
        

    }
    





    start.addEventListener('click', begin, false);

    flower1.addEventListener('click', clicked1, false);
    can1.addEventListener('click', clicked1, false);

    finish1.addEventListener('click', question1, false)

    flower2.addEventListener('click', clicked2, false);
    can2.addEventListener('click', clicked2, false);

    finish2.addEventListener('click', question2, false)

    flower3.addEventListener('click', clicked3, false);
    can3.addEventListener('click', clicked3, false);

    finish3.addEventListener('click', question3, false)
    
    flower4.addEventListener('click', clicked4, false);
    can4.addEventListener('click', clicked4, false);

    finish4.addEventListener('click', evaluate4, false)



}
