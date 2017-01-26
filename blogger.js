'use strict';

var google = require('googleapis');
var bloggerApi = google.blogger('v3');
var config = require('./config.prod');
var striptags = require('striptags');
var zlib = require('zlib')
var fs = require('fs');

let emptyBlog = { 
	locale: { country: null },
	posts: { totalItems: 0 }
};

var blogger = module.exports = {

	readBlogIDs: (callback) => {
		let maxChunck = 0;
		var blogStream = fs.createReadStream("blogIDs.csv.gz");
		blogStream.pipe(zlib.createGunzip())
		.on('data', function(blogChunck) {
			blogChunck.toString().split("\n").forEach(callback);
		})
		.on('end', function () {
			console.log("end readBlogIDs");
		});
	},

	blogExist: (blogID) => {
		let blogDir = './blogs/' + blogID + '/';
		if (!fs.existsSync(blogDir)){ 
		   	return false;
		} else {
			return true;
		}
	},

	// Stats: 25% Blogger Api Resquest
	blogGet: (blogID) => {
		let blogDir = './blogs/' + blogID + '/';

		if (blogger.blogExist(blogID)) { 
			console.log(blogID + ': already exist!');
			return true; 
		}

		console.log(blogID + ': download...');
		bloggerApi.blogs.get({
		  key: config.getApiKey(),
		  blogId: blogID,
		  maxPosts: 10
		}, function (err, blog) {
		  if (!fs.existsSync(blogDir)){ fs.mkdirSync(blogDir) };
		  if (err != null) {
			  if (err.code == 404) {
			    console.error(blogID + ': ' + err.message);
			    fs.writeFileSync(blogDir + 'self.json', JSON.stringify(emptyBlog));
			  } else {
				console.error(err);
				return false;
			  }
		  }
		  if (blog) {
		    fs.writeFileSync(blogDir + 'self.json', JSON.stringify(blog));
			if (blog.posts.totalItems > 9 && blog.locale.country == 'BR') {
				blog.posts.items.forEach( function(post) {
					return blogger.postsGet(blogID, post.id);
				});
			}
		  }
		});
	},

	// Stats: 75% Blogger Api Resquest
	postsGet: (blogID, postID) => {
		let blogDir = './blogs/' + blogID + '/';
		let postsDir = blogDir + 'posts/';

		bloggerApi.posts.get({
		  key: config.getApiKey(),
		  blogId: blogID,
		  postId: postID
		}, function (err, post) {
		  if (err != null) {
			  if (err.code == 403) {
			    console.error(blogID + ': ' + err.message);
			    process.exit();
			  } else {
				console.error(err);
				return false;
			  }
		  }
		  if (post && blogger.blogExist(blogID)) {
		    if (!fs.existsSync(postsDir)){ fs.mkdirSync(postsDir) }
		    if (striptags(post.content).length > 0) {
		    	fs.writeFileSync(postsDir + postID + '.json', JSON.stringify(post));
			}
			return true;
		  }
		});
	},

};