# Куда класть скриншоты

Положите файлы по паттерну:

`images/<slug>/step-<N>-<i>.jpg`

Примеры:
- `images/start/step-1-1.jpg`
- `images/users-and-access/step-7-1.jpg`

После добавления файла замените блок-плейсхолдер в статье на:

```html
<figure class="shot" data-lightbox-trigger>
  <img src="../images/<slug>/step-N-i.jpg" alt="описание">
</figure>
```
