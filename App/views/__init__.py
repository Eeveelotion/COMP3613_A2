# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .internship import internship_views
from .shortlist import shortlist_views
from .index import index_views


views = [user_views, index_views, internship_views, shortlist_views] 
# blueprints must be added to this list