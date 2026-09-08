/* Search index for ASIC knowledge base */
window.ASIC_SEARCH_INDEX = [
  {
    slug: "start",
    title: "Начало работы",
    audience: "Для всех",
    href: "articles/start.html",
    category: "Начало работы",
    text: "авторизация выбор объекта интерфейс боковая панель навигация главное окно список объектов добавление удаление редактирование сохранение"
  },
  {
    slug: "users-and-access",
    title: "Пользователи и права доступа",
    audience: "Для администраторов",
    href: "articles/users-and-access.html",
    category: "Модули",
    text: "роли права доступа пользователи назначение на объект администратор создание ролей распределение доступа"
  },
  {
    slug: "object-passport",
    title: "Паспорт объекта",
    audience: "Для всех",
    href: "articles/object-passport.html",
    category: "Модули",
    text: "паспорт объекта дата начала работ изображение координаты сохранить"
  },
  {
    slug: "schemes-and-localization",
    title: "Загрузка схем и локализация этапов строительства",
    audience: "Для всех",
    href: "articles/schemes-and-localization.html",
    category: "Модули",
    text: "схемы ПОС АР локализация структура объекта дерево уровней разметка шестиугольник копирование"
  },
  {
    slug: "regulatory-docs",
    title: "Нормативная документация",
    audience: "Для всех",
    href: "articles/regulatory-docs.html",
    category: "Модули",
    text: "нормативная документация PDF загрузка документов"
  },
  {
    slug: "meeting-schedule",
    title: "График планёрок",
    audience: "Для всех",
    href: "articles/meeting-schedule.html",
    category: "Модули",
    text: "график планёрок календарь подрядчики статистический контроль"
  },
  {
    slug: "contractor-registration",
    title: "Регистрация подрядчиков",
    audience: "Для всех",
    href: "articles/contractor-registration.html",
    category: "Модули",
    text: "подрядчики генподрядчик субподрядчики договоры представители"
  },
  {
    slug: "stropro",
    title: "СтроПро",
    audience: "Для всех",
    href: "articles/stropro.html",
    category: "Модули",
    text: "СтроПро ТТК библиотека технологий объёмы бригады подрядчики"
  },
  {
    slug: "work-schedule-planning",
    title: "Планирование графика работ",
    audience: "Для всех",
    href: "articles/work-schedule-planning.html",
    category: "Модули",
    text: "планирование графика работ связи ТТК excel утверждение временные отрезки"
  },
  {
    slug: "construction-control",
    title: "Контроль строительства",
    audience: "Для всех",
    href: "articles/construction-control.html",
    category: "Модули",
    text: "контроль строительства комплексный график заявки снабжение"
  },
  {
    slug: "project-management",
    title: "Оперативное управление",
    audience: "Для всех",
    href: "articles/project-management.html",
    category: "Модули",
    text: "управление проектом рабочий стол отчёты исполнительная документация календарь уведомления оптимизатор"
  },
  {
    slug: "faq",
    title: "Часто задаваемые вопросы",
    audience: "FAQ",
    href: "faq.html",
    category: "Справка",
    text: "вход фамилия роли сохранение смена объекта скрины права доступ 1С"
  }
];

