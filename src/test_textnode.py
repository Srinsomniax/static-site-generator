import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node,node2)
    def test_eq_false(self):
        node  = TextNode("This is a text node", TextType.ITALIC, "boot.dev/lessons")
        node2 = TextNode("This is a text node", TextType.LINK, None)
        self.assertNotEqual(node,node2)

    def test_eq_false2(self):
        node  = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node2", TextType.ITALIC)
        self.assertNotEqual(node,node2)

    def test_eq_url(self):
        node  = TextNode("This is a text node", TextType.TEXT, "boot.dev/lessons")
        node2  = TextNode("This is a text node", TextType.TEXT, "boot.dev/lessons")
        self.assertEqual(node,node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

#    def test_split_nodes_delimiter(self):
#        node = TextNode("This is text with a 'code block' word this is another 'code block'", TextType.TEXT)
#        new_nodes = split_nodes_delimiter([node], "'", TextType.CODE)
    def text_delim_bold_multiword(self):
        node = TextNode(
                "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
                [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("bolded word", TextType.BOLD),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("another", TextType.BOLD),
                ],
                new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
                )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
                "This is text with a link [to boot dev](https://www.boot.dev)"
                )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                    ),
                ],
            new_nodes,
            )

    def test_split_links(self):
        node = TextNode(
                "This is text with an [to boot dev](https://www.boot.dev) and another [to youtube](https://www.youtube.com)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com"
                    ),
                ],
            new_nodes,
            )







if __name__ == "__main__":
    unittest.main()
