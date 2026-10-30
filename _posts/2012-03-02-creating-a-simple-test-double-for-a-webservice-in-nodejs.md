---
layout:     post
title:      "Creating a simple Test Double for a webservice in NodeJS"
date:       2012-03-02 11:37:17
summary:    "It should be common knowledge that for certain types of automated tests, you do not want to rely on the availability of external services for a number of reasons:"
tags:
 - nodejs
 - javascript
 - testing
 - xebia blog
---

*Note: This post was originally published on [the Xebia blog](http://blog.xebia.com/2012/03/02/creating-a-simple-test-double-for-a-webservice-in-nodejs/) ([archived copy](https://web.archive.org/web/20120309020654/http://blog.xebia.com/2012/03/02/creating-a-simple-test-double-for-a-webservice-in-nodejs/)) on March 2nd, 2012 by me; the published date of this repost has been backdated to match. Markup has been converted from WordPress HTML to Markdown.*

---

It should be common knowledge that for certain types of automated tests, you do not want to rely on the availability of external services for a number of reasons:

- Uptime of said service (your tests fail if the service is unavailable)
- Dynamic nature of the data (makes your assertions harder)
- Execution speed of your tests
- Excess load generated on the service
- etc

Ideally, you therefore stub out the external service. Inside your unit tests, you do that using Mock Objects, for example. This is actually harder to do for integration tests – you do not use mock objects in integration tests, because that could change the observed behavior of your application.

In one of our projects, we’ve struggled with this problem for quite some time. There are two major components in it, an iPhone app and a server-side component, which both talk to an external webservice for retrieving the data to display on the app and to work with on the server. In our integration tests, we simply used the production webservice and ran some shallow assertions on the result with varying results.

Recently though, we drew the line. Running integration / UI tests using [KIF for iOS](https://github.com/square/KIF) on data that changes depending on what time it is ended up in unpredictable results, or assertions that we simply couldn’t make because the data kept changing (and of course because KIF does not have any actual assertions, or is able to match on partially matching UI elements). So we said “Okay, we need predictable results – make that damn fake webservice already.”

What it needed to do was:

- Return fixed, predictable results with specific, recognised requests
- Forward the request to the currently used live webservice, so our existing tests don’t all break
- (later) Add a feature to make the data returned variable, some tests rely on the test data returned to have dates that lie in the future
- Do not compromise the security – the live webservice requires HTTP authentication.

Of course, it also needed to be done quickly. We postponed making this fake webservice for a while because it seemed like a lot of work, but once we finally decided on making it, we figured “How hard can it be?”. We’ve been waiting for an opportunity to use [NodeJS](http://nodejs.org/) for a while now, and as far as we could see, this was the ideal choice in this case – we have a REST-like webservice (readonly) that mainly does i/o (from the filesystem and the external webservice), and it should be easy and lightweight to build.

So we went to hack in a few steps. Read more for the whole article and the code.

### 1. Create a webserver that listens to requests

Easy enough in Node. Let’s have it output some information for us as well, and make its port configurable so we can run it persistently on one port, and have it use an alternative port when it’s started up automatically as part of the integration test task:

```javascript
var server = http.createServer(function(request, response) {
  var params = url.parse(request.url);
  console.log("request params: " + util.inspect(params));
  response.end("woot");
});

var port = process.argv[2] || 1337;
server.listen(port)

console.log("Server running at http://localhost:" + port);
```

### 2. Match certain requests and return an expected result for those

The first version of this simply used an array of objects with a fixed path and a file: basically:

```javascript
var responseMap = [
   {path:"/mobile-api-planner?fromStation=ASD&toStation=RTD",
    file:"asd-rtd.xml"}
   {path:"/mobile-api-planner?fromStation=LW&toStation=RTD",
    file:"lw-rtd.xml"}
]
```

But, as it turns out, this would not work because the order of the parameters is simply not constant. So what’s the next option? We could fiddle about with an array of parameters to match and match all of them, but that would be a lot of code and possibly error-prone, so instead we went with regular expressions. I’ve never liked regular expressions, I just don’t get them. But with some googling and trying things out, I finally did manage to get it to work. So, a response map with regular expressions and a filename, and a simple search method that finds a matching filename:

```javascript
var responseMap = [
  // matches on mobile-api-planner w/ params hslAllowed=true, fromStation=ASD, toStation=RTD
  {pattern:/\bmobile-api-planner\?(?=.*hslAllowed=true)(?=.*fromStation=ASD)(?=.*toStation=RTD)/,
   response:{file:"ams-rtd-fyra.xml"}},

  // matches on mobile-api-planner w/ params fromCity=Purmerend, fromStreet=Nijlstraat, toStation=RTD
  {pattern:/\bmobile-api-planner\?(?=.*fromCity=Purmerend)(?=.*fromStreet=Nijlstraat)(?=.*toStation=RTD)/,
   response:{file: "pmr-nijlstraat-rtd-fyra.xml"}},

  {pattern:/\bmobile-api-planner\?(?=.*fromStation=LW)(?=.*toStation=UT)/,
   response:{file: "lwd-ut-trip-cancelled.xml"}}
];

function findResponseFor(path) {
  var result = null;
  responseMap.forEach(function(candidate) {
    if (path.match(candidate.pattern)) {
      result = candidate.response;
      return;
    }
  })
  return result;
}

// file read function, simply writes a file with the given name
// from the 'response/' directory to the response.
function writeFileToResponse(responseFile, response) {
  var filePath = path.join(__dirname, 'response', responseFile);
  response.writeHead(200, {"Content-Type": "application/xml"});

  // may want to consider using fileSystem.createReadStream etc instead
  // for chunked responses and (probably) better memory usage
  fileSystem.readFile(filePath, 'UTF-8', function(err, data) {
    response.end(data);
  });
}

// and the new request handler
var server = http.createServer(function(request, response) {
  var params = url.parse(request.url);
  var responseFile = findResponseFor(params.path);
  if (responseFile != null) {
  writeFileToResponse(responseFile, response);
  } else {
  console.log("Response not found");
  }
});
```

### 3. Proxy requests to the real webservice if a response file was not found

There’s already an else if there is no match in the fixed responses, so let’s just expand that one:

```javascript
var responseFile = findResponseFor(params.path);
if (responseFile != null) {
  writeFileToResponse(responseFile, response);
} else {
  console.log("Response not found");
  writeWebserviceToResponse(request, response);
} 
```

Next, create a simple proxy using [http.get](http://nodejs.org/docs/latest/api/http.html#http.get) and the parameters in the response. This could probably be done even simpler though. We also forward a HTTP authentication header if it exists. Coincidentially, if you call the proxy through a browser, it will still automatically ask you to provide HTTP authentication credentials – very convenient

```javascript
function writeWebserviceToResponse(request, response) {
  var params = url.parse(request.url);
  var options = {
    host: 'webservices.ns.nl',
    path: params.path,
    headers: {'Authorization' : request.headers.authorization}
  };

  var req = http.get(options, function(res) {
    res.setEncoding('utf8');
    response.writeHead(res.statusCode, res.headers);
    res.on('data', function (chunk) {
      response.write(chunk);
    });
    res.on('end', function() {
      response.end();
    });
  });

  req.on('error', function(e) {
    console.log('problem with request: ' + e.message);
  });
}
```

### 4. Make part of the result variable

As said previously, one thing we need is somewhat variable data; in some cases, we need the fixed responses to have dates relative to the current date, for example half an hour in the future. We’ll need dynamically generated dates that are generated when the request is executed, and place them into the returned file.

Dynamically generating the parameters is not that hard, actually – at least, not in Javascript. Instead of adding an array of fixed parameters in the responseMap, we can set a function.

Inserting the dynamic parameters into the returned responses isn’t hard either, as there are a number of (simple, lightweight) templating engines for Javascript out there. One of the more popular ones at the moment is [Mustache](http://mustache.github.com/), which also has a NodeJS implementation, [Mu](https://github.com/raycmorgan/Mu). We use the latter.

The cool thing about Mustache: It can use functions as parameters, and can automatically execute them. So, for our dynamic parameters, we simply send a function instead of a value to Mustache, and it will be resolved as the template is parsed.

So, we need a few things to parse templates:

- Setup and compile the templates
- Create dynamic parameters in some responses
- Replace the writeFileToResponse method to render the templates with the dynamic responses

```javascript
// Mu initialization code:
var Mu = require('mu');
var responseDir = path.join(__dirname, 'response')
Mu.root = responseDir;

// pre-compile the templates.
// https://github.com/raycmorgan/Mu/issues/14
fileSystem.readdir(responseDir, function(err, files) {
  files.forEach(function(file) {
    console.log('Compiling template file ' + file)
    Mu.compile(file, function(err, parsed) {
      if (err) { throw err; }
    });
  });
});

// Dynamic response example:
var responseMap = [
  { pattern:/\bmobile-api-planner\?(?=.*fromStation=MDB)(?=.*toStation=UT)/,
    response: {
      file: "mdb-ut-trip-cancelled.xml",
      params: {
        departure: function() {
          var now = new Date();
          return formatDate(now.setMinutes(now.getMinutes() + 32));
        }
      }
    }
  }
];

// New writeFileToResponse method:

function writeFileToResponse(responseFile, response) {
  response.writeHead(200, {"Content-Type": "application/xml"});
  Mu.render(responseFile.file, responseFile.params)
    .addListener('data', function(chunk) {
      response.write(chunk)
    })
    .addListener('end', function() {
      response.end()
    });
}
```

And there you have it. A proxying fake webservice with authentication and dynamic fields, hacked together in a few hours on a Friday afternoon. Works like a charm, so far. Less than 100 lines without the list of response matchers and parameters, which will probably become the most chunky. [I’ve put the whole code (with trimmed matchers) on Gist](https://gist.github.com/1957545) – enjoy.
