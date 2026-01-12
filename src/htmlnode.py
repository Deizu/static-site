class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        html_string = ""
        if self.props is None or len(self.props.keys()) == 0:
            return html_string
        for prop in self.props:
            html_string = html_string + f' {prop}="{self.props[prop]}"'
        html_string = html_string + " "
        return html_string

    def __repr__(self):
        def swap_none(attribute):
            return attribute if attribute is not None else "-"

        return f"HTMLNode | Tag: {swap_none(self.tag)} | Value: {swap_none(self.value)} | Children: {len(self.children) if self.children is not None else swap_none(self.children)} | Props: {swap_none(self.props)}"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError(f"No value present in node: {self}")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        def swap_none(attribute):
            return attribute if attribute is not None else "-"

        return f"HTMLNode [Leaf] | Tag: {swap_none(self.tag)} | Value: {swap_none(self.value)} | Props: {swap_none(self.props)}"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("No tag provided on parent node.")
        if self.children is None or len(self.children) == 0:
            raise ValueError("No children present for parent node.")
        return f"<{self.tag}>{''.join([child.to_html() for child in self.children])}</{self.tag}>"

    def __repr__(self):
        def swap_none(attribute):
            return attribute if attribute is not None else "-"

        return f"HTMLNode | Tag: {swap_none(self.tag)} | Value: {swap_none(self.value)} | Children: {len(self.children) if self.children is not None else swap_none(self.children)} | Props: {swap_none(self.props)}"
