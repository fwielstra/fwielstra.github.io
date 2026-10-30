just a title and an idea.

Basically, working in Go has been two steps forward, one step back, but not in a negative way. A few examples:

Two steps forward: Starting with Gin, a bigger / feature complete web application library.

Realizations: Using goda, I realized it pulls in all of grpc and a bunch of other dependencies I don't need. Also, its API is a bit more removed from go's own http interface.

One step back: simplifying to what I actually need, a route matcher (gorilla/mux) and maybe some session management. Shaved off 2 MB off my binary size, API is much closer to Go's own std lib http library.


Two steps forward: Integrating a code generator (xo) to generate code to interact with a legacy database. It generates models and various methods to fetch and insert data into the database, low level result binding code, etc.

Realization: It doesn't generate a `select * from table` query, which is what I needed. Does not expose methods to help bind a response to a result struct. Low level SQL in Go is a bit verbose. Generates a lot of code I don't need. Uses go's SQL library's nullable fields, but I don't care about that, zero values are fine.

One step back: Using sqlx to easily bind result sets to a struct, handwriting my own struct in a minute or so, and reducing code size by a lot.


 Two steps forward: Using database abstraction layers; using Ent, a really sophisticated database abstraction layer / ORM based on a graph model.

 Realization: It doesn't take out all the work. You need to write updaters on a per field basis, and you have to manage your own relationships - that is, you can't just save your aggregate, you have to break it down yourself. Caveat: This might have been my own misunderstanding. Also, no migration support for SQLite.

 One step back, then forward again: Going to a more established ORM, GORM. Decent database migration support, also for SQLite. Allows storing a model and its relationships.

 Realization: Adds a layer of complexity (a DSL) on top of plain SQL. Deeper nested relationships are not supported by default, and need a lot of awkward, manual code (link?).

 Another realization: My data model is fine, decently normalized. However, adding features like versioning and audit logging are challenging in a regular, normalized database.

 One step back, who knows where: Upending my data storage entirely; migrating towards more of a document store (json blob in sqlite) which allows for easier versioning and audit logging. Greatly simplifies database model, but may add complexity when it comes to verifying referential integrity and updating the data model later on. This step is still in a POC phase.
