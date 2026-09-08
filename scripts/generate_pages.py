#!/usr/bin/env python3
"""Generate static HTML pages for ASIC knowledge base from content markdown."""
from __future__ import annotations

import re
from pathlib import Path

CONTENT = Path(__file__).resolve().parents[1] / "content" / "articles.md"
ROOT = Path("/workspace")

UPDATED = "07.09.2026"

ARTICLES_META = [
    {
        "slug": "start",
        "title": "Начало работы",
        "audience": "Для всех",
        "minutes": 5,
        "category": "start",
        "card_title": "Введение в программу",
    },
    {
        "slug": "users-and-access",
        "title": "Пользователи и права доступа",
        "audience": "Для администраторов",
        "minutes": 3,
        "category": "module",
        "card_title": "Права доступа",
    },
    {
        "slug": "object-passport",
        "title": "Паспорт объекта",
        "audience": "Для всех",
        "minutes": 2,
        "category": "module",
        "card_title": "Паспорт объекта",
    },
    {
        "slug": "schemes-and-localization",
        "title": "Загрузка схем и локализация этапов строительства",
        "audience": "Для всех",
        "minutes": 8,
        "category": "module",
        "card_title": "Загрузка схем",
    },
    {
        "slug": "regulatory-docs",
        "title": "Нормативная документация",
        "audience": "Для всех",
        "minutes": 2,
        "category": "module",
        "card_title": "Нормативная документация",
    },
    {
        "slug": "meeting-schedule",
        "title": "График планёрок",
        "audience": "Для всех",
        "minutes": 2,
        "category": "module",
        "card_title": "График планёрок",
    },
    {
        "slug": "contractor-registration",
        "title": "Регистрация подрядчиков",
        "audience": "Для всех",
        "minutes": 3,
        "category": "module",
        "card_title": "Регистрация подрядчиков",
    },
    {
        "slug": "stropro",
        "title": "СтроПро",
        "audience": "Для всех",
        "minutes": 6,
        "category": "module",
        "card_title": "СтроПро",
    },
    {
        "slug": "work-schedule-planning",
        "title": "Планирование графика работ",
        "audience": "Для всех",
        "minutes": 5,
        "category": "module",
        "card_title": "Планирование графика работ",
    },
    {
        "slug": "construction-control",
        "title": "Контроль строительства",
        "audience": "Для всех",
        "minutes": 3,
        "category": "module",
        "card_title": "Контроль строительства",
    },
    {
        "slug": "project-management",
        "title": "Оперативное управление",
        "audience": "Для всех",
        "minutes": 7,
        "category": "module",
        "card_title": "Оперативное управление",
    },
]

META_BY_SLUG = {a["slug"]: a for a in ARTICLES_META}


def header(active: str, root_prefix: str = "") -> str:
    css = f"{root_prefix}css/styles.css"
    home = f"{root_prefix}index.html"
    faq = f"{root_prefix}faq.html"
    home_active = ' class="is-active"' if active == "home" else ""
    faq_active = ' class="is-active"' if active == "faq" else ""
    body_root = ' data-root="../"' if root_prefix == "../" else ""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>__TITLE__ — База знаний АСИК</title>
  <link rel="stylesheet" href="{css}">
</head>
<body{body_root}>
  <header class="site-header">
    <div class="site-header__inner">
      <a class="brand" href="{home}">База знаний АСИК</a>
      <div class="search">
        <label class="visually-hidden" for="search" style="position:absolute;left:-9999px">Поиск</label>
        <input id="search" type="search" placeholder="Поиск по разделам…" data-search-input autocomplete="off">
        <div class="search-results" data-search-results></div>
      </div>
      <nav class="site-nav" aria-label="Основная">
        <a href="{home}"{home_active}>Каталог</a>
        <a href="{faq}"{faq_active}>FAQ</a>
      </nav>
    </div>
  </header>
"""


FOOTER = """
  <footer class="site-footer">
    <div class="site-footer__inner">База знаний АСИК · обучающие инструкции по десктопному приложению</div>
  </footer>
  <div class="lightbox" data-lightbox aria-hidden="true">
    <div class="lightbox__panel">
      <button type="button" class="lightbox__close" data-lightbox-close aria-label="Закрыть">×</button>
      <div class="lightbox__content" data-lightbox-content></div>
    </div>
  </div>
  <script src="__JS__"></script>
