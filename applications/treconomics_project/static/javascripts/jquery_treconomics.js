$(document).ready(function()
{  
     $('.survey table tr').filter(':odd').addClass('odd');
	 $('.matrix ul').each(function() {
		$('li:first-child label input').css('float', 'right');
	  });

	  $('.addButton').toggle(function() {
      	  $('.hidden').css({display: 'inline'});
	  $(this).attr('value','-');
   	  return false;
	  }, function() {
      	  $('.hidden').css({display: 'none'});
	  $(this).attr('value','+');
   	  return false;
	   });


    $('.searchbox').focus(function() {
        $.get('/treconomics/query_focus/', function(data){
        });
    });

    $('.smallsearchbox').focus(function() {
        $.get('/treconomics/query_focus/', function(data){
        });
    });

    $('#end-task-link').click(function() {
        return confirm("Clicking OK will take you to the next stage of the experiment. If you clicked the 'End Task' link by accident, you can push the Cancel button below.");
    })

}); 


