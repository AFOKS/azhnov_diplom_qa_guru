<h1>Дипломный проект по автоматизации тестирования сервиса электронных и аудиокниг «Литрес»</h1>

> <a target="_blank" href="https://www.litres.ru">Ссылка на сайт</a>

![Главная страница Литрес](design/image/litres_page.png)

## Содержание

- [Покрытый функционал](#покрытый-функционал)
- [Технологии и инструменты](#технологии-и-инструменты)
- [Структура проекта](#структура-проекта)
- [Локальный запуск](#локальный-запуск)
- [Запуск в Jenkins](#запуск-в-jenkins)
- [Allure-отчёт](#allure-отчёт)
- [Allure TestOps](#allure-testops)
- [Уведомления в Telegram](#уведомления-в-telegram)
- [Видео прохождения тестов](#видео-прохождения-тестов)

## Покрытый функционал

Всего в проекте **19 автотестов**: 10 UI, 6 API и 3 мобильных.

### UI-тесты (10)
- [x] Авторизация: успешная и с неверным паролем
- [x] Поиск книги: по названию и по автору
- [x] Добавление книги в корзину: одна книга и несколько
- [x] Удаление книги из корзины
- [x] Перенос книги из корзины в избранное («Отложить и удалить»)
- [x] Добавление книги в избранное
- [x] Удаление книги из избранного

### API-тесты (6)
- [x] Авторизация: зарегистрированный и незарегистрированный пользователь
- [x] Поиск книги: успешный и неуспешный
- [x] Добавление книги в корзину
- [x] Удаление книги из корзины

### Mobile-тесты, Android (3)
- [x] Поиск книги: успешный и неуспешный
- [x] Добавление книги в «Сохранённое»

## Технологии и инструменты

<p align="left">
<img src="design/icons/python-original.svg" width="50" title="Python">
<img src="design/icons/pytest.png" width="50" title="Pytest">
<img src="design/icons/intellij_pycharm.png" width="50" title="PyCharm">
<img src="design/icons/selene.png" width="50" title="Selene">
<img src="design/icons/selenoid.png" width="50" title="Selenoid">
<img src="design/icons/jenkins.png" width="50" title="Jenkins">
<img src="design/icons/allure_report.png" width="50" title="Allure Report">
<img src="design/icons/allure_testops.png" width="50" title="Allure TestOps">
<img src="design/icons/tg.png" width="50" title="Telegram">
</p>

| Область | Инструмент |
|---|---|
| Язык и тестовый фреймворк | Python, Pytest |
| UI | Selene (поверх Selenium), паттерн PageObject |
| API | Requests, логирование запросов и ответов |
| Mobile | Appium, Android |
| Запуск браузеров | Selenoid (удалённо) |
| CI | Jenkins |
| Отчётность | Allure Report, Allure TestOps |
| Уведомления | Telegram-бот |
| Конфигурация | python-dotenv (`.env`) |

## Структура проекта

```
litres_test_project/
├── data/        # модели данных (Book, User)
├── pages/       # PageObject: web_pages, mobile
├── utils/       # вложения Allure, запросы API
tests/
├── api_tests/   # API-тесты
├── mobile_test/  # Mobile-тесты
└── web_tests/ # # UI-тесты, conftest.py с фикстурами браузера
```

Тесты разделены по бизнес-логике: авторизация, поиск, корзина, избранное. В каждом тесте шаги оформлены через `allure.step`, а тесты размечены `epic`, `feature`, `tag`, `severity` и `label`.

В Allure-отчёт автоматически прикладываются:
- скриншот страницы,
- HTML страницы,
- логи браузера,
- видео прохождения теста.

## Локальный запуск

Перед запуском создайте файл `.env` в корне проекта:

```
SELENOID_URL=
SELENOID_LOGIN=
SELENOID_PASSWORD=
USER_EMAIL=
USER_PASSWORD=
LITRES_NAME=
```

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# все тесты
pytest tests

# только UI, с выбором версии браузера
pytest tests/web_tests --browser_version=156.0

# только API
pytest tests/api_tests
```

Просмотр отчёта:

```bash
allure serve allure-results
```

## Запуск в Jenkins

| Сборка | Ссылка |
|---|---|
| Основная сборка со всеми тестами (UI, API, Mobile) | <a target="_blank" href="https://jenkins.qa.guru/job/azhnov_diplom_qa_guru/">azhnov_diplom_qa_guru</a> |
| Параметризованная UI-сборка | <a target="_blank" href="https://jenkins.qa.guru/job/azhnov_diplom_qa_guru_ui_parametrize/">azhnov_diplom_qa_guru_ui_parametrize</a> |

#### Параметры UI-сборки

- `BROWSER_VERSION` — версия браузера в Selenoid
- `COMMENT` — комментарий к запуску

#### Как запустить

1. Открыть нужную сборку.
2. Выбрать `Build with Parameters`.
3. Указать параметры.
4. Нажать `Build`.
5. Результаты смотреть в Allure-отчёте, Allure TestOps и в уведомлении Telegram.

#### Основная сборка

![Jenkins: основная сборка](design/image/jenkins_main.png)

#### UI-сборка

![Jenkins: UI-сборка](design/image/jenkins_ui.png)

## Allure-отчёт

Отчёт доступен на странице сборки в Jenkins: <a target="_blank" href="https://jenkins.qa.guru/job/azhnov_diplom_qa_guru/allure/">Allure Report</a>

#### Общие результаты: 19 из 19 тестов пройдены
![Allure: Overview](design/image/allure_report_overview.png)

#### Графики
![Allure: Graphs](design/image/allure_report_graphs.png)

#### Список тест-кейсов по функциональности
![Allure: Behaviors](design/image/allure_report_behaviors.png)

#### Пример отчёта UI-теста
![Allure: UI-тест](design/image/example_test_ui_allure.png)

#### Пример отчёта API-теста
![Allure: API-тест](design/image/example_test_api_allure.png)

#### Пример отчёта mobile-теста
![Allure: Mobile-тест](design/image/example_test_mobile_allure.png)

## Allure TestOps

> <a target="_blank" href="https://allure.qa.guru/project/5423/test-cases">Ссылка на проект в Allure TestOps</a>

#### История запусков
![TestOps: запуски](design/image/allure_TestOps_launches.png)

#### Результаты запуска
![TestOps: результаты запуска](design/image/allure_TestOps_launch_results.png)

#### Список тест-кейсов
![TestOps: тест-кейсы](design/image/allure_TestOps_test_cases.png)

#### Пример автотеста с вложениями
![TestOps: пример теста](design/image/example_autotests_allure_TestOps.png)

## Уведомления в Telegram

После каждой сборки Jenkins бот присылает в Telegram сводку: количество тестов, процент успешных и ссылку на отчёт.

![Telegram: уведомление](design/image/tg_notification.png)

## Видео прохождения тестов

#### UI-тест (desktop)
![UI-тест](design/image/autotest.gif)

#### Mobile-тест
![Mobile-тест](design/image/autotest_mobile.gif)
