import asyncio
from pathlib import Path

from starlette.applications import Starlette
from starlette.responses import HTMLResponse, RedirectResponse, Response
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

usbdir = Path("/sys/bus/usb/drivers/usb/1-1")
is_on = usbdir.exists


static = Path(__file__).parent.resolve() / "static"


async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    if proc.returncode:
        stdout, stderr = await proc.communicate()
        print(f"[{cmd!r} exited with {proc.returncode}]")
        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")


async def ensure_on():
    if not is_on():
        await run("echo '1-1' >/sys/bus/usb/drivers/usb/bind")


async def ensure_off():
    if is_on():
        await run("echo '1-1' >/sys/bus/usb/drivers/usb/unbind")


async def home(request):
    return HTMLResponse(
        "<html>"
        "<head>"
        '<link rel="apple-touch-icon-precomposed" sizes="57x57" href="/static/apple-touch-icon-57x57.png" />'
        '<link rel="apple-touch-icon-precomposed" sizes="114x114" href=/static/"apple-touch-icon-114x114.png" />'
        '<link rel="apple-touch-icon-precomposed" sizes="72x72" href="/static/apple-touch-icon-72x72.png" />'
        '<link rel="apple-touch-icon-precomposed" sizes="144x144" href="/static/apple-touch-icon-144x144.png" />'
        '<link rel="apple-touch-icon-precomposed" sizes="60x60" href="/static/apple-touch-icon-60x60.png" />'
        '<link rel="apple-touch-icon-precomposed" sizes="120x120" href="/static/apple-touch-icon-120x120.png" />'
        '<link rel="apple-touch-icon-precomposed" sizes="76x76" href="/static/apple-touch-icon-76x76.png" />'
        '<link rel="apple-touch-icon-precomposed" sizes="152x152" href="/static/apple-touch-icon-152x152.png" />'
        '<link rel="icon" type="image/png" href="/static/favicon-196x196.png" sizes="196x196" />'
        '<link rel="icon" type="image/png" href="/static/favicon-96x96.png" sizes="96x96" />'
        '<link rel="icon" type="image/png" href="/static/favicon-32x32.png" sizes="32x32" />'
        '<link rel="icon" type="image/png" href="/static/favicon-16x16.png" sizes="16x16" />'
        '<link rel="icon" type="image/png" href="/static/favicon-128.png" sizes="128x128" />'
        "</head>"
        f'<body style="background-color:{"green" if is_on() else "red"}">'
        '<a href="/toggle" style="width:100%; height:100%; display:block" />'
        "</body>"
        "</html>"
    )


async def toggle(request):
    if is_on():
        await ensure_off()
    else:
        await ensure_on()
    return RedirectResponse(url="/")


async def on(request):
    asyncio.create_task(ensure_on())
    return Response()


async def off(request):
    asyncio.create_task(ensure_off())
    return Response()


app = Starlette(
    # debug=True,
    routes=[
        Route("/", home),
        Route("/toggle", toggle),
        Route("/on", on),
        Route("/off", off),
        Mount("/static", app=StaticFiles(directory=static), name="static"),
    ],
)
