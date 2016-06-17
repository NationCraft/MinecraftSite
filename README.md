# MinecraftSite

Instructions for deployment

apache2 minecraft_site.conf file

<VirtualHost *:80>
    ServerName enter_server_address

    WSGIScriptAlias / /var/www/minecraft_site/minecraft_site/minecraft_site.wsgi

    <Directory /var/www/minecraft_site/minecraft_site/site>
        Order deny,allow
        Allow from all
    </Directory>
    Alias /static /var/www/minecraft_site/minecraft_site/site/static
    <Directory /var/www/minecraft_site/minecraft_site/site/static/>
        Order allow,deny
        Allow from all
    </Directory>
    ErrorLog ${APACHE_LOG_DIR}/error.log
    LogLevel warn
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

