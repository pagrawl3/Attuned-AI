//__Module Dependencies
var express		= require('express'),
	http		= require('http')

//__Express Configuration
var app = express(); 				//instantiate it
require('./config/express')(app); 	//additional express settings in the express config file. Include it here.

//__Router Configuration
require('./config/routes')(app);	//path to the router file (containing all the routes)

//__Create and start the Server
var server = http.createServer(app).listen(3000);	//will create a server accessible on localhost at port 3000

//__Expose application
exports = module.exports = app;

