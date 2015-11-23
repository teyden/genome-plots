from flask import Blueprint

# Import items (users rsIDs, suggestMsgs) from models or entire module (for readability)
from app.mod_site.models import *

# Import helper functions (are not modules)
from app.mod_site.helpers import allParametersExist, any_FieldEmpty, userExists, sessionCounter

# Define blueprint: 'site', setting url prefix: app.[url]/site
mod_snp = Blueprint('snp', __name__, url_prefix='/snp')	# change 'site' to 'SNPPAT'
