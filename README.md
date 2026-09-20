# Daria Slavkova — one-page site

**Живой сайт:** https://fingus8888-netizen.github.io/daria-slavkova/

Статический одностраничник, собранный из макета Figma
(`iHaDj0CTNNLRdb58zPTg6g`, секции `Home` и `/about`).

## Структура

```
index.html           главная (визитка)
work.html            раздел Selected work — сгенерирован build-work-html.py
assets/css/style.css стили (токены макета: #F0EEDE, #000, #6F6E63)
assets/js/main.js    сетка работ, лайтбокс, reveal, смена цвета шапки
assets/fonts/        NATS (сабсет latin, 8 КБ, OFL)
assets/img/          hero, портрет, 28 работ (превью 560px + 1500px для лайтбокса)
assets/img/work/     36 снимков листа /work (превью 760px + 1300px)
build-images.py      пересборка картинок главной из figma/raw по imageTransform макета
build-work.py        разбор листа /work макета -> work-data.json + assets/img/work
build-work-html.py   генерация work.html из work-data.json
figma/               выгрузка макета: nodes.json, fills.json, raw/ (оригиналы)
```

## Разделы

шапка → имя → hero → about me → сетка работ (28) → тёмный блок about → контакты → футер

Навигация: `Work` ведёт на work.html (открывается сверху), `About` и `Contact` —
якоря по главной. Обе страницы всегда открываются сверху: браузерное
восстановление скролла отключено (`history.scrollRestoration = 'manual'`).

### work.html

Лента листа `/work` макета: 18 пар снимков с кредитами, разделы
`Selected work` / `art` / `Clients makeup` / `Runway, backstage`, чёрный футер.
Клик по снимку открывает лайтбокс (36 фото, стрелки, Esc, свайп).

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

## Пересборка раздела Work

```
python3 build-work.py       # картинки + work-data.json из макета
python3 build-work-html.py  # work.html из work-data.json
```

Тексты и порядок блоков правятся либо в `work-data.json` с последующей
генерацией, либо прямо в `work.html`.
