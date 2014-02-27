var graph	= require('fbgraph');
var conf	= {
	client_id		: '217617381771470',
	client_secret	: '403a70ba74957d4f8a1ca77dbc6e69a2',
	scope			: 'email, user_about_me, user_birthday, user_location, publish_stream',
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
		console.log('CODE: ', req.query.code);
		graph.authorize({
			"client_id"		: conf.client_id,
			"redirect_uri"	: conf.redirect_uri,
			"client_secret"	: conf.client_secret,
			"code"			: req.query.code
		}, function (err, facebookRes) {
			console.log(facebookRes);
			res.redirect('/UserHasLoggedIn');
		});
	}
}