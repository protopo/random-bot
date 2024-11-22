# Проект "Telegram/ChatGPT".

### 1. *Эхо-бот*
Телеграм-бот, который принимает сообщение пользователя и отсылает ему в ответ
текст полученного сообщения.


### 2. *"Рандомный факт"*
Телеграм-бот должен обрабатывать команду /random.
При обработке команды он отсылает заранее заготовленное изображение
и делает запрос к ChatGPT с заранее заготовленным промптом.
Ответ ChatGPT нужно получить и передать пользователю.


### 3. *ChatGPT интерфейс*
Телеграм-бот должен обрабатывать команду /gpt.
При обработке команды он отсылает заранее заготовленное изображение
и делает запрос к ChatGPT, передавая ему
текст полученного сообщения. Ответ ChatGPT нужно получить и
передать пользователю текстовым сообщением.


### 4. *"Диалог с известной личностью"*
Телеграм-бот должен обрабатывать команду /talk.
При обработке команды бот отсылает заранее заготовленное изображение и
предлагает выбор из нескольких известных личностей,
используя кнопки. По нажатию кнопки нужно установить промпт выбранной личности.
Дальнейшие текстовые сообщения от пользователя нужно передавать ChatGPT и
возвращать его ответы пользователю.


### 5. *"Квиз"*
Телеграм-бот должен обрабатывать команду /quiz.
При обработке команды бот отсылает заранее заготовленное изображение
и предлагает выбор из нескольких тем, используя кнопки.
После выбора темы, передать запрос ChatGPT и, получив вопрос квиза, передать его
пользователю. Следующее текстовое сообщение пользователя считается ответом.
Его нужно передать ChatGPT и получить результат. Результат передать пользователю
с возможностью задать ещё вопрос с помощью кнопки.
Бот также должен вести счёт правильных ответов и
отображать вместе с очередным результатом

### 6. **"Подбор рецептов"**

Пользователь вводит ингредиенты, которые у него есть.
Бот запрашивает у ChatGPT рецепты, которые можно приготовить из этих ингредиентов, 
и отправляет их пользователю.