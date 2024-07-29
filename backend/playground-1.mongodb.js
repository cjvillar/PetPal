const database = 'PETPAL';
const collectionName = 'users';

use(database);

// create a new collection 
db.createCollection(collectionName);

// define the users data
const users = [
  {"user": "Alice", "email": "alice@example.com"},
  {"user": "Bob", "email": "bob@example.com"},
  {"user": "Charlie", "email": "charlie@example.com"},
  {"user": "Diana", "email": "diana@example.com"},
  {"user": "Eve", "email": "eve@example.com"}
];

// insert users data into collection
db[collectionName].insertMany(users);

// find all 
db[collectionName].find();
