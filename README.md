<project>
    <title>🌐 luguard</title>
    <description>Генерация конфигурации CloudFlare Warp + оживление WireGuard протокола</description>
    
    <installation>
        <heading>📦 Установка зависимостей</heading>
        <command>pip install -r requirements.txt</command>
    </installation>
    
    <launch>
        <heading>🚀 Запуск программы</heading>
        <command>python main.py</command>
    </launch>
    
    <modules>
        <module>
            <number>1️⃣</number>
            <name>Генерация конфигурации для WireGuard</name>
            <description>Генерирует конфигурацию Warp WireGuard с возможностью использования прокси.</description>
        </module>
        <module>
            <number>2️⃣</number>
            <name>Отправка фейковых пакетов на порт WireGuard</name>
            <description>Отправляет пустой UDP пакет на сервер <code>engage.cloudflareclient.com</code>, что позволяет обойти проверки на следующие пакеты.</description>
        </module>
        <module>
            <number>3️⃣</number>
            <name>Использование автоматического конфигурационного файла [settings.cfg]</name>
            <description>Производит автоматическое подключение к тунелю, отправив UDP пакет. (Для работы требуются права администратора)</description>
        </module>
    </modules>
    
    <telegram>
        <heading>📣 Присоединяйтесь к моему Telegram каналу</heading>
        <link>👉 <url>https://t.me/shalopaybase</url></link>
    </telegram>
    
</project>
