## GUI访问远程 full node



## On the daemon host

### Expose the daemon to the network

In `config.yaml`, change `self_hostname` from `localhost` to `0.0.0.0`. This binds the daemon to all IPv4 addresses on the local machine.

Next, open the port that the daemon is listening on (55400 by default). The UI assumes that the daemon is already running and it will *not* attempt to start a remote daemon. Using [ufw](https://help.ubuntu.com/community/UFW) and restricting traffic to just the UI's host:

```bash
sudo ufw allow from <IP of UI machine> to any port 55400 proto tcp
```



### Copy the daemon's cert files

To secure their connection, the GUI will need the daemon's certificates. Copy these files to the Windows machine:

```bash
~/.chia/mainnet/config/ssl/daemon/private_daemon.crt
~/.chia/mainnet/config/ssl/daemon/private_daemon.key
```



## On the GUI host

### Reference the daemon's cert files

Place the daemon's cert files, copied earlier, in the following location:

```bash
~/.chia/mainnet/config/ssl/ui/
~/.chia/mainnet/config/ssl/ui/
```



Find the `ui` section in `config.yaml` and specify the following settings:

```yaml
daemon_host: <name or IP of the daemon host>
daemon_port: 55400
daemon_ssl:
  private_crt: config/ssl/ui/private_daemon.crt
  private_key: config/ssl/ui/private_daemon.key
```