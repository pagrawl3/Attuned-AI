module.exports = function(app) {

	//__Import all the controllers
	var main = require('../app/controllers/main');

	//__All the routes are added here
	app.get('/auth/facebook', main.authenticate)	//fb authentication
	app.get('/*', main.index)	//redirect to index if the url doesn't match any params
}