</body>
</html>
"""


def parse_articles(text: str) -> dict[str, dict]:
    chunks = re.split(r"^## slug:\s*", text, flags=re.M)[1:]
    articles: dict[str, dict] = {}
    for chunk in chunks:
        lines = chunk.strip().splitlines()
        slug = lines[0].strip()
        title = ""
        category = ""
        goal = ""
        body_lines: list[str] = []
        for line in lines[1:]:
            if line.startswith("title:"):
                title = line.split(":", 1)[1].strip()
            elif line.startswith("category:"):
                category = line.split(":", 1)[1].strip()
            elif line.startswith("goal:"):
                goal = line.split(":", 1)[1].strip()
            elif line.strip() == "---":
                continue
            else:
                body_lines.append(line)
        steps = parse_steps("\n".join(body_lines).strip(), slug)
        articles[slug] = {
            "slug": slug,
            "title": title,
            "category": category,
            "goal": goal,
            "steps": steps,
        }
    return articles


def parse_steps(body: str, slug: str) -> list[dict]:
    # Split by ### headings
    parts = re.split(r"^###\s+", body, flags=re.M)
    steps = []
    display_num = 0
    for part in parts:
        part = part.strip()
        if not part:
            continue
        lines = part.splitlines()
        heading = lines[0].strip()
        content = "\n".join(lines[1:]).strip()
        display_num += 1
        # Extract step number from heading if present
        m = re.match(r"Шаг\s+([\d]+(?:–[\d]+|[a-z])?)\.\s*(.*)$", heading)
        if m:
            title = m.group(2).strip() or heading
            num_label = m.group(1)
        else:
            title = heading
            num_label = str(display_num)

        blocks: list[dict] = []
        buf: list[str] = []
        shot_i = 0

        def flush_text():
            nonlocal buf
            if not buf:
                return
            text = "\n".join(buf).strip()
            buf = []
            if text:
                blocks.append({"type": "text", "value": text})

        for line in content.splitlines():
            sm = re.match(r"^\[СКРИН:\s*(.+?)\]\s*$", line.strip())
            if sm:
                flush_text()
                shot_i += 1
                desc = sm.group(1).strip()
                # Prefer step number from heading for filename if numeric
                file_num = re.match(r"^(\d+)", str(num_label))
                n = file_num.group(1) if file_num else str(display_num)
                path = f"../images/{slug}/step-{n}-{shot_i}.jpg"
                blocks.append({"type": "shot", "desc": desc, "path": path})
            else:
                buf.append(line)
        flush_text()

        steps.append(
            {
                "id": f"step-{display_num}",
                "num": display_num,
                "num_label": num_label if False else str(display_num),
                "title": title,
                "blocks": blocks,
            }
        )
    return steps


def md_inline(text: str) -> str:
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    return text


def render_text_block(value: str) -> str:
    lines = value.splitlines()
    html_parts: list[str] = []
    list_items: list[str] = []

    def flush_list():
        nonlocal list_items
        if list_items:
            items = "".join(f"<li>{md_inline(i)}</li>" for i in list_items)
            html_parts.append(f"<ul>{items}</ul>")
            list_items = []

    for line in lines:
        if re.match(r"^[-*]\s+", line):
            list_items.append(re.sub(r"^[-*]\s+", "", line))
        elif line.strip() == "":
            flush_list()
        else:
            flush_list()
            html_parts.append(f"<p>{md_inline(line)}</p>")
    flush_list()
    return "\n".join(html_parts)


def render_step(step: dict) -> str:
    blocks_html = []
    for b in step["blocks"]:
        if b["type"] == "text":
            blocks_html.append(render_text_block(b["value"]))
        else:
            blocks_html.append(
                f"""<figure class="shot" data-lightbox-trigger>
  <div class="shot__label">Вставьте скрин</div>
  <div class="shot__hint">{md_inline(b['desc'])}</div>
  <div class="shot__hint" style="opacity:.7">{b['path']}</div>
</figure>"""
            )
    return f"""<section class="step" id="{step['id']}">
  <div class="step__head">
    <div class="step__num">{step['num']}</div>
    <h2 class="step__title">{md_inline(step['title'])}</h2>
  </div>
  {''.join(blocks_html)}
