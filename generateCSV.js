'use strict';

var fs = require('fs');
var striptags = require('striptags');
var sanitizeHtml = require('sanitize-html');

function isValidBlog (blog) {
	let blogSelf = './blogs/' + blog + '/self.json';
	let blogPosts = './blogs/' + blog + '/posts';
	if (fs.existsSync(blogSelf) && fs.existsSync(blogPosts)){ 
		let blogJson = { 
			locale: { country: null },
			posts: { totalItems: 0 }
		};
		try {
		    blogJson = JSON.parse(fs.readFileSync(blogSelf));
		} catch (e) {
		    //
		}
		if (blogJson.locale.country == 'BR' &&
			blogJson.posts.totalItems > 0 &&
			fs.readdirSync(blogPosts).length > 0
			) {
			return true;
		}
	}
	return false;
}


function cleanTxt(txt) {
	txt = txt.replace(/&lt;/g,'<');
	txt = txt.replace(/&gt;/g,'>');
	txt = sanitizeHtml(txt);
	txt = striptags(txt);
	txt = txt.replace(/(?:\r\n|\r|\n)/g, ' ').replace('"',' ');
	txt = txt.replace(/&\w+;/g,'');
	return txt;
}

function generateCSV(dirList) {
	fs.writeFileSync('posts.csv', 'blogID,postID,authorID,published,title,content,labels,replies\n');
	dirList.every( (blog, idx) => {
		if (isValidBlog(blog)) {
			console.log(blog + ', ' + idx + ' / ' + dirList.length);
			let postDir = './blogs/' + blog + '/posts/';
			let postsList = fs.readdirSync(postDir);
			postsList.forEach( (postFile) => {
				let post = JSON.parse(fs.readFileSync(postDir + postFile));
				let postString = post.blog.id + ',' + post.id + ',' + post.author.id + ',' + post.published;
				postString += ',"' + cleanTxt(post.title) + '"';
				postString += ',"' + cleanTxt(post.content) + '"';
				if (!post.labels) { post.labels = ''; }
				postString += ',"' + post.labels + '"'; 
				postString += ',' + post.replies.totalItems; 
				postString += '\n';
				fs.appendFileSync('posts.csv', postString);
			});
		}

		return true; 
	});
}

function computeCountries(dirList) {
	let countries = {};
	dirList.every( (blog, idx) => {
		console.log(blog + ', ' + idx + ' / ' + dirList.length);
		let blogSelf = './blogs/' + blog + '/self.json';
		try {
		    let blogJson = JSON.parse(fs.readFileSync(blogSelf));
		    if (countries[blogJson.locale.country] == null) { countries[blogJson.locale.country] = 0; }
		    countries[blogJson.locale.country]++;
		} catch (e) {
		    //
		}
		return true;
	});
	console.log(JSON.stringify(countries))
}

function generateTitle(dirList) {
	fs.writeFileSync('titles.csv', 'blogID,country,name,description\n');

        let countries = {};
        dirList.every( (blog, idx) => {
		console.log(blog + ', ' + idx + ' / ' + dirList.length);
                let blogSelf = './blogs/' + blog + '/self.json';
                try {
                    let blogJson = JSON.parse(fs.readFileSync(blogSelf));
		
		    if (blogJson.locale.country != null) {
		    	fs.appendFileSync('titles.csv', 
					blogJson.id +','+ 
					blogJson.locale.country +','+ 
					cleanTxt(blogJson.name) +','+
					cleanTxt(blogJson.description) +'\n');
		    }
                } catch (e) {
                    //
                }
                return true;
        });
        console.log(JSON.stringify(countries))
}


let dirList = fs.readdirSync('./blogs/');

switch(process.argv[2]) {
	case "title":
		generateTitle(dirList);
		break;
	case "country": 
		computeCountries(dirList);
		break;
	case "csv": 
		generateCSV(dirList);
		break;
	case undefined: 
	default:
		console.log("select an option: country, csv, title");
}
