"""Live Streamlit browser test for the vendored MUI binding."""

# *** imports

# ** core
import socket
import subprocess
import sys
from pathlib import Path
from time import sleep
from urllib.request import urlopen

# ** infra
import pytest

# *** functions

# ** function: _find_open_port
def _find_open_port() -> int:
    '''Return an operating-system-selected available loopback port.'''

    # Bind to port zero so the operating system chooses an available port.
    with socket.socket() as server:
        server.bind(('127.0.0.1', 0))

        # Return the port assigned to the temporary loopback socket.
        return server.getsockname()[1]

# ** function: _wait_for_server
def _wait_for_server(url: str) -> None:
    '''Wait until the local Streamlit server responds to its health endpoint.'''

    # Poll the server health endpoint while its subprocess starts.
    for _ in range(50):
        try:
            urlopen(url, timeout=1)
            return
        except OSError:
            sleep(.1)

    # Stop the test with the server location when startup never completes.
    pytest.fail(f'Streamlit server did not start at {url}.')

# *** tests

# ** test: demo_dispatches_each_real_button_interaction
def test_demo_dispatches_each_real_button_interaction():
    '''
    Test that the demo delivers both real browser button callback interactions.
    '''

    # Skip the externally gated browser test without its optional runtimes.
    playwright = pytest.importorskip('playwright.sync_api')
    pytest.importorskip('streamlit')
    port = _find_open_port()
    repository_root = Path(__file__).parents[3]
    demo_path = repository_root / 'examples' / 'streamlit_binding_demo.py'
    url = f'http://127.0.0.1:{port}'

    # Launch the externally maintained Streamlit demo on an available port.
    process = subprocess.Popen(
        [
            sys.executable,
            '-m',
            'streamlit',
            'run',
            str(demo_path),
            '--server.headless',
            'true',
            '--server.port',
            str(port),
            '--browser.gatherUsageStats',
            'false',
        ],
        cwd=repository_root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        # Wait for the demo health endpoint before attaching a real browser.
        _wait_for_server(url + '/_stcore/health')

        # Drive both callback buttons through the mounted component iframe.
        with playwright.sync_playwright() as playwright_context:
            browser = playwright_context.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            frame = page.frame_locator('iframe')
            frame.get_by_role('button', name='TRIGGER CALLBACK').click()
            page.get_by_text(
                'Button callback delivered.',
                exact=True,
            ).wait_for()
            frame = page.frame_locator('iframe')
            frame.get_by_role(
                'button',
                name='TRIGGER SECOND CALLBACK',
            ).click()
            page.get_by_text(
                'Second button callback delivered.',
                exact=True,
            ).wait_for()
            browser.close()
    finally:
        # Terminate the local Streamlit process after every test outcome.
        process.terminate()
        process.wait(timeout=10)

# ** test: gallery_renders_every_displayed_widget
def test_gallery_renders_every_displayed_widget():
    '''
    Test that the Streamlit gallery renders every cataloged widget sample.
    '''

    # Skip the externally gated browser test without its optional runtimes.
    playwright = pytest.importorskip('playwright.sync_api')
    pytest.importorskip('streamlit')
    port = _find_open_port()
    repository_root = Path(__file__).parents[3]
    gallery_path = repository_root / 'example' / 'app.py'
    url = f'http://127.0.0.1:{port}'

    # Launch the externally maintained Streamlit gallery on an available port.
    process = subprocess.Popen(
        [
            sys.executable,
            '-m',
            'streamlit',
            'run',
            str(gallery_path),
            '--server.headless',
            'true',
            '--server.port',
            str(port),
            '--browser.gatherUsageStats',
            'false',
        ],
        cwd=repository_root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        # Wait for the gallery health endpoint before attaching a real browser.
        _wait_for_server(url + '/_stcore/health')

        # Verify each cataloged widget appears in its corresponding iframe.
        with playwright.sync_playwright() as playwright_context:
            browser = playwright_context.chromium.launch()
            page = browser.new_page()
            page.goto(url)

            for index, (widget_type, sample) in enumerate([
                    ('button', 'BUTTON SAMPLE'),
                    ('text_field', 'TEXT FIELD SAMPLE'),
                    ('box', 'BOX SAMPLE'),
                    ('icon', 'home'),
                    ('card', 'CARD SAMPLE'),
                    ('form_label', 'FORM LABEL SAMPLE'),
                    ('typography', 'TYPOGRAPHY SAMPLE'),
                ]):
                # Wait for the catalog caption and its ordered component iframe.
                page.get_by_text(widget_type, exact=True).wait_for()
                frame = page.frame_locator('iframe').nth(index)
                frame.get_by_text(sample, exact=True).wait_for()

                # Verify the icon case applies and loads the Material Icons font.
                if widget_type == 'icon':
                    icon = frame.locator('.material-icons')
                    font_family = icon.evaluate(
                        '(el) => getComputedStyle(el).fontFamily',
                    )
                    assert 'Material Icons' in font_family
                    assert icon.evaluate(
                        '() => document.fonts.load('
                        '\'24px "Material Icons"\''
                        ').then(() => document.fonts.check('
                        '\'24px "Material Icons"\'))',
                    ) is True

            browser.close()
    finally:
        # Terminate the local Streamlit process after every test outcome.
        process.terminate()
        process.wait(timeout=10)