</section>"""


def render_article(article: dict, order: list[str]) -> str:
    slug = article["slug"]
    meta = META_BY_SLUG[slug]
    idx = order.index(slug)
    prev_slug = order[idx - 1] if idx > 0 else None
    next_slug = order[idx + 1] if idx < len(order) - 1 else None

    toc = "\n".join(
        f'<a href="#{s["id"]}">{s["num"]}. {md_inline(s["title"])}</a>' for s in article["steps"]
    )
    steps_html = "\n".join(render_step(s) for s in article["steps"])

    prereq = ""
    if meta["category"] == "module":
        prereq = """<p class="prereq">Сначала прочитайте <a href="start.html">Начало работы</a> — базовые принципы интерфейса АСИК.</p>"""

    prev_next = '<div class="prev-next">'
    if prev_slug:
        prev_next += f"""<a href="{prev_slug}.html"><span class="prev-next__label">← Предыдущая</span>{META_BY_SLUG[prev_slug]['title']}</a>"""
    else:
        prev_next += "<div></div>"
    if next_slug:
        prev_next += f"""<a class="next" href="{next_slug}.html"><span class="prev-next__label">Следующая →</span>{META_BY_SLUG[next_slug]['title']}</a>"""
    else:
        prev_next += f"""<a class="next" href="../faq.html"><span class="prev-next__label">Далее →</span>Часто задаваемые вопросы</a>"""
    prev_next += "</div>"

    head = header("article", "../").replace("__TITLE__", article["title"])
    foot = FOOTER.replace("__JS__", "../js/main.js")

    return f"""{head}
  <main class="page">
    <nav class="breadcrumbs" aria-label="Хлебные крошки">
      <a href="../index.html">Каталог</a>
      <span>/</span>
      <span>{md_inline(article['title'])}</span>
    </nav>
    <div class="article-layout">
      <article>
        <header class="article-header">
          <h1>{md_inline(article['title'])}</h1>
        </header>
        <div class="article-goal">
          <strong>Цель</strong>
          <p>{md_inline(article['goal'])}</p>
        </div>
        {prereq}
        {steps_html}
        {prev_next}
      </article>
      <aside class="toc">
        <div class="toc__title">На этой странице</div>
        <nav>{toc}</nav>
      </aside>
    </div>
  </main>
{foot}
"""


def render_card(meta: dict, featured: bool = False) -> str:
    cls = "card featured" if featured else "card"
    return f"""<a class="{cls}" href="articles/{meta['slug']}.html">
  <div class="card__thumb" aria-hidden="true"></div>
  <div class="card__body">
    <h2 class="card__title">{meta['card_title']}</h2>
    <p class="card__audience">{meta['audience']}</p>
    <div class="card__meta">
      <span>{UPDATED}</span>
      <span>{meta['minutes']} мин</span>
    </div>
  </div>
