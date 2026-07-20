# ESO Addons Updater

## User documentation

<details>
<summary>User documentation in English</summary>

A self-made add-on manager for The Elder Scrolls Online — a more convenient
replacement for Minion. It installs, updates and removes add-ons together with
their dependencies, keeping your AddOns folder clean: exactly what is needed to
run your add-ons and nothing extra. Add-ons are displayed with the same icons as
on ESO UI.

The interface is available in the following languages — chosen automatically from
your system language and switchable in-app:

- English
- French
- German
- Spanish
- Russian
- Ukrainian

## Download

Latest release: <https://github.com/powerbq/eso-addons-updater/releases/tag/current>

Pick the file for your system:

| System | File |
|--------|------|
| Windows | `app.exe` |
| Linux | `app` |
| macOS (Apple Silicon) | `app-macos.dmg` |

> Intel architecture on macOS is not supported at the moment.

## Installation

**Windows / Linux:**

1. Create a separate folder for the program wherever is convenient and place the
   downloaded file there.
2. Run `app.exe` (Windows) or `app` (Linux — grant execute permission first).

The program updates itself on launch.

### Windows SmartScreen

The program is not signed with a certificate and is distributed as is, so Windows
SmartScreen will most likely block it and report an unknown publisher. This is
expected. To allow it to run, click **"More info"** → **"Run anyway"**.

## Before you start

> **Important.** Back up your `AddOns` folder before first use. The program
> deletes everything from the selected folder that was not installed through it,
> so choose the folder carefully. To keep your existing add-on list, use the
> import feature (see below).

## Usage

1. **Set the game's add-ons folder** — bottom-left of the window. For example:

   ```
   C:\Users\User\Documents\Elder Scrolls Online\live\AddOns
   ```

2. **Import existing add-ons** — before the first sync you can import add-ons
   already present in the selected folder, to minimise setup of your list. You
   can also run the import later, after the first sync — for example if you added
   some add-ons by third-party means. Caution: if **Sync on launch** is enabled, the
   auto-sync will delete such externally-added add-ons on the next launch before
   you can import them — it is up to you to keep this in mind.

3. **Auto-update** — bottom-right of the window you can enable automatic updating
   of installed add-ons on launch (**Sync on launch**).

4. **Sync** — this button updates all installed add-ons and libraries.

5. **Tamriel Trade Centre** — if TTC is installed, a button appears in the
   bottom-centre of the window to launch the client for updating prices and
   uploading your sales list to the TTC site.

### Dependencies

In 99.99% of cases you do not need to install libraries (dependencies) manually —
the program does it all. It also removes stale dependencies when you delete an
add-on or when one is no longer needed after an update. You maintain only the
list of add-ons you want and never track libraries yourself (unlike in Minion).

## For advanced users

The program has an **Exclusions** tab. It prevents deletion of files created by
third-party programs — for example the Tamriel Trade Centre client or the
HarvestMap-Data map download.

Automatic exclusions are already built in and activate on their own if you have
the relevant add-ons installed. Automatic support currently exists for **Tamriel
Trade Centre** and **HarvestMap-Data**. You can extend the list manually in the
input field on the left if needed.

> If some add-on needs exclusions, it is better to leave feedback and I will add
> its support to the automatic exclusions.

How to write and test rules: <https://regex101.com/>

</details>

<details>
<summary>Documentation utilisateur en français</summary>

Un gestionnaire d'addons fait maison pour The Elder Scrolls Online — un
remplacement plus pratique de Minion. Il installe, met à jour et supprime les
addons ainsi que leurs dépendances, en gardant votre dossier AddOns propre :
exactement ce qu'il faut pour faire fonctionner vos addons et rien de superflu.
Les addons sont affichés avec les mêmes icônes que sur ESO UI.

L'interface est disponible dans les langues suivantes — choisie automatiquement
selon la langue de votre système et modifiable dans l'application :

- Anglais
- Français
- Allemand
- Espagnol
- Russe
- Ukrainien

## Téléchargement

Dernière version : <https://github.com/powerbq/eso-addons-updater/releases/tag/current>

Choisissez le fichier adapté à votre système :

| Système | Fichier |
|---------|---------|
| Windows | `app.exe` |
| Linux | `app` |
| macOS (Apple Silicon) | `app-macos.dmg` |

> L'architecture Intel sur macOS n'est pas prise en charge pour le moment.

## Installation

**Windows / Linux :**

