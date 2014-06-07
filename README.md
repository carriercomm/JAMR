JAMR:

Screen One
-----------
Please let us have your location

  POST get-location ->  server

Screen Two
-----------
Instrument / Genere

  POST profile ->  server

Screen Three
-----------
Map
  
   GET long-lat <- server
   GET ws upgrade -> server

Screen Four
-----------
Chat

   Engaged via websocket 

------------------------------------------------

<pre>
      +-------------------+
      |  JamrResource.py  |
      +-+-----------------+
               |                                                                 
+--------------+---+                                                  
|   JamrService.py |
+--------------+---+                             
               |                                      
           +---+-------+                                            
           |JamrDao.py |                              
           +-------+---+                              
                   |                                  
         +---------+-------+              
         |   DataStore.py  |              
         +-----------------+
</pre>
-----------------------------------
### Data Representations

#### Requests:
<pre>
 ADD_USER
  source_user: {user}
 INVITE
  source_user: {user}
  dest_user: {user}
 CREATE
  source_user: {user}
 LEAVE
  source_user: {user}
  room: {room}
 MESSAGE
  source_user: {user}
  room: {room}
  message: text
 USERS
  users: List{user}
</pre>
#### Objects:
<pre>

Pos.py
  lon: {double}
  lat: {double}
User.py
  pos: {pos}
  inst: {string}
  genr: {string}
Room.py
  users: list{user}
  id: {long}
</pre>

#### Instruments:
1. Guitar
2. Bass
3. Drums





















