# Running your App on EC2

0. Go to EC2 Dashboard
1. Select "Launch Instance"
   * Note the description: _"To get started, launch an Amazon EC2 instance, which is a virtual server in the cloud."_
1. Setup an EC2 instance
  * Select Ubuntu Server 20.04
  * Keep `t2.micro` — see [pricing](https://aws.amazon.com/ec2/pricing/on-demand/)
  * **Configure Instance Details**
    * Let's accept all the defaults here
    * Some things of note:
      * Spot instances vs on-demand — good way to get cheaper instance if it's ok if it goes down from time to time
      * IAM Role — we'll be working on setting this up so you and your partner can collaborate together
  * **Add Storage** — we can keep the defaults. 8 GB should be sufficient for your projects.
  * **Add Tags** — this is used for organizing projects across AWS, but optional
  * **Configure Security Group** — this allows our instance to be accessed from the Internet in different ways
    * SSH (port 22) — we need to keep this one as it's the way we will manage the instance
    * HTTP (port 80) — we need to add this rule. It will allow our API to receive HTTP requests over the internet
    * HTTPS (port 443) — for secure HTTP requests
  * Hit Launch
    * Create a new keypair — this file will allow you to log into the server from your command line
    * Download the pem file
    * Move to a relevant location
    * Change the permissions of the pem file on the command line (note: the `$` means a command line prompt, not something you type).
      ```bash
      $ chmod 400 demo-week-13-musa-509.pem
      ```
2. Click on the the `Connect` button to view how we can start changing things on this server
   * SSH into the instance (native with Mac and Linux, [Windows ssh client](https://docs.microsoft.com/en-us/windows/terminal/tutorials/ssh))
     ```bash
      $ ssh -i /path/to/pem/file.pem ubuntu@your_public_ipv4_dns
     ```
     Once you ssh into the instance, you're in a Linux environment (Ubuntu), so all commands after this will be for a Linux environment, not Windows, until you exit.
3. Install software — Python environment, your code, web server, etc.
   1. Install Miniconda
      * Download package to instance:
        `$ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh`
      * Install:
        `$ bash Miniconda3-latest-Linux-x86_64.sh -b -p ~/miniconda`
      * Add conda to command path:
        `$ echo -e '\n# Miniconda Installation\nexport PATH=~/miniconda/bin:$PATH' >> ~/.bashrc`
      * Reload the bashrc so changes take effect
        `$ source ~/.bashrc`
      * Initialize conda
        `$ conda init bash`
      * Log out of the instance and back again:
        `$ exit` — this will take you back to your computer again
        `$ ssh -i "demo-week-13-musa-509.pem" ubuntu@...
      * Note that the `(base)` is in the command line prompt
   2. One of the following
      1. Clone your GitHub repo into your instance
         * Get new GitHub token
         * Clone the repo into the instance
         * `cd` into the repo
         * Install the environment.yml as a new environment. See [conda's environment page](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file) for more information.
           ```bash
           $ conda env create -f environment.yml
           ```
         * Install [`gunicorn`](https://flask.palletsprojects.com/en/1.1.x/deploying/wsgi-standalone/#gunicorn) into the environment:
           ```bash
           $ conda install gunicorn
           ```
      2. Make a little demo application
   3. Setup and install `nginx` a webserver that can be used as a [reverse proxy](https://www.nginx.com/resources/glossary/reverse-proxy-server/) as a way to allow the public port 80 to be connected to the port we use for the Flask application as well as providing some extra security.
      * What is a reverse proxy? <https://www.nginx.com/resources/glossary/reverse-proxy-server/>
      * Setup nginx on Ubuntu: <https://ubuntu.com/tutorials/install-and-configure-nginx#1-overview>, except configure the config file as follows (based on [this tutorial](https://www.matthealy.com.au/blog/post/deploying-flask-to-amazon-web-services-ec2/):
        ```
        server {
            listen       80;
            server_name  your_public_dnsname_here;

            location / {
                proxy_pass http://127.0.0.1:8000;
            }
        }
        ```
        Note the file location will be different, as seen [here](https://ubuntu.com/tutorials/install-and-configure-nginx#4-setting-up-virtual-host)
        And mix with the SSL pieces from [this flask https walkthrough](https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https).
   3. Install tmux:
      ```
      $ sudo apt install tmux
      ```
      Nice [overview of using tmux here](https://linuxize.com/post/getting-started-with-tmux/)
   4. If setting up for HTTPS, setting up SSL Certificates
       * Flask with HTTPS: <https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https>
4. Log into tmux with a specific session name
5. Activate conda environment
   ```bash
   $ conda activate your_env_name
   ```
5. Start up the flask app, making sure that it's running with gunicorn or waitress. If your application is in a Python script called `my_fancy_app.py` and the flask object is called `app`, then you can start up your server like so:
   ```bash
   $ gunicorn my_fancy_app:app -b 127.0.0.1:8000
   ```
6. Check out your app by copying the Public IPv4 DNS and visiting it in your browser
7. Get out of tmux by running the `exit` command 
8. Log out of the server by running the `exit` command
9. Stop it or terminate it when you're done!
