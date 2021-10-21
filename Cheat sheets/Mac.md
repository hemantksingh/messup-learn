## Shortcuts

|Function                                                           | Shortcut       | Description                                         |
|-------------------------------------------------------------------|:--------------:|:---------------------------------------------------:|
|Spotlight search                                                   | `Cmd+Space`    |                                                     | 
|Display Shutdown Options                                           | `Ctlr+Power`   | Use `Tab` to navigate & `Space` to select an option |
|Close Document without saving                                      | `Cmd+D`        |                                                     |
|Switch between windows of same app                                 | ``Cmd+` ``     |                                                     |
|Delete file                                                        | `Cmd+Backspace`|                                                     |
|Delete text                                                        | `Fn+Backspace` |                                                     |

## Environment variables

PATH environment variable is simply an order list of directories over which (typically) executables are searched for and run. To include a directory to search for executables on a MAC

Edit the `/Users/<username>/.bash_profile` to include the directory where the executable resides. For example to include the Android Platform tools add the following line to `.bash_profile`.

`export PATH=$PATH:/Users/username/Library/Android/sdk/platform-tools`  
`echo export PATH=$PATH:/Users/username/Library/Android/sdk/platform-tools >> ~/.bash_profile`

The `.bash_profile file` is loaded before Terminal loads your shell environment and contains all the startup configuration and preferences for your command line interface. Within it you can change your terminal prompt, change the colors of text, add aliases to functions you use all the time, and so much more.

Similar to **Windows** `echo %VARIABLE_NAME%`, find the value of the ENV variable: `echo $VARIABLE_NAME` 

List all the path variables `env`

## Terminal Setup

You can either install [iTerm or use the default Terminal](https://apple.stackexchange.com/questions/25143/what-is-the-difference-between-iterm2-and-terminal). Since the update to version 10.15 Catalina, macOS includes Z shell (zsh) as default instead of Bash in the Terminal app. 

### Oh My ZSH

For managing your zsh configuration you can [install Oh My ZSH](https://ohmyz.sh/#install). Oh My Zsh [plugins](https://github.com/ohmyzsh/ohmyzsh/wiki/Plugins) provide auto completion support and other utilites for various tools. 

List the installed plugins

```sh
ls ~/.oh-my-zsh/plugins
```

To enable a plugin, just add its name (as shown from the above command) in `plugins=(...)` in your `.zshrc` file. 

List the enabled plugins

```sh
echo $plugins
```

### Other shortcuts 

Find path for xcode developer tools
```
$ xcode-select -p
```

Clear terminal  `Cmd+K`

## Use Magic keyboard and mouse on Windows

Download bootcamp support software https://support.apple.com/kb/dl1720?locale=en_GB

From BootCamp5.1.5621\BootCamp\Drivers\Apple install:

AppleWirelessTrackpad64
AppleWirelessMouse64
AppleMultiTouchTrackPadInstaller64

And install -> https://magicutilities.net/magic-mouse/home

