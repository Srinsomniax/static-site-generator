from enum import Enum
from htmlnode import LeafNode
import re

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (self.text == other.text and self.text_type == other.text_type and self.url == other.url)

    def __repr__(self):
        string = f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        return string

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.alt})
        case _:
            raise Exception("Invalid text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    list_of_nodes = []
    counter = 0
    for nodes in old_nodes:
        if nodes.text_type is not TextType.TEXT:
            list_of_nodes.append(nodes)
            continue
        new_list = nodes.text.split(delimiter)
        if len(list_of_nodes)%1 == 0:
            raise Exception("No closing delimiter found")
    
   
        for element in new_list:
            if new_list[element] == "":
                continue
            if counter%2 ==1:
                list_of_nodes.append(TextNode(element,text_type))
            list_of_nodes.append(TextNode(element, TextType.TEXT))
            counter+=1
        new_nodes.extend(list_of_nodes)

    
        
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches

def split_nodes_image(old_nodes):
    list_of_nodes = []
    for nodes in old_nodes:
        if nodes.text_type is not TextType.TEXT:
            list_of_nodes.append(nodes)
            continue
        
        images = extract_markdown_images(nodes.text)
        
        if not images:
            list_of_nodes.append(nodes)
            continue
        current_text = nodes.text

        for alt_text, url in images:
            image_markdown=f"![{alt_text}]({url})"
            parts = current_text.split(image_markdown, 1)

            if parts[0]:
                list_of_nodes.append(TextNode(parts[0], TextType.TEXT))

            list_of_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

            if len(parts)>1:
                 current_text = parts[1]
            else:
                 current_text = ""

        if current_text:
            list_of_nodes.append(TextNode(current_text, TextType.TEXT))

    return list_of_nodes

def split_nodes_link(old_nodes):
    list_of_nodes = []
    for nodes in old_nodes:
        if nodes.text_type is not TextType.TEXT:
            list_of_nodes.append(nodes)
            continue
        
        links = extract_markdown_links(nodes.text)
        
        if not links:
            list_of_nodes.append(nodes)
            continue
        current_text = nodes.text

        for alt_text, url in links:
            link_markdown=f"[{alt_text}]({url})"
            parts = current_text.split(link_markdown, 1)

            if parts[0]:
                list_of_nodes.append(TextNode(parts[0], TextType.TEXT))

            list_of_nodes.append(TextNode(alt_text, TextType.LINK, url))

            if len(parts)>1:
                current_text = parts[1]
            else:
                current_text = ""

        if current_text:
            list_of_nodes.append(TextNode(current_text, TextType.TEXT))

    return list_of_nodes

def text_to_textnodes(text):
    node = 





    
class TextType(Enum):
    TEXT = "text"
    BOLD= "bold"
    ITALIC= "italic"
    CODE= "code"
    LINK = "link"
    IMAGE = "image"

   
