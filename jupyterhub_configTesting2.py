# Configuration file for Jupyter Hub

#c = get_config()

#ssl encryption using letsencrypt self ser
c.JupyterHub.ssl_key = '/etc/letsencrypt/live/appsvr.asrc.cestm.albany.edu/privkey.pem'
c.JupyterHub.ssl_cert = '/etc/letsencrypt/live/appsvr.asrc.cestm.albany.edu/fullchain.pem'
c.JupyterHub.port = 443

# spawn with Docker
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

# The docker instances need access to the Hub, so the default loopback port doesn't work:
from jupyter_client.localinterfaces import public_ips
c.JupyterHub.hub_ip = public_ips()[0]

# OAuth with GitHub
c.JupyterHub.authenticator_class = 'oauthenticator.GitHubOAuthenticator'

c.Authenticator.whitelist = whitelist = set()
c.Authenticator.admin_users = admin = set()

from oauthenticator.github import LocalGitHubOAuthenticator
c.JupyterHub.authenticator_class = LocalGitHubOAuthenticator
c.LocalGitHubOAuthenticator.create_system_users = True

from oauthenticator.github import GitHubOAuthenticator
c.JupyterHub.authenticator_class = GitHubOAuthenticator
from dockerspawner import DockerSpawner
c.JupyterHub.spawner_class = DockerSpawner

from dockerspawner import DockerSpawner
c.JupyterHub.spawner_class = DockerSpawner
# The Hub's API listens on localhost by default, # but docker containers can't see that.
# Tell the Hub to listen on its docker network:
import netifaces
docker0 = netifaces.ifaddresses('docker0')
docker0_ipv4 = docker0[netifaces.AF_INET][0]
c.JupyterHub.hub_ip = docker0_ipv4['addr']

import os

join = os.path.join
here = os.path.dirname(__file__)
with open(join(here, 'userlist')) as f:
    for line in f:
        if not line:
            continue
        parts = line.split()
        name = parts[0]
        whitelist.add(name)
        if len(parts) > 1 and parts[1] == 'admin':
            admin.add(name)

#c.GitHubOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']
'''
# ssl config
ssl = join(here, 'ssl')
keyfile = join(ssl, 'ssl.key')
certfile = join(ssl, 'ssl.cert')
if os.path.exists(keyfile):
    c.JupyterHub.ssl_key = keyfile
if os.path.exists(certfile):
    c.JupyterHub.ssl_cert = certfile
'''
