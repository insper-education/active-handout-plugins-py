# Active Handout Backend

## Setting up a server on AWS

**Important:** to complete the deploy you need a domain (or subdomain) so we can setup the Let's Encrypt certificate.

### Creating the EC2 instance

This part of the documentation is based on https://londonappdeveloper.com/django-docker-deployment-with-https-using-letsencrypt/ and some parts of the text have been copied directly from there.

Create an AWS EC2 instance with at least:

- Application and OS Images: Amazon Linux 2 AMI (HVM)
- Architecture: 64-bit (x86)
- Instance type: t2.micro (should be enough for starting, but you may need to upgrade it at some point)
- Key pair name: Select your key pair for SSH auth
- Network settings: Allow SSH, HTTP and HTTPS traffic
- Configure storage: I recommend at least 25GB as Docker needs to pull a bunch of base images

In the instances dashboard ("View all instances"), select the instance you've just created and copy the public IPv4 address. Then access your instance with:

    ssh ec2-user@<address>

After you’ve connected, install Docker with the following command:

    # Install Docker
    sudo yum update -y
    sudo amazon-linux-extras install -y docker
    sudo systemctl enable docker.service
    sudo systemctl start docker.service
    sudo usermod -aG docker ec2-user

    # Install Docker Compose
    wget https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)
    sudo mv docker-compose-$(uname -s)-$(uname -m) /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

    # Install Git
    sudo yum install -y git

To confirm that everything is installed correctly, run:

    [ec2-user@ip-172-31-40-166 ~]$ docker --version
    Docker version 20.10.13, build a224086
    [ec2-user@ip-172-31-40-166 ~]$ docker-compose --version
    docker-compose version 1.29.2, build unknown

Then, type `exit` to disconnect from SSH, and then reconnect again (this is so the group change gets applied to the user)

Now run `docker run hello-world` to ensure you can run containers.

### Clone this repo on the instance

As this is a public repo you can clone it without any additional permissions.

### Setup DNS

You will need a domain/subdomain to get Let's Encrypt to work properly. Once you have access to a domain, set it up on Route 53.

**Insper faculty only:** we already have a domain. You can ask the domain admin to setup your subdomain.

On Route 53:

- Set the record name to whatever your domain/subdomain is;
- Record type: CNAME;
- Value: copy the Public IPv4 DNS from the EC2 dashboard (e.g. ec2-13-40-10-15.eu-west-2.compute.amazonaws.com);
- TTL: 300 seconds (or whatever you want);
- Routing policy: Simple routing.

### Configure app

Change directory to `backend`, copy the `.env.sample` and set the values:

    cd backend
    cp .env.sample .env
    nano .env

### Getting the first certificate

Run

    docker-compose -f docker-compose.deploy.yml run --rm certbot /opt/certify-init.sh

Now, run the following to stop and start the service:

    docker-compose -f docker-compose.deploy.yml down
    docker-compose -f docker-compose.deploy.yml up -d --build

This will restart all services and serve our application via HTTPS.

Once running, you should be able to navigate to your project at your registered domain name via HTTPS.

### Handling renewals

Automate the certificate renewal with a cron job. Create the file `/home/ec2-user/renew.sh` with the following content:

    #!/bin/sh
    set -e

    cd /home/ec2-user/active-handout-plugins-py/backend/
    /usr/local/bin/docker-compose -f docker-compose.deploy.yml run --rm certbot certbot renew

Then, run `chmod +x renew.sh` to make it executable. Then run:

    crontab -e

Then add the following:

    0 0 * * 6 sh /home/ec2-user/renew.sh

### Running migrations and collectstatic

Whenever you have to apply new migrations or update the static files, rebuild the containers and run the `post_build.sh` script.

### Creating admin user

You may run the following command to create your admin user:

    docker-compose -f docker-compose.deploy.yml exec app python manage.py createsuperuser

### Setting up Github Authentication

The backend uses Django-allauth for social logins using Github. When creating a OAuth2 application in Github, take note of the following values.

* Client ID
* Secret Key

Allauth is configured by logging into the Admin and adding a *Social App*. Use `Provider=Github` and the values above. The name of the provider is not important, but it is required to activate the *Social App* for each *Site*. Just add the entry corresponding to `SITE_ID=1` in the *Sites* field. 
