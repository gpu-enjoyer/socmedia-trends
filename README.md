
# Social Media Trends Analyze


## Get Telegram tokens

```bash
https://my.telegram.org/apps
```


## Get VK tokens

```bash
https://dev.vk.com/ru/mini-apps/management/creating-new-apps

# Select 'standalone-app'
# Select 'web'
# 'base domen':  localhost
# 'redirect URL: http://localhost
```


## Set tokens

```bash
cd input
mv tokens_template.json tokens.json

# Edit: tokens.json
```


## Select Telegram channels

Create `tg.txt` with the names of Telegram channels  
in the following format:

```
name_1
name_2
...
```


## Select VK groups

Create `vk.txt` with the ids of VK groups  
in the following format:

```
id_1
id_2
...
```


## Run

```bash
./install.sh  # Do it once

./run.sh

# Input: path to 'tg.txt'
# Input: path to 'vk.txt'

# Okay lets go ..
```
