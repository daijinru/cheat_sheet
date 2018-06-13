import base64
import random
import time

class LoginToken:
    users = {
        'admin': ['123456']
    }

    def gen_token(self, uid):
        token = ':'.join([str(uid), str(random.random()), str(time.time() + 3600)])
        token = bytes(token, encoding='utf-8')
        token = str(base64.b64encode(token), encoding='utf-8')
        self.users[uid].append(token)
        return token

    def verify_toekn(self, token):
        try:
            _token = base64.b64decode(bytes(token, encoding='utf-8'))
            _token = str(_token, encoding='utf-8')
            tokenList = _token.split(':')
            uid = tokenList[0]
            userToken = self.users[uid][-1]
            lat = tokenList[-1]
            if not userToken == token:
                return -1
            if float(lat) <= time.time():
                return 1
            return 0
        except:
            return -1

    def loginVerify(self, uid, pwd):
        if self.users[uid][0] == pwd:
            return self.gen_token(uid)
        else:
            return ''

loginToken = LoginToken()