</a>"""


def render_index() -> str:
    # Единая сетка как на референсе: введение + модули
    all_cards = "\n".join(
        render_card(m, featured=(m["slug"] == "start")) for m in ARTICLES_META
    )
    head = header("home", "").replace("__TITLE__", "Каталог")
    foot = FOOTER.replace("__JS__", "js/main.js")
    return f"""{head}
  <main class="page">
    <h1 class="page-title">База знаний АСИК</h1>
    <p class="page-lead">Пошаговые инструкции по десктопному приложению АСИК. Начните с введения, затем откройте нужный модуль.</p>

    <div class="cards">
      {all_cards}
      <a class="card" href="faq.html">
        <div class="card__thumb" aria-hidden="true"></div>
        <div class="card__body">
          <h2 class="card__title">Часто задаваемые вопросы</h2>
          <p class="card__audience">Для всех</p>
          <div class="card__meta">
            <span>{UPDATED}</span>
            <span>3 мин</span>
          </div>
        </div>
      </a>
    </div>
  </main>
{foot}
"""


FAQ_ITEMS = [
    (
        "Почему на кнопке входа нет моей фамилии?",
        "Значит специалист не внесён в 1С как ответственное лицо. Обратитесь к администратору или в отдел АСУ, чтобы вас добавили — после этого фамилия появится на кнопке входа. Подробнее: <a href=\"articles/start.html\">Начало работы</a>.",
    ),
    (
        "С чего начинать работу в АСИК?",
        "Сначала пройдите раздел <a href=\"articles/start.html\">Начало работы</a> (авторизация, интерфейс, навигация). Затем заполняйте модули первичного заполнения сверху вниз, начиная с <a href=\"articles/users-and-access.html\">прав доступа</a> и <a href=\"articles/object-passport.html\">паспорта объекта</a>.",
    ),
    (
        "Кто может создавать роли и права доступа?",
        "Создание ролей и распределение прав доступно только администраторам. Обычные пользователи видят назначенные им модули. См. <a href=\"articles/users-and-access.html\">Пользователи и права доступа</a>.",
    ),
    (
        "Почему нельзя вручную добавить пользователя?",
        "Список пользователей подтягивается из базы 1С. Задача специалиста — дополнить карточку полями справа и назначить роль, а не создавать учётную запись с нуля.",
    ),
    (
        "Что обязательно сохранять после правок?",
        "После заполнения данных нажимайте «Сохранить». Без сохранения изменения могут не попасть на сервер. Это общее правило для всех модулей.",
    ),
    (
        "Как сменить объект строительства?",
        "В главном окне нажмите «Список объектов», найдите нужный (есть поле поиска) и выберите его. Инструкция: <a href=\"articles/start.html\">Начало работы</a>, шаги про главное окно и список объектов.",
    ),
    (
        "Какую схему обязательно загружать?",
        "Схему ПОС загружают обязательно — она одна на весь объект. Схемы АР добавляют все в одно поле. См. <a href=\"articles/schemes-and-localization.html\">Загрузка схем</a>.",
    ),
    (
        "Почему модуль серый и недоступен?",
        "В главном окне синим отмечены только модули, к которым у вас есть доступ. Если модуль недоступен — проверьте роль у администратора в разделе прав доступа.",
    ),
    (
        "Где смотреть ход строительства и заявки?",
        "В модуле <a href=\"articles/construction-control.html\">Контроль строительства</a> — таблицы «Комплексный график» и «График заявок на снабжение». Сводная картина также есть в <a href=\"articles/project-management.html\">Оперативном управлении</a>.",
    ),
    (
        "Как утвердить график работ?",
        "После настройки связей и временных отрезков нажмите «Утверждено ДС» и «Утверждено ДЗ». При необходимости экспортируйте график в Excel. См. <a href=\"articles/work-schedule-planning.html\">Планирование графика работ</a>.",
    ),
]


def render_faq() -> str:
    items = []
    for q, a in FAQ_ITEMS:
        items.append(
            f"""<details class="faq-item">
  <summary>{q}</summary>
  <div class="faq-item__body"><p>{a}</p></div>
</details>"""
        )
    head = header("faq", "").replace("__TITLE__", "FAQ")
    foot = FOOTER.replace("__JS__", "js/main.js")
    return f"""{head}
  <main class="page">
    <nav class="breadcrumbs" aria-label="Хлебные крошки">
      <a href="index.html">Каталог</a>
      <span>/</span>
      <span>FAQ</span>
    </nav>
    <h1 class="page-title">Часто задаваемые вопросы</h1>
    <p class="page-lead">Короткие ответы на типичные вопросы при старте работы в АСИК. Если нужен полный сценарий — откройте соответствующий модуль.</p>
    <div class="faq-list">
      {''.join(items)}
    </div>
  </main>
{foot}
"""


def main() -> None:
    raw = CONTENT.read_text(encoding="utf-8")
    parsed = parse_articles(raw)
    order = [a["slug"] for a in ARTICLES_META]

    for slug in order:
        if slug not in parsed:
            raise SystemExit(f"Missing article in content: {slug}")
        html = render_article(parsed[slug], order)
        out = ROOT / "articles" / f"{slug}.html"
        out.write_text(html, encoding="utf-8")
        print("wrote", out)

    (ROOT / "index.html").write_text(render_index(), encoding="utf-8")
    print("wrote index.html")
    (ROOT / "faq.html").write_text(render_faq(), encoding="utf-8")
    print("wrote faq.html")

    # Update README
    (ROOT / "README.md").write_text(
        """# База знаний АСИК

Статический HTML-макет обучающей базы знаний по десктопному приложению АСИК.

## Запуск

Откройте `index.html` в браузере или поднимите локальный сервер:

```bash
python3 -m http.server 8080
```

## Структура

- `index.html` — каталог разделов
- `faq.html` — часто задаваемые вопросы
- `articles/` — статьи (начало работы + 10 модулей)
- `css/styles.css`, `js/main.js`
- `images/<slug>/` — сюда кладите скриншоты (см. `images/README.md`)

Скриншоты в макете — плейсхолдеры с описанием и рекомендуемым путём файла.
""",
        encoding="utf-8",
    )
    print("wrote README.md")


if __name__ == "__main__":
    main()
