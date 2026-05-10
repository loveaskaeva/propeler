# Инструкции по настройке GitHub для проекта Propeler

Для успешного выполнения 3-го спринта вам необходимо выполнить следующие действия в интерфейсе GitHub:

## 1. Добавление участников команды
1. Перейдите в ваш репозиторий на GitHub.
2. Откройте вкладку **Settings** (Настройки).
3. В левом меню выберите **Collaborators** (Соавторы).
4. Нажмите кнопку **Add people** и введите логины GitHub ваших коллег.

## 2. Настройка защиты основной ветки (main)
1. В разделе **Settings** выберите **Branches** (Ветки).
2. Нажмите **Add branch protection rule** (Добавить правило защиты ветки).
3. В поле **Branch name pattern** введите `main`.
4. Установите галочки:
   - **Require a pull request before merging** (Требовать Pull Request перед слиянием).
   - **Require approvals** (Требовать одобрения) — установите минимум 1.
   - **Do not allow bypassing the above settings** (Запретить обход этих настроек, если применимо).
5. Нажмите **Create** внизу страницы.

## 3. Работа с Pull Request
1. После того как вы запушите ветку `feature/add-footer` (`git push origin feature/add-footer`), на GitHub появится кнопка **Compare & pull request**.
2. Нажмите её и используйте текст из файла `PR_DESCRIPTION.md` для заполнения описания.
3. Назначьте коллегу для **Review** (Проверки).
4. После получения одобрения (Approve) нажмите **Merge pull request**.

## 4. Обновление локальной версии
После слияния на GitHub, вернитесь в терминал и выполните:
```bash
git checkout main
git pull origin main
```
И продолжайте работу от актуальной версии `main`.
