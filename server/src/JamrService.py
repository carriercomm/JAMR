from JamrDao import JamrDao
import models.RequestTypes
import json

class JamrService(object):
  def __init__(self):
    self.dao = JamrDao()

  def dispatch(self, message, peer_address):
    #print 'dispatch ' + str(message) + ' ' + str(peer_address)
    
    if(str(message) == "Ping" or str(message) == "1"):
      return

    jd = json.loads(message)
  
    if jd['kind'] == "ADD_USER":
      desr = self.getObj(models.RequestTypes.AddUser, jd)
      self.addUser(desr, peer_address)
      return self.getAllUsers()

    elif jd['kind'] == "INVITE":
      desr = self.getObj(models.RequestTypes.Invite, jd)
      return self.doInvite(desr, peer_address)

    elif jd['kind'] == "CREATE":
      desr = self.getObj(models.RequestTypes.Create, jd)
      return self.createRoom(desr, peer_address)

    elif jd['kind'] == "LEAVE":
      desr = self.getObj(models.RequestTypes.Leave, jd)
      return self.doLeave(desr, peer_address)

    elif jd['kind'] == "MESSAGE":
      desr = self.getObj(models.RequestTypes.Message, jd)
      return self.doMessage(desr, peer_address)

    else:
      print 'ERROR no message type for message: ' + str(message)
    
  def addUser(self, user, peer_address):
    uuid = user['model']["uid"]
    self.putWSKey(uuid, peer_address)
    self.dao.insertUser(user['model'])

  def createRoom(self, room, peer_address):
    self.dao.insertRoom(room['model'])

  def doMessage(self, msgObj, peer_address):
    roomObj = msgObj['model']['room']
    roomId = roomObj['uid']
    roomData = self.dao.getRoom(roomId)
    roomUsers = roomData["users"]
    for user in roomUsers:
      self.dao.getWebsocket(wskey).send(msgObj, False)

  def doInvite(self, invite, peer_address):
    dstUser = invite['model']['dst_user']
    dstUserId = dstUser['uid']
    wskey = self.dao.getWSKey(dstUserId)
    self.dao.getWebsocket(wskey).send(self.toJSON(invite), False)

  def doLeave(self, leave, peer_address):
    roomObj = leave['model']['room']
    roomId = roomObj['uid']
    roomData = self.dao.getRoom(roomId)
    roomUsers = roomData['users']
    roomUsers.remove(leave['model']['src_user'])
    roomData['users'] = roomUsers
    self.dao.insertRoom(roomData)
    for user in roomUsers:
      self.dao.getWebsocket(wskey).send(self.toJSON(leave), False)


  def getUser(self,uid):
    return self.dao.getUser(uid)

  def getRoom(self,uid):
    return self.dao.getRoom(uid)

  def getAllUsers(self):
    users = self.toJSON(self.dao.getAllUsers())
    for ws in self.dao.getAllWebSockets():
      ws.send(users, False)
    return users 

  def getObj(self, funcType, jsonBlob):
    return funcType().deserialize(jsonBlob)

  def toJSON(self, obj):
    return json.dumps(obj)

  def putWS(self, peer_address, ws):
    self.dao.insertWebsocket(peer_address, ws)

  def getWS(self, peer_address):
    return self.dao.getWebsocket(peer_address)

  def putWSKey(self, uuid, wskey):
    self.dao.associateKey(uuid,wskey)

  def getWSKey(self, uuid):
    return self.dao.getKey(uuid)



