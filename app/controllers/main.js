var graph	= require('fbgraph');
var conf	= {
	client_id		: '217617381771470',
	client_secret	: '403a70ba74957d4f8a1ca77dbc6e69a2',
	scope			: 'email, user_about_me, user_birthday, user_location, publish_stream, user_actions:music',
	redirect_uri	: 'http://localhost:3000/auth/facebook'
}

exports.index = function(req, res) {
	res.render('index');	//render index.jade placed inside app/views
}

exports.authenticate = function(req, res) {
	// we don't have a code yet
 	// so we'll redirect to the oauth dialog
 	if (!req.query.code) {
		var authUrl = graph.getOauthUrl({
			"client_id"		: conf.client_id,
			"redirect_uri"	: conf.redirect_uri,
			"scope"			: conf.scope
		});

		if (!req.query.error)
			res.redirect(authUrl); //checks whether a user denied the app facebook login/permissions
		else
			res.send('access denied'); //req.query.error == 'access_denied'
	}
	else {
		// code is set
		// we'll send that and get the access token
		graph.authorize({
			"client_id"		: conf.client_id,
			"redirect_uri"	: conf.redirect_uri,
			"client_secret"	: conf.client_secret,
			"code"			: req.query.code
		}, function (err, facebookRes) {
			graph.setAccessToken(facebookRes);	//set the access token -- need to figure out auto renewal


			//configuration options for the web request mad by the Request module
			var options = {
			    timeout:  3000
			  , pool:     { maxSockets:  Infinity }
			  , headers:  { connection:  "keep-alive" }
			};

			var all_likes = [];	//this array will hold all the like objects returned from facebook

	    	var fetchNextPage = function(data) {
	    		if(data.paging && data.paging.next) {	//check if this is not the last page
	    			graph.get(data.paging.next, function(err, res) {
						all_likes = all_likes.concat(res.data);	//merge the new data with the all_likes array
						fetchNextPage(res);	//recursively call the function to fetch the next page
	    			});
				}
				else {
					//done fetching all likes
					all_likes.shift();			//remove that weird null value at the beginning of the array
					res.send(all_likes);		//send all the likes to the client (browser)
					sendToPython(all_likes);
				}
	    	}

	    	var sendToPython = function(data) {
				var zerorpc = require("zerorpc");
	    		var client 	= new zerorpc.Client();

				client.connect("tcp://127.0.0.1:4242");

	    		client.invoke("processLikes", data, function(error, res, more) {
					console.log(res);
	    		});
	    	}


			graph
				.setOptions(options)
				.get("me/likes",{access_token: facebookRes.access_token}, function(err, data) {	//retreive likes
					all_likes = all_likes.concat(res.data);		//merge the new data with the all_likes array
			    	fetchNextPage(data);						//recursive function fetches the remaining pages
				});

		});
	}
}