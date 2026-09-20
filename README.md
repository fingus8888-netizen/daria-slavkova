# Daria Slavkova — one-page site

**Живой сайт:** https://fingus8888-netizen.github.io/daria-slavkova/

Статический одностраничник, собранный из макета Figma
(`iHaDj0CTNNLRdb58zPTg6g`, секции `Home` и `/about`).

## Структура

```
index.html           разметка страницы
assets/css/style.css стили (токены макета: #F0EEDE, #000, #6F6E63)
assets/js/main.js    сетка работ, лайтбокс, reveal, смена цвета шапки
assets/fonts/        NATS (сабсет latin, 8 КБ, OFL)
assets/img/          hero, портрет, 28 работ (превью 560px + 1500px для лайтбокса)
build-images.py      пересборка картинок из figma/raw по imageTransform макета
figma/               выгрузка макета: nodes.json, fills.json, raw/ (оригиналы)
```

## Разделы

шапка → имя → hero → about me → сетка работ (28) → тёмный блок about → контакты → футер

Навигация `Work / About / Contact` — якоря по этой же странице.

## Локальный просмотр

```
python3 -m http.server 8765 --bind 127.0.0.1
# http://127.0.0.1:8765/
```

## Публикация

Сайт стоит на GitHub Pages, репозиторий `fingus8888-netizen/daria-slavkova`,
ветка `main`, корень репозитория. Обновление — обычным пушем:

```
git add -A && git commit -m "..." && git push
```

Сборка полностью статическая, ничего компилировать не нужно — Pages
раскатывает содержимое ветки за 30-60 секунд.

## Пересборка картинок

Оригиналы лежат в `figma/raw/`. Кадрирование берётся из `imageTransform`
макета, поэтому кадры совпадают с Figma один в один:

```
python3 build-images.py
```

## Что осталось за рамками

Секция `/work` макета (36 фото с кредитами «Ph / model / makeup artist»)
в одностраничник не вошла — при необходимости добавляется отдельным блоком.
