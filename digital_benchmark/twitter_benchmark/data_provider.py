from requests_oauthlib import OAuth1Session


class DataProvider:

    def get_authorization(consumer_key, consumer_secret):
        request_token_url = "https://api.twitter.com/oauth/request_token"
        oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
        fetch_response = oauth.fetch_request_token(request_token_url)
        resource_owner_key = fetch_response.get('oauth_token')
        resource_owner_secret = fetch_response.get('oauth_token_secret')
        #print("Got OAuth token: %s" % resource_owner_key)
        base_authorization_url = 'https://api.twitter.com/oauth/authorize'
        authorization_url = oauth.authorization_url(base_authorization_url)
        return authorization_url

    def get_user_profile_data(verifier_token,consumer_key, consumer_secret,resource_owner_key,resource_owner_secret):
        access_token_url = 'https://api.twitter.com/oauth/access_token'
        oauth = OAuth1Session(consumer_key,
                              client_secret=consumer_secret,
                              resource_owner_key=resource_owner_key,
                              resource_owner_secret=resource_owner_secret,
                              verifier=verifier_token)
        oauth_tokens = oauth.fetch_access_token(access_token_url)

        access_token = oauth_tokens['oauth_token']
        access_token_secret = oauth_tokens['oauth_token_secret']

        # Make the request
        oauth = OAuth1Session(consumer_key,
                              client_secret=consumer_secret,
                              resource_owner_key=access_token,
                              resource_owner_secret=access_token_secret)
        response = oauth.get("https://api.twitter.com/1.1/account/settings.json")
        return response.text
