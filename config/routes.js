module.exports = function(app) {

	//__Import all the controllers
	var main = require('../app/controllers/main');

	//__All the routes are added here
	//____more routes will be added here
	app.get('/*', main.index)	//redirect to index if the url doesn't match any params
}