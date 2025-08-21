# RP42 📮
rp42 will enable discord reach presence (now with 100% more sus!)


## setup
first, create an intra application `https://profile.intra.42.fr/oauth/applications/new`

none of the field matter, put whaterver you want


you will need a config.json file like this:
```json
{
	"login":"LOGIN",
	"UID":"APP_UID",
	"SECRET":"APP_SECRET"
}
```

## Installation 

1. clone the repo
```bash
  git clone https://github.com/Maxime-juncker/42_rich_presence.git RP42
  cd RP42
```

2. install pip packages
```bash
  pip install -r requirements.txt
```


3. edit launch / stop script
use your's favorite editor and change the `EXEC` variable of `launch.sh` and `stop.sh`    
you will also need to change the `CONFIG` path in launch.sh

```bash
EXEC="EXEC_PATH"
CONFIG="CONFIG_PATH"
```


#### Run the script

``` bash
bash launch.sh
```
The script will run in the backgorund, you can close the terminal

#### Stop the script

``` bash
bash stop.sh
```


## Customisation
inside the rp.py you can choose which infos are display:   
these are some basic one (now with extra sus! 📮)
```
- login      // your login + title  
- wallet     // wallet amount (kinda sus)
- state      // where are you connected in the cluster (or hiding in vents)
- rank       // are you a student / trancender / etc... (not the impostor)
- pp         // your intra profil picture
```
you can make your own varaible using the `user` variable 

inside `RPC.update()` choose what to display and where

**🔍 Sus Features Added:**
- All status messages now include Among Us themed references
- Location shows "hiding in vents" when unavailable  
- Level display includes sus emojis
- Acting sus at 42 school indicator
