import wtforms

from mediagoblin.tools.text import tag_length_validator
from mediagoblin.tools.translate import lazy_pass_to_ugettext as _
from mediagoblin.tools.licenses import licenses_as_choices


class BlogPostEditForm(wtforms.Form):
    title = wtforms.TextField(
        _('Title'),
        [wtforms.validators.Length(min=0, max=500)])
    
    description = wtforms.TextAreaField(
        _('Post'))
    
    tags = wtforms.TextField(
        _('Tags'),
        [tag_length_validator],
        description=_(
          "Separate tags by commas."))
    
    license = wtforms.SelectField(
        _('License'),
        [wtforms.validators.Optional(),],
        choices=licenses_as_choices())
    
        
