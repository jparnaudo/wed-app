import os
import jinja2


# Set useful fields
root_dir = os.path.dirname(__file__)

# Initialize the jinja2 environment
jinja_environment = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(root_dir))
