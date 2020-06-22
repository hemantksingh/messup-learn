# Ubuntu development setup

## Running on VirtualBox
In order to get full screen mode and copy-paste working, install the VirtualBox Guest Addition. Instructions here
https://askubuntu.com/questions/73059/how-to-copy-paste-from-ubuntu-virtualbox-guest-to-windows-host

## Dev setup runbook

### Update apt packages 
```
sudo apt-get update
```

Install docker by following the 'INSTALL DOCKER ENGINE - COMMUNITY' instructions here https://docs.docker.com/install/linux/docker-ce/ubuntu/

### Installing dev tools
```
sudo apt-get install git make curl net-tools docker-compose -y
```

### Installing vscode
```
sudo snap install --classic code
```

### Installing azcli
```
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

## Keyboard shortcuts

|Function                                                           | Shortcut       |
|-------------------------------------------------------------------|:--------------:|
|Switch between windows within an application                       | `Alt` + `key above Tab` |

### switch between windows within an application

