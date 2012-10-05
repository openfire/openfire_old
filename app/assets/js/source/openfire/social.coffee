# openfire social classes

class Comment extends Model
    model:
        username: String()
        content: String()
        created: String()
        modified: String()
        reply_to: String()

class Update extends Comment

