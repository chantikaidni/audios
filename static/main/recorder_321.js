// function getCookie(c_name) {
//         if (document.cookie.length > 0) {
//             c_start = document.cookie.indexOf(c_name + "=");
//             if (c_start != -1) {
//                 c_start = c_start + c_name.length + 1;
//                 c_end = document.cookie.indexOf(";", c_start);
//                 if (c_end == -1) c_end = document.cookie.length;
//                 return unescape(document.cookie.substring(c_start, c_end));
//             }
//         }
//         return "";
//     }

//     $(function() {
//         $.ajaxSetup({
//             headers: {
//                 "X-CSRFToken": getCookie("csrftoken")
//             }
//         });
//     });

var h1 = document.getElementById('timer'),
    seconds = 0,
    minutes = 0,
    hours = 0,
    t;

function add() {
    seconds++;
    if (seconds >= 60) {
        seconds = 0;
        minutes++;
        if (minutes >= 60) {
            minutes = 0;
            hours++;
        }
    }

    h1.textContent = (hours ? (hours > 9 ? hours : "0" + hours) : "00") + ":" + (minutes ? (minutes > 9 ? minutes : "0" + minutes) : "00") + ":" + (seconds > 9 ? seconds : "0" + seconds);

    timer();
}

function timer() {
    t = setTimeout(add, 1000);
}


function __log(e, data) {
    log.innerHTML += "\n" + e + " " + (data || '');
}

var audio_context;
var recorder;

function startUserMedia(stream) {
    var input = audio_context.createMediaStreamSource(stream);
    // __log('Media stream created.');

    // Uncomment if you want the audio to feedback directly
    //input.connect(audio_context.destination);
    //__log('Input connected to audio context destination.');

    recorder = new Recorder(input);
    // __log('Recorder initialised.');
}

function startRecording() {
    timer();
    recorder && recorder.record();
    // button.disabled = true;
    // button.nextElementSibling.disabled = false;
    // __log('Recording...');
}

function stopRecording() {
    recorder && recorder.stop();
    clearTimeout(t);
    console.log("stopped");
    // button.disabled = true;
    // button.previousElementSibling.disabled = false;
    // __log('Stopped recording.');

    // create WAV download link using audio data blob
    createDownloadLink();
    recorder.clear();
    h1.textContent = "00:00:00";
    seconds = 0;
    minutes = 0;
    hours = 0;
}

function createDownloadLink() {
    recorder && recorder.exportWAV(function(blob) {
        console.log(blob);
        var fd = new FormData();
        fd.append('blob', blob);
        fd.append('sachin', 'sachin');
        fd.append('csrfmiddlewaretoken', token);
        fd.append('sachi', 'hhj');
        $.ajax({
            url: '../upload/',
            type: 'POST',
            data: fd,
            processData: false,
            contentType: false,
            success: function(data) {
                console.log('test_binary ' + JSON.stringify(data));
                var url = URL.createObjectURL(blob);
                var audio = document.getElementById('play_audio_confirm_modal');
                var str = '<audio controls src = ' + url + "> </audio>";
                audio.innerHTML = str;
            }
        });
    });
}

function get_permissions() {
    try {
        // webkit shim
        window.AudioContext = window.AudioContext || window.webkitAudioContext;
        navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
        window.URL = window.URL || window.webkitURL;

        audio_context = new AudioContext;
        // __log('Audio context set up.');
        // __log('navigator.getUserMedia ' + (navigator.getUserMedia ? 'available.' : 'not present!'));
    } catch (e) {
        alert('We were not able to detect your microphone. Please retry or contact support if problem persists.');
    }


    navigator.getUserMedia({
        audio: true
    }, startUserMedia, function(e) {
        // __log('No live audio input: ' + e);
        // startRecording();
    });

};
