var http = require('http');
var sockjs = require('sockjs');

var globalSessions = {}
var globalUsers = []
var arr = []

var generate = function(){
    var chars = 'qwertyuioplkjhgfdsazxcvbnm'
    var output = "", i = 0
	
    for(;i < 10; i++)
        output += chars[Math.floor((Math.random() * 25) + 0)]

    return output
}

var wsSend = function(message){
	for(i in arr)
	{
		arr[i].write(message)
	}
}

var echo = sockjs.createServer();
echo.on('connection', function(conn) {
	arr.push(conn)
    conn.on('data', function(message) {
		var handler = JSON.parse(message)
		var type = handler[0]
		var text = handler[1].body
		
		switch(type)
		{
			case 'chat.ping':
				wsSend(JSON.stringify(['chat.text', {body: text, sender: {name: globalSessions[conn].name, id: globalSessions[conn].id}}]))
				//console.log(JSON.stringify([{body: text, sender: {name: "temp", id: ""}}]))
				break;
			case 'chat.join':
				var username = globalUsers[0]
				var chatId = generate()
				
				conn.write(JSON.stringify(['chat.id', {name: globalUsers.shift(), id: chatId}]))
				
				globalSessions[conn] = {name: username, id: chatId}
				break;
		}
		wsSend(message)
    });
    conn.on('close', function() {
		arr.splice(arr.indexOf(conn), 1)
	});
});

echo.on('error', function(e){
	console.log('problem with request: ' + e.message);
})

var server = http.createServer(function(request, response){
	
	request.on('data', function(data){
		var handler = data.toString()
		globalUsers.push(handler.split('=')[1])
	})

	response.write("HURRAY")
	response.end()
});

//var server = http.createServer()

echo.installHandlers(server, {prefix:'/echo'});
server.listen(9000, '127.0.0.1');