# SimplyDB

Simple DBaaS REST API that lets users save private notes.

## Functionality

Users register with credentials and are given a fixed amount of tokens. Tokens are required 
to request information. Users are then able to retrieve their notes using tokens. 

Credentials are hashed and salted before storing in MongoDB.

## Resource

|Resource        | Address   | Protocol  | Parameters               | Response/Status                                                  |
| -------------- | --------- | --------- | ------------------------ | -----------------------------------------------------------------|
| Register User  | /register | POST      | Username, Password       | 200 OK                                                           |
| Add/Edit Note  | /store    | POST      | Username, Password, Note | 200 OK <br />401 Invalid Credentials <br />402 Not enough tokens |
| Retrieve Note  | /get      | POST      | Username, Password       | 200 OK <br />401 Invalid Credentials <br />402 Not enough tokens |

### Token System
- Each user gets 10 tokens upon registering.
- Token are required to store and fetch notes.
- Buy more tokens when user runs out. [Not implemented yet]