(function () {
  const rootPrefix = document.body.dataset.root || "";

  function resolveHref(href) {
    if (/^https?:|^\//.test(href)) return href;
    // From articles/* pages, index links need ../
    if (rootPrefix) {
      if (href.startsWith("articles/")) return href.replace(/^articles\//, "");
      if (href === "faq.html" || href === "index.html") return "../" + href;
      return rootPrefix + href;
    }
    return href;
  }

  /* ----- Search ----- */
  const searchInput = document.querySelector("[data-search-input]");
  const searchResults = document.querySelector("[data-search-results]");

  function normalize(s) {
    return (s || "").toLowerCase().replace(/ё/g, "е");
  }

  function renderResults(items) {
    if (!searchResults) return;
    if (!items.length) {
      searchResults.innerHTML = '<div class="search-results__empty">Ничего не найдено</div>';
      searchResults.classList.add("is-open");
      return;
    }
    searchResults.innerHTML = items
      .map(function (item) {
        const href = resolveHref(item.href);
        return (
          '<a href="' +
          href +
          '"><div class="search-results__title">' +
          item.title +
          '</div><div class="search-results__meta">' +
          item.category +
          " · " +
          item.audience +
          "</div></a>"
        );
      })
      .join("");
    searchResults.classList.add("is-open");
  }

  function search(query) {
    const q = normalize(query).trim();
    if (!q) {
      searchResults.classList.remove("is-open");
      searchResults.innerHTML = "";
      return;
    }
    const parts = q.split(/\s+/).filter(Boolean);
    const hits = window.ASIC_SEARCH_INDEX.filter(function (item) {
      const hay = normalize(item.title + " " + item.text + " " + item.category);
      return parts.every(function (p) {
        return hay.indexOf(p) !== -1;
      });
    }).slice(0, 8);
    renderResults(hits);
  }

  if (searchInput && searchResults) {
    searchInput.addEventListener("input", function () {
      search(searchInput.value);
    });
    searchInput.addEventListener("focus", function () {
      if (searchInput.value.trim()) search(searchInput.value);
    });
    document.addEventListener("click", function (e) {
      if (!e.target.closest(".search")) {
        searchResults.classList.remove("is-open");
      }
    });
    searchInput.addEventListener("keydown", function (e) {
      if (e.key === "Escape") {
        searchResults.classList.remove("is-open");
        searchInput.blur();
      }
    });
  }

  /* ----- Lightbox ----- */
  const lightbox = document.querySelector("[data-lightbox]");
  const lightboxContent = document.querySelector("[data-lightbox-content]");
  const lightboxClose = document.querySelector("[data-lightbox-close]");

  function openLightbox(node) {
    if (!lightbox || !lightboxContent) return;
    const img = node.querySelector("img");
    if (img) {
      lightboxContent.innerHTML = '<img src="' + img.src + '" alt="' + (img.alt || "") + '">';
    } else {
      const label = node.querySelector(".shot__label");
      const hint = node.querySelector(".shot__hint");
      lightboxContent.innerHTML =
        '<p><strong>' +
        (label ? label.textContent : "Скриншот") +
        "</strong></p><p>" +
        (hint ? hint.textContent : "Вставьте изображение на место плейсхолдера.") +
        "</p>";
    }
    lightbox.classList.add("is-open");
    document.body.style.overflow = "hidden";
  }

  function closeLightbox() {
    if (!lightbox) return;
    lightbox.classList.remove("is-open");
    document.body.style.overflow = "";
  }

  document.querySelectorAll("[data-lightbox-trigger]").forEach(function (el) {
    el.addEventListener("click", function () {
      openLightbox(el);
    });
  });

  if (lightboxClose) lightboxClose.addEventListener("click", closeLightbox);
  if (lightbox) {
    lightbox.addEventListener("click", function (e) {
      if (e.target === lightbox) closeLightbox();
    });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeLightbox();
  });

  /* ----- TOC active state ----- */
  const tocLinks = Array.from(document.querySelectorAll(".toc a[href^='#']"));
  const stepEls = tocLinks
    .map(function (a) {
      return document.querySelector(a.getAttribute("href"));
    })
    .filter(Boolean);

  if (tocLinks.length && "IntersectionObserver" in window) {
    const map = new Map();
    const observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          map.set(entry.target.id, entry.isIntersecting);
        });
        let activeId = null;
        for (let i = 0; i < stepEls.length; i++) {
          if (map.get(stepEls[i].id)) {
            activeId = stepEls[i].id;
            break;
          }
        }
        tocLinks.forEach(function (a) {
          a.classList.toggle("is-active", a.getAttribute("href") === "#" + activeId);
        });
      },
      { rootMargin: "-20% 0px -65% 0px", threshold: 0 }
    );
    stepEls.forEach(function (el) {
      observer.observe(el);
    });
  }
})();
