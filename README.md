
# Social Media Trends Analyze


## Get Telegram token & id

```bash
https://my.telegram.org/apps
```


## Get VK token & id

```bash
https://dev.vk.com/ru/mini-apps/management/creating-new-apps

# select 'standalone-app'
# select 'web'
# 'base domen':  localhost
# 'redirect URL: http://localhost
```


## Set tokens

```bash
cd input
mv tokens_template.json tokens.json

# Edit: tokens.json
```


## Select channels

```bash
# Edit: input/tg.txt
# Edit: input/vk.txt
```


## Run

```bash
./install.sh  # do it once
./run.sh
```
