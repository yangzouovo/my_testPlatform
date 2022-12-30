from bs4 import BeautifulSoup
import os
import base64
import mimetypes
import requests

def guess_type(filepath):
    """
    Return the mimetype of a file, given it's path.
    This is a wrapper around two alternative methods - Unix 'file'-style
    magic which guesses the type based on file content (if available),
    and simple guessing based on the file extension (eg .jpg).
    :param filepath: Path to the file.
    :type filepath: str
    :return: Mimetype string.
    :rtype: str
    """
    try:
        import magic  # python-magic
        return magic.from_file(filepath, mime=True)
    except ImportError:
        import mimetypes
        return mimetypes.guess_type(filepath)[0]

def file_to_base64(filepath):
    """
    Returns the content of a file as a Base64 encoded string.
    :param filepath: Path to the file.
    :type filepath: str
    :return: The file content, Base64 encoded.
    :rtype: str
    """
    import base64
    with open(filepath, 'rb') as f:
        encoded_str = base64.b64encode(f.read())
    return encoded_str.decode('utf-8')

def make_css_inline(soup:BeautifulSoup, input_file, output_file):
    """
    Takes an HTML file and writes a new version with inline encoded css style.
    :param input_file: Input file path (HTML)
    :type input_file: str
    :param output_file: Output file path (HTML)
    :type output_file: str
    """
    basepath = os.path.split(input_file.rstrip(os.path.sep))[0]
    stylesheets = soup.findAll("link", {"rel": "stylesheet"})
    for s in stylesheets:
        with open(os.path.join(basepath, s["href"])) as cs:
            s.replaceWith('<style type="text/css" media="screen">' \
                            + cs.read() +\
                            '</style>')

    with open(output_file, "w", encoding='utf-8') as f:    
        f.write(str(soup.prettify(formatter=None)))
    

def make_image_inline(soup:BeautifulSoup, input_file, output_file):
    """
    Takes an HTML file and writes a new version with inline Base64 encoded
    images.
    :param input_file: Input file path (HTML)
    :type input_file: str
    :param output_file: Output file path (HTML)
    :type output_file: str
    """
    imagesheets = soup.findAll("img")
    basepath = os.path.split(input_file.rstrip(os.path.sep))[0]

    for img in imagesheets:
        # convert http image to base64
        img_src = img.attrs['src']
        if img_src.startswith('http'):
            mimetype = mimetypes.guess_type(img_src)[0]
            img_b64 = base64.b64encode(requests.get(img_src).content)

            img.attrs['src'] = \
                "data:%s;base64,%s" % (mimetype, img_b64.decode('utf-8'))
            continue

        # convert local image to base64
        img_path = os.path.join(basepath, img.attrs['src'])
        mimetype = guess_type(img_path)
        img.attrs['src'] = \
            "data:%s;base64,%s" % (mimetype, file_to_base64(img_path))

    with open(output_file, 'w', encoding='utf-8') as of:
        of.write(str(soup.prettify(formatter=None)))
        
def merge_css_and_img_to_html(input_file, output_file):
    soup = BeautifulSoup(open(input_file, 'rb').read(), features='lxml')
    make_css_inline(soup, input_file, output_file)
    make_image_inline(soup, input_file, output_file)
    print('merge file successfully!')
    

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print("usage:\n\tpython %s input-html-file output-html-file" % sys.argv[0])
        sys.exit(-1)
    merge_css_and_img_to_html(sys.argv[1], sys.argv[2])
