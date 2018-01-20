$(

	$("#test").click(function(){
		$.post('/api/getsuggestions', {word: 'hello'}, function(suggestions){
			console.log(suggestions);
		})
	})
)