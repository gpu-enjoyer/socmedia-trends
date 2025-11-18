
# Social Media Trend Analysis

## Task

1. Вам предоставлены различные источники данных (VK, Telegram), каждый из которых содержит миллионы текстовых сообщений.
2. Вам нужно создать программу, которая параллельно соберет данные из всех источников. Каждый источник должен быть обработан в отдельном потоке или процессе.
3. После сбора данных, они должны быть предварительно обработаны для удаления стоп-слов, пунктуации и других ненужных символов. Этот этап также должен выполняться параллельно для увеличения производительности.
4. Затем вы должны провести анализ данных с целью выявления ключевых слов, хэштегов и популярных тем, которые обсуждаются в социальных сетях.
5. Результаты анализа должны быть сохранены в базе данных или файле для последующего анализа.

## Roadmap

- [ ] Refactoring: separate module for any class
- [ ] ~~`LDA_model`~~ `frequency_counter.py`
- [ ] GUI: output `frequency`
- [ ] GUI: input: `topics_num` `parsing_depth`
- [ ] GUI: button: `init`
- [ ] `DataParser.async_vk_task()`


## Supported OSs

```
Linux
```


## GUI demo

<img src="md/gui_demo.png" width="80%">


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
./script/install.sh  # Do it once

./script/run.sh

# Input:
#  paths to tg.txt, vk.txt
#   relative to the project root directory

# Push:
#  [Okay lets go]
```


[Notes](md/notes.md)
