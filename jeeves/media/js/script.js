/*
Handle message box
*/
$(document).ready(function(){
    if ($("#message").text().length < 1) {
        $("#message").hide();
    } else {
        $("#message").fadeOut(10000, function(){ 
            $("#message").remove()
        });
    }
});






