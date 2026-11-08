def pytest_addoption(parser):
    parser.addoption(
        '--browser',
        default='chrome',
        choices=('chrome', 'firefox'),
        help='Browser name',
    )
    parser.addoption(
        '--browser_version',
        default=None,
        help='Browser version, default depends on the browser',
    )
    parser.addoption(
        '--headless',
        action='store_true',
        help='Run browser in headless mode',
    )