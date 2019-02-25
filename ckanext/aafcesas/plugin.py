import uuid
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class AafcesasPlugin(plugins.SingletonPlugin):
    '''A CKAN plugin that enables SSO using a simple header parameter.
    '''
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IAuthenticator)


    def update_config(self, config):
        '''Update CKAN's config with settings needed by this plugin.
        '''
        toolkit.add_template_directory(config, 'templates')
        self.header_userid = config.get('ckan.aafcesas.header_userid', 'partyID')
        self.header_email = config.get('ckan.aafcesas.header_email', 'email')

    def login(self):
        pass

    def identify(self):
        '''Identify which user (if any) is logged in via simple SSO header.
        If a logged in user is found, set toolkit.c.user to be their user name.
        '''
        if self.header_userid in toolkit.request.headers:
            userid = toolkit.request.headers.get(self.header_userid).lower()
            email = toolkit.request.headers.get(self.header_email).lower()
            username = <construct username>
            user = get_user_by_email(email)
            if not user:
                # A user with this email doesn't yet exist in CKAN
                # - so create one.
                user = toolkit.get_action('user_create')(
                    context={'ignore_auth': True},
                    data_dict={'id':userid,
                               'email': email,
                               'name': username,
                               'password': generate_password()})
            toolkit.c.user = user['name']

    def logout(self):
        pass

    def abort(self, status_code, detail, headers, comment):
        pass

    def get_user_by_username(username):
       '''Return the CKAN user with the given username.
       :rtype: A CKAN user dict
       '''
       # We do this by accessing the CKAN model directly, because there isn't a
       # way to search for users by email address using the API yet.
       import ckan.model
       user = ckan.model.User.get(username)

       if user:
          user_dict = toolkit.get_action('user_show')(data_dict={'id': user.id})
          return user_dict
       else:
          return None

    def get_user_by_email(email):
       '''Return the CKAN user with the given email address.
       :rtype: A CKAN user dict

       '''
       # We do this by accessing the CKAN model directly, because there isn't a
       # way to search for users by email address using the API yet.
       import ckan.model
       users = ckan.model.User.by_email(email)
       assert len(users) in (0, 1), ("The SimpleSSO plugin doesn't know what to do "
                                  "when CKAN has more than one user with the "
                                  "same email address.")
       if users:
          # But we need to actually return a user dict, so we need to convert it
          # here.
          user = users[0]
          user_dict = toolkit.get_action('user_show')(data_dict={'id': user.id})
          return user_dict
       else:
          return None

   def generate_password():
       '''Generate a random password.
       '''
       # FIXME: Replace this with a better way of generating passwords, or enable
       # users without passwords in CKAN.
       return str(uuid.uuid4())

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'aafcesas')
