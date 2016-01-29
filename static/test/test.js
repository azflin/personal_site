function doCalculation(){
    $.get('/test/test_function/', function(response){
            console.log(response);
    });
    pollProgress();
}

function pollProgress(){
    $.get('/test/test_poll/', function(response){
        console.log(response);
        if (response.done) {
            console.log("Done!");
        } else {
            console.log(response.data);
            pollProgress()
        }

    });
}

$(function(){
    console.log('ready!');
    $("#click_me").click(function(){
        console.log("clicked!");
        doCalculation();
    });
});