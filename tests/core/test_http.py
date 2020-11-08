import pytest

from src.core.http import GetHtml, GetBinary
from tests.conftest import ReadFromTestDataFunc


@pytest.mark.skip("Кидает запрос в интернет")
@pytest.mark.asyncio
async def test_get_html():
    get_html = GetHtml()
    url = "https://turing.plymouth.edu/~zshen/Webfiles/notes/CS130/PythonExamples/jscript.html"

    html = await get_html(url)

    assert html.html == """<html><head>
  <title>The Simplest Web Page</title>
  <script>
   function test(){
     document.writeln("This is a test");
   }
  </script>
 </head>
 <body>
   <h1>A simple heading</h1>
   <p>This is a very simple web page.</p>
   <img src="barbara.jpg">

   <script>test()</script>This is a test


 

</body></html>"""


@pytest.mark.skip("Кидает запрос в интернет")
@pytest.mark.asyncio
async def test_get_binary(read_from_test_data: ReadFromTestDataFunc) -> None:
    get_binary = GetBinary()
    test_image = read_from_test_data("avatarko_anonim.jpg", binary=True)

    data = await get_binary("https://avatarko.ru/img/kartinka/1/avatarko_anonim.jpg")

    assert data.read() == test_image
