# Ubuntu development setup

## Running on VirtualBox
To get full screen mode and copy-paste working, [install the VirtualBox Guest Addition](https://askubuntu.com/questions/73059/how-to-copy-paste-from-ubuntu-virtualbox-guest-to-windows-host) through the Devices menu on your guest VM.


## Dev setup runbook
`apt-get` is one of apt's backends so you could also just use `apt` alone

### Update apt packages 
```
sudo apt-get update
```

### Installing dev tools

Install docker by following the 'INSTALL DOCKER ENGINE - COMMUNITY' instructions here https://docs.docker.com/install/linux/docker-ce/ubuntu/

```
sudo apt-get install git make curl net-tools zsh docker-compose -y
# zsh is z shell, alternative to bash
```

### Installing oh my zsh

Oh My Zsh - framework for managing your zsh configuration - https://github.com/ohmyzsh/ohmyzsh

```
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
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

