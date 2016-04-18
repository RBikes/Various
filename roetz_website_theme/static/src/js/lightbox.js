 $(document).ready(function(){
           $('li img').on('click',function(){
                var src = $(this).attr('src');
                var img = '<img src="' + src + '" class="img-responsive gallery"/>';
                
                //start of new code new code
    	var index = $(this).parent('li').index();   
		
		var html = '';
		html += img;                
		html += '<div style="height:25px;clear:both;display:block;">';
		html += '<a class="gallery-control gallery-right" href="'+ (index+2) + '">NEXT&nbsp;<span class="fa fa-chevron-right"></span></a>';
		html += '<a class="gallery-control gallery-left" href="' + (index) + '"><span class="fa fa-chevron-left"></span>&nbsp;PREV</a>';
		html += '</div>';
                
                
                $('#myModal').modal();
                $('#myModal').on('shown.bs.modal', function(){
                    $('#myModal .modal-body').html(html);
                });
                $('#myModal').on('hidden.bs.modal', function(){
                    $('#myModal .modal-body').html('');
                });
           });  
        })

        $(document).on('click', 'a.gallery-control', function(){
    var index = $(this).attr('href');
	var src = $('ul.row li:nth-child('+ index +') img').attr('src');             
	
	$('.modal-body img').attr('src', src);
	
	var newPrevIndex = parseInt(index) - 1; 
	var newNextIndex = parseInt(newPrevIndex) + 2; 
	
	if($(this).hasClass('gallery-left')){               
		$(this).attr('href', newPrevIndex); 
		$('a.gallery-right').attr('href', newNextIndex);
	}else{
		$(this).attr('href', newNextIndex); 
		$('a.gallery-left').attr('href', newPrevIndex);
	}
	
	var total = $('ul.row li').length + 1; 
	//hide next button
	if(total === newNextIndex){
		$('a.gallery-right').hide();
	}else{
		$('a.gallery-right').show()
	}            
	//hide previous button
	if(newPrevIndex === 0){
		$('a.gallery-left').hide();
	}else{
		$('a.gallery-left').show()
	}
	
	
	return false;
});