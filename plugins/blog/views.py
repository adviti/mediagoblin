# GNU MediaGoblin -- federated, autonomous media hosting
# Copyright (C) 2011, 2012 MediaGoblin contributors.  See AUTHORS.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import logging
import mediagoblin.mg_globals as mg_globals

_log = logging.getLogger(__name__)

from mediagoblin.tools.translate import lazy_pass_to_ugettext as _
from mediagoblin.tools.text import convert_to_tag_list_of_dicts
from mediagoblin.tools.response import render_to_response, redirect
from mediagoblin.decorators import require_active_login

from mediagoblin.messages import add_message, SUCCESS

from mediagoblin.plugins.blog import forms
from mediagoblin.db.models import MediaEntry        
from mediagoblin.db.models import User


@require_active_login
def edit_blog_post(request):
    """
    First view for submitting a file.
    """
    form = forms.BlogPostEditForm(request.form,
        license=request.user.license_preference)
    if request.method == 'POST' and form.validate():
         
            media_type = 'blogpost'
            entry = request.db.MediaEntry()
            entry.media_type = unicode(media_type)
            entry.title = unicode(form.title.data)
            entry.description = unicode(form.description.data)
            entry.license = unicode(form.license.data) or None
            entry.uploader = request.user.id

            entry.tags = convert_to_tag_list_of_dicts(form.tags.data)

            entry.generate_slug()
            
            entry.save()

            add_message(request, SUCCESS, _('Woohoo! Submitted!'))

            return redirect(request, "mediagoblin.plugins.blog.blog.view",
                            user=request.user.username)

    return render_to_response(
        request,
        'blog/blogpost_edit.html',
        {'form': form,
         'app_config': mg_globals.app_config,
         'user': request.user})


def view_blog(request):
    blog_owner_username = request.matchdict.get('user')
    _log.info("Username is %s"%(blog_owner_username))
    owner_user = User.query.filter(User.username==blog_owner_username).one()
    
    all_blog_posts = MediaEntry.query.filter(
        (MediaEntry.uploader==owner_user.id)
        & (MediaEntry.media_type==u'blogpost'))
    
    return render_to_response(
        request,
        'blog/blog_view.html',
        {'blog_posts': all_blog_posts,
         'blog_owner': blog_owner_username,
         'request': request,
        })
        
