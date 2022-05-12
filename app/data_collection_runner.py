from scripts.initial_data_scripts.countries import get_countries
from scripts.initial_data_scripts.hs_and_commodity_codes import get_hs_and_comm_codes
from scripts.initial_data_scripts.mot_codes import get_mot_codes
from scripts.initial_data_scripts.quantities import get_quantities
from scripts.initial_data_scripts.customs import get_customs_codes
from scripts.initial_data_scripts.flows import get_flows
from scripts.initial_data_scripts.mos_codes import get_mos_codes

from db.database_connection import initialize

initialize()

get_mot_codes()
get_quantities()
get_customs_codes()
get_flows()
get_mos_codes()
get_countries()
get_hs_and_comm_codes()

