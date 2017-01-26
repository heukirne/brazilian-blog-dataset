var config = {};

config.blogger = {};
config.blogger.api = ['<YOUR API KEY HERE>'];
config.blogger.blogID = '<YOUR BLOG ID HERE>';

config.getApiKey = () => {
	return config.blogger.api[Math.floor(Math.random()*config.blogger.api.length)];
}

module.exports = config;