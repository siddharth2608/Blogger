$(document).ready(function(){
	$('.like-btn').on('click',function(){
		console.log('pressed');
		//var post_id = $(this).data('id');
		var post_id = $(this).attr("data-id");
		console.log(post_id)
		$clicked_btn = $(this);
		var action = '';
		if($clicked_btn.hasClass('fa-thumbs-o-up')){
			action = 'like';
		}
		else if($clicked_btn.hasClass('fa-thumbs-up')){
			action = 'unlike';
		}
		console.log(action);
		//var like_count = document.getElementById('post_like_'+post_id).innerHTML;
		//console.log(like_count);
		$.ajax({ 
			url:'http://127.0.0.1:5000/posts/react',
			type:'post',
			data:{
				'action':action,
				'post_id':post_id
			},
			success: function(data){
				console.log('inside success');
				//res = JSON.parse(data);
				if(action=="like"){
					console.log('inside like');
					$clicked_btn.removeClass('fa-thumbs-o-up').addClass('fa-thumbs-up');
					document.getElementById('post_like_'+post_id).innerHTML = parseInt(document.getElementById('post_like_'+post_id).innerHTML) + 1;
				}
				else if(action=='unlike'){
					console.log('inside unlike')
					$clicked_btn.removeClass('fa-thumbs-up').addClass('fa-thumbs-o-up');
					document.getElementById('post_like_'+post_id).innerHTML = parseInt(document.getElementById('post_like_'+post_id).innerHTML) - 1;
				}
				$clicked_btn.siblings('i.fa-thumbs-down').removeClass('fa-thumbs-down').addClass('fa-thumbs-o-down');
			}
			// error: function(data){
			// 	console.log('failed');
			// }
		});

	});

	//dislike button
	$('.dislike-btn').on('click',function(){
		var post_id = $(this).attr("data-dislike-id");
		$clicked_btn = $(this);
		var action = '';
		if($clicked_btn.hasClass('fa-thumbs-o-down')){
			action = 'dislike';
		}
		else if($clicked_btn.hasClass('fa-thumbs-down')){
			action = 'undislike';
		}
		$.ajax({
			url:'http://127.0.0.1:5000/posts/react/',
			type:'post',
			data: {
				'action':action,
				'post_id':post_id
			},
			success:function(data){
				console.log('inside success');
				//res = JSON.parse(data);
				if (action=="dislike"){
					$clicked_btn.removeClass('fa-thumbs-o-down').addClass('fa-thumbs-down');
					document.getElementById('post_like_'+post_id).innerHTML = parseInt(document.getElementById('post_like_'+post_id).innerHTML) + 1;
				}
				else if(action=="undislike"){
					$clicked_btn.removeClass('fa-thumbs-down').addClass('fa-thumbs-o-down');
					document.getElementById('post_like_'+post_id).innerHTML = parseInt(document.getElementById('post_like_'+post_id).innerHTML) - 1;
				}
				$clicked_btn.siblings('i.fa-thumbs-up').removeClass('fa-thumbs-up').addClass('fa-thumbs-o-up');
			}
		});
	});
});	