1. Créez un dossier séparé pour le programme à un endroit pratique et placez-y le
   fichier téléchargé.
2. Lancez `app.exe` (Windows) ou `app` (Linux — accordez d'abord les droits
   d'exécution).

Le programme se met à jour automatiquement au démarrage.

### Windows SmartScreen

Le programme n'est pas signé par un certificat et est distribué tel quel ;
Windows SmartScreen le bloquera donc probablement et signalera un éditeur
inconnu. C'est normal. Pour autoriser son exécution, cliquez sur
**« Informations complémentaires »** → **« Exécuter quand même »**.

## Avant de commencer

> **Important.** Sauvegardez votre dossier `AddOns` avant la première
> utilisation. Le programme supprime du dossier sélectionné tout ce qui n'a pas
> été installé via lui — choisissez donc le dossier avec soin. Pour conserver
> votre liste d'addons existante, utilisez l'import (voir ci-dessous).

## Utilisation

1. **Indiquez le dossier d'addons du jeu** — en bas à gauche de la fenêtre. Par
   exemple :

   ```
   C:\Users\User\Documents\Elder Scrolls Online\live\AddOns
   ```

2. **Importez les addons existants** — avant la première synchronisation, vous
   pouvez importer les addons déjà présents dans le dossier sélectionné, afin de
   réduire au minimum la configuration de votre liste. Vous pouvez aussi lancer
   l'import plus tard, après la première synchronisation — par exemple si vous
   avez ajouté des addons par d'autres moyens. Attention : si **Synchroniser au
   démarrage** est activé, la synchronisation supprimera ces addons ajoutés par
   d'autres moyens au prochain démarrage avant que vous puissiez les importer —
   il vous appartient d'y faire attention.

3. **Mise à jour automatique** — en bas à droite de la fenêtre, vous pouvez
   activer la mise à jour automatique des addons installés au démarrage
   (**Synchroniser au démarrage**).

4. **Synchroniser** — ce bouton lance la mise à jour de tous les addons et
   bibliothèques installés.

5. **Tamriel Trade Centre** — si TTC est installé, un bouton apparaît en bas au
   centre de la fenêtre pour lancer le client afin de mettre à jour les prix et
   d'envoyer votre liste de ventes sur le site TTC.

### Dépendances

Dans 99,99 % des cas, vous n'avez pas besoin d'installer les bibliothèques
(dépendances) manuellement — le programme s'en charge. Il supprime aussi les
dépendances obsolètes lorsque vous supprimez un addon ou qu'une dépendance n'est
plus nécessaire après une mise à jour. Vous ne gérez que la liste des addons que
vous voulez et ne suivez jamais les bibliothèques vous-même (contrairement à
Minion).

## Pour les utilisateurs avancés

Le programme possède un onglet **Exclusions**. Il empêche la suppression des
fichiers créés par des programmes tiers — par exemple le client Tamriel Trade
Centre ou le téléchargement de la carte HarvestMap-Data.

Des exclusions automatiques sont déjà intégrées et s'activent d'elles-mêmes si
vous avez les addons concernés installés. La prise en charge automatique existe
actuellement pour **Tamriel Trade Centre** et **HarvestMap-Data**. Vous pouvez
étendre la liste manuellement dans le champ de saisie à gauche si nécessaire.

> Si un addon nécessite des exclusions, il vaut mieux laisser un retour et
> j'ajouterai sa prise en charge aux exclusions automatiques.

Comment écrire et tester les règles : <https://regex101.com/>

</details>

<details>
<summary>Benutzerdokumentation auf Deutsch</summary>

Ein selbst entwickelter Addon-Manager für The Elder Scrolls Online — ein
komfortablerer Ersatz für Minion. Er installiert, aktualisiert und entfernt
Addons samt ihren Abhängigkeiten und hält Ihren AddOns-Ordner sauber: genau das,
was zum Ausführen Ihrer Addons nötig ist, und nichts Überflüssiges. Addons werden
mit denselben Symbolen wie auf ESO UI angezeigt.

Die Oberfläche ist in den folgenden Sprachen verfügbar — automatisch nach Ihrer
Systemsprache gewählt und in der App umschaltbar:

- Englisch
- Französisch
- Deutsch
- Spanisch
- Russisch
- Ukrainisch

## Download

Neueste Version: <https://github.com/powerbq/eso-addons-updater/releases/tag/current>

Wählen Sie die Datei für Ihr System:

| System | Datei |
|--------|-------|
| Windows | `app.exe` |
| Linux | `app` |
| macOS (Apple Silicon) | `app-macos.dmg` |

> Die Intel-Architektur unter macOS wird derzeit nicht unterstützt.

## Installation

**Windows / Linux:**

1. Erstellen Sie an einem beliebigen Ort einen eigenen Ordner für das Programm
   und legen Sie die heruntergeladene Datei dort ab.
2. Starten Sie `app.exe` (Windows) oder `app` (Linux — erteilen Sie zuvor
   Ausführungsrechte).

Das Programm aktualisiert sich beim Start selbst.

### Windows SmartScreen

Das Programm ist nicht mit einem Zertifikat signiert und wird wie besehen
verteilt, daher wird Windows SmartScreen es höchstwahrscheinlich blockieren und
einen unbekannten Herausgeber melden. Das ist zu erwarten. Um die Ausführung zu
erlauben, klicken Sie auf **„Weitere Informationen“** → **„Trotzdem
ausführen“**.

## Vor dem Start

> **Wichtig.** Sichern Sie Ihren `AddOns`-Ordner vor der ersten Verwendung. Das
> Programm löscht aus dem ausgewählten Ordner alles, was nicht über es
> installiert wurde — wählen Sie den Ordner also sorgfältig. Um Ihre bestehende
> Addon-Liste zu behalten, nutzen Sie den Import (siehe unten).

## Verwendung

1. **Legen Sie den Addon-Ordner des Spiels fest** — unten links im Fenster. Zum
   Beispiel:

   ```
   C:\Users\User\Documents\Elder Scrolls Online\live\AddOns
   ```

2. **Vorhandene Addons importieren** — vor der ersten Synchronisierung können Sie
   bereits im ausgewählten Ordner vorhandene Addons importieren, um die
   Einrichtung Ihrer Liste zu minimieren. Sie können den Import auch später
   ausführen, nach der ersten Synchronisierung — zum Beispiel, wenn Sie Addons
   mit anderen Mitteln hinzugefügt haben. Achtung: Wenn **Beim Start
   synchronisieren** aktiviert ist, entfernt die Synchronisierung solche extern
   hinzugefügten Addons beim nächsten Start, bevor Sie sie importieren können —
   das liegt in Ihrer Verantwortung.

3. **Automatische Aktualisierung** — unten rechts im Fenster können Sie die
   automatische Aktualisierung installierter Addons beim Start aktivieren
   (**Beim Start synchronisieren**).

4. **Synchronisieren** — diese Schaltfläche startet die Aktualisierung aller
   installierten Addons und Bibliotheken.

5. **Tamriel Trade Centre** — wenn TTC installiert ist, erscheint unten in der
   Mitte des Fensters eine Schaltfläche, um den Client zu starten, die Preise zu
   aktualisieren und Ihre Verkaufsliste auf die TTC-Website hochzuladen.

### Abhängigkeiten

In 99,99 % der Fälle müssen Sie Bibliotheken (Abhängigkeiten) nicht manuell
installieren — das Programm erledigt alles. Es entfernt auch veraltete
Abhängigkeiten, wenn Sie ein Addon löschen oder eine Abhängigkeit nach einer
Aktualisierung nicht mehr benötigt wird. Sie pflegen nur die Liste der
gewünschten Addons und behalten die Bibliotheken nie selbst im Blick (anders als
in Minion).

## Für fortgeschrittene Benutzer

Das Programm hat einen Reiter **Ausschlüsse**. Er verhindert das Löschen von
Dateien, die von Drittprogrammen erstellt werden — zum Beispiel dem
Tamriel-Trade-Centre-Client oder dem Herunterladen der HarvestMap-Data-Karte.

Automatische Ausschlüsse sind bereits integriert und aktivieren sich selbst, wenn
Sie die entsprechenden Addons installiert haben. Automatische Unterstützung gibt
es derzeit für **Tamriel Trade Centre** und **HarvestMap-Data**. Bei Bedarf
können Sie die Liste manuell im Eingabefeld links erweitern.

> Wenn ein Addon Ausschlüsse benötigt, geben Sie besser Feedback, und ich füge
> seine Unterstützung zu den automatischen Ausschlüssen hinzu.

So schreiben und testen Sie Regeln: <https://regex101.com/>

</details>

<details>
<summary>Documentación de usuario en español</summary>

Un gestor de complementos hecho por mí para The Elder Scrolls Online — un
reemplazo más cómodo de Minion. Instala, actualiza y elimina complementos junto
con sus dependencias, manteniendo tu carpeta AddOns limpia: exactamente lo
necesario para que funcionen tus complementos y nada de sobra. Los complementos
se muestran con los mismos iconos que en ESO UI.

La interfaz está disponible en los siguientes idiomas — se elige automáticamente
según el idioma de tu sistema y se puede cambiar dentro de la aplicación:

- Inglés
- Francés
- Alemán
- Español
- Ruso
- Ucraniano

## Descarga

Última versión: <https://github.com/powerbq/eso-addons-updater/releases/tag/current>

Elige el archivo para tu sistema:

| Sistema | Archivo |
|---------|---------|
| Windows | `app.exe` |
| Linux | `app` |
| macOS (Apple Silicon) | `app-macos.dmg` |

> La arquitectura Intel en macOS no es compatible por el momento.

## Instalación

**Windows / Linux:**

1. Crea una carpeta aparte para el programa donde te resulte cómodo y coloca allí
   el archivo descargado.
2. Ejecuta `app.exe` (Windows) o `app` (Linux — concede primero permisos de
   ejecución).

El programa se actualiza solo al iniciarse.

### Windows SmartScreen

El programa no está firmado con un certificado y se distribuye tal cual, por lo
que Windows SmartScreen probablemente lo bloqueará e indicará un editor
desconocido. Es lo esperado. Para permitir su ejecución, haz clic en **«Más
información»** → **«Ejecutar de todas formas»**.

## Antes de empezar

> **Importante.** Haz una copia de seguridad de tu carpeta `AddOns` antes del
> primer uso. El programa elimina de la carpeta seleccionada todo lo que no se
> haya instalado a través de él, así que elige la carpeta con cuidado. Para
> conservar tu lista de complementos existente, usa la importación (ver más
> abajo).

## Uso

1. **Indica la carpeta de complementos del juego** — en la parte inferior
   izquierda de la ventana. Por ejemplo:

   ```
   C:\Users\User\Documents\Elder Scrolls Online\live\AddOns
   ```

2. **Importa los complementos existentes** — antes de la primera sincronización
   puedes importar los complementos ya presentes en la carpeta seleccionada, para
   reducir al mínimo la configuración de tu lista. También puedes ejecutar la
   importación más tarde, después de la primera sincronización — por ejemplo si
   has añadido complementos por otros medios. Atención: si **Sincronizar al iniciar**
   está activado, la sincronización eliminará esos complementos añadidos por otros
   medios en el próximo inicio antes de que puedas importarlos — es tu
   responsabilidad tenerlo en cuenta.

3. **Actualización automática** — en la parte inferior derecha de la ventana
   puedes activar la actualización automática de los complementos instalados al
   iniciar (**Sincronizar al iniciar**).

4. **Sincronizar** — este botón inicia la actualización de todos los complementos
   y bibliotecas instalados.

5. **Tamriel Trade Centre** — si TTC está instalado, aparece un botón en la parte
   inferior central de la ventana para iniciar el cliente, actualizar los precios
   y subir tu lista de ventas al sitio de TTC.

### Dependencias

En el 99,99 % de los casos no necesitas instalar las bibliotecas (dependencias)
manualmente: el programa lo hace todo. También elimina las dependencias obsoletas
cuando eliminas un complemento o cuando una deja de ser necesaria tras una
actualización. Solo mantienes la lista de complementos que quieres y nunca
controlas las bibliotecas por tu cuenta (a diferencia de Minion).

## Para usuarios avanzados

El programa tiene una pestaña de **Exclusiones**. Sirve para que no se eliminen
archivos creados por programas de terceros, por ejemplo el cliente de Tamriel
Trade Centre o la descarga del mapa HarvestMap-Data.

Las exclusiones automáticas ya están integradas y se activan solas si tienes
instalados los complementos correspondientes. Actualmente hay soporte automático
para **Tamriel Trade Centre** y **HarvestMap-Data**. Si hace falta, puedes
ampliar la lista manualmente en el campo de entrada de la izquierda.

> Si algún complemento necesita exclusiones, mejor deja tu comentario y añadiré
> su soporte a las exclusiones automáticas.

Cómo escribir y probar las reglas: <https://regex101.com/>

</details>

<details>
<summary>Документация пользователя на русском</summary>

Самописный менеджер аддонов для The Elder Scrolls Online — более удобная замена
Minion. Программа устанавливает, обновляет и удаляет аддоны вместе с их
зависимостями, сохраняя папку аддонов в чистоте: ровно то, что нужно для работы,
и ничего лишнего. Аддоны отображаются с теми же иконками, что и на ESO UI.

Интерфейс доступен на следующих языках — язык выбирается автоматически по
системному, сменить можно прямо в программе:

- Английский
- Французский
- Немецкий
- Испанский
- Русский
- Украинский

## Загрузка

Последний релиз: <https://github.com/powerbq/eso-addons-updater/releases/tag/current>

Выберите файл под свою систему:

| Система | Файл |
|---------|------|
| Windows | `app.exe` |
| Linux | `app` |
| macOS (Apple Silicon) | `app-macos.dmg` |

> Поддержки Intel-архитектуры на macOS пока нет.

## Установка

**Windows / Linux:**

1. Создайте отдельную папку для программы в удобном месте и положите туда
   загруженный файл.
2. Запустите `app.exe` (Windows) или `app` (Linux — предварительно дайте файлу
   права на запуск).

Программа обновляется самостоятельно при запуске.

### Windows SmartScreen

Программа не подписана сертификатом и распространяется «как есть», поэтому Windows
SmartScreen, скорее всего, заблокирует запуск и сообщит о неизвестном издателе.
Это ожидаемо. Чтобы разрешить запуск, нажмите **«Подробнее»** → **«Выполнить в
любом случае»**.

## Перед началом

> **Важно.** Сделайте резервную копию папки `AddOns` перед первым использованием.
> Программа удаляет из выбранной папки всё, что было установлено не с помощью неё,
> поэтому внимательно выбирайте папку. Чтобы не потерять список уже установленных
> аддонов, воспользуйтесь импортом (см. ниже).

## Использование

1. **Укажите папку аддонов игры** — в нижней левой части окна. Например:

   ```
   C:\Users\User\Documents\Elder Scrolls Online\live\AddOns
   ```

2. **Импорт существующих аддонов** — перед первой синхронизацией можно
   импортировать аддоны, уже находящиеся в выбранной папке, чтобы свести
   настройку списка к минимуму. Импорт также можно выполнить и после первой
   синхронизации — например, если вы добавили какие-то аддоны сторонними
   средствами. Внимание: если включена галочка **Синхронизация при запуске**, при
   следующем запуске синхронизация удалит такие добавленные сторонними средствами
   аддоны раньше, чем вы успеете их импортировать — это остаётся на вашей
   ответственности.

3. **Автообновление** — в нижней правой части окна можно включить автоматическое
   обновление установленных аддонов при запуске программы (**Синхронизация при
   запуске**).

4. **Синхронизировать** — кнопка запускает обновление всех установленных аддонов
   и библиотек.

5. **Tamriel Trade Centre** — если установлен TTC, в нижней центральной части
   окна появится кнопка запуска клиента для обновления цен и выгрузки вашего
   списка продаж на сайт TTC.

### Зависимости

В 99,99 % случаев библиотеки (зависимости) устанавливать вручную не нужно —
программа сделает всё сама. Она также удаляет неактуальные зависимости, когда вы
удаляете аддон или когда после обновления зависимость больше не нужна. Вы ведёте
только список нужных вам аддонов и не следите за библиотеками самостоятельно (в
отличие от Minion).

## Для опытных пользователей

В программе есть вкладка **Исключения**. Она нужна, чтобы не удалялись файлы,
создаваемые сторонними программами — например клиентом Tamriel Trade Centre или
загрузкой карты HarvestMap-Data.

Автоматические исключения уже встроены и включаются сами, если у вас установлены
соответствующие аддоны. Сейчас есть автоматическая поддержка для **Tamriel Trade
Centre** и **HarvestMap-Data**. При необходимости список можно расширить вручную
в поле ввода слева.

> Если какому-то аддону нужны исключения — лучше оставьте фидбек, и я добавлю его
> поддержку в автоматические исключения.

Как писать и тестировать правила: <https://regex101.com/>

</details>

<details>
<summary>Документація користувача українською</summary>

Самописний менеджер аддонів для The Elder Scrolls Online — зручніша заміна
Minion. Програма встановлює, оновлює та видаляє аддони разом з їхніми
залежностями, тримаючи теку аддонів у чистоті: рівно те, що потрібно для роботи,
і нічого зайвого. Аддони відображаються з тими самими іконками, що й на ESO UI.

Інтерфейс доступний такими мовами — мова обирається автоматично за системною,
змінити можна прямо в програмі:

- Англійська
- Французька
- Німецька
- Іспанська
- Російська
- Українська

## Завантаження

Останній реліз: <https://github.com/powerbq/eso-addons-updater/releases/tag/current>

Оберіть файл під свою систему:

| Система | Файл |
|---------|------|
| Windows | `app.exe` |
| Linux | `app` |
| macOS (Apple Silicon) | `app-macos.dmg` |

> Підтримки Intel-архітектури на macOS наразі немає.

## Встановлення

**Windows / Linux:**

1. Створіть окрему теку для програми у зручному місці та покладіть туди
   завантажений файл.
2. Запустіть `app.exe` (Windows) або `app` (Linux — попередньо надайте файлу
   права на запуск).

Програма оновлюється самостійно під час запуску.

### Windows SmartScreen

Програма не підписана сертифікатом і розповсюджується «як є», тому Windows
SmartScreen, найімовірніше, заблокує запуск і повідомить про невідомого видавця.
Це очікувано. Щоб дозволити запуск, натисніть **«Додаткова інформація»** →
**«Виконати в будь-якому разі»**.

## Перед початком

> **Важливо.** Зробіть резервну копію вашої теки `AddOns` перед першим
> використанням. Програма видаляє з обраної теки все, що було встановлено не
> за її допомогою — тож уважно обирайте теку. Щоб не втратити наявний список аддонів,
> скористайтеся імпортом (див. нижче).

## Використання

1. **Вкажіть теку аддонів гри** — у нижній лівій частині вікна. Наприклад:

   ```
   C:\Users\User\Documents\Elder Scrolls Online\live\AddOns
   ```

2. **Імпорт наявних аддонів** — перед першою синхронізацією можна імпортувати
   аддони, які вже є в обраній теці, щоб звести налаштування списку до мінімуму.
   Імпорт також можна виконати й після першої синхронізації — наприклад, якщо ви
   додали якісь аддони сторонніми засобами. Увага: якщо ввімкнено
   **Синхронізація під час запуску**, під час наступного запуску синхронізація
   видалить такі додані сторонніми засобами аддони раніше, ніж ви встигнете їх
   імпортувати — це залишається на вашій відповідальності.

3. **Автооновлення** — у нижній правій частині вікна можна ввімкнути автоматичне
   оновлення встановлених аддонів під час запуску програми (**Синхронізація під
   час запуску**).

4. **Синхронізувати** — кнопка запускає оновлення всіх встановлених аддонів та
   бібліотек.

5. **Tamriel Trade Centre** — якщо встановлено TTC, у нижній центральній частині
   вікна з'явиться кнопка запуску клієнта для оновлення цін і відвантаження
   вашого списку продажів на сайт TTC.

### Залежності

У 99,99 % випадків бібліотеки (залежності) встановлювати вручну не потрібно —
програма зробить усе сама. Вона також видаляє неактуальні залежності, коли ви
видаляєте аддон або коли після оновлення залежність більше не потрібна. Ви
формуєте лише список потрібних вам аддонів і не слідкуєте за бібліотеками
самостійно (на відміну від Minion).

## Для досвідчених користувачів

У програмі є вкладка **Виключення**. Вона потрібна, щоб не видалялися файли, які
створюються сторонніми програмами — наприклад, клієнтом Tamriel Trade Centre або
завантаженням карти HarvestMap-Data.

Автоматичні виключення вже вбудовані та вмикаються самі, якщо у вас встановлені
відповідні аддони. Наразі є автоматична підтримка для **Tamriel Trade Centre**
та **HarvestMap-Data**. За потреби список можна розширити вручну в полі вводу
зліва.

> Якщо якийсь аддон потребує виключень — краще залиште фідбек, і я додам його
> підтримку в автоматичні виключення.

Як писати та тестувати правила: <https://regex101.com/>

</details>

## Usage

This repository contains the **updater** only. The manager's codebase and the
runtime assets the updater downloads live in
[powerbq/eso-addons-manager](https://github.com/powerbq/eso-addons-manager).

## Build

Build the updater with Rust and Cargo:

```bash
./build.sh   # Linux / macOS
build.cmd    # Windows
```

This runs `cargo build --release`; the binary is written to `target/release/`.

## License

Released under the [MIT License](LICENSE). Copyright (c) 2026 powerbq.
