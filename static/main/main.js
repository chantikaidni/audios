$('#show_emailup').click(function(){
	// console.log("sach");
	$('.social').css('display','none');
	$('#email_up').css('display','block');
})
$('#go_back_signup').click(function(){
	$('#email_up').css('display','none');		
	$('.social').css('display','block');
})