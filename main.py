import sys

from src.app import App


if __name__ == '__main__':
    plguins = []

    from src.plugins import TraceRoute
    from src.plugins import DNS
    plguins.append(TraceRoute('1.1.1.1'))
    plguins.append(DNS([
        'google.com', 
        'mioffice.cn',
        'cas.mioffice.cn'
    ]))

    if sys.platform == 'win32':
        from src.plugins import WiFi
        wifi = WiFi(scanning=5)
        plguins.append(wifi)

    app = App(plguins)
    app.run()
