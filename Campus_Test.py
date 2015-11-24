from CampusFlask import app

import os
import json
import unittest
import tempfile

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def login(self, username, password):
        return self.app.post('/SignIn', data=dict(
            inputEmail=username,
            inputPassword=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def profile(self, ID):
         with self.app as c:
            with c.session_transaction() as sess:
                sess['colleagueID'] = ID
            return self.app.get('/profileUserInfo')

    def event(self, ID):
         with self.app as c:
            with c.session_transaction() as sess:
                sess['eventID'] = ID
            return self.app.get('/eventsInfo')

    def group(self, ID):
         with self.app as c:
            with c.session_transaction() as sess:
                sess['groupID'] = ID
            return self.app.get('/groupsInfo')


    def test_login(self):
        self.login('carlos.rosario10@upr.edu', '5555')
        with self.app.session_transaction() as sess:
            assert sess['current_user'] != None and  sess['logged_in'] == True
            print('Successfully Logged In')

    def test_logout(self):
        self.logout()
        with self.app.session_transaction() as sess:
            assert sess['current_user'] == None and  sess['logged_in'] == False
            print('Successfully Logged Out')

    def test_profile(self):
        response = self.profile(23)
        data =  json.loads(response.data)
        assert data['userInfo'] != []
        print('Profile Successfully Loaded')

    def test_event(self):
        response = self.event(2)
        data =  json.loads(response.data)
        assert data['eventsInfo'] != []
        print('Group Successfully Loaded')

    def test_group(self):
        response = self.group(3)
        data =  json.loads(response.data)
        assert data['groupsInfo'] != []
        print('Event Successfully Loaded')

if __name__ == '__main__':
    unittest.main()