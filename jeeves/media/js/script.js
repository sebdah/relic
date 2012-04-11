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


/*
Enter key should submit forms.
*/
$('input').keypress(function(e){
    if(e.which == 13){
        $('input').closest('form').submit();
    }
});