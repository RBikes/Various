window.onload = function () {
$('#ladies').click(function(){
    $('#men').toggleClass('small');
    $('#men').toggleClass('big');
    $('#ladies').toggleClass('big');
    $('#ladies').toggleClass('small');
});

$('#men').click(function(){
    $('#ladies').toggleClass('big');
    $('#ladies').toggleClass('small');
    $('#men').toggleClass('small');
    $('#men').toggleClass('big');
});

});