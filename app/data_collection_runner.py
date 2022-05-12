from scripts.initial_data_scripts.countries import get_countries
from scripts.initial_data_scripts.hs_and_commodity_codes import get_hs_and_comm_codes
from scripts.initial_data_scripts.mot_codes import get_mot_codes
from scripts.initial_data_scripts.quantities import get_quantities

from db.database_connection import initialize

initialize()
get_mot_codes()
get_quantities()
get_countries()
get_hs_and_comm_codes()

