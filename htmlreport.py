from jinja2 import Environment, FileSystemLoader
import os
import json
root = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join('data','smb_template')
env = Environment( loader = FileSystemLoader(templates_dir) )
template = env.get_template('smb_template.html')
 
with open("data/final_result/202010262120.json") as file :
    data = json.load(file)
    filename = os.path.join('result.html')
    with open(filename, 'w') as fh:
        fh.write(template.render(
            h1 = "Hello Jinja2",
            show_one = True,
            show_two = False,
            names    = ["Foo", "Bar", "Qux"],
        ))
