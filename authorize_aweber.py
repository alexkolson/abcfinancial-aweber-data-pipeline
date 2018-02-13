import os
from aweber_api import AWeberAPI

# replace XXX with your keys
consumer_key = os.environ['AWEBER_KEY']
consumer_secret = os.environ['AWEBER_SECRET']

# create new instance of AWeberAPI
application = AWeberAPI(consumer_key, consumer_secret)

# get a request token
request_token, token_secret = application.get_request_token('oob')

# prompt user to go to the auth url
# pylint: disable=E1601
print 'Go to this url in your browser: %s' % application.authorize_url

# prompt for verifier code
code = raw_input('Type code here: ')

# exchange request token + verifier code for access token
application.user.request_token = request_token
application.user.token_secret = token_secret
application.user.verifier = code
access_token, access_secret = application.get_access_token()

# show the results
print access_token, access_secret
