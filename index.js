'use strict';

var fs = require('fs');
var blogger = require('./blogger');
var config = require('./config.prod');

// define event for synchronous calls
const EventEmitter = require('events');
class BlogEvent extends EventEmitter {}
var blogEvent = new BlogEvent();

// global variables
var count = 0;
var total = config.blogger.api.length-1;
var error = false;

// define 'get' listener
blogEvent.on('get', (blogID) => {
    if (count++ < total && !error) { 
    	error = blogger.blogGet(blogID); 
    }
});

// read blog IDs
function getBlogChunk () {
	count = 0;
	error = false;
	var dirList = fs.readdirSync('./blogs/');
	console.log('### getBlogChunk : ' + dirList.length + ' ###');
	blogger.readBlogIDs((blogID) => {
		if (count < total) {
			if (!blogger.blogExist(blogID)){ 
			   	blogEvent.emit('get',blogID);
			}
		}
	});
}

setInterval(getBlogChunk, 30 * 1000);