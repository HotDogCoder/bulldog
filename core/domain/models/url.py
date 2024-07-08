class Url:

    def __init__(self, id=0, url="", new_url="", title="", description="", keywords="", flag=True, redirection_type=301):
        self.id = id
        self.url = url
        self.new_url = new_url
        self.title = title
        self.description = description
        self.keywords = keywords
        self.flag = flag
        self.redirection_type = redirection_type
