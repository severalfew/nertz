import streamlit as st
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from marko import Markdown
from marko import inline
from marko.helpers import MarkoExtension


colormap = {
    "Radmar": "#8dd3c7",
    "Joan": "#ffed6f",
    "Mo": "#bebada",
    "Stu": "#fb8072",
    "Teresa": "#80b1d3",
    "Phil": "#fdb462",
    "Becca": "#b3de69",
    "ThiThoa": "#fccde5",
    "David": "#ffffb3",
    "Tri": "#d9d9d9",
    "Jack": "#b22222",
    "Mallory": "#bc80bd",
    "Phil+Becca": "#ccebc5",
    "David+Tri": "#ffffb3",
    "Draw": "#d9d9d9",
    "Tie": "#d9d9d9",
    "Stu+Teresa": "#bc80bd",
    "All-Star Break (US)": "#b22222",
}


def player_cols(df):
    return [col for col in df if col in colormap.keys()]


def plotly_to_html(filehandle, fig, include_plotlyjs=False):
    """
    Convert a Plotly figure to an HTML string.

    This function takes a Plotly figure and converts it into an HTML string.
    The HTML string can then be written to a file or used in a web application.

    Parameters:
    filehandle (file-like object): The file-like object to write the HTML string to.
    fig (plotly.graph_objects.Figure): The Plotly figure to convert.
    include_plotlyjs (bool, optional): Whether or not to include the Plotly.js library in the HTML.
                                      The default is False.

    Returns:
    None: The function writes the HTML string to the filehandle, so it does not return anything.

    Note:
    The `full_html` parameter in `fig.to_html()` is set to False by default,
    which means only the div and script tags containing the Plotly figure data
    are included in the HTML string. If you want a complete HTML document,
    you should set `full_html` to True.
    """
    filehandle.write(fig.to_html(include_plotlyjs=include_plotlyjs, full_html=False))


class PlayerElement(inline.InlineElement):
    pattern = "|".join(colormap.keys())
    parse_children = True

    def __init__(self, element):
        self.target = element.group()


class PlayerRendererMixin(object):
    def render_player_element(self, element):
        return f'<strong style="color: {colormap[element.target]};">{element.target}</strong>'


PlayerExtension = MarkoExtension(
    elements=[PlayerElement],
    renderer_mixins=[PlayerRendererMixin],
)

md = Markdown(extensions=[PlayerExtension])

env = Environment(loader=FileSystemLoader("."), autoescape=False)


def enhanced_markdown(path_or_text: str, **kwargs) -> None:
    try:
        # Read markdown as template
        template = env.get_template(path_or_text)
        # Render Jinja2 template using kwargs
        text = template.render(**kwargs)
    except TemplateNotFound:
        text = path_or_text
    # Convert to html
    html = md.convert(text)
    # Write to streamlit
    st.html(html)
