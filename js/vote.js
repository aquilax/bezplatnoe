$(function(){
	$("a.vote_up").click(function(){
	//get the id
	the_id = $(this).attr('rel');

	// show the spinner
	//$(this).parent().html("<img src='/img/spinner.gif'/>");

	//fadeout the vote-count
	$("span#votes_count"+the_id).fadeOut("fast");

	//the main ajax request
		$.ajax({
			type: "POST",
			data: "action=1&id="+$(this).attr("rel"),
			url: "/vote",
			success: function(msg)
			{
				$("span#votes_count"+the_id).html(msg);
				//fadein the vote count
				$("span#votes_count"+the_id).fadeIn();
				//remove the spinner
				$("span#vote_buttons"+the_id).remove();
			}
		});
	});

	$("a.vote_down").click(function(){
	//get the id
	the_id = $(this).attr('rel');

	// show the spinner
	//$(this).parent().html("<img src='/img/spinner.gif'/>");

	//the main ajax request
		$.ajax({
			type: "POST",
			data: "action=-1&id="+$(this).attr("rel"),
			url: "/vote",
			success: function(msg)
			{
				$("span#votes_count"+the_id).fadeOut();
				$("span#votes_count"+the_id).html(msg);
				$("span#votes_count"+the_id).fadeIn();
				$("span#vote_buttons"+the_id).remove();
			}
		});
	});
});