import sys

from src.app import App


if __name__ == '__main__':
    plguins = []

    from src.plugins import IFConfig
    from src.plugins import TraceRoute
    from src.plugins import DNS
    plguins.append(IFConfig())

    if sys.platform == 'win32':
        from src.plugins import WiFi
        wifi = WiFi(scanning=5)
        plguins.append(wifi)

    plguins.append(DNS([
        'google.com',
        'mioffice.cn'
    ]))

    plguins.append(TraceRoute('1.1.1.1'))

    app = App(plguins)
    app.run()
