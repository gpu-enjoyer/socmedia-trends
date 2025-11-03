
# Social Media Trend Analysis


## Roadmap

### in-progress

- [ ] `TesxProcessor: pool.map()`
- [ ] `DataParser.async_vk_task()`

### todo

- [ ] ~~`LDA_model`~~ `frequency = {}`
- [ ] GUI: input `topics_num`
- [ ] GUI: input `parsing_depth`
- [ ] GUI: output `frequency`
- [ ] GUI: `init_button`


## Supported OSs

```
Linux
```


## GUI demo

<img src="gui_demo.png" width="80%">


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
habr_com
vcnews
d_code
...
```


## Select VK groups

Create `vk.txt` with the ids of VK groups  
in the following format:

```
59518047
50260527
31131060
...
```


## Run

```bash
./install.sh  # Do it once

./run.sh

# Input: path to 'tg.txt'
# Input: path to 'vk.txt'

# Okay lets go
```
