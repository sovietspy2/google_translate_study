import csv
import json
from jinja2 import Template
import logging

# Read the CSV file and convert it to a list of dictionaries
csv_file = 'vocab.csv'

def html_process():
    logging.info("going to process {csv_file}")
    csv_data = []
    with open(csv_file, mode='r', encoding="utf-8") as file:
        csv_reader = csv.reader(file, delimiter=',', quotechar='"')
        for row in csv_reader:
            if len(row) == 4:
                csv_data.append({
                    "lang1": row[0],
                    "lang1_word": row[2],
                    "lang2": row[1],
                    "lang2_word": row[3]
                })
    # Convert the list of dictionaries to a JSON object
    json_data = json.dumps(csv_data)

    logging.info(f"Loaded {len(csv_data)} words to memory")

    # Load the HTML template
    with open('./html/template.html', 'r') as template_file:
        template = Template(template_file.read())

    # Render the HTML template with the JSON data
    rendered_html = template.render(data=json_data)

    # Save the rendered HTML to a file or serve it via a web framework
    output_path = './html_output/index.html'
    with open(output_path, 'w') as output_file:
        output_file.write(rendered_html)

    logging.info(f"file output generated @ {output_path}")


if __name__ == '__main__':
    html_process()