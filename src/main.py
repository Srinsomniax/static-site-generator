from textnode import *


def main():
    sldkf = TextNode("ein Text",TextType.BOLD,"eine URL")

    print(sldkf)

    node= TextNode("This is text with a 'cod block' word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "'", TextType.CODE)

if __name__ == '__main__':
    main()
