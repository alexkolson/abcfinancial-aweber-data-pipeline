import os
import json
from aweber_api import AWeberAPI, APIException

consumer_key = os.environ['AWEBER_CONSUMER_KEY']
consumer_secret = os.environ['AWEBER_CONSUMER_SECRET']

# create new instance of AWeberAPI
application = AWeberAPI(consumer_key, consumer_secret)

# get a request token
request_token, token_secret = application.get_request_token('oob')

# pylint: disable=E1601
print 'Go to this url in your browser: %s' % application.authorize_url

# prompt for verifier code
code = raw_input('Type code here: ')

# exchange request token + verifier code for access token
application.user.request_token = request_token
application.user.token_secret = token_secret
application.user.verifier = code
access_key, access_secret = application.get_access_token()

members_list_id = os.environ['MEMBERS_LIST_ID']
prospects_list_id = os.environ['PROSPECTS_LIST_ID']

data = json.load(open('members-and-prospects.json'))

aweber = AWeberAPI(consumer_key, consumer_secret)
account = aweber.get_account(access_key, access_secret)

for member in data['members']:
    try:
        print member['personal']['email']
        # list_url = '/accounts/%s/lists/%s' % (account.id, members_list_id)
        # list_ = account.load_from_url(list_url)

        # create a subscriber
        # params = {
        #    'email': '',
        # }
        # subscribers = list_.subscribers
        # new_subscriber = subscribers.create(**params)

        # success!
        # pylint: disable=E1601
        # print "A new subscriber was added to the %s list!" % (list_.name)
    except (KeyError, APIException), exc:
        print 'Error: %s' % str(exc)
        continue
