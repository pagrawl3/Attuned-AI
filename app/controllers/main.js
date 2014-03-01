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
			res.redirect(authUrl); 		//checks whether a user denied the app facebook login/permissions
		else
			res.send('access denied'); 	//req.query.error == 'access_denied'
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

			var fetch = function(fetchURL, data, all_data, callback) {
				if (!data) {																				//data doesn't exist, make the first call
					graph.get(fetchURL, {access_token: facebookRes.access_token}, function(err, data) {		//retreive likes
						all_data = all_data.concat(data.data);												//merge the new data with the all_data array
						console.log(all_data);
					   	fetch(fetchURL, data, all_data, callback);											//recursive function fetches the remaining pages
					});
				} else if (data && data.paging && data.paging.next) {
					graph.get(data.paging.next, function(err, data) {
						all_data = all_data.concat(data.data);												//merge the new data with the all_data array
						fetch(fetchURL, data, all_data, callback);											//recursively call the function to fetch the next pages
	    			});
				} else {
					callback(all_data);																		//done fetching, call the callback function
				}
			}

	    	var sendToPython = function(channel, data) {
				var zerorpc = require("zerorpc");
	    		var client 	= new zerorpc.Client();
				client.connect("tcp://127.0.0.1:4242");
	    		client.invoke(channel, data, function(error, data, more) {
					console.log(data);
	    		});
	    	}

	    	var all_likes = [];
			fetch('me/likes', false, all_likes, function(data){
				res.send(data);
				sendToPython('processLikes', data);
			});


		});
	}
}